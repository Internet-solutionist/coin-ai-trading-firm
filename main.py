# CoIn AI Trading Firm - Meta Orchestrator v2.10
# Sovereign 8-Agent Council with MemPalace + Notion + Protected Keys + Floci Option
# Powered by Grok (xAI) as primary own capable model

import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()  # Load .env for protected keys

from strategies.strategy_registry import get_registry
from memory.palace import get_memory_palace
from integrations.notion_bridge import get_notion_bridge

# Prompt for API keys and model if not set (secure, user-friendly)
def ensure_api_keys():
    if not os.getenv("OPENAI_API_KEY"):
        key = input("Enter your Grok (OpenAI-compatible) API key (or press enter for local Ollama): ").strip()
        if key:
            os.environ["OPENAI_API_KEY"] = key
            with open(".env", "a") as f:
                f.write(f"\nOPENAI_API_KEY={key}")
        else:
            os.environ["OPENAI_API_BASE"] = input("Enter Ollama base URL (default http://localhost:11434/v1): ") or "http://localhost:11434/v1"
            os.environ["LLM_PROVIDER"] = "ollama"
    if not os.getenv("LLM_PROVIDER"):
        os.environ["LLM_PROVIDER"] = input("Choose model provider (grok/ollama/other): ") or "grok"
    print(f"Using {os.getenv('LLM_PROVIDER')} as primary own capable model.")

# Agent imports
# ... (same as before)

from agents.ceo_agent import CEOAgent
# ... other agents

class MetaOrchestrator:
    def __init__(self):
        ensure_api_keys()  # v2.10 secure prompting
        self.registry = get_registry()
        self.memory = get_memory_palace()
        self.notion = get_notion_bridge()
        # Floci optional local AWS emulator (future sovereign cloud sim)
        if os.getenv("FLOCI_ENABLED", "false").lower() == "true":
            print("Floci local AWS emulator enabled for sovereign data storage.")
        self.agents = { ... }  # same
        print('CoIn AI Trading Firm v2.10 ready - keys protected, models configurable.')

    # ... rest of run_heartbeat same, with Notion and memory calls

if __name__ == '__main__':
    orchestrator = MetaOrchestrator()
    orchestrator.run_heartbeat()
