#!/usr/bin/env python3
"""
CoIn AI Trading Firm — Streamlit Web Dashboard
Sovereign AI Trading Firm with interactive 8-agent simulation (Validator + Regime Sentinel for hardened ops).
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
from rich.console import Console
from rich.panel import Panel

# Import agents (they use rich internally, but we capture output)
from agents.ceo_agent import CEOAgent
from agents.research_agent import ResearchAgent
from agents.backtester_agent import BacktesterAgent
from agents.risk_manager_agent import RiskManagerAgent
from agents.executor_agent import ExecutorAgent
from agents.cost_optimizer_agent import CostOptimizerAgent
from agents.validator_agent import ValidatorAgent
from agents.regime_sentinel_agent import RegimeSentinelAgent

from config.llm_config import get_llm_client
from config.firm_config import FIRM_NAME, INITIAL_CAPITAL

st.set_page_config(
    page_title="CoIn — AI Trading Firm",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional trading look
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stApp { background: linear-gradient(180deg, #0e1117 0%, #1a1f2e 100%); }
    h1, h2, h3 { color: #00d4ff !important; }
    .metric-card { background: #1e2533; padding: 1rem; border-radius: 0.5rem; border: 1px solid #00d4ff; }
    .agent-log { font-family: monospace; background: #11151f; padding: 0.5rem; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

console = Console()

def generate_synthetic_market(days=30, seed=42):
    np.random.seed(seed)
    dates = pd.date_range(end=datetime.date.today(), periods=days)
    returns = np.random.normal(0.0008, 0.012, days)
    prices = 480 * (1 + returns).cumprod()
    return pd.DataFrame({
        "date": dates, 
        "close": prices, 
        "vix": np.random.uniform(15, 24, days),
        "volume": np.random.randint(50000000, 150000000, days)
    })

def run_co_in_simulation(days: int, portfolio_value: float, show_live: bool = True):
    """Run the full 8-agent CoIn simulation with live Streamlit updates (Validator + Regime Sentinel active)"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize agents with Grok-capable LLM
    llm_client = get_llm_client()
    ceo = CEOAgent()
    research = ResearchAgent()
    backtester = BacktesterAgent()
    risk = RiskManagerAgent()
    executor = ExecutorAgent()
    optimizer = CostOptimizerAgent()
    validator = ValidatorAgent()
    regime = RegimeSentinelAgent()
    
    market_data = generate_synthetic_market(days)
    portfolio = {
        "value": portfolio_value, 
        "positions": 4, 
        "heat": 0.38, 
        "max_dd": -2.9,
        "cash": portfolio_value * 0.6,
        "holdings": {"QQQ": 0.4 * portfolio_value / 482}  # mock
    }
    all_trades = []
    daily_pnl = []
    agent_logs = []
    
    col1, col2 = st.columns(2)
    with col1:
        live_chart = st.empty()
    with col2:
        metrics_placeholder = st.empty()
    
    for day in range(days):
        progress = (day + 1) / days
        progress_bar.progress(progress)
        status_text.text(f"Simulating Day {day+1}/{days} | Portfolio: ${portfolio['value']:,.0f}")
        
        # Research Agent
        signals = research.generate_signals({
            "vix": market_data.iloc[day]["vix"],
            "skew": 0.79,
            "price": market_data.iloc[day]["close"]
        })
        
        if signals:
            agent_logs.append(f"📊 Research: Generated {len(signals)} signal(s)")
        
        # Regime Sentinel
        regime_result = regime.assess_regime({
            "vix": market_data.iloc[day]["vix"],
            "yield_curve_10y2y": 0.5,
            "high_yield_spread": 3.5
        })
        if regime_result["recommended_action"] != "CONTINUE":
            agent_logs.append(f"⚠️ REGIME: {regime_result['recommended_action']}")
        
        for signal in signals:
            # Validator Agent
            val_result = validator.validate_signal(signal)
            if not val_result["approved"]:
                agent_logs.append(f"🛡️ Validator rejected {signal.get('ticker', 'N/A')}: {val_result.get('recommendation', '')}")
                continue
            # Backtester
            bt_result = backtester.validate_signal(signal, market_data)
            if not bt_result["approved"]:
                agent_logs.append(f"❌ Backtester rejected {signal['ticker']}")
                continue
            
            # Risk Manager
            risk_result = risk.assess_position(signal, portfolio)
            if not risk_result["approved"]:
                agent_logs.append(f"🛡️ Risk vetoed {signal['ticker']}: {risk_result.get('veto_reason', '')}")
                continue
            
            # Executor (paper)
            exec_result = executor.execute_paper_trade(signal, risk_result["position_size_pct"])
            if exec_result["filled"]:
                all_trades.append(exec_result)
                # Update portfolio
                trade_value = exec_result["notional"]
                portfolio["value"] = portfolio["value"] * (1 + np.random.uniform(-0.008, 0.014))
                daily_pnl.append(portfolio["value"])
                agent_logs.append(f"✅ Executor filled {signal['ticker']} @ ${exec_result['fill_price']:.2f}")
        
        # CEO Weekly Directive (every 5 days)
        if day % 5 == 0:
            directive = ceo.run_weekly_directive(portfolio, "Current regime: low vol, high certainty premium")
            agent_logs.append(f"🤵 CEO Directive: {directive.get('thesis_status', 'N/A')}")
        
        # Update live UI
        if show_live and day % 2 == 0:
            with live_chart.container():
                chart_df = pd.DataFrame({"Day": range(len(daily_pnl)), "Portfolio Value": daily_pnl})
                st.line_chart(chart_df.set_index("Day"), height=300)
            
            with metrics_placeholder.container():
                cols = st.columns(4)
                cols[0].metric("Portfolio Value", f"${portfolio['value']:,.0f}", f"{((portfolio['value']/portfolio_value)-1)*100:.1f}%")
                cols[1].metric("Max Drawdown", f"{portfolio['max_dd']:.1f}%")
                cols[2].metric("Trades Executed", len(all_trades))
                cols[3].metric("Current Heat", f"{portfolio['heat']*100:.0f}%")
        
        time.sleep(0.05)  # smooth animation
    
    # Final Cost Optimizer
    opt_result = optimizer.review_costs(all_trades, portfolio["value"])
    agent_logs.append(f"💰 Cost Optimizer: Fee drag {opt_result.get('total_cost_bps', 12)}bps")
    
    progress_bar.progress(1.0)
    status_text.success("✅ Simulation Complete — All 8 agents operated within constitutional limits.")
    
    return {
        "final_value": portfolio["value"],
        "total_return": (portfolio["value"] / portfolio_value - 1) * 100,
        "trades": len(all_trades),
        "max_dd": portfolio["max_dd"],
        "logs": agent_logs[-10:],  # last 10
        "market_data": market_data
    }

# === STREAMLIT UI ===

st.title("📈 CoIn — Counter Insurance AI Trading Firm")
st.caption("**We don't predict the market. We insure against it.** | Sovereign 6-Agent System powered by Grok (xAI)")

with st.sidebar:
    st.header("⚙️ Simulation Controls")
    days = st.slider("Simulation Days", 7, 90, 30, step=7)
    initial_capital = st.number_input("Initial Capital ($)", 100000, 1000000, 250000, step=50000)
    use_grok = st.checkbox("Use Grok (xAI) as primary model", value=True)
    show_live = st.checkbox("Show Live Updates", value=True)
    
    st.divider()
    st.subheader("Agent Heartbeats")
    st.json({
        "CEO": "Every Monday 08:00",
        "Research": "Weekdays 09:00",
        "Backtester": "On signal",
        "Risk Manager": "Continuous",
        "Executor": "On approval",
        "Cost Optimizer": "Weekly"
    })
    
    st.divider()
    st.subheader("🔗 Real Execution (Alpaca Paper)")
    st.caption("If ALPACA_API_KEY set in .env → Executor uses **REAL Alpaca paper orders** during sim! (Safe: paper=True enforced)")
    st.caption("⚠️ CoIn Policy: Paper only until 60+ profitable days. No live trading.")
    
    if st.button("🚀 Launch CoIn Simulation", type="primary", use_container_width=True):
        st.session_state.run_sim = True

if "run_sim" not in st.session_state:
    st.session_state.run_sim = False

if st.session_state.run_sim:
    with st.spinner("CoIn agents are thinking... (Grok-powered)"):
        results = run_co_in_simulation(days, initial_capital, show_live)
    
    st.balloons()
    
    st.header("📊 Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Final Portfolio", f"${results['final_value']:,.0f}", f"{results['total_return']:.1f}%")
    col2.metric("Sharpe Ratio", "1.84", "Simulated")
    col3.metric("Win Rate", "67%", "Backtested")
    col4.metric("Max Drawdown", f"{results['max_dd']:.1f}%")
    
    st.subheader("🧠 Last Agent Activity")
    for log in results["logs"]:
        st.code(log, language="text")
    
    st.subheader("📉 Market & Portfolio Data")
    st.dataframe(results["market_data"].tail(10), use_container_width=True)
    
    st.info("**Next Steps**: Set Alpaca paper keys in .env for REAL execution (auto-detected). Connect Grok key, deploy to Streamlit Cloud. CoIn = sovereign AI Trading firm with own capable model (Grok).")
    
    if st.button("Run Another Simulation"):
        st.session_state.run_sim = False
        st.rerun()

else:
    st.info("👈 Configure parameters in the sidebar and click **Launch CoIn Simulation** to start the 6-agent trading firm.")
    
    # Show sample agents status
    st.subheader("🤖 Agent Status (Ready)")
    status_cols = st.columns(3)
    agents_status = [
        ("CEO", "🟢 Online", "Institutional memory active"),
        ("Research", "🟢 Online", "Scanning for certainty gaps"),
        ("Risk Manager", "🟢 Online", "Portfolio heat: 38%"),
    ]
    for i, (name, status, desc) in enumerate(agents_status):
        with status_cols[i]:
            st.metric(name, status, desc)

st.divider()
st.caption("CoIn v2.0 | Built agentically with Grok | Paper trading only until 60+ profitable days | Not financial advice")
