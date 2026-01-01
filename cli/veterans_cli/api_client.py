"""
Veterans CLI - API Client
"""
import requests
from typing import Optional, Dict, Any


class APIClient:
    """Client for communicating with the Veterans Verification API."""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an API request."""
        url = f"{self.api_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def create_verification(self, service_type: str, program_id: Optional[str] = None) -> Dict:
        """Create a new verification request."""
        data = {"serviceType": service_type}
        if program_id:
            data["programId"] = program_id
        return self._request("POST", "/api/verify/create", json=data)
    
    def submit_verification(
        self,
        verification_id: str,
        first_name: str,
        last_name: str,
        birth_date: str,
        branch: str,
        military_status: str,
        email: str,
        discharge_date: Optional[str] = None,
    ) -> Dict:
        """Submit veteran information for verification."""
        data = {
            "verificationId": verification_id,
            "veteran": {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": birth_date,
                "branch": branch,
                "militaryStatus": military_status,
            },
            "email": email,
        }
        if discharge_date:
            data["veteran"]["dischargeDate"] = discharge_date
        
        return self._request("POST", "/api/verify/submit", json=data)
    
    def get_status(self, verification_id: str) -> Dict:
        """Get verification status."""
        return self._request("GET", f"/api/verify/{verification_id}/status")
    
    def search_grave_locator(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        state: Optional[str] = None,
    ) -> Dict:
        """Search VA Grave Locator."""
        params = {}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if state:
            params["state"] = state
        return self._request("GET", "/api/lookup/grave", params=params)
    
    def search_vlm(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> Dict:
        """Search Veterans Legacy Memorial."""
        params = {}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if branch:
            params["branch"] = branch
        return self._request("GET", "/api/lookup/vlm", params=params)
    
    def search_army_explorer(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Dict:
        """Search Army National Cemetery Explorer."""
        params = {}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        return self._request("GET", "/api/lookup/army", params=params)
    
    def search_all_sources(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> Dict:
        """Search all VA sources."""
        params = {}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if branch:
            params["branch"] = branch
        return self._request("GET", "/api/lookup/aggregate", params=params)
    
    def get_history(self, page: int = 1, per_page: int = 20) -> Dict:
        """Get verification history."""
        params = {"page": page, "per_page": per_page}
        return self._request("GET", "/api/history", params=params)
