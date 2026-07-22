"""Trading strategies as pure functions: prices in, target positions out."""

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
