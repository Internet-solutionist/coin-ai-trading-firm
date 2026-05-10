"""
CoIn Executor Agent
Paper trading execution with realistic slippage and partial fills.
"""

from rich.console import Console
from rich.panel import Panel
import random

console = Console()

class ExecutorAgent:
    def __init__(self):
        self.name = "Executor"

    def execute_paper_trade(self, signal: dict, size_pct: float) -> dict:
        console.print(Panel.fit("[bold blue]EXECUTOR AGENT — Paper Fill[/bold blue]"))

        fill_price = float(signal.get("entry_range", "480-485").split("–")[0].strip()) + random.uniform(-0.8, 1.2)
        slippage_bps = random.randint(4, 18)
        filled = random.random() > 0.15  # 85% fill rate

        result = {
            "filled": filled,
            "fill_price": round(fill_price, 2),
            "slippage_bps": slippage_bps,
            "size_pct": size_pct,
            "notional": round(size_pct * 250000, 0)  # assume $250k portfolio
        }

        if filled:
            console.print(f"[green]FILLED[/green] {signal['ticker']} @ {result['fill_price']} | Slippage: {slippage_bps}bps | Size: {size_pct}%")
        else:
            console.print("[yellow]PARTIAL / NO FILL[/yellow] — Market moved too fast")

        return result