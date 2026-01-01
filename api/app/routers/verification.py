"""
Veterans Verification API - Verification Router
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header
from typing import Optional
from datetime import datetime

from ..models import (
    CreateVerificationRequest,
    CreateVerificationResponse,
    SubmitVerificationRequest,
    SubmitVerificationResponse,
    VerificationStatusResponse,
    UploadDocumentResponse,
    VerificationStatus,
    APIError,
)
from ..services import get_supabase_service, get_sheerid_service

router = APIRouter(prefix="/verify", tags=["Verification"])


async def get_current_user(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Get current user from authorization header or API key."""
    supabase = get_supabase_service()
    
    if x_api_key:
        profile = await supabase.get_profile_by_api_key(x_api_key)
        if profile:
            return profile
    
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        # In production, verify JWT token with Supabase
        # For now, return a mock user or None
        pass
    
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing authentication"
    )


@router.post("/create", response_model=CreateVerificationResponse)
async def create_verification(
    request: CreateVerificationRequest,
    user: dict = Depends(get_current_user)
):
    """
    Create a new verification request.
    
    This initializes the verification process and returns a verification ID
    that will be used for subsequent steps.
    """
    supabase = get_supabase_service()
    
    # Create verification record in database
    verification = await supabase.create_verification(
        user_id=user["id"],
        data={
            "service_type": request.service_type.value,
            "program_id": request.program_id,
            "request_data": request.model_dump()
        }
    )
    
    if not verification:
        raise HTTPException(
            status_code=500,
            detail="Failed to create verification"
        )
    
    # If ChatGPT, also create SheerID verification
    sheerid_verification_id = None
    if request.service_type.value == "chatgpt":
        sheerid = get_sheerid_service()
        try:
            result = await sheerid.create_verification("chatgpt")
            if result.get("success"):
                sheerid_verification_id = result.get("verification_id")
                await supabase.update_verification(
                    verification["id"],
                    {"sheerid_verification_id": sheerid_verification_id}
                )
        finally:
            await sheerid.close()
    
    return CreateVerificationResponse(
        verification_id=verification["id"],
        sheerid_verification_id=sheerid_verification_id,
        status=VerificationStatus.PENDING,
        created_at=datetime.fromisoformat(verification["created_at"].replace("Z", "+00:00"))
    )


@router.post("/submit", response_model=SubmitVerificationResponse)
async def submit_verification(
    request: SubmitVerificationRequest,
    user: dict = Depends(get_current_user)
):
    """
    Submit veteran personal information for verification.
    
    This is the main verification step where the veteran's information
    is sent to SheerID for verification against the DoD/DEERS database.
    """
    supabase = get_supabase_service()
    
    # Get verification record
    verification = await supabase.get_verification_by_id(request.verification_id)
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    if verification["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create veteran record
    veteran = await supabase.create_veteran(
        user_id=user["id"],
        data={
            "first_name": request.veteran.first_name,
            "last_name": request.veteran.last_name,
            "birth_date": request.veteran.birth_date.isoformat() if request.veteran.birth_date else None,
            "branch": request.veteran.branch.value,
            "military_status": request.veteran.military_status.value,
            "discharge_date": request.veteran.discharge_date.isoformat() if request.veteran.discharge_date else None,
            "source": "MANUAL"
        }
    )
    
    # Update verification with veteran ID
    await supabase.update_verification(
        request.verification_id,
        {
            "veteran_id": veteran["id"] if veteran else None,
            "status": "processing",
            "submitted_at": datetime.utcnow().isoformat()
        }
    )
    
    # Submit to SheerID if we have a SheerID verification ID
    status = VerificationStatus.PROCESSING
    message = "Verification submitted successfully"
    next_step = None
    
    if verification.get("sheerid_verification_id"):
        sheerid = get_sheerid_service()
        try:
            # Submit military status
            await sheerid.submit_military_status(
                verification["sheerid_verification_id"],
                request.veteran.military_status.value
            )
            
            # Submit personal info
            result = await sheerid.submit_personal_info(
                verification_id=verification["sheerid_verification_id"],
                first_name=request.veteran.first_name,
                last_name=request.veteran.last_name,
                birth_date=request.veteran.birth_date,
                branch=request.veteran.branch.value,
                discharge_date=request.veteran.discharge_date,
                email=request.email
            )
            
            if result.get("success"):
                if result.get("status") == "approved":
                    status = VerificationStatus.APPROVED
                    message = "Verification approved!"
                elif result.get("status") == "document_required":
                    status = VerificationStatus.DOCUMENT_REQUIRED
                    message = "Document upload required"
                    next_step = "document_upload"
                else:
                    message = result.get("message", "Processing verification")
            else:
                status = VerificationStatus.ERROR
                message = result.get("error", "Verification failed")
            
            await supabase.update_verification(
                request.verification_id,
                {
                    "status": status.value,
                    "response_data": result
                }
            )
            
        finally:
            await sheerid.close()
    
    return SubmitVerificationResponse(
        verification_id=request.verification_id,
        status=status,
        message=message,
        next_step=next_step
    )


@router.get("/{verification_id}/status", response_model=VerificationStatusResponse)
async def get_verification_status(
    verification_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Get the current status of a verification request.
    """
    supabase = get_supabase_service()
    
    verification = await supabase.get_verification_by_id(verification_id)
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    if verification["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check SheerID status if available
    if verification.get("sheerid_verification_id") and verification["status"] == "processing":
        sheerid = get_sheerid_service()
        try:
            result = await sheerid.check_verification_status(
                verification["sheerid_verification_id"]
            )
            if result.get("success"):
                new_status = result.get("status")
                if new_status and new_status != verification["status"]:
                    await supabase.update_verification(
                        verification_id,
                        {
                            "status": new_status,
                            "response_data": result
                        }
                    )
                    verification["status"] = new_status
        finally:
            await sheerid.close()
    
    # Build veteran response if available
    veteran_response = None
    if verification.get("veterans"):
        v = verification["veterans"]
        from ..models import VeteranResponse, MilitaryBranch, MilitaryStatus
        veteran_response = VeteranResponse(
            id=v["id"],
            first_name=v["first_name"],
            last_name=v["last_name"],
            birth_date=v.get("birth_date"),
            branch=MilitaryBranch(v["branch_code"]) if v.get("branch_code") else MilitaryBranch.ARMY,
            military_status=MilitaryStatus(v.get("military_status", "VETERAN")),
            discharge_date=v.get("discharge_date"),
            is_verified=v.get("is_verified", False),
            source=v.get("source"),
            created_at=datetime.fromisoformat(v["created_at"].replace("Z", "+00:00"))
        )
    
    return VerificationStatusResponse(
        verification_id=verification["id"],
        status=VerificationStatus(verification["status"]),
        service_type=verification["service_type"],
        veteran=veteran_response,
        created_at=datetime.fromisoformat(verification["created_at"].replace("Z", "+00:00")),
        submitted_at=datetime.fromisoformat(verification["submitted_at"].replace("Z", "+00:00")) if verification.get("submitted_at") else None,
        completed_at=datetime.fromisoformat(verification["completed_at"].replace("Z", "+00:00")) if verification.get("completed_at") else None,
        error_message=verification.get("error_message")
    )


@router.post("/{verification_id}/document", response_model=UploadDocumentResponse)
async def upload_document(
    verification_id: str,
    document_type: str,
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    """
    Upload a verification document (DD-214, Military ID, etc.).
    """
    supabase = get_supabase_service()
    
    verification = await supabase.get_verification_by_id(verification_id)
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    if verification["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if verification["status"] != "document_required":
        raise HTTPException(
            status_code=400,
            detail="Document upload not required or already uploaded"
        )
    
    # Read file content
    content = await file.read()
    
    # Upload to SheerID
    status = VerificationStatus.PROCESSING
    message = "Document uploaded successfully"
    
    if verification.get("sheerid_verification_id"):
        sheerid = get_sheerid_service()
        try:
            result = await sheerid.upload_document(
                verification["sheerid_verification_id"],
                content,
                document_type
            )
            
            if result.get("success"):
                message = "Document uploaded, verification in progress"
            else:
                status = VerificationStatus.ERROR
                message = result.get("error", "Failed to upload document")
                
        finally:
            await sheerid.close()
    
    # Update verification
    await supabase.update_verification(
        verification_id,
        {
            "status": status.value,
            "document_type": document_type
        }
    )
    
    return UploadDocumentResponse(
        verification_id=verification_id,
        document_url="",  # Would be storage URL in production
        status=status,
        message=message
    )
