"""The bug the two tests never meet.

It is expected to fail (xfail, strict) so the suite stays green while the bug stays visible.
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


# [snippet: bug]
@pytest.mark.xfail(strict=True, reason="planted bug: the threshold reads the subtotal")
def test_free_shipping_after_discount() -> None:
    order = Order(
        lines=[Line("book", Decimal(55))], email="a@example.com", coupon_valid_until=TODAY
    )
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("60.00")  # (55 - 10 + 5) * 1.20: 45 of goods do not earn free shipping


# [/snippet]
