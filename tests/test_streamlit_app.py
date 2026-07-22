import numpy as np
import pandas as pd
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

import trading.data


@pytest.fixture(autouse=True)
def clear_streamlit_cache():
    # st.cache_data persists across AppTest runs in one process; without
    # this, one test's fetched data leaks into the next test's app run.
    st.cache_data.clear()


@pytest.fixture
def synthetic_prices(monkeypatch):
    """Serve deterministic price history so app tests never hit the network."""
    index = pd.bdate_range("2015-01-01", periods=600)
    rng = np.random.default_rng(seed=7)
    close = pd.Series(100 * np.cumprod(1 + rng.normal(0.0004, 0.01, 600)), index=index)
    frame = pd.DataFrame({"close": close})
    monkeypatch.setattr(trading.data, "fetch_daily", lambda ticker, years=25: frame)


def _run_app():
    at = AppTest.from_file("streamlit_app.py", default_timeout=30)
    return at.run()


def test_app_runs_and_shows_results(synthetic_prices):
    at = _run_app()
    assert not at.exception
    assert "Backtest Lab" in at.title[0].value
    assert len(at.metric) == 4  # CAGR, Sharpe, max drawdown, trades


def test_invalid_sma_windows_show_error(synthetic_prices):
    at = AppTest.from_file("streamlit_app.py", default_timeout=30)
    at.run()
    at.sidebar.slider[0].set_value(150).run()  # fast
    at.sidebar.slider[1].set_value(20).run()  # slow < fast
    assert not at.exception
    assert any("Fast SMA" in e.value for e in at.error)


def test_strategy_selector_switches_strategies(synthetic_prices):
    at = _run_app()
    for name in ["Momentum", "RSI mean reversion"]:
        at.sidebar.selectbox[0].select(name)
        at.run()
        assert not at.exception, f"{name} raised"
        assert len(at.metric) == 4


def test_support_link_hidden_by_default_and_shown_when_configured(
    synthetic_prices, monkeypatch
):
    monkeypatch.delenv("SUPPORT_URL", raising=False)
    at = _run_app()
    assert not any("Support this project" in m.value for m in at.markdown)

    monkeypatch.setenv("SUPPORT_URL", "https://example.com/pay")
    at = _run_app()
    assert any("https://example.com/pay" in m.value for m in at.markdown)


def test_fetch_failure_shows_friendly_error(monkeypatch):
    def boom(ticker, years=25):
        raise RuntimeError("network down")

    monkeypatch.setattr(trading.data, "fetch_daily", boom)
    at = _run_app()
    assert not at.exception
    assert any("Couldn't fetch price data" in e.value for e in at.error)
