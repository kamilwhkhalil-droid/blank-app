"""Backtest SMA-crossover variants on a symbol and compare to buy-and-hold.

Usage: python -m scripts.run_backtest [SYMBOL]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from trading.backtest import buy_and_hold, run_backtest
from trading.data import fetch_daily
from trading.strategy import sma_crossover_positions


def main() -> None:
    symbol = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    df = fetch_daily(symbol)
    close = df["close"]
    print(f"{symbol}: {len(close)} daily bars, "
          f"{close.index[0].date()} → {close.index[-1].date()}\n")

    bh = buy_and_hold(close)
    print(f"{'buy & hold':<18} {bh.summary()}")
    for fast, slow in [(20, 100), (50, 200), (100, 300)]:
        positions = sma_crossover_positions(close, fast, slow)
        result = run_backtest(close, positions)
        print(f"{f'SMA {fast}/{slow}':<18} {result.summary()}")

    print(
        "\nCosts modeled at 5 bps per trade. Past performance does not "
        "predict future results; backtests overstate live performance."
    )


if __name__ == "__main__":
    main()
