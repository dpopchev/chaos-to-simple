"""Pricing context: what the goods cost after discounts. Bits b0 and b1.

One language: a coupon is valid on a day, the member discount comes after it.
The contract out of this context is a value, the discounted goods; no flag leaves.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from s04_what.money import Money, eur

COUPON_VALUE = eur(10)
# [snippet: member-factor]
MEMBER_FACTOR = Decimal("0.90")
# [/snippet]


# [snippet: coupon]
@dataclass(frozen=True)
class Coupon:
    valid_until: date

    def is_valid_on(self, today: date) -> bool:
        return today <= self.valid_until


# [/snippet]


# [snippet: discounted]
def discounted_goods(goods: Money, coupon: Coupon | None, member: bool, today: date) -> Money:
    total = goods
    if coupon is not None and coupon.is_valid_on(today):  # b0
        total = total - COUPON_VALUE
    if member:  # b1, after the coupon: the red card said so
        total = total * MEMBER_FACTOR
    return max(total, eur(0))  # a decision hidden in max(): a negative price is not a price


# [/snippet]
