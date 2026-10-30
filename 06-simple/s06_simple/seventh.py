"""The seventh if: the shipped fee plus one decision, digital, written beside the core."""

from __future__ import annotations

from s04_what.money import Money, bgn
from s04_what.shipping import FREE_SHIPPING_FROM, GIFT_WRAP, Zone, base_fee


# [snippet: fee-digital]
def shipping_fee(discounted_goods: Money, zone: Zone, gift_wrap: bool, digital: bool) -> Money:
    if digital:  # b6: nothing to ship
        return bgn(0)
    fee = base_fee(zone)
    if discounted_goods >= FREE_SHIPPING_FROM:  # b2
        fee = bgn(0)
    if gift_wrap:  # b4
        fee = fee + GIFT_WRAP
    return fee


# [/snippet]
