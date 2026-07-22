"""Daily price data via Yahoo Finance's public chart API.

Uses plain `requests` (honors HTTPS_PROXY / REQUESTS_CA_BUNDLE) rather than
yfinance, whose curl backend does not work behind TLS-intercepting proxies.
"""

import pandas as pd
import requests

CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def fetch_daily(symbol: str, years: int = 25) -> pd.DataFrame:
    """Return a DataFrame indexed by date with an adjusted `close` column."""
    resp = requests.get(
        CHART_URL.format(symbol=symbol),
        params={"range": f"{years}y", "interval": "1d"},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=60,
    )
    resp.raise_for_status()
    result = resp.json()["chart"]["result"][0]
    adjclose = result["indicators"]["adjclose"][0]["adjclose"]
    df = pd.DataFrame(
        {"close": adjclose},
        index=pd.to_datetime(result["timestamp"], unit="s").normalize(),
    )
    return df.dropna()
