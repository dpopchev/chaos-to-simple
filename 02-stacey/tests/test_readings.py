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


# [snippet: r1]
def test_r1_marketing_reads_the_cart() -> None:
    order = Order(
        lines=[Line("book", Decimal(55))], email="a@example.com", coupon_valid_until=TODAY
    )
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("54.00")  # (55 - 10 + 0) * 1.20: the cart ships free


# [/snippet]


@pytest.mark.xfail(strict=True, reason="R2: the code reads R1")
# [snippet: r2]
def test_r2_logistics_reads_what_they_pay() -> None:
    order = Order(
        lines=[Line("book", Decimal(55))], email="a@example.com", coupon_valid_until=TODAY
    )
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("60.00")  # (55 - 10 + 5) * 1.20: the parcel is paid for


# [/snippet]
