"""The other payment provider fits the same port: the shell stays as it is."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from s05_how.fakes import FakeInventory, FakeMailer
from s06_simple.core import Request
from s06_simple.other_gateway import OtherGateway
from s06_simple.shell import Accepted, Rejected, checkout

PLAIN_TOTAL = Decimal("30.00")


def test_the_shell_accepts_the_plain_order_through_the_other_gateway(
    plain: Request, today: date
) -> None:
    """The plain order is accepted when the other provider answers ok."""
    gateway = OtherGateway(post=lambda path, body: {"ok": True, "id": "ch_1"})
    outcome = checkout(plain, today, gateway, FakeInventory(), FakeMailer())
    assert outcome == Accepted(PLAIN_TOTAL, confirmed=True)


def test_its_decline_rejects_the_order(plain: Request, today: date) -> None:
    """The other provider's refusal reaches the shell as a declined rejection."""
    gateway = OtherGateway(post=lambda path, body: {"ok": False, "error": "card refused"})
    outcome = checkout(plain, today, gateway, FakeInventory(), FakeMailer())
    assert outcome == Rejected("declined: card refused")
