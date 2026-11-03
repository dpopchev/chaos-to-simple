"""Two tests and 100% branch coverage of a function with 64 paths.

make artifacts runs this file under coverage and puts the report on the slide. The bug they
never meet lives in test_planted_bug.py.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date
from decimal import Decimal

from s01_bits.chaos import Line, Order, checkout

TODAY = date(2026, 11, 5)


def charge(amount: Decimal) -> None:
    """The payment provider, doing nothing."""


def reserve(lines: Sequence[Line]) -> None:
    """The warehouse, doing nothing."""


def send(email: str, total: Decimal) -> None:
    """The mail server, doing nothing."""


# [snippet: two-tests]
def test_regular_order() -> None:
    """The customer: one 40 EUR book, domestic, no policy asked for."""
    order = Order(lines=[Line("book", Decimal(40))], email="a@example.com")
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("54.00")


def test_order_with_everything() -> None:
    """Every policy on: coupon, member, abroad, gift wrap, VAT ID."""
    order = Order(
        lines=[Line("book", Decimal(60)), Line("pen", Decimal(40))],
        email="a@example.com",
        coupon_valid_until=TODAY,
        member=True,
        international=True,
        gift_wrap=True,
        vat_id="BG123456789",
    )
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("84.00")


# [/snippet]
