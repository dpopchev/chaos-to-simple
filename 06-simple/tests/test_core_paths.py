"""Sixty-four paths, one test each, built from the bit pattern. We counted them."""

from __future__ import annotations

from datetime import date

import pytest

from s04_what.money import eur
from s04_what.pricing import Coupon
from s04_what.shipping import GIFT_WRAP, Zone
from s04_what.tax import VatId
from s06_simple.core import Priced, Request, price

TODAY = date(2026, 11, 5)


# [snippet: request-from-bits]
def request_from_bits(bits: int) -> Request:
    """Bit k of the path number sets decision bk; 000000 is the plainest order."""
    return Request(
        skus=("book",),
        goods=eur(100) if bits & 0b000100 else eur(20),  # b2: the threshold is reachable
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
class TestEveryCorePath:
    @pytest.fixture
    def order(self, bits: int) -> Request:
        return request_from_bits(bits)

    @pytest.fixture
    def priced(self, order: Request) -> Priced:
        return price(order, TODAY)

    def test_discounts_never_add(self, order: Request, priced: Priced) -> None:
        assert 0 <= priced.goods <= order.goods

    # [/snippet]
    # [snippet: invariants]
    def test_shipping_is_free_iff_discounted_goods_reach_50(self, order: Request, priced: Priced):
        assert (priced.shipping - GIFT_WRAP * order.gift_wrap == 0) == (priced.goods >= 50)

    def test_vat_never_reduces_the_total(self, priced: Priced) -> None:
        assert priced.total >= priced.goods + priced.shipping

    # [/snippet]
