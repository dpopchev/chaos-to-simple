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


@pytest.mark.xfail(strict=True, reason="planted bug: the threshold reads the subtotal")
# [snippet: bug]
def test_free_shipping_after_discount() -> None:
    """Logistics: 45 of goods after the coupon do not earn free shipping; with VAT 60.00."""
    order = Order(
        lines=[Line("book", Decimal(55))], email="a@example.com", coupon_valid_until=TODAY
    )
    total = checkout(order, TODAY, charge, reserve, send)
    assert total == Decimal("60.00")


# [/snippet]
