from __future__ import annotations

from s05_how.ports import Inventory, OutOfStock, Reserved
from s05_how.warehouse_adapter import WarehouseHttp


def test_reserved_answer_becomes_reserved() -> None:
    """The warehouse's 'reserved' answer reaches the shell as Reserved, nothing else."""
    inventory: Inventory = WarehouseHttp(post=lambda path, body: {"status": "reserved", "id": 7})
    assert inventory.reserve(["book"]) == Reserved()


def test_missing_answer_names_the_sku() -> None:
    """The warehouse's 'missing' answer reaches the shell as OutOfStock naming the sku."""
    missing: dict[str, object] = {"status": "missing", "sku": "pen"}
    inventory: Inventory = WarehouseHttp(post=lambda path, body: missing)
    assert inventory.reserve(["book", "pen"]) == OutOfStock("pen")
