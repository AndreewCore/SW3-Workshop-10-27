
"""Master integration tests for complete membership quotes."""

from decimal import Decimal

import pytest

from gym_quote.calculator import calculate_quote


@pytest.mark.parametrize(
    "plan, extras, members, expected_subtotal, expected_total",
    [
        ("BASIC", [], 1, "30", 30),
        ("STANDARD", ["PERSONAL_TRAINING"], 1, "70", 70),
        ("BASIC", ["GROUP_CLASSES"], 2, "90", 81),
        ("BASIC", ["GROUP_CLASSES"], 3, "135", 122),
        (
            "STANDARD",
            ["GROUP_CLASSES", "PERSONAL_TRAINING"],
            4,
            "340",
            286,
        ),
        (
            "PREMIUM",
            ["GROUP_CLASSES", "SPA"],
            2,
            "230",
            215,
        ),
        (
            "PREMIUM",
            ["SPA", "SPECIALIZED_PROGRAM"],
            3,
            "420",
            412,
        ),
        (
            "PREMIUM",
            [
                "SPA",
                "SPECIALIZED_PROGRAM",
                "PERSONAL_TRAINING",
            ],
            4,
            "660",
            626,
        ),
    ],
)
def test_complete_quote_scenarios(
    plan,
    extras,
    members,
    expected_subtotal,
    expected_total,
):
    """The complete calculation matches each worked example."""
    result = calculate_quote(plan, extras, members)

    assert result.is_valid()
    assert result.breakdown["subtotal"] == Decimal(expected_subtotal)
    assert result.total == expected_total


@pytest.mark.parametrize(
    "plan, extras, members",
    [
        ("GOLD", [], 1),
        ("BASIC", ["SPA"], 1),
        ("BASIC", ["UNKNOWN_EXTRA"], 1),
        ("BASIC", [], 0),
        ("BASIC", [], -1),
    ],
)
def test_invalid_selections_return_minus_one(plan, extras, members):
    """Invalid selections must not produce a valid quote."""
    result = calculate_quote(plan, extras, members)

    assert result.total == -1
    assert not result.is_valid()


def test_premium_quote_has_surcharge_and_rounds_at_the_end():
    """The premium surcharge is applied before final rounding."""
    result = calculate_quote(
        "PREMIUM",
        ["GROUP_CLASSES", "SPA"],
        2,
    )

    assert result.breakdown["after_special_offer"] == Decimal("187")
    assert result.breakdown["premium_surcharge"] == Decimal("28.05")
    assert result.breakdown["before_rounding"] == Decimal("215.05")
    assert result.total == 215
