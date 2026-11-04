"""The warehouse adapter: its answer format stops here, the shell sees Reserved | OutOfStock."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from s05_how.ports import OutOfStock, Reserved, ReserveResult


class UnknownWarehouseAnswerError(ValueError):
    """The warehouse answered with a status this adapter does not know."""


# [snippet: adapter]
@dataclass(frozen=True)
class WarehouseHttp:
    post: Callable[[str, dict[str, object]], dict[str, object]]

    def reserve(self, skus: Sequence[str]) -> ReserveResult:
        answer = self.post("/reservations", {"skus": list(skus), "hold_minutes": 15})
        match answer["status"]:
            case "reserved":
                return Reserved()
            case "missing":
                return OutOfStock(str(answer["sku"]))
            case other:
                raise UnknownWarehouseAnswerError(f"warehouse status {other!r}")


# [/snippet]
