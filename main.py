# Updated main.py snippet (orchestrator now wires StrategyRegistry)
# ... (full file would include)
from strategies.strategy_registry import get_registry

# In heartbeat loop:
registry = get_registry()
# After validation:
if validated:
    signal_id = registry.store_valid_signal(signal, score, regime)
    # Then executor...
# After execution:
    registry.log_execution(signal_id, execution_details, pnl)
