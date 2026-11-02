"""The grid's tested.csv rows are the paths the exhibit orders take through the code.

path_bits reads the six conditions of s01_bits.chaos.checkout off an order, b5 to b0.
"""

from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from s01_bits.chaos import Line, Order

TODAY = date(2026, 11, 5)
TESTED = Path(__file__).resolve().parents[1] / "data" / "tested.csv"


def path_bits(order: Order, today: date) -> str:
    """The six conditions as 0 and 1, left b5 to right b0."""
    goods = sum((line.price * line.qty for line in order.lines), Decimal(0))
    conditions = (
        order.vat_id is not None,
        order.gift_wrap,
        order.international,
        goods >= Decimal(50),
        order.member,
        order.coupon_valid_until is not None and order.coupon_valid_until >= today,
    )
    return "".join("1" if c else "0" for c in conditions)


def bits_of(name: str) -> str:
    """The bits column of the tested.csv row named name."""
    with TESTED.open(newline="") as handle:
        return next(row["bits"] for row in csv.DictReader(handle) if row["name"] == name)


def test_the_bug_row_is_the_i1_order_in_code_bits() -> None:
    order = Order(
        lines=[Line("book", Decimal(55))], email="a@example.com", coupon_valid_until=TODAY
    )
    assert path_bits(order, TODAY) == bits_of("test_free_shipping_after_discount")


def test_the_all_ones_row_is_the_order_with_everything() -> None:
    order = Order(
        lines=[Line("book", Decimal(60)), Line("pen", Decimal(40))],
        email="a@example.com",
        coupon_valid_until=TODAY,
        member=True,
        international=True,
        gift_wrap=True,
        vat_id="BG123456789",
    )
    assert path_bits(order, TODAY) == bits_of("test_order_with_everything")
