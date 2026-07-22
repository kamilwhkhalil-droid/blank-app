import numpy as np
import pandas as pd
import pytest

from trading.strategy import sma_crossover_positions


def _series(values):
    return pd.Series(values, index=pd.RangeIndex(len(values)), dtype=float)


def test_uptrend_goes_long():
    close = _series(np.arange(1, 51))
    positions = sma_crossover_positions(close, fast=3, slow=10)
    assert positions.iloc[-1] == 1.0
    assert set(positions.unique()) <= {0.0, 1.0}


def test_downtrend_stays_flat():
    close = _series(np.arange(100, 50, -1))
    positions = sma_crossover_positions(close, fast=3, slow=10)
    assert positions.iloc[-1] == 0.0


def test_signal_is_lagged_one_bar():
    # Crossover information from bar t must apply at t+1, not t.
    close = _series(np.arange(1, 31))
    positions = sma_crossover_positions(close, fast=2, slow=5)
    raw = (close.rolling(2).mean() > close.rolling(5).mean()).astype(float)
    first_cross = raw.idxmax()
    assert positions.loc[first_cross] == 0.0
    assert positions.loc[first_cross + 1] == 1.0


def test_rejects_fast_not_below_slow():
    close = _series(np.arange(1, 21))
    with pytest.raises(ValueError):
        sma_crossover_positions(close, fast=10, slow=10)
