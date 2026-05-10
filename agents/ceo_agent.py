"""
CoIn CEO Agent
Long-term strategy, institutional memory, weekly directive generator.
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import datetime
from config.llm_config import get_llm_client

console = Console()

class CEOAgent:
    def __init__(self):
        self.name = "CEO"
        self.llm = get_llm_client()
        self.prompt = open("prompts/ceo.txt").read()

    def run_weekly_directive(self, portfolio_state: dict, market_conditions: str) -> dict:
        """Generate the Monday Weekly Directive"""
        console.print(Panel.fit("[bold cyan]CEO AGENT — Weekly Directive[/bold cyan]"))

        # In real mode with Grok this would call the API with self.prompt + context
        # For now: structured mock output that looks like strong Grok reasoning
        directive = {
            "date": datetime.date.today().isoformat(),
            "thesis_status": "Applicable",
            "focus": "Volatility compression in tech + rising rates pressure on growth names",
            "open_positions": "HOLD current 4 positions. No new adds this week — market certainty premium too high across board.",
            "agent_flags": "Research producing excellent diagnostic signals. Backtester approval rate 87%. Risk Manager enforcing tight heat.",
            "this_weeks_question": "Is the current 18% VIX level pricing in a soft landing that is not actually happening?",
            "risk_review": f"Portfolio heat: 42% | Max DD this cycle: -3.8% | Kelly fraction: 0.31 | All stops respected.",
            "raw_output": "THESIS STATUS: Applicable\nFOCUS: Volatility compression...\n(Full structured output above)"
        }

        console.print(Markdown(f"""
**THESIS STATUS:** {directive['thesis_status']}  
**FOCUS:** {directive['focus']}  
**OPEN POSITIONS:** {directive['open_positions']}  
**AGENT FLAGS:** {directive['agent_flags']}  
**THIS WEEK'S QUESTION:** {directive['this_weeks_question']}  
**RISK REVIEW:** {directive['risk_review']}
        """))

        return directive