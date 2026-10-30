from __future__ import annotations

from decimal import Decimal

from s04_what.money import bgn
from s04_what.tax import VatId, total_with_vat


def test_vat_without_id() -> None:
    assert total_with_vat(bgn(45), None) == Decimal("54.00")


def test_vat_exempt_with_id() -> None:
    assert total_with_vat(bgn(45), VatId("BG123456789")) == Decimal("45.00")
