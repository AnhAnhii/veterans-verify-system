"""
Veterans Verification API - VA Lookup Router
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from ..models import (
    VALookupRequest,
    VALookupResponse,
    VAAggregateResponse,
    VASource,
    MilitaryBranch,
)
from ..services import get_va_lookup_service

router = APIRouter(prefix="/lookup", tags=["VA Lookup"])


@router.get("/grave", response_model=VALookupResponse)
async def search_grave_locator(
    first_name: Optional[str] = Query(None, description="First name to search"),
    last_name: Optional[str] = Query(None, description="Last name to search"),
    state: Optional[str] = Query(None, description="State code (e.g., CA, TX)"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    """
    Search the VA National Gravesite Locator.
    
    This searches the public database of veterans buried in VA national cemeteries.
    """
    if not first_name and not last_name:
        raise HTTPException(
            status_code=400,
            detail="At least first_name or last_name is required"
        )
    
    va_service = get_va_lookup_service()
    
    try:
        results = await va_service.search_grave_locator(
            first_name=first_name,
            last_name=last_name,
            state=state,
            use_cache=use_cache
        )
        
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        return VALookupResponse(
            query=query,
            source=VASource.GRAVE_LOCATOR,
            total_results=len(results),
            results=results,
            cached=use_cache
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vlm", response_model=VALookupResponse)
async def search_veterans_legacy_memorial(
    first_name: Optional[str] = Query(None, description="First name to search"),
    last_name: Optional[str] = Query(None, description="Last name to search"),
    branch: Optional[MilitaryBranch] = Query(None, description="Military branch"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    """
    Search the Veterans Legacy Memorial.
    
    This searches veteran memorial pages with photos, stories, and tributes.
    """
    if not first_name and not last_name:
        raise HTTPException(
            status_code=400,
            detail="At least first_name or last_name is required"
        )
    
    va_service = get_va_lookup_service()
    
    try:
        results = await va_service.search_veterans_legacy_memorial(
            first_name=first_name,
            last_name=last_name,
            branch=branch.value if branch else None,
            use_cache=use_cache
        )
        
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        return VALookupResponse(
            query=query,
            source=VASource.VLM,
            total_results=len(results),
            results=results,
            cached=use_cache
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/army", response_model=VALookupResponse)
async def search_army_explorer(
    first_name: Optional[str] = Query(None, description="First name to search"),
    last_name: Optional[str] = Query(None, description="Last name to search"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    """
    Search the Army National Cemetery Explorer.
    
    This searches Arlington National Cemetery and other Army cemeteries.
    """
    if not first_name and not last_name:
        raise HTTPException(
            status_code=400,
            detail="At least first_name or last_name is required"
        )
    
    va_service = get_va_lookup_service()
    
    try:
        results = await va_service.search_army_explorer(
            first_name=first_name,
            last_name=last_name,
            use_cache=use_cache
        )
        
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        return VALookupResponse(
            query=query,
            source=VASource.ARMY_EXPLORER,
            total_results=len(results),
            results=results,
            cached=use_cache
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/aggregate", response_model=VAAggregateResponse)
async def search_all_sources(
    first_name: Optional[str] = Query(None, description="First name to search"),
    last_name: Optional[str] = Query(None, description="Last name to search"),
    branch: Optional[MilitaryBranch] = Query(None, description="Military branch"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    """
    Search all VA sources and aggregate results.
    
    This searches Grave Locator, Veterans Legacy Memorial, and Army Explorer
    simultaneously and returns combined results.
    """
    if not first_name and not last_name:
        raise HTTPException(
            status_code=400,
            detail="At least first_name or last_name is required"
        )
    
    va_service = get_va_lookup_service()
    
    try:
        results = await va_service.search_all_sources(
            first_name=first_name,
            last_name=last_name,
            branch=branch.value if branch else None,
            use_cache=use_cache
        )
        
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        # Build source responses
        sources = {}
        total = 0
        
        for source_name, source_results in results.items():
            source_enum = {
                "grave_locator": VASource.GRAVE_LOCATOR,
                "vlm": VASource.VLM,
                "army_explorer": VASource.ARMY_EXPLORER
            }.get(source_name, VASource.GRAVE_LOCATOR)
            
            sources[source_name] = VALookupResponse(
                query=query,
                source=source_enum,
                total_results=len(source_results),
                results=source_results,
                cached=use_cache
            )
            total += len(source_results)
        
        return VAAggregateResponse(
            query=query,
            total_results=total,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
