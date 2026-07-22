import os

import pandas as pd
import streamlit as st

from trading import data
from trading.backtest import buy_and_hold, run_backtest
from trading.strategy import sma_crossover_positions

st.set_page_config(page_title="Backtest Lab", page_icon="📈", layout="wide")

st.title("📈 Backtest Lab")
st.write(
    "Test a moving-average crossover strategy on any stock or ETF — "
    "free, no signup. Costs included, no lookahead bias, honest numbers."
)

with st.sidebar:
    st.header("Strategy")
    symbol = st.text_input("Ticker", "SPY").strip().upper()
    fast = st.slider("Fast SMA (days)", 5, 150, 50)
    slow = st.slider("Slow SMA (days)", 20, 400, 200)
    cost_bps = st.number_input(
        "Cost per trade (basis points)", min_value=0.0, max_value=100.0, value=5.0
    )
    st.caption(
        "Long when the fast average is above the slow average, "
        "otherwise in cash. Signals act on the next bar."
    )

if fast >= slow:
    st.error("Fast SMA must be shorter than slow SMA.")
    st.stop()

if not symbol:
    st.info("Enter a ticker to begin.")
    st.stop()


@st.cache_data(ttl=3600, show_spinner="Fetching price history…")
def load_history(ticker: str) -> pd.DataFrame:
    return data.fetch_daily(ticker)


try:
    history = load_history(symbol)
except Exception:
    st.error(f"Couldn't fetch price data for “{symbol}”. Check the ticker symbol.")
    st.stop()

close = history["close"]
positions = sma_crossover_positions(close, fast, slow)
strategy = run_backtest(close, positions, cost_bps=cost_bps)
benchmark = buy_and_hold(close, cost_bps=cost_bps)

st.subheader(
    f"{symbol}: {close.index[0].date()} → {close.index[-1].date()} "
    f"({len(close):,} trading days)"
)

cols = st.columns(4)
cols[0].metric(
    "CAGR", f"{strategy.cagr:+.2%}", f"{strategy.cagr - benchmark.cagr:+.2%} vs hold"
)
cols[1].metric(
    "Sharpe", f"{strategy.sharpe:.2f}", f"{strategy.sharpe - benchmark.sharpe:+.2f} vs hold"
)
cols[2].metric(
    "Max drawdown",
    f"{strategy.max_drawdown:.1%}",
    f"{strategy.max_drawdown - benchmark.max_drawdown:+.1%} vs hold",
)
cols[3].metric("Trades", f"{strategy.n_trades}")

st.line_chart(
    pd.DataFrame(
        {f"SMA {fast}/{slow}": strategy.equity, "Buy & hold": benchmark.equity}
    ),
    height=360,
)

with st.expander("Drawdown"):
    drawdowns = pd.DataFrame(
        {
            f"SMA {fast}/{slow}": strategy.equity / strategy.equity.cummax() - 1.0,
            "Buy & hold": benchmark.equity / benchmark.equity.cummax() - 1.0,
        }
    )
    st.line_chart(drawdowns, height=280)

def _support_url() -> str:
    """Payment/donation link, configured via env var or Streamlit secrets.

    Hidden entirely until one is set, so the app never shows a dead link.
    """
    url = os.environ.get("SUPPORT_URL", "")
    if url:
        return url
    try:
        return st.secrets.get("SUPPORT_URL", "")
    except Exception:
        return ""


if _support_url():
    st.markdown(f"☕ **[Support this project]({_support_url()})** — keeps it free.")

st.caption(
    "Educational tool, not investment advice. Backtests overstate live "
    "performance; past results do not predict future returns. "
    "Data: Yahoo Finance, adjusted daily closes."
)
