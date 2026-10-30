"""The green cards of the example map, one named test per card.

The names are shared with data/examples.csv; the first test fails when a card
has no test, so the map and the suite cannot drift apart.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from s04_what.money import bgn
from s04_what.pricing import Coupon
from s04_what.shipping import Zone
from s04_what.tax import VatId
from s06_simple.core import Request, price
from scripts.utils.examples import example_names, missing_tests

EXAMPLES = Path(__file__).resolve().parents[2] / "data" / "examples.csv"
Order = Callable[..., Request]


def valid(today: date) -> Coupon:
    return Coupon(valid_until=today)


def expired(today: date) -> Coupon:
    return Coupon(valid_until=today - timedelta(days=1))


def test_every_core_example_has_a_test() -> None:
    assert missing_tests(example_names(EXAMPLES, scope="core"), globals()) == []


def test_coupon_valid_today(order: Order, today: date) -> None:
    assert price(order(goods=bgn(60), coupon=valid(today)), today).goods == 50


def test_coupon_expired_yesterday(order: Order, today: date) -> None:
    assert price(order(goods=bgn(60), coupon=expired(today)), today).goods == 60


def test_member_after_coupon(order: Order, today: date) -> None:
    assert price(order(goods=bgn(60), coupon=valid(today), member=True), today).goods == 45


def test_coupon_never_below_zero(order: Order, today: date) -> None:
    assert price(order(goods=bgn(5), coupon=valid(today)), today).goods == 0


def test_free_shipping_after_discount(order: Order, today: date) -> None:
    assert price(order(goods=bgn(55), coupon=valid(today)), today).shipping == 5


def test_free_shipping_at_threshold(order: Order, today: date) -> None:
    assert price(order(goods=bgn(50)), today).shipping == 0


def test_international_zone(order: Order, today: date) -> None:
    assert price(order(zone=Zone.INTERNATIONAL), today).shipping == 20


def test_gift_wrap_on_free_shipping(order: Order, today: date) -> None:
    assert price(order(goods=bgn(100), gift_wrap=True), today).shipping == 3


def test_vat_without_id(order: Order, today: date) -> None:
    assert price(order(goods=bgn(40)), today).total == Decimal("54.00")


def test_vat_exempt_with_id(order: Order, today: date) -> None:
    exempt = order(goods=bgn(40), vat_id=VatId("BG123456789"))
    assert price(exempt, today).total == Decimal("45.00")
