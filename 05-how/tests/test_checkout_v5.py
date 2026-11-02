from __future__ import annotations

from datetime import date
from decimal import Decimal

from s01_bits.chaos import Line, Order
from s05_how.checkout_v5 import Accepted, Rejected, checkout
from s05_how.fakes import FakeGateway, FakeInventory, FakeMailer

TODAY = date(2026, 11, 2)


def an_order() -> Order:
    return Order(lines=[Line("book", Decimal(40))], email="a@example.com")


def test_out_of_stock_rejects() -> None:
    inventory = FakeInventory(out_of_stock=True)
    result = checkout(an_order(), TODAY, FakeGateway(), inventory, FakeMailer())
    assert result == Rejected("out of stock: book")


def test_out_of_stock_charges_nothing() -> None:
    gateway = FakeGateway()
    checkout(an_order(), TODAY, gateway, FakeInventory(out_of_stock=True), FakeMailer())
    assert gateway.charged == []


def test_declined_rejects() -> None:
    result = checkout(an_order(), TODAY, FakeGateway(declines=True), FakeInventory(), FakeMailer())
    assert result == Rejected("declined: card refused")


def test_declined_sends_no_mail() -> None:
    mailer = FakeMailer()
    checkout(an_order(), TODAY, FakeGateway(declines=True), FakeInventory(), mailer)
    assert mailer.sent == []


def test_bounce_accepts_unconfirmed() -> None:
    gateway = FakeGateway()
    result = checkout(an_order(), TODAY, gateway, FakeInventory(), FakeMailer(bounces=True))
    assert result == Accepted(gateway.charged[0], confirmed=False)


def test_success_charges_the_total() -> None:
    gateway = FakeGateway()
    result = checkout(an_order(), TODAY, gateway, FakeInventory(), FakeMailer())
    assert result == Accepted(gateway.charged[0], confirmed=True)
