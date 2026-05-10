"""
CoIn LLM Configuration
Primary recommendation: Grok (xAI) for superior multi-step reasoning and tool use.
Fully swappable — any OpenAI-compatible endpoint works.
"""

import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "grok")  # grok | openai | ollama | anthropic

# Grok (xAI) — Recommended
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
GROK_BASE_URL = "https://api.x.ai/v1"
GROK_MODEL = os.getenv("GROK_MODEL", "grok-2-latest")

# Fallback / Alternative (OpenAI compatible)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Local sovereign (Ollama example)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:70b")

# Default system prompt style
DEFAULT_TEMPERATURE = 0.2  # Low for deterministic trading logic
MAX_TOKENS = 4096

def get_llm_client():
    """
    Returns a client object ready for agent use.
    In production, replace with your actual Grok / xAI SDK or OpenAI client.
    This stub allows immediate demo runs.
    """
    if LLM_PROVIDER == "grok" and GROK_API_KEY:
        # Example: from xai import Grok  (user installs xai-sdk or uses openai compat)
        print("[CoIn] Using Grok (xAI) as primary reasoning engine — best in class for agentic trading.")
        # Placeholder — user should implement real client
        return {"provider": "grok", "model": GROK_MODEL, "api_key": GROK_API_KEY}
    
    elif LLM_PROVIDER == "ollama":
        print("[CoIn] Using local Ollama for fully sovereign operation.")
        return {"provider": "ollama", "model": OLLAMA_MODEL, "base_url": OLLAMA_BASE_URL}
    
    elif LLM_PROVIDER == "anthropic":
        print("[CoIn] Using Anthropic API as alternative frontier model (placeholder for advanced reasoning integration).")
        ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        if ANTHROPIC_API_KEY:
            return {"provider": "anthropic", "model": ANTHROPIC_MODEL, "api_key": ANTHROPIC_API_KEY}
        else:
            print("[CoIn] No Anthropic key found — falling back to mock.")
            return {"provider": "mock", "model": "demo"}
    
    else:
        print("[CoIn] Using mock LLM for demo. Replace with real client for production.")
        return {"provider": "mock", "model": "demo"}
