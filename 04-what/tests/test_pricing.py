from __future__ import annotations

from datetime import date, timedelta

from s04_what.money import eur
from s04_what.pricing import Coupon, discounted_goods

TODAY = date(2026, 11, 5)
VALID = Coupon(valid_until=TODAY)
EXPIRED = Coupon(valid_until=TODAY - timedelta(days=1))


def test_coupon_valid_today() -> None:
    assert discounted_goods(eur(60), VALID, member=False, today=TODAY) == 50


def test_coupon_expired_yesterday() -> None:
    assert discounted_goods(eur(60), EXPIRED, member=False, today=TODAY) == 60


def test_member_after_coupon() -> None:
    assert discounted_goods(eur(60), VALID, member=True, today=TODAY) == 45


def test_coupon_never_below_zero() -> None:
    assert discounted_goods(eur(5), VALID, member=False, today=TODAY) == 0
