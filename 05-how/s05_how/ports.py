"""The seam: what the shell may ask of the world, and the answers it must handle.

Every answer is a sum type: never a boolean, never an exception for a business
outcome. Section 05 draws this seam; section 06 puts code on both sides of it.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from s04_what.money import Money


# [snippet: results]
@dataclass(frozen=True)
class Charged:
    reference: str


@dataclass(frozen=True)
class Declined:
    reason: str


@dataclass(frozen=True)
class Reserved:
    pass


@dataclass(frozen=True)
class OutOfStock:
    sku: str


@dataclass(frozen=True)
class Sent:
    pass


@dataclass(frozen=True)
class Bounced:
    pass


# [/snippet]


# [snippet: types]
type ChargeResult = Charged | Declined
type ReserveResult = Reserved | OutOfStock
type SendResult = Sent | Bounced
# [/snippet]


# [snippet: ports]
class PaymentGateway(Protocol):
    def charge(self, amount: Money) -> ChargeResult: ...


class Inventory(Protocol):
    def reserve(self, skus: Sequence[str]) -> ReserveResult: ...


class Mailer(Protocol):
    def send(self, email: str, total: Money) -> SendResult: ...


# [/snippet]
