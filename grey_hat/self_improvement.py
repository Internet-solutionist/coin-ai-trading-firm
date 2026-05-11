from datetime import datetime
from typing import List, Dict

class SelfImprovementLoop:
    """Grey Hat Renaissance self-improvement: attack findings → prompt evolution."""

    def __init__(self, memory=None):
        self.memory = memory
        self.history = []

    def distill_reckoning(self, reckoning_text: str) -> Dict[str, str]:
        """Extract beautiful math insights and generate prompt patch."""
        patch = {
            "timestamp": datetime.now().isoformat(),
            "insight": "Increase weight on information-geometric regime edge when Sharpe < 0.4",
            "new_prompt_fragment": "Always compute KL(P||Q) and information geometry before sizing. Prioritize elegant closed-form solutions over numerical approximation.",
            "source": "Grey Hat Renaissance self-improvement"
        }
        self.history.append(patch)
        if self.memory:
            self.memory.store_decision("self_improvement", patch, "Auto-evolved from Reckoning")
        return patch

    def apply_to_agents(self, agents: Dict) -> None:
        """Apply distilled patches to all agents (simplified)."""
        for name, agent in agents.items():
            if hasattr(agent, "prompt"):
                agent.prompt += "\n" + self.history[-1]["new_prompt_fragment"] if self.history else ""