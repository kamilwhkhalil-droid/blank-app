"""Minimal Alpaca REST client. Paper trading by default; live is gated.

Credentials come from the environment and are never stored in the repo:
    APCA_API_KEY_ID, APCA_API_SECRET_KEY

Live trading requires BOTH `live=True` and the environment variable
ALPACA_LIVE_TRADING set to the exact acknowledgement string below. This is
deliberate friction: paper and live keys are different, and a config slip
must never silently spend real money.
"""

import os
from pathlib import Path

import requests

PAPER_URL = "https://paper-api.alpaca.markets"
LIVE_URL = "https://api.alpaca.markets"
LIVE_ACK = "I_ACCEPT_THE_RISK_OF_REAL_LOSSES"
KILL_SWITCH = Path.home() / ".alpaca_kill_switch"


class AlpacaClient:
    def __init__(self, live: bool = False, max_order_notional: float = 1_000.0):
        key = os.environ.get("APCA_API_KEY_ID")
        secret = os.environ.get("APCA_API_SECRET_KEY")
        if not key or not secret:
            raise RuntimeError(
                "Set APCA_API_KEY_ID and APCA_API_SECRET_KEY in the environment "
                "(never commit them to the repo)."
            )
        if live and os.environ.get("ALPACA_LIVE_TRADING") != LIVE_ACK:
            raise RuntimeError(
                "Live trading is locked. Set ALPACA_LIVE_TRADING="
                f"{LIVE_ACK} to enable real-money orders."
            )
        self.live = live
        self.base_url = LIVE_URL if live else PAPER_URL
        self.max_order_notional = max_order_notional
        self._headers = {
            "APCA-API-KEY-ID": key,
            "APCA-API-SECRET-KEY": secret,
        }

    def _request(self, method: str, path: str, **kwargs):
        resp = requests.request(
            method, f"{self.base_url}{path}", headers=self._headers,
            timeout=30, **kwargs,
        )
        resp.raise_for_status()
        return resp.json()

    def account(self) -> dict:
        return self._request("GET", "/v2/account")

    def positions(self) -> list:
        return self._request("GET", "/v2/positions")

    def submit_market_order(self, symbol: str, notional: float, side: str) -> dict:
        """Submit a market order sized in dollars. Enforces the kill switch
        and the per-order notional cap regardless of paper/live mode."""
        if KILL_SWITCH.exists():
            raise RuntimeError(
                f"Kill switch present at {KILL_SWITCH} — refusing to trade. "
                "Delete the file to re-enable."
            )
        if side not in ("buy", "sell"):
            raise ValueError(f"side must be 'buy' or 'sell', got {side!r}")
        if notional <= 0 or notional > self.max_order_notional:
            raise ValueError(
                f"Order notional ${notional:.2f} outside (0, "
                f"${self.max_order_notional:.2f}] cap"
            )
        return self._request(
            "POST",
            "/v2/orders",
            json={
                "symbol": symbol,
                "notional": str(round(notional, 2)),
                "side": side,
                "type": "market",
                "time_in_force": "day",
            },
        )
