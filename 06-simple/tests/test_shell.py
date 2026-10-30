"""Eight world configurations, four outcomes, and no money moves when the stock is gone."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from s05_how.fakes import FakeGateway, FakeInventory, FakeMailer
from s06_simple.core import Request
from s06_simple.shell import Accepted, Rejected, checkout
from scripts.utils.examples import example_names, missing_tests

EXAMPLES = Path(__file__).resolve().parents[2] / "data" / "examples.csv"
PLAIN_TOTAL = Decimal("30.00")  # (20 + 5) * 1.20


# [snippet: eight]
@pytest.mark.parametrize("bits", range(8), ids=lambda b: f"{b:03b}")
def test_every_shell_configuration(bits: int, plain: Request, today: date) -> None:
    gateway = FakeGateway(declines=bool(bits & 0b001))  # s0
    inventory = FakeInventory(out_of_stock=bool(bits & 0b010))  # s1
    mailer = FakeMailer(bounces=bool(bits & 0b100))  # s2
    outcome = checkout(plain, today, gateway, inventory, mailer)
    if inventory.out_of_stock:
        assert outcome == Rejected("out of stock: book")
        assert gateway.charged == []  # nothing moves for a parcel that does not exist
    elif gateway.declines:
        assert outcome == Rejected("payment declined: card refused")
        assert mailer.sent == []
    else:
        assert outcome == Accepted(PLAIN_TOTAL, "pay-1", confirmed=not mailer.bounces)


# [/snippet]


def test_every_shell_example_has_a_test() -> None:
    assert missing_tests(example_names(EXAMPLES, scope="shell"), globals()) == []


# [snippet: wound-i3]
def test_out_of_stock_rejects_before_payment(plain: Request, today: date) -> None:
    gateway = FakeGateway()
    outcome = checkout(plain, today, gateway, FakeInventory(out_of_stock=True), FakeMailer())
    assert outcome == Rejected("out of stock: book")
    assert gateway.charged == []


# [/snippet]


def test_declined_payment_rejects(plain: Request, today: date) -> None:
    mailer = FakeMailer()
    outcome = checkout(plain, today, FakeGateway(declines=True), FakeInventory(), mailer)
    assert outcome == Rejected("payment declined: card refused")
    assert mailer.sent == []


def test_bounced_mail_still_accepts(plain: Request, today: date) -> None:
    outcome = checkout(plain, today, FakeGateway(), FakeInventory(), FakeMailer(bounces=True))
    assert outcome == Accepted(PLAIN_TOTAL, "pay-1", confirmed=False)


def test_happy_path_accepts(plain: Request, today: date) -> None:
    outcome = checkout(plain, today, FakeGateway(), FakeInventory(), FakeMailer())
    assert outcome == Accepted(PLAIN_TOTAL, "pay-1", confirmed=True)
