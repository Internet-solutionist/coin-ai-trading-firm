"""
CoIn Cost Optimizer Agent
Budget allocation, fee minimization, opportunity cost analysis.
"""

from rich.console import Console
from rich.panel import Panel

console = Console()

class CostOptimizerAgent:
    def __init__(self):
        self.name = "Cost Optimizer"

    def review_costs(self, weekly_trades: list, portfolio_value: float) -> dict:
        console.print(Panel.fit("[bold magenta]COST OPTIMIZER AGENT — Efficiency Review[/bold magenta]"))

        total_fees = sum(t.get("slippage_bps", 10) * 0.0001 * t.get("notional", 10000) for t in weekly_trades)
        opportunity_cost = 0.12 * portfolio_value * 0.01  # rough

        efficiency = {
            "total_cost_bps": round(total_fees / portfolio_value * 10000, 1),
            "recommendation": "Rebalance only on signals with >2.5R edge. Current fee drag acceptable.",
            "budget_remaining": 4200
        }

        console.print(f"Weekly fee drag: {efficiency['total_cost_bps']}bps | Budget left: ${efficiency['budget_remaining']}")
        return efficiency
