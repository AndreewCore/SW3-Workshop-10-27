"""Final rounding of the total and the invalid result (R7)."""

from decimal import ROUND_HALF_UP, Decimal

from gym_quote.quote import QuoteResult

INVALID_RESULT = QuoteResult.INVALID


def round_half_up(amount):
    """Round an amount to a whole number, with halves going up (R7)."""
    return int(Decimal(amount).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def final_result(amount, valid):
    """Return the final total, or -1 if the selection is invalid or was cancelled (R7).

    Call this once, at the very end of the calculation, so that the amount
    is rounded only after every discount and surcharge has been applied.
    """
    if not valid:
        return INVALID_RESULT
    return round_half_up(amount)
