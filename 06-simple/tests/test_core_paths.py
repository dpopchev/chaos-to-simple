"""Sixty-four paths, one test each, built from the bit pattern. We counted them."""

from __future__ import annotations

from datetime import date

import pytest

from s04_what.money import bgn
from s04_what.pricing import Coupon
from s04_what.shipping import GIFT_WRAP, Zone
from s04_what.tax import VatId
from s06_simple.core import Request, price

TODAY = date(2026, 11, 5)


# [snippet: request-from-bits]
def request_from_bits(bits: int) -> Request:
    """Bit k of the path number sets decision bk; 000000 is the plainest order."""
    return Request(
        skus=("book",),
        goods=bgn(100) if bits & 0b000100 else bgn(20),  # b2: the threshold is reachable
        email="a@example.com",
        coupon=Coupon(valid_until=TODAY) if bits & 0b000001 else None,  # b0
        member=bool(bits & 0b000010),  # b1
        zone=Zone.INTERNATIONAL if bits & 0b001000 else Zone.DOMESTIC,  # b3
        gift_wrap=bool(bits & 0b010000),  # b4
        vat_id=VatId("BG123456789") if bits & 0b100000 else None,  # b5
    )


# [/snippet]


# [snippet: from-bits]
@pytest.mark.parametrize("bits", range(64), ids=lambda b: f"{b:06b}")
def test_every_core_path_holds_the_invariants(bits: int) -> None:
    request = request_from_bits(bits)
    priced = price(request, TODAY)
    wrap = GIFT_WRAP if request.gift_wrap else 0
    assert 0 <= priced.goods <= request.goods  # discounts never add and never go below zero
    assert (priced.shipping - wrap == 0) == (priced.goods >= 50)  # free iff discounted >= 50
    assert priced.total >= priced.goods + priced.shipping  # VAT never reduces the total


# [/snippet]
