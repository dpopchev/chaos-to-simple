from __future__ import annotations

from datetime import date

from s04_what.money import bgn
from s04_what.pricing import Coupon
from s05_how.oo_checkout import Checkout

TODAY = date(2026, 11, 5)


# [snippet: order-bit]
def test_call_order_is_a_hidden_bit() -> None:
    coupon_first = Checkout(bgn(60), Coupon(TODAY), member=True, today=TODAY)
    coupon_first.apply_coupon()
    coupon_first.apply_member()

    member_first = Checkout(bgn(60), Coupon(TODAY), member=True, today=TODAY)
    member_first.apply_member()
    member_first.apply_coupon()

    assert coupon_first.total == 45  # (60 - 10) * 0.90, what the rule says
    assert member_first.total == 44  # 60 * 0.90 - 10, what nobody decided


# [/snippet]
