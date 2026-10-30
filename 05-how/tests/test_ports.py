from __future__ import annotations

from s04_what.money import bgn
from s05_how.fakes import FakeGateway, FakeInventory, FakeMailer
from s05_how.ports import (
    Bounced,
    Charged,
    Declined,
    Inventory,
    Mailer,
    OutOfStock,
    PaymentGateway,
    Reserved,
    Sent,
)


def test_fakes_satisfy_the_ports() -> None:
    gateway: PaymentGateway = FakeGateway()
    inventory: Inventory = FakeInventory()
    mailer: Mailer = FakeMailer()
    assert gateway.charge(bgn(10)) == Charged("pay-1")
    assert inventory.reserve(["book"]) == Reserved()
    assert mailer.send("a@example.com", bgn(10)) == Sent()


def test_fakes_answer_with_the_other_half() -> None:
    assert FakeGateway(declines=True).charge(bgn(10)) == Declined("card refused")
    assert FakeInventory(out_of_stock=True).reserve(["book"]) == OutOfStock("book")
    assert FakeMailer(bounces=True).send("a@example.com", bgn(10)) == Bounced()
