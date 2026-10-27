"""Tests for R7 rounding and the -1 result."""

from decimal import Decimal

import pytest

from gym_quote.rounding import INVALID_RESULT, final_result, round_half_up


@pytest.mark.parametrize(
    "amount, expected",
    [
        ("81", 81),
        ("81.49", 81),
        ("81.5", 82),
        ("81.50", 82),
        ("0.5", 1),
        ("411.7", 412),
        ("215.05", 215),
    ],
)
def test_round_half_up(amount, expected):
    """Amounts are rounded to a whole number, with halves going up (R7)."""
    assert round_half_up(Decimal(amount)) == expected


def test_round_half_up_returns_an_int():
    """The rounded total is an int, not a Decimal."""
    assert isinstance(round_half_up(Decimal("10.2")), int)


def test_final_result_rounds_a_valid_amount():
    """A valid amount is rounded once at the end (R7)."""
    assert final_result(Decimal("187") * Decimal("1.15"), valid=True) == 215


def test_final_result_is_minus_one_when_invalid():
    """An invalid selection or a cancelled quote gives -1 (R7)."""
    assert final_result(Decimal("187"), valid=False) == INVALID_RESULT
    assert INVALID_RESULT == -1
