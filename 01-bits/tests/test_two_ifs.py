"""The two-ifs zoom-in: two tests cover all four lines, the bug sits on the third path."""

from __future__ import annotations

from decimal import Decimal

import pytest

from s01_bits.two_ifs import ship


# [snippet: ship-tests]
def test_ship_regular_order() -> None:
    assert ship(Decimal(40), coupon=False) == Decimal(45)


def test_ship_order_with_everything() -> None:
    assert ship(Decimal(60), coupon=True) == Decimal(50)


# [/snippet]


@pytest.mark.xfail(strict=True, reason="planted bug: the threshold reads the subtotal")
def test_ship_bug_coupon_over_threshold() -> None:
    """45 of goods after the coupon do not earn free shipping: 45 + 5 = 50."""
    assert ship(Decimal(55), coupon=True) == Decimal(50)
