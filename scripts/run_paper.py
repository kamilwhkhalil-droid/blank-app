"""Daily trading runner: compute today's SMA signal and sync the position.

Usage: python -m scripts.run_paper [SYMBOL] [--live]

Paper by default. --live additionally requires ALPACA_LIVE_TRADING to be set
to the acknowledgement string (see trading/alpaca.py) — both gates on
purpose. Designed to run once per day after market close or before open.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from trading.alpaca import AlpacaClient
from trading.data import fetch_daily
from trading.execution import decide_order
from trading.strategy import sma_crossover_positions

FAST, SLOW = 50, 200
ORDER_NOTIONAL = 500.0  # dollars per entry; also the per-order cap


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    symbol = args[0].upper() if args else "SPY"
    live = "--live" in sys.argv

    client = AlpacaClient(live=live, max_order_notional=ORDER_NOTIONAL)
    mode = "LIVE" if live else "paper"
    print(f"[{mode}] account equity: ${float(client.account()['equity']):,.2f}")

    close = fetch_daily(symbol)["close"]
    target = sma_crossover_positions(close, FAST, SLOW).iloc[-1]

    held_qty = 0.0
    for position in client.positions():
        if position["symbol"] == symbol:
            held_qty = float(position["qty"])

    decision = decide_order(float(target), held_qty)
    print(f"{symbol}: SMA {FAST}/{SLOW} target={target:.0f}, held={held_qty} "
          f"→ {decision.action} ({decision.reason})")

    if decision.action == "buy":
        order = client.submit_market_order(symbol, ORDER_NOTIONAL, "buy")
        print(f"submitted buy ${ORDER_NOTIONAL:.2f}: order id {order['id']}")
    elif decision.action == "sell":
        result = client._request("DELETE", f"/v2/positions/{symbol}")
        print(f"closed position: order id {result.get('id', '?')}")
    else:
        print("no order needed")


if __name__ == "__main__":
    main()
