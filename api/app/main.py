"""
Veterans Verification API - Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import get_settings
from .routers import (
    verification_router,
    va_lookup_router,
    health_router,
    history_router,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="""
    ## Veterans Verification API
    
    A comprehensive API for verifying U.S. military veteran status and 
    looking up veteran information from public VA databases.
    
    ### Features
    
    - **Verification**: Verify veteran status through SheerID integration
    - **VA Lookup**: Search public VA databases (Grave Locator, VLM, Army Explorer)
    - **History**: Track verification history
    
    ### Authentication
    
    Use either:
    - Bearer token in `Authorization` header
    - API key in `X-API-Key` header
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(verification_router, prefix="/api")
app.include_router(va_lookup_router, prefix="/api")
app.include_router(history_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"CORS Origins: {settings.cors_origins_list}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down...")


# For Vercel serverless
handler = app
