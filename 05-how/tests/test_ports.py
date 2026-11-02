from __future__ import annotations

from s04_what.money import eur
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


def test_fake_gateway_satisfies_the_port() -> None:
    gateway: PaymentGateway = FakeGateway()
    assert gateway.charge(eur(10)) == Charged("pay-1")


def test_fake_inventory_satisfies_the_port() -> None:
    inventory: Inventory = FakeInventory()
    assert inventory.reserve(["book"]) == Reserved()


def test_fake_mailer_satisfies_the_port() -> None:
    mailer: Mailer = FakeMailer()
    assert mailer.send("a@example.com", eur(10)) == Sent()


def test_fake_gateway_declines() -> None:
    assert FakeGateway(declines=True).charge(eur(10)) == Declined("card refused")


def test_fake_inventory_runs_out() -> None:
    assert FakeInventory(out_of_stock=True).reserve(["book"]) == OutOfStock("book")


def test_fake_mailer_bounces() -> None:
    assert FakeMailer(bounces=True).send("a@example.com", eur(10)) == Bounced()
