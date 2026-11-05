"""The member discount rehearsal: 15 percent, and shipping applies its own rule to the new value."""

from __future__ import annotations

from datetime import date

from s04_what.money import eur
from s04_what.pricing import Coupon
from s04_what.pricing import discounted_goods as discounted_goods_at_10
from s04_what.shipping import Zone, shipping_fee
from s06_simple.member15 import discounted_goods

TODAY = date(2026, 7, 1)


def test_member_goods_at_fifteen_percent() -> None:
    """Goods 60 with a valid coupon and a member price at 42.50: (60 - 10) * 0.85."""
    coupon = Coupon(valid_until=date(2026, 7, 31))
    assert discounted_goods(eur(60), coupon, True, TODAY) == eur("42.50")


def test_shipping_eligibility_moves_with_the_new_value() -> None:
    """Goods 58 for a member now pay 5 domestic: shipping applied its own rule, unchanged."""
    goods = discounted_goods(eur(58), None, True, TODAY)
    assert shipping_fee(goods, Zone.DOMESTIC, False) == eur(5)


# [snippet: crossing]
def test_member15_moves_a_57_eur_member_order_across_the_threshold() -> None:
    today = date(2026, 11, 5)
    goods_10 = discounted_goods_at_10(eur(57), None, True, today)
    goods_15 = discounted_goods(eur(57), None, True, today)
    fee_at_10 = shipping_fee(goods_10, Zone.DOMESTIC, gift_wrap=False)
    fee_at_15 = shipping_fee(goods_15, Zone.DOMESTIC, gift_wrap=False)
    assert (fee_at_10, fee_at_15) == (eur(0), eur(5))


# [/snippet]
