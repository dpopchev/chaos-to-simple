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
def checkout(order: Order, today: date, charge: Charge, reserve: Reserve, send: Send) -> Decimal:
    goods = sum((line.price * line.qty for line in order.lines), Decimal(0))
    subtotal = goods
    if order.coupon_valid_until is not None and order.coupon_valid_until >= today:
        goods -= Decimal(10)
    if order.member:
        goods = goods * Decimal("0.90")
    shipping = Decimal(5)
    if order.international:
        shipping = Decimal(20)
    if subtotal >= Decimal(50):
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
