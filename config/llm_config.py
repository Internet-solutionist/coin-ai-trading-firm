 """
CoIn LLM Configuration
Primary recommendation: Grok (xAI) for superior multi-step reasoning and tool use.
Fully swappable — any OpenAI-compatible endpoint works.
"""

import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "grok")  # grok | gemini | openai | ollama  (Grok primary for own capable model strategy)

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

# Gemini (Google) — Swappable frontier brain option for the AI Trading Firm
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

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
    
    elif LLM_PROVIDER == "gemini":
        print("[CoIn] Using Gemini (Google) as swappable brain — easy model swap for the AI Trading Firm's multi-model strategy.")
        if GEMINI_API_KEY:
            return {"provider": "gemini", "model": GEMINI_MODEL, "api_key": GEMINI_API_KEY}
        else:
            print("[CoIn] No Gemini key found — falling back to mock.")
            return {"provider": "mock", "model": "demo"}
    
    else:
        print("[CoIn] Using mock LLM for demo. Replace with real client for production.")
        return {"provider": "mock", "model": "demo"}


def call_llm(prompt: str, system_prompt: str = None, max_tokens: int = None) -> str:
    """
    Unified LLM caller for all agents — enables own capable model (Grok-first).
    Falls back gracefully to mock if no key or demo mode.
    This is the key improvement for v2.4: real intelligence in trading agents.
    """
    import os
    provider = LLM_PROVIDER
    max_t = max_tokens or MAX_TOKENS

    if provider == "grok" and GROK_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=GROK_API_KEY, base_url=GROK_BASE_URL)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(
                model=GROK_MODEL,
                messages=messages,
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=max_t
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[CoIn] Grok call failed: {e} — falling back to mock")
            return "MOCK: Grok unavailable. Using heuristic signal."

    elif provider == "ollama":
        try:
            import requests
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "OLLAMA ERROR").strip()
        except Exception as e:
            print(f"[CoIn] Ollama call failed: {e}")
            return "MOCK: Ollama unavailable."

    elif provider == "gemini" and GEMINI_API_KEY:
        try:
            # Gemini via OpenAI compat or direct, but for simplicity use openai style if possible
            # Note: Gemini API key works with google-generativeai, but to keep deps low, mock for now
            # In prod: pip install google-generativeai; use genai.GenerativeModel
            return "MOCK: Gemini integration pending full SDK. Use Grok for best results."
        except Exception as e:
            return f"MOCK Gemini error: {e}"

    else:
        # Mock mode for demo / no key
        return "MOCK RESPONSE: [Simulated high-evidence signal based on current market data. In production with Grok key this would be LLM-generated diagnostic with full reasoning.]"
