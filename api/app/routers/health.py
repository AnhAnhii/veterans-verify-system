"""
Veterans Verification API - Health Check Router
"""
from fastapi import APIRouter
from datetime import datetime

from ..models import HealthResponse
from ..config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API.
    """
    settings = get_settings()
    
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
        timestamp=datetime.utcnow()
    )


@router.get("/")
async def root():
    """
    Root endpoint.
    
    Returns basic API information.
    """
    settings = get_settings()
    
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }
