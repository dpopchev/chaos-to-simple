"""Imperative shell: three effects, one call into the core, one match per answer.

House rule: no if on a domain field in this file. The shell sequences the world
and reports; the core decides. Reserve first, then charge, then send, so money
never moves for a parcel that does not exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

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
    SendResult,
    Sent,
)
from s06_simple.core import Request, price


# [snippet: outcome]
@dataclass(frozen=True)
class Accepted:
    total: Money
    reference: str
    confirmed: bool


@dataclass(frozen=True)
class Rejected:
    reason: str


type Outcome = Accepted | Rejected


# [/snippet]


# [snippet: checkout]
def checkout(
    request: Request,
    today: date,
    gateway: PaymentGateway,
    inventory: Inventory,
    mailer: Mailer,
) -> Outcome:
    priced = price(request, today)  # the only call into the core
    match inventory.reserve(request.skus):  # s1
        case OutOfStock(sku=sku):
            return Rejected(f"out of stock: {sku}")
        case Reserved():
            pass
    match gateway.charge(priced.total):  # s0
        case Declined(reason=reason):
            return Rejected(f"payment declined: {reason}")
        case Charged(reference=reference):
            confirmed = delivered(mailer.send(request.email, priced.total))  # s2
            return Accepted(priced.total, reference, confirmed)


def delivered(result: SendResult) -> bool:
    match result:
        case Sent():
            return True
        case Bounced():
            return False


# [/snippet]
