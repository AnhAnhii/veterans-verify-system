"""
Veterans Verification API - History Router
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional

from ..models import VerificationHistoryResponse, VerificationHistoryItem, VerificationStatus, ServiceType
from ..services import get_supabase_service
from .verification import get_current_user

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=VerificationHistoryResponse)
async def get_verification_history(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[VerificationStatus] = Query(None, description="Filter by status"),
    service_type: Optional[ServiceType] = Query(None, description="Filter by service type"),
    user: dict = Depends(get_current_user)
):
    """
    Get verification history for the authenticated user.
    
    Returns a paginated list of all verification requests.
    """
    supabase = get_supabase_service()
    
    result = await supabase.get_verification_history(
        user_id=user["id"],
        page=page,
        per_page=per_page
    )
    
    # Transform items
    items = []
    for v in result.get("items", []):
        veteran_name = None
        if v.get("veterans"):
            vet = v["veterans"]
            veteran_name = f"{vet.get('first_name', '')} {vet.get('last_name', '')}".strip()
        
        # Apply filters
        if status and v["status"] != status.value:
            continue
        if service_type and v["service_type"] != service_type.value:
            continue
        
        from datetime import datetime
        
        items.append(VerificationHistoryItem(
            id=v["id"],
            service_type=ServiceType(v["service_type"]),
            status=VerificationStatus(v["status"]),
            veteran_name=veteran_name,
            created_at=datetime.fromisoformat(v["created_at"].replace("Z", "+00:00")),
            completed_at=datetime.fromisoformat(v["completed_at"].replace("Z", "+00:00")) if v.get("completed_at") else None
        ))
    
    return VerificationHistoryResponse(
        total=result["total"],
        page=page,
        per_page=per_page,
        items=items
    )
