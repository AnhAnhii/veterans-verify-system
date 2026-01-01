"""
Veterans Verification API - Routers Package
"""
from .verification import router as verification_router
from .va_lookup import router as va_lookup_router
from .health import router as health_router
from .history import router as history_router

__all__ = [
    "verification_router",
    "va_lookup_router",
    "health_router",
    "history_router",
]
