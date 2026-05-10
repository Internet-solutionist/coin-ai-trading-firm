"""
CoIn Regime Sentinel Agent
Live macro regime detection and thesis stress testing.
Closes the live regime detection & thesis stress gap identified in v2.2 audit.
"""

from rich.console import Console
from rich.panel import Panel
import numpy as np
import datetime

console = Console()

class RegimeSentinelAgent:
    def __init__(self):
        self.name = "Regime Sentinel"
        self.prompt = "You are the Regime Sentinel for CoIn. You detect macro regimes (liquidity crisis, euphoria, stagflation, etc.) using VIX, yield curve, credit spreads, on-chain flows, and news sentiment. If current regime mismatches the core counter-insurance thesis with >70% probability, you recommend PAUSE NEW POSITIONS and trigger CEO Revision Directive. Output structured JSON only."

    def assess_regime(self, macro_data: dict) -> dict:
        """Daily regime assessment and auto-pause trigger."""
        console.print(Panel.fit("[bold magenta]REGIME SENTINEL — Macro Stress Test[/bold magenta]"))

        vix = macro_data.get("vix", 18)
        yield_curve = macro_data.get("yield_curve_10y2y", 0.5)  # 10y-2y spread
        credit_spread = macro_data.get("high_yield_spread", 3.5)

        # Simple heuristic (real: Grok + unsupervised clustering on live macro series)
        regime = "normal"
        mismatch_probability = 0.2
        action = "CONTINUE"

        if vix > 30 and yield_curve < -0.2:
            regime = "liquidity_crisis"
            mismatch_probability = 0.85
            action = "PAUSE_NEW_POSITIONS_AND_TRIGGER_REVISION"
        elif vix < 14 and credit_spread < 2.5:
            regime = "euphoria"
            mismatch_probability = 0.65
            action = "REDUCE_POSITION_SIZE_30pct"

        result = {
            "regime": regime,
            "mismatch_probability": mismatch_probability,
            "recommended_action": action,
            "thesis_stress_score": min(1.0, vix / 40 + abs(yield_curve) * 2),
            "last_assessed": datetime.datetime.now().isoformat(),
            "sentinel_version": "v2.2-stub"
        }

        console.print(f"Regime: {regime.upper()} | Mismatch: {mismatch_probability*100:.0f}% | Action: {action}")
        if action != "CONTINUE":
            console.print("[bold red]THESIS STRESS DETECTED — Escalating to CEO[/bold red]")

        return result
