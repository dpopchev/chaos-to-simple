from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from s01_bits.chaos import Line, Order
from s04_what.checkout_v4 import checkout

TODAY = date(2026, 11, 2)


@pytest.mark.xfail(strict=True, reason="I3: v4 charges before it reserves")
# [snippet: i3]
def test_reserve_comes_before_charge() -> None:
    calls: list[str] = []
    order = Order(lines=[Line("book", Decimal(40))], email="a@example.com")
    checkout(
        order,
        TODAY,
        charge=lambda total: calls.append("charge"),
        reserve=lambda lines: calls.append("reserve"),
        send=lambda email, total: None,
    )
    assert calls == ["reserve", "charge"]


# [/snippet]
