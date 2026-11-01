"""The checkout as it was found.

Six if statements in one function, three calls to the outside world with no
decision around them, and one planted bug that only a few of the 64 paths can
reach. Section 01 shows this file as the opening exhibit. Nothing in it is
meant to be good; everything in it is meant to be ordinary.

The bug: the free-shipping threshold reads the subtotal, not the discounted
goods, so a coupon can take an order under 50 and it still ships free.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


# [snippet: order]
@dataclass
class Line:
    sku: str
    price: Decimal
    qty: int = 1


@dataclass
class Order:
    lines: list[Line]
    email: str
    coupon_valid_until: date | None = None
    member: bool = False
    international: bool = False
    gift_wrap: bool = False
    vat_id: str | None = None


# [/snippet]

Charge = Callable[[Decimal], None]
Reserve = Callable[[Sequence[Line]], None]
Send = Callable[[str, Decimal], None]


# [snippet: checkout]
def checkout(order: Order, today: date, charge: Charge, reserve: Reserve, send: Send):  # [step: 0]
    goods = sum((line.price * line.qty for line in order.lines), Decimal(0))  # [step: 0]
    subtotal = goods  # [step: 0]
    if order.coupon_valid_until is not None and order.coupon_valid_until >= today:  # [step: 1]
        goods -= Decimal(10)  # [step: 1]
    if order.member:  # [step: 2]
        goods = goods * Decimal("0.90")  # [step: 2]
    shipping = Decimal(5)  # [step: 0]
    if order.international:  # [step: 4]
        shipping = Decimal(20)  # [step: 4]
    if subtotal >= Decimal(50):  # [step: 3]
        shipping = Decimal(0)  # [step: 3]
    if order.gift_wrap:  # [step: 5]
        shipping += Decimal(3)  # [step: 5]
    total = goods + shipping  # [step: 0]
    if order.vat_id is None:  # [step: 6]
        total = total * Decimal("1.20")  # [step: 6]
    total = total.quantize(CENT, rounding=ROUND_HALF_UP)  # [step: 0]
    charge(total)  # what if it is declined?  # [step: 0]
    reserve(order.lines)  # what if the stock is gone?  # [step: 0]
    send(order.email, total)  # what if it bounces?  # [step: 0]
    return total  # [step: 0]


# [/snippet]
