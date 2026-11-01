"""Functional core: six bits, values in, values out, no world."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from s04_what.money import Money
from s04_what.pricing import Coupon, discounted_goods
from s04_what.shipping import Zone, shipping_fee
from s04_what.tax import VatId, total_with_vat


# [snippet: request]
@dataclass(frozen=True)
class Request:
    skus: tuple[str, ...]
    goods: Money
    email: str
    coupon: Coupon | None
    member: bool
    zone: Zone
    gift_wrap: bool
    vat_id: VatId | None


@dataclass(frozen=True)
class Priced:
    goods: Money
    shipping: Money
    total: Money


# [/snippet]


# [snippet: price]
def price(request: Request, today: date) -> Priced:
    """Composes three contexts; every bit stays where it was named."""
    goods = discounted_goods(request.goods, request.coupon, request.member, today)
    shipping = shipping_fee(goods, request.zone, request.gift_wrap)
    total = total_with_vat(goods + shipping, request.vat_id)
    return Priced(goods=goods, shipping=shipping, total=total)


# [/snippet]
