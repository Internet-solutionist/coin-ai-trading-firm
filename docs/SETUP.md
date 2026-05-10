# CoIn Setup Guide

## Local Run (Recommended First)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --mode paper --simulate-days 60 --dashboard
```

## Sovereign Portable (USB Pendrive Style)
1. Install Ubuntu or Debian on USB
2. Clone this repo
3. Add to autostart: `python /path/to/main.py --mode paper`
4. Use LUKS encryption + regular backups

## Connect Real Grok
1. Get API key at https://x.ai
2. `cp .env.example .env`
3. Edit `.env` with your key

## Connect Real Alpaca Paper Trading (Production Execution)
1. Sign up at https://alpaca.markets (free paper trading)
2. Go to Dashboard → Paper Trading → Generate API Keys
3. Add to `.env`:
   ```
   ALPACA_API_KEY=PK...
   ALPACA_SECRET_KEY=...
   ALPACA_PAPER=True
   ```
4. Executor Agent will now place **real paper orders** automatically on approved signals.
5. Monitor at alpaca.markets dashboard. All orders logged in CoIn for full audit trail.

**CoIn Policy Reminder**: Paper trading only until 60+ consecutive profitable days with full decision logs reviewed by CEO Agent.
4. Re-run — agents will now use live Grok reasoning

## Next Level
- Add Alpaca paper keys for real paper trading fills
- Extend to 32 agents (see XVII_The_Expansion philosophy in original corpus)
- Deploy to always-on mini PC or VPS
