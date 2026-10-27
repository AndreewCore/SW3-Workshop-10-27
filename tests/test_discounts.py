from decimal import Decimal

import pytest

from discounts import (apply_group_discount, apply_premium_surcharge,
                       apply_special_offer)


def test_r4_no_discount_with_one_member():
    assert apply_group_discount(100, 1) == 100


@pytest.mark.parametrize("members", [2, 3, 10])
def test_r4_ten_percent_from_two_members(members):
    assert apply_group_discount(100, members) == 90


def test_r4_keeps_decimals():
    assert apply_group_discount(135, 3) == Decimal("121.5")


@pytest.mark.parametrize("amount", [0, 100, 200])
def test_r5_no_offer_up_to_200(amount):
    assert apply_special_offer(amount) == amount


@pytest.mark.parametrize("amount,expected", [
    (Decimal("200.01"), Decimal("180.01")), (300, 280), (400, 380),
])
def test_r5_minus_20_between_200_and_400(amount, expected):
    assert apply_special_offer(amount) == expected


@pytest.mark.parametrize("amount,expected", [
    (Decimal("400.01"), Decimal("350.01")), (594, 544),
])
def test_r5_minus_50_above_400(amount, expected):
    assert apply_special_offer(amount) == expected


def test_r5_never_adds_up():
    assert apply_special_offer(1000) == 950


def test_r6_surcharge_with_premium_extra():
    assert apply_premium_surcharge(100, True) == 115


def test_r6_no_surcharge_without_premium_extra():
    assert apply_premium_surcharge(100, False) == 100


def test_r6_keeps_decimals():
    assert apply_premium_surcharge(Decimal("187"), True) == Decimal("215.05")