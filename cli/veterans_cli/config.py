"""
Veterans CLI - Configuration Management
"""
import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


CONFIG_DIR = Path.home() / ".veterans-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    """CLI configuration."""
    api_key: str
    api_url: str = "http://localhost:8000"


def get_config() -> Optional[Config]:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        return None
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return Config(**data)
    except Exception:
        return None


def save_config(config: Config) -> None:
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "api_key": config.api_key,
            "api_url": config.api_url,
        }, f, indent=2)


def delete_config() -> None:
    """Delete configuration file."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
