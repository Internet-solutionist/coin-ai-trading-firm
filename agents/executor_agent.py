"""
CoIn Executor Agent
Real Alpaca paper trading execution (with simulated fallback for demo).
ALWAYS paper trading per CoIn policy until 60+ profitable days.
"""

from rich.console import Console
from rich.panel import Panel
import random
import os
from dotenv import load_dotenv

console = Console()

class ExecutorAgent:
    def __init__(self):
        self.name = "Executor"
        load_dotenv()
        self.alpaca_client = None
        self._init_alpaca()

    def _init_alpaca(self):
        """Initialize Alpaca client if keys present (paper mode enforced)."""
        try:
            from config.broker_config import get_alpaca_client
            self.alpaca_client = get_alpaca_client()
        except Exception as e:
            console.print(f"[yellow]Broker config error: {e} — using pure simulation[/yellow]")

    def execute_trade(self, signal: dict, size_pct: float, portfolio_value: float = 250000.0) -> dict:
        """
        Execute trade: real Alpaca paper if client available, else realistic simulation.
        """
        ticker = signal.get("ticker", "QQQ")
        side = signal.get("side", "buy").lower()  # buy or sell

        if self.alpaca_client:
            return self._execute_alpaca_order(signal, size_pct, portfolio_value, side)
        else:
            return self._execute_simulated_trade(signal, size_pct, side)

    def _execute_simulated_trade(self, signal: dict, size_pct: float, side: str) -> dict:
        """Original realistic paper simulation."""
        console.print(Panel.fit("[bold blue]EXECUTOR AGENT — Simulated Paper Fill[/bold blue]"))

        entry_str = signal.get("entry_range", "480-485")
        try:
            entry_low = float(entry_str.split("–")[0].strip())
        except:
            entry_low = 480.0
        fill_price = entry_low + random.uniform(-0.8, 1.2)
        slippage_bps = random.randint(4, 18)
        filled = random.random() > 0.15  # 85% fill rate

        notional = round(size_pct * 250000, 0)
        result = {
            "filled": filled,
            "fill_price": round(fill_price, 2),
            "slippage_bps": slippage_bps,
            "size_pct": size_pct,
            "notional": notional,
            "mode": "simulated",
            "side": side
        }

        if filled:
            console.print(f"[green]SIMULATED {side.upper()}[/green] {signal['ticker']} @ {result['fill_price']} | Slippage: {slippage_bps}bps | Size: {size_pct}% | Notional: ${notional:,.0f}")
        else:
            console.print("[yellow]SIMULATED PARTIAL / NO FILL[/yellow] — Market moved too fast")
        return result

    def _execute_alpaca_order(self, signal: dict, size_pct: float, portfolio_value: float, side: str) -> dict:
        """Real Alpaca paper trading execution."""
        console.print(Panel.fit("[bold green]EXECUTOR AGENT — REAL ALPACA PAPER ORDER[/bold green]"))

        ticker = signal.get("ticker", "QQQ")
        try:
            from alpaca.trading.requests import MarketOrderRequest
            from alpaca.trading.enums import OrderSide, TimeInForce
        except ImportError:
            console.print("[red]alpaca-py missing — falling back to sim[/red]")
            return self._execute_simulated_trade(signal, size_pct, side)

        # Calculate quantity (simple: size_pct of portfolio / price)
        # For production, use Alpaca's position sizing or risk-based
        try:
            # Get current price for qty calc (simplified, in prod use snapshot)
            price = float(signal.get("entry_range", "480-485").split("–")[0].strip())
            qty = max(1, int((portfolio_value * size_pct / 100) / price))
        except:
            qty = 10  # fallback

        try:
            order_side = OrderSide.BUY if side == "buy" else OrderSide.SELL
            order_request = MarketOrderRequest(
                symbol=ticker,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.DAY
            )
            order = self.alpaca_client.submit_order(order_request)
            
            result = {
                "filled": True,
                "fill_price": price,  # Alpaca fills at market, we log estimated
                "order_id": str(order.id),
                "status": order.status,
                "size_pct": size_pct,
                "qty": qty,
                "notional": round(qty * price, 0),
                "mode": "alpaca_paper",
                "side": side,
                "alpaca_response": str(order)
            }
            console.print(f"[green]REAL ALPACA {side.upper()} ORDER SUBMITTED[/green] {ticker} qty={qty} | Order ID: {order.id} | Status: {order.status}")
            return result

        except Exception as e:
            console.print(f"[red]Alpaca order failed: {e} — falling back to simulation[/red]")
            return self._execute_simulated_trade(signal, size_pct, side)

    # Legacy method for backward compatibility
    def execute_paper_trade(self, signal: dict, size_pct: float) -> dict:
        return self.execute_trade(signal, size_pct)
