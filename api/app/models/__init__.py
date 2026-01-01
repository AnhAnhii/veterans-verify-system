"""
Veterans Verification API - Models Package
"""
from .schemas import (
    # Enums
    MilitaryBranch,
    MilitaryStatus,
    VerificationStatus,
    ServiceType,
    VASource,
    
    # Veteran Models
    VeteranBase,
    VeteranCreate,
    VeteranResponse,
    
    # Verification Models
    CreateVerificationRequest,
    CreateVerificationResponse,
    SubmitVerificationRequest,
    SubmitVerificationResponse,
    VerificationStatusResponse,
    UploadDocumentRequest,
    UploadDocumentResponse,
    
    # VA Lookup Models
    VALookupRequest,
    VALookupResult,
    VALookupResponse,
    VAAggregateResponse,
    
    # API Models
    APIResponse,
    APIError,
    HealthResponse,
    
    # History Models
    VerificationHistoryItem,
    VerificationHistoryResponse,
)

__all__ = [
    "MilitaryBranch",
    "MilitaryStatus",
    "VerificationStatus",
    "ServiceType",
    "VASource",
    "VeteranBase",
    "VeteranCreate",
    "VeteranResponse",
    "CreateVerificationRequest",
    "CreateVerificationResponse",
    "SubmitVerificationRequest",
    "SubmitVerificationResponse",
    "VerificationStatusResponse",
    "UploadDocumentRequest",
    "UploadDocumentResponse",
    "VALookupRequest",
    "VALookupResult",
    "VALookupResponse",
    "VAAggregateResponse",
    "APIResponse",
    "APIError",
    "HealthResponse",
    "VerificationHistoryItem",
    "VerificationHistoryResponse",
]
