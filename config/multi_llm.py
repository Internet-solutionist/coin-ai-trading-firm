# CoIn AI Trading Firm - Multi-LLM Provider Support (v2.19)
# Grok (xAI) primary own capable model + Gemini + other clouds to prevent vendor lock-in
# All sovereign, local-first where possible

from typing import Dict, Any

import os

class MultiLLMProvider:
    def __init__(self):
        self.primary = "grok"  # Grok (xAI) as primary own capable model
        self.fallbacks = ["gemini", "ollama", "openai_compatible"]
        self.providers = {
            "grok": self._call_grok,
            "gemini": self._call_gemini,
            "ollama": self._call_ollama,
            "openai_compatible": self._call_openai_compatible
        }

    def generate(self, prompt: str, system_prompt: str = None, provider: str = None) -> str:
        provider = provider or self.primary
        if provider not in self.providers:
            provider = self.primary
        return self.providers[provider](prompt, system_prompt)

    def _call_grok(self, prompt: str, system_prompt: str = None) -> str:
        # Use openai-compatible Grok API
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("GROK_API_KEY"), base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-2-latest",
            messages=[{"role": "system", "content": system_prompt or ""}, {"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    def _call_gemini(self, prompt: str, system_prompt: str = None) -> str:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([system_prompt or "", prompt])
        return response.text

    def _call_ollama(self, prompt: str, system_prompt: str = None) -> str:
        import requests
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "system": system_prompt or ""}
        )
        return response.json().get("response", "")

    def _call_openai_compatible(self, prompt: str, system_prompt: str = None) -> str:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("OPENAI_COMPATIBLE_KEY", "sk-..."),
            base_url=os.getenv("OPENAI_COMPATIBLE_BASE", "https://api.openai.com/v1")
        )
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_COMPATIBLE_MODEL", "gpt-4o-mini"),
            messages=[{"role": "system", "content": system_prompt or ""}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

# Usage in agents: llm = MultiLLMProvider(); response = llm.generate(prompt, provider="gemini")