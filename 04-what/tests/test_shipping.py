from __future__ import annotations

from s04_what.money import eur
from s04_what.shipping import Zone, shipping_fee


def test_free_shipping_after_discount() -> None:
    assert shipping_fee(eur(45), Zone.DOMESTIC, gift_wrap=False) == 5


def test_free_shipping_at_threshold() -> None:
    assert shipping_fee(eur(50), Zone.DOMESTIC, gift_wrap=False) == 0


def test_international_zone() -> None:
    assert shipping_fee(eur(20), Zone.INTERNATIONAL, gift_wrap=False) == 20


def test_gift_wrap_on_free_shipping() -> None:
    assert shipping_fee(eur(100), Zone.DOMESTIC, gift_wrap=True) == 3
