"""Eight world configurations, four outcomes, and no money moves when the stock is gone."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from s05_how.fakes import FakeGateway, FakeInventory, FakeMailer
from s06_simple.core import Request
from s06_simple.shell import Accepted, Rejected, checkout
from s06_simple.worlds import world
from scripts.utils.examples import example_names, missing_tests

EXAMPLES = Path(__file__).resolve().parents[2] / "data" / "examples.csv"
PLAIN_TOTAL = Decimal("30.00")
"""The plain order: 20 of goods plus 5 postage, with 20% VAT."""


OUT_OF_STOCK = [b for b in range(8) if b & 0b010]
DECLINED = [b for b in range(8) if b & 0b001 and not b & 0b010]
ACCEPTED = [b for b in range(8) if not b & 0b011]


def ids(bits: int) -> str:
    return f"{bits:03b}"


@pytest.mark.parametrize("bits", OUT_OF_STOCK, ids=ids)
class TestOutOfStock:
    def test_rejects(self, bits: int, plain: Request, today: date) -> None:
        outcome = checkout(plain, today, *world(bits))
        assert outcome == Rejected("out of stock: book")

    def test_charges_nothing(self, bits: int, plain: Request, today: date) -> None:
        """Nothing moves for a parcel that does not exist."""
        gateway, inventory, mailer = world(bits)
        checkout(plain, today, gateway, inventory, mailer)
        assert gateway.charged == []


@pytest.mark.parametrize("bits", DECLINED, ids=ids)
class TestDeclined:
    def test_rejects(self, bits: int, plain: Request, today: date) -> None:
        outcome = checkout(plain, today, *world(bits))
        assert outcome == Rejected("declined: card refused")

    def test_sends_no_mail(self, bits: int, plain: Request, today: date) -> None:
        gateway, inventory, mailer = world(bits)
        checkout(plain, today, gateway, inventory, mailer)
        assert mailer.sent == []


@pytest.mark.parametrize("bits", ACCEPTED, ids=ids)
class TestAccepted:
    def test_accepts_and_confirms_unless_the_mail_bounces(
        self, bits: int, plain: Request, today: date
    ) -> None:
        gateway, inventory, mailer = world(bits)
        outcome = checkout(plain, today, gateway, inventory, mailer)
        assert outcome == Accepted(PLAIN_TOTAL, confirmed=not mailer.bounces)


def test_every_shell_example_has_a_test() -> None:
    assert missing_tests(example_names(EXAMPLES, scope="shell"), globals()) == []


# [snippet: wound-i3]
class TestOutOfStockRejectsBeforePayment:
    @pytest.fixture
    def gateway(self) -> FakeGateway:
        return FakeGateway()

    @pytest.fixture
    def outcome(self, gateway: FakeGateway, plain: Request, today: date) -> object:
        return checkout(plain, today, gateway, FakeInventory(out_of_stock=True), FakeMailer())

    def test_rejected(self, outcome: object) -> None:
        assert outcome == Rejected("out of stock: book")

    def test_nothing_charged(self, outcome: object, gateway: FakeGateway) -> None:
        assert gateway.charged == []


# [/snippet]


class TestDeclinedPaymentRejects:
    @pytest.fixture
    def mailer(self) -> FakeMailer:
        return FakeMailer()

    @pytest.fixture
    def outcome(self, mailer: FakeMailer, plain: Request, today: date) -> object:
        return checkout(plain, today, FakeGateway(declines=True), FakeInventory(), mailer)

    def test_rejected(self, outcome: object) -> None:
        assert outcome == Rejected("declined: card refused")

    def test_no_mail_sent(self, outcome: object, mailer: FakeMailer) -> None:
        assert mailer.sent == []


def test_bounced_mail_still_accepts(plain: Request, today: date) -> None:
    outcome = checkout(plain, today, FakeGateway(), FakeInventory(), FakeMailer(bounces=True))
    assert outcome == Accepted(PLAIN_TOTAL, confirmed=False)


def test_happy_path_accepts(plain: Request, today: date) -> None:
    outcome = checkout(plain, today, FakeGateway(), FakeInventory(), FakeMailer())
    assert outcome == Accepted(PLAIN_TOTAL, confirmed=True)
