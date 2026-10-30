"""The How before the seam: one object, a mutable total, methods that both do and tell.

Shown in section 05 as the counter-example. The call order of apply_coupon and
apply_member changes the total: a bit no test enumerates because nobody wrote
it down. Command Query Separation is what removes it.
"""

from __future__ import annotations

from datetime import date

from s04_what.money import Money
from s04_what.pricing import COUPON_VALUE, MEMBER_FACTOR, Coupon


# [snippet: oo]
class Checkout:
    def __init__(self, goods: Money, coupon: Coupon | None, member: bool, today: date) -> None:
        self.total = goods
        self.coupon = coupon
        self.member = member
        self.today = today

    def apply_coupon(self) -> bool:  # a command that also answers: CQS broken
        if self.coupon is not None and self.coupon.is_valid_on(self.today):
            self.total = self.total - COUPON_VALUE
            return True
        return False

    def apply_member(self) -> bool:  # call it before apply_coupon and the total changes
        if self.member:
            self.total = self.total * MEMBER_FACTOR
            return True
        return False


# [/snippet]
