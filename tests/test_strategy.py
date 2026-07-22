import numpy as np
import pandas as pd
import pytest

from trading.strategy import (
    momentum_positions,
    rsi,
    rsi_positions,
    sma_crossover_positions,
)


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


def test_momentum_long_in_uptrend_flat_in_downtrend():
    up = _series(np.arange(1, 61))
    down = _series(np.arange(120, 60, -1))
    assert momentum_positions(up, lookback=20).iloc[-1] == 1.0
    assert momentum_positions(down, lookback=20).iloc[-1] == 0.0


def test_momentum_rejects_bad_lookback():
    with pytest.raises(ValueError):
        momentum_positions(_series([1, 2, 3]), lookback=0)


def test_rsi_bounded_and_extreme_on_monotonic_moves():
    up = _series(np.arange(1, 41))
    values = rsi(up, period=14).dropna()
    assert ((values >= 0) & (values <= 100)).all()
    assert values.iloc[-1] == pytest.approx(100.0)  # all gains, no losses


def test_rsi_positions_buy_dip_then_exit():
    # Steep selloff pushes RSI to oversold; recovery lifts it past exit.
    prices = np.concatenate([np.full(20, 100.0),
                             np.linspace(100, 60, 20),
                             np.linspace(60, 110, 30)])
    positions = rsi_positions(_series(prices), period=14, entry=30, exit=55)
    assert positions.max() == 1.0  # entered during the selloff
    assert positions.iloc[-1] == 0.0  # exited after the recovery
    assert set(positions.unique()) <= {0.0, 1.0}


def test_rsi_positions_rejects_entry_above_exit():
    with pytest.raises(ValueError):
        rsi_positions(_series(np.arange(1, 31)), entry=60, exit=50)
