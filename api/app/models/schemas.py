"""
Veterans Verification API - Pydantic Models
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal, Dict, Any
from datetime import date, datetime
from enum import Enum


# ============================================
# ENUMS
# ============================================

class MilitaryBranch(str, Enum):
    ARMY = "Army"
    NAVY = "Navy"
    AIR_FORCE = "Air Force"
    MARINE_CORPS = "Marine Corps"
    COAST_GUARD = "Coast Guard"
    SPACE_FORCE = "Space Force"
    ARMY_NATIONAL_GUARD = "Army National Guard"
    ARMY_RESERVE = "Army Reserve"
    AIR_NATIONAL_GUARD = "Air National Guard"
    AIR_FORCE_RESERVE = "Air Force Reserve"
    NAVY_RESERVE = "Navy Reserve"
    MARINE_CORPS_RESERVE = "Marine Corps Reserve"
    COAST_GUARD_RESERVE = "Coast Guard Reserve"


class MilitaryStatus(str, Enum):
    ACTIVE_DUTY = "ACTIVE_DUTY"
    VETERAN = "VETERAN"
    RESERVE = "RESERVE"
    RETIRED = "RETIRED"


class VerificationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    DOCUMENT_REQUIRED = "document_required"
    ERROR = "error"
    EXPIRED = "expired"


class ServiceType(str, Enum):
    CHATGPT = "chatgpt"
    SPOTIFY = "spotify"
    YOUTUBE = "youtube"
    GOOGLE_ONE = "google_one"
    OTHER = "other"


class VASource(str, Enum):
    GRAVE_LOCATOR = "grave_locator"
    VLM = "vlm"
    ARMY_EXPLORER = "army_explorer"


# ============================================
# VETERAN MODELS
# ============================================

class VeteranBase(BaseModel):
    """Base veteran information."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    birth_date: Optional[date] = None
    branch: MilitaryBranch
    military_status: MilitaryStatus = MilitaryStatus.VETERAN
    discharge_date: Optional[date] = None


class VeteranCreate(VeteranBase):
    """Create veteran request."""
    pass


class VeteranResponse(VeteranBase):
    """Veteran response with ID."""
    id: str
    is_verified: bool = False
    source: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# VERIFICATION MODELS
# ============================================

class CreateVerificationRequest(BaseModel):
    """Request to create a new verification."""
    service_type: ServiceType
    program_id: Optional[str] = None


class CreateVerificationResponse(BaseModel):
    """Response after creating verification."""
    verification_id: str
    sheerid_verification_id: Optional[str] = None
    status: VerificationStatus = VerificationStatus.PENDING
    created_at: datetime


class SubmitVerificationRequest(BaseModel):
    """Request to submit veteran info for verification."""
    verification_id: str
    veteran: VeteranCreate
    email: EmailStr


class SubmitVerificationResponse(BaseModel):
    """Response after submitting verification."""
    verification_id: str
    status: VerificationStatus
    message: str
    next_step: Optional[str] = None


class VerificationStatusResponse(BaseModel):
    """Verification status response."""
    verification_id: str
    status: VerificationStatus
    service_type: ServiceType
    veteran: Optional[VeteranResponse] = None
    created_at: datetime
    submitted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class UploadDocumentRequest(BaseModel):
    """Request to upload verification document."""
    document_type: Literal["DD214", "MILITARY_ID", "VA_CARD", "OTHER"]


class UploadDocumentResponse(BaseModel):
    """Response after document upload."""
    verification_id: str
    document_url: str
    status: VerificationStatus
    message: str


# ============================================
# VA LOOKUP MODELS
# ============================================

class VALookupRequest(BaseModel):
    """Request to search VA databases."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    branch: Optional[MilitaryBranch] = None
    state: Optional[str] = None


class VALookupResult(BaseModel):
    """Single VA lookup result."""
    source: VASource
    name: str
    branch: Optional[str] = None
    rank: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    cemetery: Optional[str] = None
    location: Optional[str] = None
    service_dates: Optional[str] = None
    awards: Optional[List[str]] = None
    metadata: Dict[str, Any] = {}


class VALookupResponse(BaseModel):
    """Response containing VA lookup results."""
    query: str
    source: Optional[VASource] = None
    total_results: int
    results: List[VALookupResult]
    cached: bool = False


class VAAggregateResponse(BaseModel):
    """Aggregated response from all VA sources."""
    query: str
    total_results: int
    sources: Dict[str, VALookupResponse]


# ============================================
# API RESPONSE MODELS
# ============================================

class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None


class APIError(BaseModel):
    """API error response."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    environment: str
    timestamp: datetime


# ============================================
# HISTORY MODELS
# ============================================

class VerificationHistoryItem(BaseModel):
    """Single verification history item."""
    id: str
    service_type: ServiceType
    status: VerificationStatus
    veteran_name: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class VerificationHistoryResponse(BaseModel):
    """Verification history response."""
    total: int
    page: int
    per_page: int
    items: List[VerificationHistoryItem]
