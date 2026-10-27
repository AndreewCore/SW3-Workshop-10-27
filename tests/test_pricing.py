"""Tests for the R3 subtotal, using the subtotal column of the worked examples."""

from decimal import Decimal

import pytest

from gym_quote.pricing import subtotal


@pytest.mark.parametrize(
    "plan, extras, members, expected",
    [
        ("BASIC", [], 1, "30"),
        ("STANDARD", ["PERSONAL_TRAINING"], 1, "70"),
        ("BASIC", ["GROUP_CLASSES"], 2, "90"),
        ("BASIC", ["GROUP_CLASSES"], 3, "135"),
        ("STANDARD", ["GROUP_CLASSES", "PERSONAL_TRAINING"], 4, "340"),
        ("PREMIUM", ["GROUP_CLASSES", "SPA"], 2, "230"),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"], 3, "420"),
        ("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM", "PERSONAL_TRAINING"], 4, "660"),
    ],
)
def test_subtotal_is_plan_plus_extras_times_members(plan, extras, members, expected):
    """The subtotal is (plan + extras) x members (R3)."""
    assert subtotal(plan, extras, members) == Decimal(expected)


def test_subtotal_with_no_extras_is_plan_price_times_members():
    """Without extras the subtotal is the plan price times members (R3)."""
    assert subtotal("STANDARD", [], 2) == Decimal("90")


def test_subtotal_returns_a_decimal():
    """The subtotal is a Decimal so that later percentages stay exact."""
    assert isinstance(subtotal("BASIC", [], 1), Decimal)


@pytest.mark.parametrize(
    "plan, extras, members",
    [
        ("BASIC", ["SPA"], 1),
        ("GOLD", [], 1),
        ("BASIC", [], 0),
    ],
)
def test_subtotal_raises_for_invalid_selection(plan, extras, members):
    """An invalid selection has no subtotal (R2, R3)."""
    with pytest.raises(ValueError):
        subtotal(plan, extras, members)
