"""The staged checkouts: the fix and the three-context version give the same totals."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import date
from decimal import Decimal

import pytest

from s01_bits.chaos import Charge, Line, Order, Reserve, Send, checkout
from s04_what.checkout_fixed import checkout as checkout_fixed
from s04_what.checkout_v4 import checkout as checkout_v4

TODAY = date(2026, 11, 5)

type Checkout = Callable[[Order, date, Charge, Reserve, Send], Decimal]


def charge(amount: Decimal) -> None:
    """The payment provider, doing nothing."""


def reserve(lines: Sequence[Line]) -> None:
    """The warehouse, doing nothing."""


def send(email: str, total: Decimal) -> None:
    """The mail server, doing nothing."""


def regular() -> Order:
    return Order(lines=[Line("book", Decimal(40))], email="a@example.com")


def everything() -> Order:
    return Order(
        lines=[Line("book", Decimal(60)), Line("pen", Decimal(40))],
        email="a@example.com",
        coupon_valid_until=TODAY,
        member=True,
        international=True,
        gift_wrap=True,
        vat_id="BG123456789",
    )


def i1() -> Order:
    return Order(
        lines=[Line("book", Decimal(55))],
        email="a@example.com",
        coupon_valid_until=TODAY,
    )


STAGES = [pytest.param(checkout_fixed, id="fixed"), pytest.param(checkout_v4, id="v4")]


# [snippet: i1]
@pytest.mark.parametrize("stage", STAGES)
def test_i1_example_pays_shipping(stage: Checkout) -> None:
    """The I1 order, 55 EUR with the coupon: 45 of goods pays 5 EUR postage,
    logistics' rule; with VAT 60.00."""
    assert stage(i1(), TODAY, charge, reserve, send) == Decimal("60.00")


# [/snippet]


@pytest.mark.parametrize("stage", STAGES)
def test_regular_order_agrees_with_chaos(stage: Checkout) -> None:
    assert stage(regular(), TODAY, charge, reserve, send) == checkout(
        regular(), TODAY, charge, reserve, send
    )


@pytest.mark.parametrize("stage", STAGES)
def test_order_with_everything_agrees_with_chaos(stage: Checkout) -> None:
    assert stage(everything(), TODAY, charge, reserve, send) == checkout(
        everything(), TODAY, charge, reserve, send
    )
