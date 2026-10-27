"""Tests for R1, R2 and R3 validation."""

import pytest

from gym_quote.catalog import PLANS
from gym_quote.validation import (
    is_valid_extras,
    is_valid_members,
    is_valid_plan,
    is_valid_selection,
)


@pytest.mark.parametrize("plan", ["BASIC", "STANDARD", "PREMIUM"])
def test_catalog_plans_are_valid(plan):
    """Each plan in the table is accepted (R1)."""
    assert is_valid_plan(plan)


@pytest.mark.parametrize("plan", ["GOLD", "basic", "", " BASIC", "Premium"])
def test_other_plans_are_invalid(plan):
    """Plans that are not in the table are rejected (R1)."""
    assert not is_valid_plan(plan)


@pytest.mark.parametrize("plan", list(PLANS))
def test_zero_extras_is_valid_for_every_plan(plan):
    """Choosing no extras is allowed with any plan (R2)."""
    assert is_valid_extras(plan, [])


@pytest.mark.parametrize("plan", list(PLANS))
def test_standard_extras_are_valid_for_every_plan(plan):
    """Extras without the premium flag can be added to any plan (R2)."""
    assert is_valid_extras(plan, ["GROUP_CLASSES"])
    assert is_valid_extras(plan, ["PERSONAL_TRAINING"])


def test_unknown_extra_is_invalid():
    """An extra that is not in the table is rejected (R2)."""
    assert not is_valid_extras("PREMIUM", ["JACUZZI"])


@pytest.mark.parametrize("plan", ["BASIC", "STANDARD"])
def test_premium_extra_is_invalid_without_premium_plan(plan):
    """Premium extras require the PREMIUM plan (R2)."""
    assert not is_valid_extras(plan, ["SPA"])
    assert not is_valid_extras(plan, ["SPECIALIZED_PROGRAM"])


def test_premium_extras_are_valid_with_premium_plan():
    """Premium extras are accepted with the PREMIUM plan (R2)."""
    assert is_valid_extras("PREMIUM", ["SPA"])
    assert is_valid_extras("PREMIUM", ["SPA", "SPECIALIZED_PROGRAM"])


def test_repeated_extra_is_invalid():
    """The same extra twice is rejected so it is not charged twice (R2)."""
    assert not is_valid_extras("BASIC", ["GROUP_CLASSES", "GROUP_CLASSES"])


@pytest.mark.parametrize("members", [1, 2, 10])
def test_members_of_one_or_more_are_valid(members):
    """One or more members is a valid group size (R3)."""
    assert is_valid_members(members)


@pytest.mark.parametrize("members", [0, -1])
def test_members_below_one_are_invalid(members):
    """Zero or negative members is rejected (R3)."""
    assert not is_valid_members(members)


@pytest.mark.parametrize("members", [1.5, "2", None, True])
def test_members_must_be_an_integer(members):
    """Members must be an integer, not a float, string, None or bool (R3)."""
    assert not is_valid_members(members)


def test_selection_is_valid_when_all_parts_are_valid():
    """A selection is valid when plan, extras and members are valid."""
    assert is_valid_selection("PREMIUM", ["SPA", "GROUP_CLASSES"], 3)


@pytest.mark.parametrize(
    "plan, extras, members",
    [
        ("BASIC", ["SPA"], 1),  # premium extra without PREMIUM plan
        ("GOLD", [], 1),  # unknown plan
        ("BASIC", [], 0),  # no members
    ],
)
def test_selection_is_invalid_when_any_part_is_invalid(plan, extras, members):
    """A selection is invalid if any one of its parts is invalid."""
    assert not is_valid_selection(plan, extras, members)
