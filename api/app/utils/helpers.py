"""
Veterans Verification API - Utility Functions
"""
import hashlib
import time
import uuid
import base64
import json
from typing import Dict


# Military Branch to SheerID Organization ID mapping
BRANCH_ORG_MAP = {
    "Army": {"id": 4070, "name": "Army"},
    "Air Force": {"id": 4073, "name": "Air Force"},
    "Navy": {"id": 4072, "name": "Navy"},
    "Marine Corps": {"id": 4071, "name": "Marine Corps"},
    "Coast Guard": {"id": 4074, "name": "Coast Guard"},
    "Space Force": {"id": 4544268, "name": "Space Force"},
    "Army National Guard": {"id": 4075, "name": "Army National Guard"},
    "Army Reserve": {"id": 4076, "name": "Army Reserve"},
    "Air National Guard": {"id": 4079, "name": "Air National Guard"},
    "Air Force Reserve": {"id": 4080, "name": "Air Force Reserve"},
    "Navy Reserve": {"id": 4078, "name": "Navy Reserve"},
    "Marine Corps Reserve": {"id": 4077, "name": "Marine Corps Forces Reserve"},
    "Coast Guard Reserve": {"id": 4081, "name": "Coast Guard Reserve"},
}


def generate_fingerprint() -> str:
    """Generate a device fingerprint for SheerID requests."""
    screens = ["1920x1080", "2560x1440", "1366x768", "1440x900", "1536x864"]
    screen = screens[hash(str(time.time())) % len(screens)]
    raw = f"{screen}|{time.time()}|{uuid.uuid4()}"
    return hashlib.md5(raw.encode()).hexdigest()


def generate_newrelic_headers() -> Dict[str, str]:
    """Generate NewRelic tracking headers for SheerID requests."""
    trace_id = (uuid.uuid4().hex + uuid.uuid4().hex[:8])[:32]
    span_id = uuid.uuid4().hex[:16]
    timestamp = int(time.time() * 1000)

    payload = {
        "v": [0, 1],
        "d": {
            "ty": "Browser",
            "ac": "364029",
            "ap": "134291347",
            "id": span_id,
            "tr": trace_id,
            "ti": timestamp
        }
    }

    return {
        "newrelic": base64.b64encode(json.dumps(payload).encode()).decode(),
        "traceparent": f"00-{trace_id}-{span_id}-01",
        "tracestate": f"364029@nr=0-1-364029-134291347-{span_id}----{timestamp}"
    }


def get_sheerid_headers(include_newrelic: bool = True) -> Dict[str, str]:
    """Get headers for SheerID API requests."""
    headers = {
        "sec-ch-ua": '"Chromium";v="131", "Google Chrome";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json",
        "content-type": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "clientversion": "2.157.0",
        "clientname": "jslib",
        "origin": "https://services.sheerid.com"
    }
    
    if include_newrelic:
        nr_headers = generate_newrelic_headers()
        headers.update(nr_headers)
    
    return headers


def get_branch_org_id(branch_name: str) -> Dict:
    """Get SheerID organization info for a military branch."""
    return BRANCH_ORG_MAP.get(branch_name, BRANCH_ORG_MAP["Army"])


def normalize_branch_name(input_str: str) -> str:
    """Normalize and match input string to a valid branch name."""
    normalized = input_str.upper().replace("US ", "").strip()

    # Direct match
    for branch in BRANCH_ORG_MAP:
        if branch.upper() == normalized:
            return branch

    # Fuzzy matching
    if "MARINE" in normalized and "RESERVE" not in normalized:
        return "Marine Corps"
    if "ARMY" in normalized and "NATIONAL" in normalized:
        return "Army National Guard"
    if "ARMY" in normalized and "RESERVE" in normalized:
        return "Army Reserve"
    if "ARMY" in normalized:
        return "Army"
    if "NAVY" in normalized and "RESERVE" in normalized:
        return "Navy Reserve"
    if "NAVY" in normalized:
        return "Navy"
    if "AIR" in normalized and "NATIONAL" in normalized:
        return "Air National Guard"
    if "AIR" in normalized and "RESERVE" in normalized:
        return "Air Force Reserve"
    if "AIR" in normalized:
        return "Air Force"
    if "COAST" in normalized and "RESERVE" in normalized:
        return "Coast Guard Reserve"
    if "COAST" in normalized:
        return "Coast Guard"
    if "SPACE" in normalized:
        return "Space Force"

    return "Army"  # Default
