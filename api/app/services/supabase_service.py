"""
Veterans Verification API - Supabase Service
"""
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from ..config import get_settings

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for interacting with Supabase database."""
    
    def __init__(self):
        settings = get_settings()
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_key or settings.supabase_key
        )
    
    # ============================================
    # PROFILES
    # ============================================
    
    async def get_profile_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user profile by ID."""
        try:
            result = self.client.table("profiles").select("*").eq("id", user_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting profile: {e}")
            return None
    
    async def get_profile_by_api_key(self, api_key: str) -> Optional[Dict]:
        """Get user profile by API key."""
        try:
            result = self.client.table("profiles").select("*").eq("api_key", api_key).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting profile by API key: {e}")
            return None
    
    # ============================================
    # VETERANS
    # ============================================
    
    async def create_veteran(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Create a new veteran record."""
        try:
            veteran_data = {
                "user_id": user_id,
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "birth_date": data.get("birth_date"),
                "branch_code": data.get("branch"),
                "military_status": data.get("military_status", "VETERAN"),
                "discharge_date": data.get("discharge_date"),
                "source": data.get("source", "MANUAL"),
            }
            result = self.client.table("veterans").insert(veteran_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating veteran: {e}")
            return None
    
    async def get_veteran_by_id(self, veteran_id: str) -> Optional[Dict]:
        """Get veteran by ID."""
        try:
            result = self.client.table("veterans").select("*").eq("id", veteran_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting veteran: {e}")
            return None
    
    async def search_veterans(self, first_name: str = None, last_name: str = None) -> List[Dict]:
        """Search veterans by name."""
        try:
            query = self.client.table("veterans").select("*")
            if first_name:
                query = query.ilike("first_name", f"%{first_name}%")
            if last_name:
                query = query.ilike("last_name", f"%{last_name}%")
            result = query.limit(50).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error searching veterans: {e}")
            return []
    
    # ============================================
    # VERIFICATIONS
    # ============================================
    
    async def create_verification(self, user_id: str, data: Dict) -> Optional[Dict]:
        """Create a new verification request."""
        try:
            verification_data = {
                "user_id": user_id,
                "service_type": data["service_type"],
                "sheerid_program_id": data.get("program_id"),
                "status": "pending",
                "request_data": data.get("request_data", {}),
            }
            result = self.client.table("verifications").insert(verification_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating verification: {e}")
            return None
    
    async def get_verification_by_id(self, verification_id: str) -> Optional[Dict]:
        """Get verification by ID."""
        try:
            result = self.client.table("verifications").select("*, veterans(*)").eq("id", verification_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting verification: {e}")
            return None
    
    async def update_verification(self, verification_id: str, data: Dict) -> Optional[Dict]:
        """Update verification record."""
        try:
            result = self.client.table("verifications").update(data).eq("id", verification_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating verification: {e}")
            return None
    
    async def get_verification_history(
        self, 
        user_id: str, 
        page: int = 1, 
        per_page: int = 20
    ) -> Dict:
        """Get verification history for a user."""
        try:
            offset = (page - 1) * per_page
            
            # Get total count
            count_result = self.client.table("verifications").select("id", count="exact").eq("user_id", user_id).execute()
            total = count_result.count or 0
            
            # Get paginated data
            result = self.client.table("verifications")\
                .select("*, veterans(first_name, last_name)")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .range(offset, offset + per_page - 1)\
                .execute()
            
            return {
                "total": total,
                "page": page,
                "per_page": per_page,
                "items": result.data or []
            }
        except Exception as e:
            logger.error(f"Error getting verification history: {e}")
            return {"total": 0, "page": page, "per_page": per_page, "items": []}
    
    # ============================================
    # VA LOOKUP CACHE
    # ============================================
    
    async def get_cached_lookup(self, source: str, query: str) -> Optional[Dict]:
        """Get cached VA lookup result."""
        try:
            result = self.client.table("va_lookup_cache")\
                .select("*")\
                .eq("source", source)\
                .eq("search_query", query)\
                .gt("expires_at", datetime.utcnow().isoformat())\
                .single()\
                .execute()
            return result.data
        except Exception as e:
            logger.debug(f"No cache found: {e}")
            return None
    
    async def cache_lookup_result(self, source: str, query: str, results: List[Dict]) -> None:
        """Cache VA lookup result."""
        try:
            cache_data = {
                "source": source,
                "search_query": query,
                "results": results,
                "result_count": len(results),
            }
            self.client.table("va_lookup_cache").upsert(
                cache_data,
                on_conflict="source,search_query"
            ).execute()
        except Exception as e:
            logger.error(f"Error caching lookup result: {e}")
    
    # ============================================
    # API LOGS
    # ============================================
    
    async def log_api_request(
        self,
        user_id: Optional[str],
        endpoint: str,
        method: str,
        request_body: Optional[Dict] = None,
        response_status: Optional[int] = None,
        response_body: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        duration_ms: Optional[int] = None
    ) -> None:
        """Log an API request."""
        try:
            log_data = {
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "request_body": request_body,
                "response_status": response_status,
                "response_body": response_body,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "duration_ms": duration_ms,
            }
            self.client.table("api_logs").insert(log_data).execute()
        except Exception as e:
            logger.error(f"Error logging API request: {e}")


# Singleton instance
_supabase_service: Optional[SupabaseService] = None


def get_supabase_service() -> SupabaseService:
    """Get singleton Supabase service instance."""
    global _supabase_service
    if _supabase_service is None:
        _supabase_service = SupabaseService()
    return _supabase_service
