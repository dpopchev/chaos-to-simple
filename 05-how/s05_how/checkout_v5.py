"""The checkout with its three effects behind the ports: one match per answer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import assert_never

from s01_bits.chaos import Order
from s04_what.money import Money, eur
from s04_what.pricing import Coupon, discounted_goods
from s04_what.shipping import Zone, shipping_fee
from s04_what.tax import VatId, total_with_vat
from s05_how.ports import (
    Bounced,
    Charged,
    Declined,
    Inventory,
    Mailer,
    OutOfStock,
    PaymentGateway,
    Reserved,
    Sent,
)


@dataclass(frozen=True)
class Accepted:
    total: Money
    confirmed: bool


@dataclass(frozen=True)
class Rejected:
    reason: str


type CheckoutResult = Accepted | Rejected


def checkout(
    order: Order,
    today: date,
    gateway: PaymentGateway,
    inventory: Inventory,
    mailer: Mailer,
) -> CheckoutResult:
    # [snippet: checkout]
    goods = sum((line.price * line.qty for line in order.lines), eur(0))
    coupon = Coupon(order.coupon_valid_until) if order.coupon_valid_until else None
    zone = Zone.INTERNATIONAL if order.international else Zone.DOMESTIC
    vat_id = VatId(order.vat_id) if order.vat_id else None
    net_goods = discounted_goods(goods, coupon, order.member, today)
    fee = shipping_fee(net_goods, zone, order.gift_wrap)
    total = total_with_vat(net_goods + fee, vat_id)
    match inventory.reserve([line.sku for line in order.lines]):
        case OutOfStock(sku=sku):
            return Rejected(f"out of stock: {sku}")
        case Reserved():
            pass
        case _ as unreachable:
            assert_never(unreachable)
    match gateway.charge(total):
        case Declined(reason=reason):
            return Rejected(f"declined: {reason}")
        case Charged():
            pass
        case _ as unreachable:
            assert_never(unreachable)
    match mailer.send(order.email, total):
        case Sent():
            return Accepted(total, confirmed=True)
        case Bounced():
            return Accepted(total, confirmed=False)
        case _ as unreachable:
            assert_never(unreachable)
    # [/snippet]
