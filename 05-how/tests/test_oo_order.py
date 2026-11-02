from __future__ import annotations

from datetime import date

import pytest

from s04_what.money import eur
from s04_what.pricing import Coupon
from s05_how.oo_checkout import Checkout

TODAY = date(2026, 11, 5)


# [snippet: order-bit]
class TestCallOrder:
    @pytest.fixture
    def checkout(self) -> Checkout:
        return Checkout(eur(60), Coupon(TODAY), member=True, today=TODAY)

    def test_coupon_first_follows_the_rule(self, checkout: Checkout) -> None:
        checkout.apply_coupon()
        checkout.apply_member()
        assert checkout.total == 45  # (60 - 10) * 0.90, what the rule says

    def test_member_first_differs(self, checkout: Checkout) -> None:
        checkout.apply_member()
        checkout.apply_coupon()
        assert checkout.total == 44  # 60 * 0.90 - 10, what nobody decided


# [/snippet]
