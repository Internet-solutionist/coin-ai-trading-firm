"""
CoIn Broker Configuration
Alpaca integration for real paper trading execution.
ALWAYS use paper trading until 60+ days profitable simulation.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")
ALPACA_PAPER = os.getenv("ALPACA_PAPER", "True").lower() == "true"

# CoIn strict policy: never enable live trading without explicit override
ENABLE_LIVE_TRADING = os.getenv("ENABLE_LIVE_TRADING", "False").lower() == "true" and ALPACA_PAPER == False

def get_alpaca_client():
    """
    Returns Alpaca TradingClient if keys are set, else None (simulation mode).
    Always forces paper=True for safety unless explicitly overridden (not recommended).
    """
    if not ALPACA_API_KEY or not ALPACA_SECRET_KEY:
        print("[CoIn] No Alpaca keys found — falling back to simulation mode.")
        return None
    
    try:
        from alpaca.trading.client import TradingClient
        client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=ALPACA_PAPER)
        print(f"[CoIn] Alpaca {'PAPER' if ALPACA_PAPER else 'LIVE'} Trading client initialized successfully.")
        if not ALPACA_PAPER and not ENABLE_LIVE_TRADING:
            print("[CoIn WARNING] Live trading disabled by policy. Set ENABLE_LIVE_TRADING=True only after 60+ days paper profits.")
            # force paper anyway
            client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        return client
    except ImportError:
        print("[CoIn] alpaca-py not installed. Run: pip install alpaca-py")
        return None
    except Exception as e:
        print(f"[CoIn] Alpaca client error: {e}")
        return None
