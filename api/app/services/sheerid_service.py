"""
Veterans Verification API - SheerID Service
"""
import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime, date

from ..config import get_settings
from ..utils import get_sheerid_headers, get_branch_org_id, generate_fingerprint

logger = logging.getLogger(__name__)

SHEERID_API = "https://services.sheerid.com/rest/v2"
CHATGPT_API = "https://chatgpt.com/backend-api"
DEFAULT_PROGRAM_ID = "690415d58971e73ca187d8c9"


class SheerIDService:
    """Service for interacting with SheerID API."""
    
    def __init__(self, access_token: Optional[str] = None):
        settings = get_settings()
        self.program_id = settings.sheerid_program_id or DEFAULT_PROGRAM_ID
        self.access_token = access_token
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    def _get_chatgpt_headers(self) -> Dict[str, str]:
        """Get headers for ChatGPT API requests."""
        import uuid
        return {
            "sec-ch-ua": '"Chromium";v="131", "Google Chrome";v="131"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
            "accept": "application/json",
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {self.access_token}" if self.access_token else "",
            "origin": "https://chatgpt.com",
            "oai-device-id": str(uuid.uuid4()),
            "oai-language": "en-US",
            "referer": "https://chatgpt.com/veterans-claim"
        }
    
    async def create_verification(self, service_type: str = "chatgpt") -> Dict[str, Any]:
        """
        Step 1: Create a new verification request.
        Returns verification_id from the service.
        """
        logger.info(f"Creating verification for service: {service_type}")
        
        if service_type == "chatgpt":
            try:
                response = await self.client.post(
                    f"{CHATGPT_API}/veterans/create_verification",
                    headers=self._get_chatgpt_headers(),
                    json={"program_id": self.program_id}
                )
                response.raise_for_status()
                data = response.json()
                return {
                    "success": True,
                    "verification_id": data.get("verification_id"),
                    "service": "chatgpt"
                }
            except httpx.HTTPError as e:
                logger.error(f"Error creating ChatGPT verification: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "service": "chatgpt"
                }
        else:
            # For other services, return a placeholder
            # In production, implement specific service integrations
            return {
                "success": True,
                "verification_id": None,
                "service": service_type,
                "message": f"Direct {service_type} integration not implemented"
            }
    
    async def submit_military_status(
        self, 
        verification_id: str, 
        status: str = "VETERAN"
    ) -> Dict[str, Any]:
        """
        Step 2: Submit military status to SheerID.
        """
        logger.info(f"Submitting military status: {status}")
        
        try:
            response = await self.client.post(
                f"{SHEERID_API}/verification/{verification_id}/step/collectMilitaryStatus",
                headers=get_sheerid_headers(),
                json={"status": status}
            )
            response.raise_for_status()
            return {
                "success": True,
                "verification_id": verification_id,
                "status": status
            }
        except httpx.HTTPError as e:
            logger.error(f"Error submitting military status: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def submit_personal_info(
        self,
        verification_id: str,
        first_name: str,
        last_name: str,
        birth_date: date,
        branch: str,
        discharge_date: Optional[date] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Step 3: Submit personal information for verification.
        """
        logger.info(f"Submitting personal info for: {first_name} {last_name}")
        
        org = get_branch_org_id(branch)
        fingerprint = generate_fingerprint()
        
        # Format dates
        birth_date_str = birth_date.strftime("%Y-%m-%d") if isinstance(birth_date, date) else birth_date
        discharge_date_str = None
        if discharge_date:
            discharge_date_str = discharge_date.strftime("%Y-%m-%d") if isinstance(discharge_date, date) else discharge_date
        
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "birthDate": birth_date_str,
            "organization": org,
            "metadata": {
                "fingerprint": fingerprint
            }
        }
        
        if email:
            payload["email"] = email
        
        if discharge_date_str:
            payload["dischargeDate"] = discharge_date_str
        
        try:
            response = await self.client.post(
                f"{SHEERID_API}/verification/{verification_id}/step/collectMilitaryPersonalInfo",
                headers=get_sheerid_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            # Check verification result
            current_step = data.get("currentStep", "")
            
            if current_step == "success":
                return {
                    "success": True,
                    "status": "approved",
                    "verification_id": verification_id,
                    "message": "Verification approved"
                }
            elif current_step == "docUpload":
                return {
                    "success": True,
                    "status": "document_required",
                    "verification_id": verification_id,
                    "message": "Document upload required"
                }
            else:
                return {
                    "success": True,
                    "status": "processing",
                    "verification_id": verification_id,
                    "current_step": current_step,
                    "message": f"Verification in progress: {current_step}"
                }
                
        except httpx.HTTPError as e:
            logger.error(f"Error submitting personal info: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def upload_document(
        self,
        verification_id: str,
        document_data: bytes,
        document_type: str = "DD214"
    ) -> Dict[str, Any]:
        """
        Step 4: Upload verification document.
        """
        logger.info(f"Uploading document type: {document_type}")
        
        try:
            # First, get upload URL
            response = await self.client.post(
                f"{SHEERID_API}/verification/{verification_id}/step/docUpload",
                headers=get_sheerid_headers(),
                files={"file": ("document.jpg", document_data, "image/jpeg")}
            )
            response.raise_for_status()
            
            # Complete upload
            complete_response = await self.client.post(
                f"{SHEERID_API}/verification/{verification_id}/step/completeDocUpload",
                headers=get_sheerid_headers(),
                json={}
            )
            complete_response.raise_for_status()
            
            return {
                "success": True,
                "verification_id": verification_id,
                "message": "Document uploaded successfully"
            }
            
        except httpx.HTTPError as e:
            logger.error(f"Error uploading document: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_verification_status(
        self, 
        verification_id: str
    ) -> Dict[str, Any]:
        """
        Check the current status of a verification.
        """
        logger.info(f"Checking verification status: {verification_id}")
        
        try:
            response = await self.client.get(
                f"{SHEERID_API}/verification/{verification_id}",
                headers=get_sheerid_headers()
            )
            response.raise_for_status()
            data = response.json()
            
            current_step = data.get("currentStep", "unknown")
            
            status_map = {
                "success": "approved",
                "rejected": "rejected",
                "docUpload": "document_required",
                "pending": "processing",
            }
            
            return {
                "success": True,
                "verification_id": verification_id,
                "status": status_map.get(current_step, "processing"),
                "current_step": current_step,
                "data": data
            }
            
        except httpx.HTTPError as e:
            logger.error(f"Error checking verification status: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Factory function
def get_sheerid_service(access_token: Optional[str] = None) -> SheerIDService:
    """Get SheerID service instance."""
    return SheerIDService(access_token=access_token)
