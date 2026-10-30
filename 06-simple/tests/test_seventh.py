"""The seventh if: a digital order ships free; the rest agree with the shipped fee."""

from __future__ import annotations

import pytest

from s04_what.money import bgn
from s04_what.shipping import Zone
from s04_what.shipping import shipping_fee as shipped_fee
from s06_simple.seventh import shipping_fee


def test_digital_ships_free() -> None:
    assert shipping_fee(bgn(20), Zone.INTERNATIONAL, True, True) == bgn(0)


@pytest.mark.parametrize("bits", range(16), ids=lambda b: f"{b:04b}")
def test_sixteen_paths_of_the_fee(bits: int) -> None:
    goods = bgn(100) if bits & 0b0001 else bgn(20)
    zone = Zone.INTERNATIONAL if bits & 0b0010 else Zone.DOMESTIC
    gift_wrap = bool(bits & 0b0100)
    digital = bool(bits & 0b1000)
    expected = bgn(0) if digital else shipped_fee(goods, zone, gift_wrap)
    assert shipping_fee(goods, zone, gift_wrap, digital) == expected
