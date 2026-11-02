"""Fixtures shared by the tests of this section: one plain request, every flag off."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import date
from typing import Any

import pytest

from s04_what.money import eur
from s04_what.shipping import Zone
from s06_simple.core import Request

PLAIN = Request(
    skus=("book",),
    goods=eur(20),
    email="a@example.com",
    coupon=None,
    member=False,
    zone=Zone.DOMESTIC,
    gift_wrap=False,
    vat_id=None,
)


@pytest.fixture
def today() -> date:
    return date(2026, 11, 5)


@pytest.fixture
def plain() -> Request:
    return PLAIN


@pytest.fixture
def order() -> Callable[..., Request]:
    """The plain request with some fields changed: order(goods=eur(60), member=True)."""

    def make(**changes: Any) -> Request:
        return replace(PLAIN, **changes)

    return make
