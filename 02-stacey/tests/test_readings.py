"""The two readings of one order: each a test, and no code can pass both.

R2 is expected to fail (xfail, strict) so the suite stays green while the dispute stays visible.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date
from decimal import Decimal

import pytest

from s01_bits.chaos import Line, Order, checkout

TODAY = date(2026, 11, 5)


def charge(amount: Decimal) -> None:
    """The payment provider, doing nothing."""


def reserve(lines: Sequence[Line]) -> None:
    """The warehouse, doing nothing."""


def send(email: str, total: Decimal) -> None:
    """The mail server, doing nothing."""


def test_r1_marketing_reads_the_cart() -> None:
    """Marketing reads the cart, 55 EUR: shipping free, 45 + VAT = 54.00."""
    order = Order(
        lines=[Line("book", Decimal(55))],
        email="a@example.com",
        coupon_valid_until=TODAY,
    )
    # [snippet: r1]
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("54.00")
    # [/snippet]


@pytest.mark.xfail(strict=True, reason="R2: the code reads R1")
def test_r2_logistics_reads_what_they_pay() -> None:
    """Logistics reads the goods after the coupon, 45 EUR: 45 + 5 + VAT = 60.00."""
    order = Order(
        lines=[Line("book", Decimal(55))],
        email="a@example.com",
        coupon_valid_until=TODAY,
    )
    # [snippet: r2]
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("60.00")
    # [/snippet]
