"""
CoIn Firm Configuration
"""

FIRM_NAME = "CoIn — Counter Insurance"
INITIAL_CAPITAL = 250_000
MAX_POSITIONS_PER_WEEK = 3
MAX_DRAWDOWN_HALT = 0.05
PAPER_TRADING_ONLY_UNTIL = "60+ profitable days"

AGENT_HEARTBEATS = {
    "CEO": "every Monday 08:00",
    "Research": "weekdays 09:00",
    "Backtester": "on signal",
    "Risk Manager": "continuous",
    "Executor": "on approved signal",
    "Cost Optimizer": "weekly + per trade"
}
