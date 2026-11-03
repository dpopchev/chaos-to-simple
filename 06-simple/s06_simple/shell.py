"""Imperative shell: three effects, one call into the core, one match per answer.

House rule: no if on a domain field in this file. The shell sequences the world
and reports; the core decides. Reserve first, then charge, then send, so money
never moves for a parcel that does not exist. The only call into the core is price().
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import assert_never

from s04_what.money import Money
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
from s06_simple.core import Request, price


# [snippet: outcome]
@dataclass(frozen=True)
class Accepted:
    total: Money
    confirmed: bool


@dataclass(frozen=True)
class Rejected:
    reason: str


type Outcome = Accepted | Rejected


# [/snippet]


def checkout(
    request: Request,
    today: date,
    gateway: PaymentGateway,
    inventory: Inventory,
    mailer: Mailer,
) -> Outcome:
    # [snippet: checkout]
    priced = price(request, today)
    match inventory.reserve(request.skus):
        case OutOfStock(sku=sku):
            return Rejected(f"out of stock: {sku}")
        case Reserved():
            pass
        case _ as unreachable:
            assert_never(unreachable)
    match gateway.charge(priced.total):
        case Declined(reason=reason):
            return Rejected(f"declined: {reason}")
        case Charged():
            pass
        case _ as unreachable:
            assert_never(unreachable)
    match mailer.send(request.email, priced.total):
        case Sent():
            return Accepted(priced.total, confirmed=True)
        case Bounced():
            return Accepted(priced.total, confirmed=False)
        case _ as unreachable:
            assert_never(unreachable)
    # [/snippet]
