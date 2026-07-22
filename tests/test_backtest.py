import numpy as np
import pandas as pd
import pytest

from trading.backtest import buy_and_hold, run_backtest


def _close(values):
    return pd.Series(values, index=pd.RangeIndex(len(values)), dtype=float)


def test_always_flat_equity_stays_at_one():
    close = _close([100, 110, 105, 120])
    positions = pd.Series(0.0, index=close.index)
    result = run_backtest(close, positions)
    assert result.total_return == pytest.approx(0.0)
    assert result.n_trades == 0


def test_buy_and_hold_matches_price_move_minus_entry_cost():
    close = _close([100, 200])
    result = buy_and_hold(close, cost_bps=0.0)
    assert result.total_return == pytest.approx(1.0)


def test_costs_reduce_returns():
    close = _close(list(np.linspace(100, 150, 60)))
    positions = pd.Series([0.0, 1.0] * 30, index=close.index)  # churn daily
    cheap = run_backtest(close, positions, cost_bps=0.0)
    expensive = run_backtest(close, positions, cost_bps=50.0)
    assert expensive.total_return < cheap.total_return


def test_max_drawdown_is_negative_after_crash():
    close = _close([100, 120, 60, 65])
    result = buy_and_hold(close, cost_bps=0.0)
    assert result.max_drawdown == pytest.approx(-0.5, rel=1e-6)


def test_index_mismatch_rejected():
    close = _close([100, 101, 102])
    positions = pd.Series([1.0, 1.0], index=pd.RangeIndex(2))
    with pytest.raises(ValueError):
        run_backtest(close, positions)
