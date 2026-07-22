"""Trading strategies as pure functions: prices in, target positions out.

Every strategy shifts its signal by one bar — a signal observed at today's
close is only acted on tomorrow — so backtests have no lookahead bias.
"""

import numpy as np
import pandas as pd


def sma_crossover_positions(
    close: pd.Series, fast: int = 50, slow: int = 200
) -> pd.Series:
    """Long (1.0) while the fast SMA is above the slow SMA, else flat (0.0).

    The signal is shifted by one bar: a crossover observed at today's close
    is only acted on tomorrow, so the backtest has no lookahead bias.
    """
    if fast >= slow:
        raise ValueError(f"fast ({fast}) must be < slow ({slow})")
    fast_ma = close.rolling(fast).mean()
    slow_ma = close.rolling(slow).mean()
    positions = (fast_ma > slow_ma).astype(float)
    return positions.shift(1).fillna(0.0)


def momentum_positions(close: pd.Series, lookback: int = 126) -> pd.Series:
    """Time-series momentum: long while the trailing `lookback`-day return
    is positive, else flat."""
    if lookback < 1:
        raise ValueError(f"lookback must be >= 1, got {lookback}")
    trailing_return = close.pct_change(lookback)
    positions = (trailing_return > 0).astype(float)
    return positions.shift(1).fillna(0.0)


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index on 0–100, using simple rolling averages."""
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    strength = gain / loss
    return 100 - 100 / (1 + strength)


def rsi_positions(
    close: pd.Series, period: int = 14, entry: float = 30.0, exit: float = 55.0
) -> pd.Series:
    """Mean reversion: enter long when RSI drops below `entry` (oversold),
    hold until RSI rises above `exit`."""
    if not entry < exit:
        raise ValueError(f"entry ({entry}) must be below exit ({exit})")
    indicator = rsi(close, period)
    signal = pd.Series(np.nan, index=close.index)
    signal[indicator < entry] = 1.0
    signal[indicator > exit] = 0.0
    return signal.ffill().fillna(0.0).shift(1).fillna(0.0)
