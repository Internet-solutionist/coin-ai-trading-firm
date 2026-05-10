import json
from datetime import datetime
from mempalace import Palace
from strategies.strategy_registry import get_registry

class MemoryPalace:
    def __init__(self, root: str = 'trading_palace'):
        self.palace = Palace(root=root)
        self.registry = get_registry()
        # Ensure agent wings exist for sovereign 8-agent council
        self.agent_wings = {
            'ceo': 'CEO Wing - Strategy & Institutional Memory',
            'research': 'Research Wing - Market Intelligence & Signals',
            'backtester': 'Backtester Wing - Historical Validation',
            'risk': 'Risk Manager Wing - Capital Preservation Logs',
            'executor': 'Executor Wing - Trade Execution & Fills',
            'cost': 'Cost Optimizer Wing - Efficiency & Burn Rate Memory',
            'validator': 'Validator Wing - Integrity & Injection Defense',
            'regime': 'Regime Sentinel Wing - Macro Stress & Thesis Health'
        }
        for wing in self.agent_wings:
            self.palace.create_wing(wing)

    def store_signal(self, signal: dict, validation_score: float, regime: str, agent: str = 'research'):
        # Store in v2.5 Strategy Registry (structured)
        signal_id = self.registry.store_valid_signal(signal, validation_score, regime)
        # Verbatim to MemPalace for long-term semantic recall (no loss)
        content = json.dumps({
            'signal': signal,
            'validation_score': validation_score,
            'regime': regime,
            'timestamp': datetime.now().isoformat(),
            'agent': agent
        })
        self.palace.add_drawer(wing=agent, room='validated_signals', content=content)
        # Knowledge graph for temporal queries e.g. 'risk limit changes'
        self.palace.graph.add_entity(
            entity_id=f'signal_{signal_id}',
            name='Validated Signal',
            valid_from=datetime.now().isoformat(),
            attributes={'ticker': signal.get('ticker'), 'direction': signal.get('direction')}
        )
        return signal_id

    def recall_past_signals(self, query: str, wing: str = 'research', limit: int = 10):
        results = self.palace.search(query, wing=wing, room='validated_signals', limit=limit)
        return [json.loads(r['content']) for r in results]

    def wake_council(self):
        # Wake all 8 agents with relevant long-term memory
        context = {}
        for wing in self.agent_wings:
            context[wing] = self.palace.wake_up(wing=wing)
        return context

    def store_decision(self, agent: str, decision: dict, context: str = ''):
        content = json.dumps({'decision': decision, 'context': context, 'timestamp': datetime.now().isoformat()})
        self.palace.add_drawer(wing=agent, room='decisions', content=content)

    def close(self):
        self.registry.close()

# Singleton for easy agent use
memory_palace = None
def get_memory_palace() -> MemoryPalace:
    global memory_palace
    if memory_palace is None:
        memory_palace = MemoryPalace()
    return memory_palace
