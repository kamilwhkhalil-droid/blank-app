# Launch kit

Everything needed to take Backtest Lab from repo to revenue. Total human
time: ~20 minutes.

## 1. Deploy (5 min, free)

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → pick `kamilwhkhalil-droid/blank-app`, branch
   `main`, file `streamlit_app.py`.
3. You get a public URL, e.g. `https://backtest-lab.streamlit.app`.

## 2. Turn on the money link (5 min)

Pick one — both take minutes to create:

- **Buy Me a Coffee**: create a page at https://buymeacoffee.com, copy your
  page URL.
- **Stripe Payment Link**: in the Stripe dashboard, Payment Links → New,
  set an amount (or "customer chooses"), copy the URL.

Then in your Streamlit Cloud app: **Settings → Secrets**, add:

```toml
SUPPORT_URL = "https://buymeacoffee.com/yourname"
```

The support button appears in the app footer automatically. No code change.

## 3. Post it (10 min)

Post where the audience already is. Copy below — edit to taste, and only
post each once (spam kills credibility and gets accounts banned).

### Show HN (news.ycombinator.com/submit)

> **Show HN: Backtest Lab – honest SMA backtests vs buy-and-hold, free**
>
> I built a small tool that backtests moving-average crossover strategies
> on any stock/ETF with up to 25 years of data. The twist: it always shows
> buy-and-hold next to the strategy, includes transaction costs, and lags
> signals one bar so there's no lookahead bias. Most backtesting sites
> quietly flatter the strategy; this one tries not to.
> Open source (Python/Streamlit): [repo link]

### r/algotrading (read the sub rules first; flair as "Research" or similar)

> **Free tool: SMA crossover backtests with costs and no lookahead, always
> benchmarked against buy-and-hold**
>
> Weekend project: a Streamlit app that runs SMA crossover backtests on any
> Yahoo ticker. Costs modeled per trade, signals lag one bar, and every
> result shows buy-and-hold alongside so you can see whether the strategy
> actually earns its complexity. Feedback welcome — what metrics or
> strategies would make this useful to you? [app link] / [repo link]

### X / Twitter

> Most backtest tools flatter your strategy. I built one that doesn't:
> costs included, no lookahead, buy-and-hold shown next to every result.
> Free, open source: [app link]

## 4. What to watch, and when to build more

- If a post gets traction, reply to every comment for the first day —
  that's where the audience compounds.
- Watch Streamlit Cloud analytics for repeat visitors. Repeat usage is the
  signal to build a paid tier (more strategies, portfolio backtests, CSV
  export, saved results) — not before.
- Expectation setting: typical outcome for a free niche tool is small
  donations and an audience. The audience is the asset; the paid tier is
  where real revenue would come from if usage justifies it.
