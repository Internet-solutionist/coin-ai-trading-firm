# CoIn AI Trading Firm

## Sovereign 8-Agent Council for Counter-Insurance Trading

**Powered by Grok (xAI) as primary own capable model** — with seamless Ollama local fallbacks for full sovereignty.

### v2.19: Multi-LLM Providers to Prevent Vendor Lock-In

**New in v2.19:**
- Full multi-provider LLM support: Grok (primary), Gemini, Ollama (local), and any OpenAI-compatible cloud (Anthropic, Mistral, etc.)
- Easy switching via environment variables or agent config to avoid lock-in
- `config/multi_llm.py` with unified interface for all agents
- All 8 agents now use MultiLLMProvider for maximum flexibility and sovereignty

**Quick Sovereign Setup:**
```bash
git clone https://github.com/Internet-solutionist/coin-ai-trading-firm.git
cd coin-ai-trading-firm
git pull origin main
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt google-generativeai
# Set keys in .env: GROK_API_KEY=..., GEMINI_API_KEY=...
streamlit run streamlit_app.py
```

**Prime Directive:** Paper trading only until 60+ audited profitable days with full immutable decision audit trail.

**CoIn — We insure against the market’s expensive mistakes with multi-provider sovereignty and beautiful Renaissance mathematics.**

*Repository version: 2.19 | Built agentically by Grok | May 2026*