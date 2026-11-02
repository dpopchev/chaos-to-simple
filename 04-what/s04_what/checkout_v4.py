"""The checkout as three context calls and the three raw effects."""

from __future__ import annotations

from datetime import date

from s01_bits.chaos import Charge, Order, Reserve, Send
from s04_what.money import eur
from s04_what.pricing import Coupon, discounted_goods
from s04_what.shipping import Zone, shipping_fee
from s04_what.tax import VatId, total_with_vat


# [snippet: checkout]
def checkout(order: Order, today: date, charge: Charge, reserve: Reserve, send: Send):
    goods = sum((line.price * line.qty for line in order.lines), eur(0))
    coupon = (
        Coupon(order.coupon_valid_until)  # no date, no coupon
        if order.coupon_valid_until
        else None
    )
    zone = Zone.INTERNATIONAL if order.international else Zone.DOMESTIC
    vat_id = VatId(order.vat_id) if order.vat_id else None
    net_goods = discounted_goods(goods, coupon, order.member, today)
    fee = shipping_fee(net_goods, zone, order.gift_wrap)
    total = total_with_vat(net_goods + fee, vat_id)
    charge(total)  # what if it is declined?
    reserve(order.lines)  # what if the stock is gone?
    send(order.email, total)  # what if it bounces?
    return total


# [/snippet]
