"""
CoIn Risk Manager Agent
Position sizing, portfolio heat, drawdown control. Has veto power.
"""

from rich.console import Console
from rich.panel import Panel
import numpy as np

console = Console()

class RiskManagerAgent:
    def __init__(self):
        self.name = "Risk Manager"

    def assess_position(self, signal: dict, current_portfolio: dict) -> dict:
        console.print(Panel.fit("[bold red]RISK MANAGER AGENT — Sizing & Veto[/bold red]"))

        kelly_fraction = 0.28
        position_size = min(0.08, kelly_fraction * 0.5)  # half-Kelly for safety
        new_heat = current_portfolio.get("heat", 0.35) + position_size

        veto = new_heat > 0.55 or current_portfolio.get("max_dd", 0) < -4.5

        decision = {
            "approved": not veto,
            "kelly_fraction": kelly_fraction,
            "position_size_pct": round(position_size * 100, 1),
            "new_portfolio_heat": round(new_heat * 100, 1),
            "veto_reason": "Portfolio heat would exceed 55% or drawdown limit breached" if veto else "Within all risk parameters"
        }

        if veto:
            console.print(f"[red]VETO[/red] — {decision['veto_reason']}")
        else:
            console.print(f"[green]APPROVED[/green] — {position_size*100:.1f}% position | New heat: {new_heat*100:.1f}%")

        return decision
