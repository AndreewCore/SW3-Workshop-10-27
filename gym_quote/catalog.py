"""Catalog of gym plans and extras with their prices (R1, R2)."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Extra:
    """An optional extra, priced per member."""

    price: Decimal
    premium: bool


PLANS = {
    "BASIC": Decimal("30"),
    "STANDARD": Decimal("45"),
    "PREMIUM": Decimal("70"),
}

EXTRAS = {
    "GROUP_CLASSES": Extra(Decimal("15"), premium=False),
    "PERSONAL_TRAINING": Extra(Decimal("25"), premium=False),
    "SPA": Extra(Decimal("30"), premium=True),
    "SPECIALIZED_PROGRAM": Extra(Decimal("40"), premium=True),
}
