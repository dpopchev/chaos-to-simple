"""Two tests, 100% branch coverage, and the bug they never meet.

make artifacts runs only the regular order and the order with everything under
coverage and puts the report on the slide. The third test is the bug; it is
expected to fail (xfail, strict) so the suite stays green while the bug stays
visible.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date
from decimal import Decimal

import pytest

from s01_bits.chaos import Line, Order, checkout

TODAY = date(2026, 11, 5)


class Recorder:
    """The outside world, as a list of what was asked of it."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def charge(self, amount: Decimal) -> None:
        self.calls.append(f"charge {amount}")

    def reserve(self, lines: Sequence[Line]) -> None:
        self.calls.append(f"reserve {len(lines)}")

    def send(self, email: str, total: Decimal) -> None:
        self.calls.append(f"send {email}")


# [snippet: two-tests]
def test_regular_order() -> None:
    order = Order(lines=[Line("book", Decimal(40))], email="a@example.com")
    world = Recorder()
    total = checkout(order, TODAY, world.charge, world.reserve, world.send)
    assert total == Decimal("54.00")  # (40 + 5) * 1.20
    assert world.calls == ["charge 54.00", "reserve 1", "send a@example.com"]


def test_order_with_everything() -> None:
    order = Order(
        lines=[Line("book", Decimal(60)), Line("pen", Decimal(40))],
        email="a@example.com",
        coupon_valid_until=TODAY,
        member=True,
        international=True,
        gift_wrap=True,
        vat_id="BG123456789",
    )
    world = Recorder()
    total = checkout(order, TODAY, world.charge, world.reserve, world.send)
    assert total == Decimal("84.00")  # (100 - 10) * 0.90 + 0 shipping + 3 wrap, no VAT


# [/snippet]


# [snippet: bug]
@pytest.mark.xfail(strict=True, reason="planted bug: the threshold reads the subtotal")
def test_free_shipping_after_discount() -> None:
    order = Order(
        lines=[Line("book", Decimal(55))], email="a@example.com", coupon_valid_until=TODAY
    )
    world = Recorder()
    total = checkout(order, TODAY, world.charge, world.reserve, world.send)
    assert total == Decimal("60.00")  # (55 - 10 + 5) * 1.20: 45 of goods do not earn free shipping


# [/snippet]
