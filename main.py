# CoIn AI Trading Firm - Meta Orchestrator v2.7
# Sovereign 8-Agent Council with MemPalace Long-Term Memory
# Powered by Grok (xAI) as primary own capable model - fully local sovereign option

from datetime import datetime
import time

from strategies.strategy_registry import get_registry
from memory.palace import get_memory_palace

# Agent imports (full implementations in agents/)
from agents.ceo_agent import CEOAgent
from agents.research_agent import ResearchAgent
from agents.backtester_agent import BacktesterAgent
from agents.risk_manager_agent import RiskManagerAgent
from agents.executor_agent import ExecutorAgent
from agents.cost_optimizer_agent import CostOptimizerAgent
from agents.validator_agent import ValidatorAgent
from agents.regime_sentinel_agent import RegimeSentinelAgent

class MetaOrchestrator:
    def __init__(self):
        self.registry = get_registry()
        self.memory = get_memory_palace()  # v2.7 MemPalace sovereign memory
        self.agents = {
            'ceo': CEOAgent(memory=self.memory),
            'research': ResearchAgent(memory=self.memory),
            'backtester': BacktesterAgent(memory=self.memory),
            'risk': RiskManagerAgent(memory=self.memory),
            'executor': ExecutorAgent(memory=self.memory),
            'cost': CostOptimizerAgent(memory=self.memory),
            'validator': ValidatorAgent(memory=self.memory),
            'regime': RegimeSentinelAgent(memory=self.memory)
        }
        print('CoIn AI Trading Firm v2.7 initialized with MemPalace.')
        print('All 8 agents awakened with Grok-powered long-term recall. Sovereign, no external memory vendors.')

    def run_heartbeat(self, days: int = 1):
        print(f'\n=== HEARTBEAT CYCLE STARTED: {datetime.now()} ===')
        # Wake council with MemPalace context
        context = self.memory.wake_council()
        for name, agent in self.agents.items():
            agent.wake(context.get(name, {}))

        # Market data (live or sim)
        market_data = {'ticker': 'AAPL', 'price': 220.5, 'volume': 45000000, 'regime': 'bullish_continuation'}
        
        # Research generates signal using Grok + memory recall
        signal = self.agents['research'].generate_signals(market_data)
        
        # Multi-agent validation
        validated, score, regime = self.agents['validator'].validate(signal, self.agents['regime'].detect_regime(market_data))
        
        if validated:
            # Store in Strategy Registry + MemPalace (verbatim)
            signal_id = self.memory.store_signal(signal, score, regime, agent='research')
            print(f'Signal {signal_id} persisted to Registry + Palace.')
            
            # Backtest
            approved = self.agents['backtester'].backtest(signal)
            if approved:
                size = self.agents['risk'].calculate_size(signal, portfolio_value=250000)
                execution = self.agents['executor'].execute(signal, size)
                self.memory.store_decision('executor', execution, 'Risk approved')
                pnl = 1250.75  # simulated
                self.registry.log_execution(signal_id, execution, pnl)
                print(f'Execution complete. P&L: ${pnl}')

        # CEO directive using Palace recall
        if datetime.now().weekday() == 0:
            past_strategies = self.memory.recall_past_signals('successful strategies last month')
            self.agents['ceo'].issue_directive(past_strategies)

        print('=== HEARTBEAT COMPLETE - Capital Preserved ===\n')

if __name__ == '__main__':
    orchestrator = MetaOrchestrator()
    orchestrator.run_heartbeat()
