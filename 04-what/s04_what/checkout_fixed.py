"""The checkout with the planted bug fixed: the threshold reads the discounted goods."""

from __future__ import annotations

from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from s01_bits.chaos import Charge, Order, Reserve, Send

CENT = Decimal("0.01")


# [snippet: checkout]
def checkout(order: Order, today: date, charge: Charge, reserve: Reserve, send: Send):
    goods = sum((line.price * line.qty for line in order.lines), Decimal(0))
    if order.coupon_valid_until is not None and order.coupon_valid_until >= today:
        goods -= Decimal(10)
    if order.member:
        goods = goods * Decimal("0.90")
    shipping = Decimal(5)
    if order.international:
        shipping = Decimal(20)
    if goods >= Decimal(50):
        shipping = Decimal(0)
    if order.gift_wrap:
        shipping += Decimal(3)
    total = goods + shipping
    if order.vat_id is None:
        total = total * Decimal("1.20")
    total = total.quantize(CENT, rounding=ROUND_HALF_UP)
    charge(total)  # what if it is declined?
    reserve(order.lines)  # what if the stock is gone?
    send(order.email, total)  # what if it bounces?
    return total


# [/snippet]
