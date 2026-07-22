"""Vectorized daily backtester with transaction costs."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

TRADING_DAYS = 252


@dataclass
class BacktestResult:
    equity: pd.Series
    total_return: float
    cagr: float
    sharpe: float
    max_drawdown: float
    n_trades: int

    def summary(self) -> str:
        return (
            f"total return {self.total_return:+.1%} | CAGR {self.cagr:+.2%} | "
            f"Sharpe {self.sharpe:.2f} | max drawdown {self.max_drawdown:.1%} | "
            f"{self.n_trades} trades"
        )


def run_backtest(
    close: pd.Series, positions: pd.Series, cost_bps: float = 5.0
) -> BacktestResult:
    """Apply target positions (0..1) to daily returns, charging `cost_bps`
    of traded notional on every position change."""
    if not close.index.equals(positions.index):
        raise ValueError("close and positions must share the same index")

    daily_returns = close.pct_change().fillna(0.0)
    turnover = positions.diff().abs().fillna(positions.iloc[0])
    strategy_returns = positions * daily_returns - turnover * cost_bps / 1e4
    equity = (1.0 + strategy_returns).cumprod()

    years = len(close) / TRADING_DAYS
    total_return = equity.iloc[-1] - 1.0
    cagr = equity.iloc[-1] ** (1 / years) - 1.0 if years > 0 else 0.0
    vol = strategy_returns.std()
    sharpe = (
        float(strategy_returns.mean() / vol * np.sqrt(TRADING_DAYS)) if vol > 0 else 0.0
    )
    max_drawdown = float((equity / equity.cummax() - 1.0).min())
    n_trades = int((turnover > 0).sum())

    return BacktestResult(
        equity=equity,
        total_return=float(total_return),
        cagr=float(cagr),
        sharpe=sharpe,
        max_drawdown=max_drawdown,
        n_trades=n_trades,
    )


def buy_and_hold(close: pd.Series, cost_bps: float = 5.0) -> BacktestResult:
    positions = pd.Series(1.0, index=close.index)
    return run_backtest(close, positions, cost_bps=cost_bps)
