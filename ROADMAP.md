# Backtest Lab roadmap

Working agreement for autonomous dev sessions: pick the **topmost unchecked
item**, implement it with tests, run `python3 -m pytest` and only ship green,
keep the increment small enough to finish in one session, check the box in
this file in the same PR. Never commit secrets; never weaken the honest-
metrics framing (buy-and-hold benchmark, costs, no lookahead).

## Done

- [x] Core engine: data fetch, SMA crossover, costed backtester, metrics
- [x] Streamlit app with equity/drawdown charts vs buy-and-hold
- [x] Momentum and RSI mean-reversion strategies with selector UI
- [x] CSV export of results
- [x] Configurable SUPPORT_URL payment link
- [x] CI (pytest + coverage on push/PR), launch kit

## Next

- [ ] Date-range selector so users can test specific periods (e.g. 2008, 2020)
- [ ] Parameter sweep view: small table/heatmap of CAGR across a grid of
      strategy parameters, with an explicit overfitting warning
- [ ] Multi-ticker comparison: run the chosen strategy across 2–5 tickers
      side by side
- [ ] Walk-forward split: fit-period vs holdout-period metrics shown
      separately, to demonstrate out-of-sample decay honestly
- [ ] Portfolio mode: fixed-weight basket with periodic rebalancing vs the
      strategy
- [ ] Shareable results: encode config in URL query params so a backtest can
      be linked directly (great for social distribution)
- [ ] SEO/meta polish: page description, social preview text
- [ ] Premium groundwork (only if usage justifies): saved results, more data
      (weekly/intraday), Stripe-gated tier

## Parked

- Live/paper trading operations (needs user's Alpaca keys — see
  `trading/alpaca.py`; live mode stays triple-gated)
