"""The four orders the memo implies, and the one finance reads differently.

The 55 EUR order with a coupon is expected to fail (xfail, strict) so the suite stays green
while the disagreement stays visible.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date
from decimal import Decimal

import pytest
from pytest import param

from s01_bits.chaos import Line, Order, checkout

TODAY = date(2026, 11, 5)
XFAIL = pytest.mark.xfail(strict=True, reason="45 earns no free shipping")


def charge(amount: Decimal) -> None:
    """The payment provider, doing nothing."""


def reserve(lines: Sequence[Line]) -> None:
    """The warehouse, doing nothing."""


def send(email: str, total: Decimal) -> None:
    """The mail server, doing nothing."""


def total_of(eur: int, coupon: bool) -> Decimal:
    """Check out one book of the given price, with the coupon or without."""
    until = TODAY if coupon else None
    order = Order([Line("book", Decimal(eur))], "a@example.com", until)
    return checkout(order, TODAY, charge, reserve, send)


# [snippet: memo-orders]
class TestMemoOrders:
    """One order per cell: with or without the coupon, the cart under or over 50 EUR before it;
    want is what logistics pays."""

    @pytest.mark.parametrize(
        ("eur", "coupon", "want"),
        [
            param(40, False, "54.00", id="40-no-coupon"),
            param(50, False, "60.00", id="50-no-coupon"),
            param(60, True, "60.00", id="60-coupon"),
            param(55, True, "60.00", id="55-coupon", marks=XFAIL),
        ],
    )
    def test_total(self, eur: int, coupon: bool, want: str) -> None:
        assert total_of(eur, coupon) == Decimal(want)


# [/snippet]
