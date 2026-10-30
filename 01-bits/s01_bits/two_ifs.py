"""The whole bug in two ifs: four paths, the coupon (first bit) and the subtotal at 50 (second bit).

The shipping threshold reads the subtotal, not the goods after the coupon.
"""

from __future__ import annotations

from decimal import Decimal


# [snippet: ship]
def ship(subtotal: Decimal, coupon: bool) -> Decimal:
    goods = subtotal
    if coupon:
        goods -= Decimal(10)
    shipping = Decimal(5)
    if subtotal >= Decimal(50):
        shipping = Decimal(0)
    return goods + shipping


# [/snippet]
