# 📈 Backtest Lab

Test a moving-average crossover strategy on any stock or ETF — free, no
signup. Transaction costs included, no lookahead bias, honest numbers with a
buy-and-hold benchmark alongside every result.

## Features

- Any Yahoo Finance ticker, up to 25 years of adjusted daily history
- Configurable fast/slow SMA windows and per-trade cost
- CAGR, Sharpe ratio, max drawdown, and trade count vs. buy & hold
- Equity-curve and drawdown charts

## Run it locally

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Development

```
pip install -r requirements-dev.txt
pytest --cov=. --cov-report=term-missing
```

The `trading/` package (data, strategy, backtest, broker client) is plain
Python and unit-tested; the Streamlit UI is tested with `AppTest`.

## Disclaimer

Educational tool, not investment advice. Backtests overstate live
performance; past results do not predict future returns.
