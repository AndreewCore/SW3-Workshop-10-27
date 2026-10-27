
"""Integration of membership pricing rules (R1-R7)."""

from decimal import Decimal

from gym_quote.catalog import EXTRAS, PLANS
from gym_quote.discounts import (
    apply_group_discount,
    apply_premium_surcharge,
    apply_special_offer,
)
from gym_quote.pricing import subtotal
from gym_quote.quote import QuoteResult
from gym_quote.rounding import final_result


def calculate_quote(
    plan: str,
    extras: list[str],
    members: int,
) -> QuoteResult:
    """Calculate a complete quote without interacting with the user.

    Applies the subtotal, group discount, special offer, premium
    surcharge, and final rounding in that order.
    Invalid selections return a QuoteResult with total -1.
    """
    try:
        subtotal_amount = subtotal(plan, extras, members)
    except (ValueError, TypeError):
        return QuoteResult()

    has_premium_extra = any(
        EXTRAS[name].premium for name in extras
    )

    after_group_discount = apply_group_discount(
        subtotal_amount, members
    )

    after_special_offer = apply_special_offer(
        after_group_discount
    )

    final_amount = apply_premium_surcharge(
        after_special_offer,
        has_premium_extra,
    )

    total = final_result(final_amount, valid=True)

    breakdown = {
        "plan": PLANS[plan] * members,
        "extras": sum(
            (EXTRAS[name].price * members for name in extras),
            Decimal("0"),
        ),
        "subtotal": subtotal_amount,
        "group_discount": (
            subtotal_amount - after_group_discount
        ),
        "after_group_discount": after_group_discount,
        "special_offer_discount": (
            after_group_discount - after_special_offer
        ),
        "after_special_offer": after_special_offer,
        "premium_surcharge": (
            final_amount - after_special_offer
        ),
        "before_rounding": final_amount,
        "total": total,
    }

    return QuoteResult(total, breakdown=breakdown)
