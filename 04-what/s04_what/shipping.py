"""Shipping context: what the parcel costs. Bits b2, b3 and b4.

The zone is a sum type, so the type checker counts that bit for us; the
threshold takes the discounted goods as a value, so it never multiplies with
the pricing bits.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import assert_never

from s04_what.money import Money, eur

FREE_SHIPPING_FROM = eur(50)
GIFT_WRAP = eur(3)


# [snippet: zone]
class Zone(Enum):
    DOMESTIC = auto()
    INTERNATIONAL = auto()


def base_fee(zone: Zone) -> Money:  # b3
    match zone:
        case Zone.DOMESTIC:
            return eur(5)
        case Zone.INTERNATIONAL:
            return eur(20)
        case _:
            assert_never(zone)


# [/snippet]


# [snippet: fee]
def shipping_fee(discounted_goods: Money, zone: Zone, gift_wrap: bool) -> Money:
    fee = base_fee(zone)
    if discounted_goods >= FREE_SHIPPING_FROM:  # b2, on the discounted goods: the bug, fixed
        fee = eur(0)
    if gift_wrap:  # b4
        fee = fee + GIFT_WRAP
    return fee


# [/snippet]
