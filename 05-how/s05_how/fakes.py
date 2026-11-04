"""Test doubles for the ports, one bit each, so a shell test can enumerate the world."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from s04_what.money import Money
from s05_how.ports import Bounced, Charged, Declined, OutOfStock, Reserved, Sent


# [snippet: fakes]
@dataclass
class FakeGateway:
    declines: bool = False
    charged: list[Money] = field(default_factory=list)

    def charge(self, amount: Money) -> Charged | Declined:
        if self.declines:
            return Declined("card refused")
        self.charged.append(amount)
        return Charged(reference=f"pay-{len(self.charged)}")


@dataclass
class FakeInventory:
    out_of_stock: bool = False

    def reserve(self, skus: Sequence[str]) -> Reserved | OutOfStock:
        if self.out_of_stock:
            return OutOfStock(sku=skus[0])
        return Reserved()


# [/snippet]
@dataclass
class FakeMailer:
    bounces: bool = False
    sent: list[str] = field(default_factory=list)

    def send(self, email: str, total: Money) -> Sent | Bounced:
        if self.bounces:
            return Bounced()
        self.sent.append(email)
        return Sent()
