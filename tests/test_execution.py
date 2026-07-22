import pytest

from trading.execution import decide_order


def test_buys_when_signal_long_and_flat():
    assert decide_order(1.0, 0.0).action == "buy"


def test_sells_when_signal_flat_and_long():
    assert decide_order(0.0, 3.5).action == "sell"


def test_holds_when_already_matching_signal():
    assert decide_order(1.0, 2.0).action == "hold"
    assert decide_order(0.0, 0.0).action == "hold"


def test_idempotent_after_acting():
    # After a buy fills, the same signal must produce "hold", not another buy.
    assert decide_order(1.0, 1.2).action == "hold"


def test_rejects_fractional_target():
    with pytest.raises(ValueError):
        decide_order(0.5, 0.0)
