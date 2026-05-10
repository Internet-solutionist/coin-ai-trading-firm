# CoIn AI Trading Firm

## Sovereign 8-Agent Council for Counter-Insurance Trading

**Powered by Grok (xAI) as primary own capable model** — with seamless Ollama local fallbacks for full sovereignty.

### Trading Setup & Strategy Storage (NEW - v2.5)

**Full Trading Flow:**
1. Market data ingested by Research + Backtester Agents.
2. Structured signal generated (ticker, direction, entry_range, confidence, strategy_id).
3. Validator + Regime Sentinel perform multi-layer validation.
4. **Every validatable signal is automatically persisted** to SQLite Strategy Registry + Signal Journal (`data/strategies.db`).
5. Executor routes to Alpaca paper trading (real orders when Prime Directive satisfied).
6. P&L feedback loops back into registry for strategy evolution.

**Strategy Storage Details:**
- New `strategies/strategy_registry.py` with SQLite backend.
- Every validated signal stored as versioned JSON + metadata (timestamp, validation_score, regime, execution status, PNL).
- Strategies are auto-versioned and queryable for backtesting, audit, and council learning.
- Full audit trail for every decision — capital preservation first.

Clone and run:
```bash
git clone https://github.com/Internet-solutionist/coin-ai-trading-firm.git
cd coin-ai-trading-firm
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Initialize registry & run
streamlit run streamlit_app.py
```

**Prime Directive:** Paper only until 60+ audited profitable days.

**CoIn — We insure against the market’s expensive mistakes.**