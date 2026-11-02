"""Money as a value: a Decimal with a name and two helpers, nothing more."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

type Money = Decimal

CENT = Decimal("0.01")


def eur(amount: int | str) -> Money:
    return Decimal(amount)


def rounded(amount: Money) -> Money:
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)
