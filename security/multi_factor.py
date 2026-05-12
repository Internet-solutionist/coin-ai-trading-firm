import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import os

class MultiFactorSecurity:
    """PIN, Password, Passcodeword with recovery for trading firm actions."""

    def __init__(self, storage_path: str = "security/credentials.json"):
        self.storage_path = storage_path
        self.credentials = self._load_credentials()
        self.recovery_codes = []

    def _load_credentials(self) -> Dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"pin": None, "password_hash": None, "passcodeword": None, "recovery_codes": []}

    def _save_credentials(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.credentials, f, indent=2)

    def set_pin(self, pin: str) -> bool:
        """Set 4-6 digit PIN for quick actions (e.g., approve signal)."""
        if not pin.isdigit() or not (4 <= len(pin) <= 6):
            return False
        self.credentials["pin"] = hashlib.sha256(pin.encode()).hexdigest()
        self._save_credentials()
        return True

    def verify_pin(self, pin: str) -> bool:
        if not self.credentials.get("pin"):
            return True
        return hashlib.sha256(pin.encode()).hexdigest() == self.credentials["pin"]

    def set_password(self, password: str) -> bool:
        """Set strong password for high-risk actions (e.g., live trading toggle)."""
        if len(password) < 12:
            return False
        self.credentials["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        self._save_credentials()
        return True

    def verify_password(self, password: str) -> bool:
        if not self.credentials.get("password_hash"):
            return True
        return hashlib.sha256(password.encode()).hexdigest() == self.credentials["password_hash"]

    def set_passcodeword(self, word: str) -> bool:
        """Set memorable passcodeword for voice/text confirmation."""
        if len(word) < 6 or not word.isalpha():
            return False
        self.credentials["passcodeword"] = word.lower()
        self._save_credentials()
        return True

    def verify_passcodeword(self, word: str) -> bool:
        if not self.credentials.get("passcodeword"):
            return True
        return word.lower() == self.credentials["passcodeword"]

    def generate_recovery_codes(self, count: int = 5) -> List[str]:
        """Generate one-time recovery codes (MemPalace-encrypted in production)."""
        codes = [secrets.token_urlsafe(8) for _ in range(count)]
        self.credentials["recovery_codes"] = [hashlib.sha256(c.encode()).hexdigest() for c in codes]
        self._save_credentials()
        return codes

    def use_recovery_code(self, code: str) -> bool:
        """Use a recovery code (one-time)."""
        hashed = hashlib.sha256(code.encode()).hexdigest()
        if hashed in self.credentials.get("recovery_codes", []):
            self.credentials["recovery_codes"].remove(hashed)
            self._save_credentials()
            return True
        return False

    def require_mfa(self, action: str, pin: str = None, password: str = None, passcodeword: str = None) -> bool:
        """Require appropriate MFA based on action sensitivity."""
        if action in ["approve_signal", "view_reckoning"]:
            return self.verify_pin(pin) if pin else False
        elif action in ["toggle_live", "export_audit", "change_settings"]:
            return self.verify_password(password) and self.verify_passcodeword(passcodeword)
        elif action == "emergency_stop":
            return self.verify_passcodeword(passcodeword) or self.use_recovery_code(pin)
        return True