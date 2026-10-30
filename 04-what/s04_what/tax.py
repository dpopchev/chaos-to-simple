"""Tax context: VAT. Bit b5."""

from __future__ import annotations

from decimal import Decimal
from typing import NewType

from s04_what.money import Money, rounded

VatId = NewType("VatId", str)
VAT_FACTOR = Decimal("1.20")


# [snippet: vat]
def total_with_vat(net: Money, vat_id: VatId | None) -> Money:
    if vat_id is None:  # b5
        return rounded(net * VAT_FACTOR)
    return rounded(net)


# [/snippet]
