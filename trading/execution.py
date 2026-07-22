"""Turn a strategy's target position into a concrete order decision."""

from dataclasses import dataclass


@dataclass
class OrderDecision:
    action: str  # "buy", "sell", or "hold"
    reason: str


def decide_order(target_position: float, held_qty: float) -> OrderDecision:
    """Reconcile the strategy's target (0 = flat, 1 = long) with what the
    account currently holds. Idempotent: running twice changes nothing."""
    if target_position not in (0.0, 1.0):
        raise ValueError(f"target_position must be 0.0 or 1.0, got {target_position}")
    if target_position == 1.0 and held_qty <= 0:
        return OrderDecision("buy", "signal long, currently flat")
    if target_position == 0.0 and held_qty > 0:
        return OrderDecision("sell", "signal flat, currently long")
    state = "long" if held_qty > 0 else "flat"
    return OrderDecision("hold", f"already {state}, matches signal")
