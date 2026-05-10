"""
CoIn Research Agent
Diagnostician — finds market certainty gaps.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import numpy as np
import datetime
from config.llm_config import get_llm_client

console = Console()

class ResearchAgent:
    def __init__(self):
        self.name = "Research"
        self.llm = get_llm_client()
        self.prompt = open("prompts/research.txt").read()

    def generate_signals(self, market_data: dict) -> list:
        """Produce 0-3 high-evidence signals"""
        console.print(Panel.fit("[bold green]RESEARCH AGENT — Signal Report[/bold green]"))

        signals = []

        # Sophisticated mock logic (in real Grok mode this would be LLM-driven on real data)
        # Example: detect vol crush + positive skew = potential gap
        if market_data.get("vix", 18) < 22 and market_data.get("skew", 0.8) > 0.7:
            signals.append({
                "ticker": "QQQ",
                "diagnosis": "Market pricing near-certain soft landing and continued AI capex boom",
                "counter_thesis": "Tariff escalation + China slowdown creating hidden earnings risk not priced in",
                "evidence": "VIX at 18.4 (lowest since Feb), 30d realized vol 11.2%, skew elevated at 0.82, put/call ratio 0.71",
                "invalidation": "QQQ closes below 478 on volume > 2x average",
                "entry_range": "482.50 – 485.00",
                "stop_loss": "477.80",
                "target": "498.00 (1:2.6 R/R)",
                "confidence": "Medium-High"
            })

        if len(signals) == 0:
            console.print("[yellow]SIGNAL: NONE — Conditions too aligned. No clear certainty gap today.[/yellow]")
            return []

        table = Table(title="High-Evidence Signals")
        table.add_column("Ticker", style="cyan")
        table.add_column("Diagnosis", style="white")
        table.add_column("Counter-Thesis", style="green")
        table.add_column("Confidence", style="yellow")

        for s in signals:
            table.add_row(s["ticker"], s["diagnosis"][:60]+"...", s["counter_thesis"][:50]+"...", s["confidence"])

        console.print(table)
        return signals
