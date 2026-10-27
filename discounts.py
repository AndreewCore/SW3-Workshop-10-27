"""Descuento grupal, oferta especial y recargo premium (R4, R5, R6)."""

from decimal import Decimal

GROUP_DISCOUNT_RATE = Decimal("0.10")
OFFER_HIGH_LIMIT = Decimal(400)
OFFER_HIGH_DISCOUNT = Decimal(50)
OFFER_LOW_LIMIT = Decimal(200)
OFFER_LOW_DISCOUNT = Decimal(20)
PREMIUM_SURCHARGE_RATE = Decimal("0.15")


def apply_group_discount(amount, members):
    """R4: con 2 o mas miembros, descuenta 10%."""
    amount = Decimal(amount)
    if members >= 2:
        return amount - amount * GROUP_DISCOUNT_RATE
    return amount


def apply_special_offer(amount):
    """R5: si es mayor a 400 resta 50; si no, si es mayor a 200 resta 20."""
    amount = Decimal(amount)
    if amount > OFFER_HIGH_LIMIT:
        return amount - OFFER_HIGH_DISCOUNT
    if amount > OFFER_LOW_LIMIT:
        return amount - OFFER_LOW_DISCOUNT
    return amount


def apply_premium_surcharge(amount, has_premium_extra):
    """R6: si hay al menos un extra premium, suma 15%."""
    amount = Decimal(amount)
    if has_premium_extra:
        return amount + amount * PREMIUM_SURCHARGE_RATE
    return amount
