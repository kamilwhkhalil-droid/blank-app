import pytest

from trading.alpaca import LIVE_ACK, LIVE_URL, PAPER_URL, AlpacaClient


@pytest.fixture
def fake_keys(monkeypatch):
    monkeypatch.setenv("APCA_API_KEY_ID", "test-key")
    monkeypatch.setenv("APCA_API_SECRET_KEY", "test-secret")
    monkeypatch.delenv("ALPACA_LIVE_TRADING", raising=False)


def test_missing_credentials_rejected(monkeypatch):
    monkeypatch.delenv("APCA_API_KEY_ID", raising=False)
    monkeypatch.delenv("APCA_API_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="APCA_API_KEY_ID"):
        AlpacaClient()


def test_defaults_to_paper(fake_keys):
    assert AlpacaClient().base_url == PAPER_URL


def test_live_locked_without_acknowledgement(fake_keys):
    with pytest.raises(RuntimeError, match="locked"):
        AlpacaClient(live=True)


def test_live_unlocks_with_acknowledgement(fake_keys, monkeypatch):
    monkeypatch.setenv("ALPACA_LIVE_TRADING", LIVE_ACK)
    assert AlpacaClient(live=True).base_url == LIVE_URL


def test_order_notional_cap_enforced(fake_keys):
    client = AlpacaClient(max_order_notional=100.0)
    with pytest.raises(ValueError, match="cap"):
        client.submit_market_order("SPY", notional=101.0, side="buy")


def test_invalid_side_rejected(fake_keys):
    client = AlpacaClient()
    with pytest.raises(ValueError, match="side"):
        client.submit_market_order("SPY", notional=50.0, side="short")


def test_kill_switch_blocks_orders(fake_keys, monkeypatch, tmp_path):
    switch = tmp_path / "kill"
    switch.touch()
    monkeypatch.setattr("trading.alpaca.KILL_SWITCH", switch)
    client = AlpacaClient()
    with pytest.raises(RuntimeError, match="Kill switch"):
        client.submit_market_order("SPY", notional=50.0, side="buy")
