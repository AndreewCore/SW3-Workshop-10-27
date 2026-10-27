"""Subtotal of a valid selection (R3)."""

from decimal import Decimal

from gym_quote.catalog import EXTRAS, PLANS
from gym_quote.validation import is_valid_selection


def subtotal(plan: str, extras: list[str], members: int) -> Decimal:
    """Return (plan price + price of the extras) x members, as a Decimal.

    Raises ValueError if the selection is invalid. The result is not rounded
    and has no discounts applied; those are applied later (R4, R5, R6).
    """
    if not is_valid_selection(plan, extras, members):
        raise ValueError("invalid selection")
    per_member = PLANS[plan] + sum((EXTRAS[name].price for name in extras), Decimal("0"))
    return per_member * members
