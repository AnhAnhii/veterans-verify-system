"""
Veterans Verification API - VA Lookup Service
"""
import httpx
import logging
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup
import re

from ..models import VASource, VALookupResult
from .supabase_service import get_supabase_service

logger = logging.getLogger(__name__)


class VALookupService:
    """Service for looking up veteran information from VA public databases."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
                "Accept": "application/json, text/html",
                "Accept-Language": "en-US,en;q=0.9"
            }
        )
        self.supabase = get_supabase_service()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def search_grave_locator(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        state: Optional[str] = None,
        use_cache: bool = True
    ) -> List[VALookupResult]:
        """
        Search the VA National Gravesite Locator.
        URL: https://gravelocator.cem.va.gov/
        """
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        if use_cache:
            cached = await self.supabase.get_cached_lookup("grave_locator", query)
            if cached:
                logger.info(f"Using cached grave locator results for: {query}")
                return [VALookupResult(**r) for r in cached.get("results", [])]
        
        results = []
        
        try:
            # VA Grave Locator API endpoint
            search_url = "https://gravelocator.cem.va.gov/ngl/search"
            
            params = {}
            if first_name:
                params["firstName"] = first_name
            if last_name:
                params["lastName"] = last_name
            if state:
                params["state"] = state
            
            response = await self.client.get(search_url, params=params)
            
            if response.status_code == 200:
                data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                
                for record in data.get("results", []):
                    results.append(VALookupResult(
                        source=VASource.GRAVE_LOCATOR,
                        name=f"{record.get('firstName', '')} {record.get('lastName', '')}".strip(),
                        branch=record.get("branchOfService"),
                        rank=record.get("rank"),
                        birth_date=record.get("birthDate"),
                        death_date=record.get("deathDate"),
                        cemetery=record.get("cemeteryName"),
                        location=f"{record.get('cemeteryCity', '')}, {record.get('cemeteryState', '')}".strip(", "),
                        service_dates=record.get("serviceDates"),
                        metadata=record
                    ))
            
        except httpx.HTTPError as e:
            logger.error(f"Error searching grave locator: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in grave locator search: {e}")
        
        # Cache results
        if results and use_cache:
            await self.supabase.cache_lookup_result(
                "grave_locator", 
                query, 
                [r.model_dump() for r in results]
            )
        
        return results
    
    async def search_veterans_legacy_memorial(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        branch: Optional[str] = None,
        use_cache: bool = True
    ) -> List[VALookupResult]:
        """
        Search the Veterans Legacy Memorial.
        URL: https://www.vlm.cem.va.gov/
        """
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        if use_cache:
            cached = await self.supabase.get_cached_lookup("vlm", query)
            if cached:
                logger.info(f"Using cached VLM results for: {query}")
                return [VALookupResult(**r) for r in cached.get("results", [])]
        
        results = []
        
        try:
            # VLM search API
            search_url = "https://www.vlm.cem.va.gov/SEARCH/SearchVeterans"
            
            payload = {
                "veteranName": query,
                "branch": branch or "",
                "page": 1,
                "pageSize": 50
            }
            
            response = await self.client.post(
                search_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                
                for record in data.get("veterans", []):
                    results.append(VALookupResult(
                        source=VASource.VLM,
                        name=record.get("veteranName", ""),
                        branch=record.get("branchOfService"),
                        rank=record.get("rank"),
                        birth_date=record.get("birthYear"),
                        death_date=record.get("deathYear"),
                        cemetery=record.get("cemeteryName"),
                        location=record.get("cemeteryLocation"),
                        service_dates=f"{record.get('serviceStartDate', '')} - {record.get('serviceEndDate', '')}".strip(" -"),
                        awards=record.get("awards", []),
                        metadata=record
                    ))
            
        except httpx.HTTPError as e:
            logger.error(f"Error searching VLM: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in VLM search: {e}")
        
        # Cache results
        if results and use_cache:
            await self.supabase.cache_lookup_result(
                "vlm", 
                query, 
                [r.model_dump() for r in results]
            )
        
        return results
    
    async def search_army_explorer(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        use_cache: bool = True
    ) -> List[VALookupResult]:
        """
        Search the Army National Cemetery Explorer.
        URL: https://ancexplorer.army.mil/
        """
        query = f"{first_name or ''} {last_name or ''}".strip()
        
        if use_cache:
            cached = await self.supabase.get_cached_lookup("army_explorer", query)
            if cached:
                logger.info(f"Using cached Army Explorer results for: {query}")
                return [VALookupResult(**r) for r in cached.get("results", [])]
        
        results = []
        
        try:
            # Army Explorer API
            search_url = "https://ancexplorer.army.mil/publicwmv/api/search"
            
            payload = {
                "searchTerm": query,
                "searchType": "all",
                "page": 1,
                "pageSize": 50
            }
            
            response = await self.client.post(
                search_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                
                for record in data.get("results", []):
                    full_name = f"{record.get('firstName', '')} {record.get('middleName', '')} {record.get('lastName', '')}".strip()
                    full_name = re.sub(r'\s+', ' ', full_name)
                    
                    results.append(VALookupResult(
                        source=VASource.ARMY_EXPLORER,
                        name=full_name,
                        branch=record.get("branch"),
                        rank=record.get("rank"),
                        birth_date=record.get("birthDate"),
                        death_date=record.get("deathDate"),
                        cemetery=record.get("cemetery"),
                        location=record.get("section"),
                        service_dates=None,
                        metadata=record
                    ))
            
        except httpx.HTTPError as e:
            logger.error(f"Error searching Army Explorer: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Army Explorer search: {e}")
        
        # Cache results
        if results and use_cache:
            await self.supabase.cache_lookup_result(
                "army_explorer", 
                query, 
                [r.model_dump() for r in results]
            )
        
        return results
    
    async def search_all_sources(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        branch: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, List[VALookupResult]]:
        """
        Search all VA sources and aggregate results.
        """
        results = {
            "grave_locator": [],
            "vlm": [],
            "army_explorer": []
        }
        
        # Search all sources concurrently
        import asyncio
        
        grave_task = self.search_grave_locator(first_name, last_name, use_cache=use_cache)
        vlm_task = self.search_veterans_legacy_memorial(first_name, last_name, branch, use_cache=use_cache)
        army_task = self.search_army_explorer(first_name, last_name, use_cache=use_cache)
        
        grave_results, vlm_results, army_results = await asyncio.gather(
            grave_task, vlm_task, army_task,
            return_exceptions=True
        )
        
        if not isinstance(grave_results, Exception):
            results["grave_locator"] = grave_results
        else:
            logger.error(f"Grave locator search failed: {grave_results}")
        
        if not isinstance(vlm_results, Exception):
            results["vlm"] = vlm_results
        else:
            logger.error(f"VLM search failed: {vlm_results}")
        
        if not isinstance(army_results, Exception):
            results["army_explorer"] = army_results
        else:
            logger.error(f"Army Explorer search failed: {army_results}")
        
        return results


# Singleton instance
_va_lookup_service: Optional[VALookupService] = None


def get_va_lookup_service() -> VALookupService:
    """Get singleton VA lookup service instance."""
    global _va_lookup_service
    if _va_lookup_service is None:
        _va_lookup_service = VALookupService()
    return _va_lookup_service
