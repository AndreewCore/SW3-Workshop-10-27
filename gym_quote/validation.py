"""Validation of the user's choices (R1, R2, R3)."""

from gym_quote.catalog import EXTRAS, PLANS

PREMIUM_PLAN = "PREMIUM"


def is_valid_plan(plan: str) -> bool:
    """Return True if the plan is one of the catalog plans (R1)."""
    return plan in PLANS


def is_valid_extras(plan: str, extras: list[str]) -> bool:
    """Return True if the extras are known, not repeated, and premium only with PREMIUM (R2).

    Zero extras is valid. Repeated extras are treated as invalid so that
    no extra is charged twice by accident.
    """
    if len(set(extras)) != len(extras):
        return False
    for name in extras:
        if name not in EXTRAS:
            return False
        if EXTRAS[name].premium and plan != PREMIUM_PLAN:
            return False
    return True


def is_valid_members(members: int) -> bool:
    """Return True if the number of members is an integer of at least 1 (R3)."""
    return isinstance(members, int) and not isinstance(members, bool) and members >= 1


def is_valid_selection(plan: str, extras: list[str], members: int) -> bool:
    """Return True if the plan, the extras and the number of members are all valid."""
    return is_valid_plan(plan) and is_valid_extras(plan, extras) and is_valid_members(members)
