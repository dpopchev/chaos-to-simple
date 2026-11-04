"""The change rehearsal: the member discount at 15 percent, written beside the shipped pricing."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from s04_what.money import Money, eur
from s04_what.pricing import COUPON_VALUE, Coupon

# [snippet: member15-factor]
MEMBER_FACTOR = Decimal("0.85")
# [/snippet]


# [snippet: member15]
def discounted_goods(goods: Money, coupon: Coupon | None, member: bool, today: date) -> Money:
    total = goods
    if coupon is not None and coupon.is_valid_on(today):  # b0
        total = total - COUPON_VALUE
    if member:  # b1, after the coupon: the red card said so
        total = total * MEMBER_FACTOR
    return max(total, eur(0))  # a decision hidden in max(): a negative price is not a price


# [/snippet]
