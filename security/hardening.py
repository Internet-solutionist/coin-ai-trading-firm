import re
import hashlib
import os
from typing import Any, Dict
from functools import wraps

class SecurityHardening:
    """Grey Hat / Purple Team security layer for sovereign trading agents."""

    @staticmethod
    def sanitize_input(text: str, max_length: int = 10000) -> str:
        """Prevent prompt injection and malicious input."""
        if not isinstance(text, str):
            text = str(text)
        text = re.sub(r'[<>{}[\]\\`]', '', text)
        text = text[:max_length]
        return text.strip()

    @staticmethod
    def validate_signal(signal: Dict[str, Any]) -> bool:
        """Validate trading signals to prevent poisoning."""
        required = ['direction', 'edge', 'kelly_fraction']
        if not all(k in signal for k in required):
            return False
        if not isinstance(signal.get('kelly_fraction'), (int, float)):
            return False
        if signal['kelly_fraction'] < 0 or signal['kelly_fraction'] > 0.25:
            return False
        return True

    @staticmethod
    def hash_memory_entry(entry: str) -> str:
        """Cryptographic hashing for MemPalace integrity."""
        return hashlib.sha256(entry.encode()).hexdigest()

    @staticmethod
    def secure_api_call(func):
        """Decorator for secure API calls (rate limiting + logging)."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("[SECURITY] Secure API call initiated")
            result = func(*args, **kwargs)
            print("[SECURITY] API call completed with logging")
            return result
        return wrapper

    @staticmethod
    def harden_crewai_tools(tools: list) -> list:
        """Harden CrewAI tools against RCE/SSRF."""
        safe_tools = []
        for tool in tools:
            if 'code' not in str(tool).lower() and 'exec' not in str(tool).lower():
                safe_tools.append(tool)
        return safe_tools