import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

class StrategyRegistry:
    def __init__(self, db_path: str = 'data/strategies.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategies (
                id TEXT PRIMARY KEY,
                name TEXT,
                prompt_hash TEXT,
                version INTEGER DEFAULT 1,
                created_at TEXT,
                description TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id TEXT,
                timestamp TEXT,
                signal_json TEXT,
                validation_score FLOAT,
                regime TEXT,
                executed BOOLEAN DEFAULT FALSE,
                execution_details TEXT,
                pnl FLOAT DEFAULT 0.0,
                FOREIGN KEY (strategy_id) REFERENCES strategies (id)
            )
        ''')
        self.conn.commit()

    def store_strategy(self, name: str, description: str = '') -> str:
        strategy_id = f'strategy_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO strategies (id, name, prompt_hash, version, created_at, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (strategy_id, name, 'pending_hash', 1, datetime.now().isoformat(), description))
        self.conn.commit()
        return strategy_id

    def store_valid_signal(self, signal: Dict, validation_score: float, regime: str, strategy_id: Optional[str] = None) -> int:
        if strategy_id is None:
            strategy_id = self.store_strategy('auto_generated_from_signal')
        signal_json = json.dumps(signal)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO signals (strategy_id, timestamp, signal_json, validation_score, regime, executed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (strategy_id, datetime.now().isoformat(), signal_json, validation_score, regime, False))
        self.conn.commit()
        return cursor.lastrowid

    def log_execution(self, signal_id: int, execution_details: Dict, pnl: float = 0.0):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE signals SET executed = 1, execution_details = ?, pnl = ? WHERE id = ?
        ''', (json.dumps(execution_details), pnl, signal_id))
        self.conn.commit()

    def get_recent_signals(self, limit: int = 50) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM signals ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]

    def close(self):
        self.conn.close()

# Singleton for easy use across agents
registry = None
def get_registry() -> StrategyRegistry:
    global registry
    if registry is None:
        registry = StrategyRegistry()
    return registry
