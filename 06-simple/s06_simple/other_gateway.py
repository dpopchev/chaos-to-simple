"""The other payment provider: its answer format stops here, the shell sees Charged | Declined."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from s04_what.money import Money
from s05_how.ports import Charged, ChargeResult, Declined


class UnknownGatewayAnswerError(ValueError):
    """The other provider answered with an ok flag this adapter does not know."""


# [snippet: gateway]
@dataclass(frozen=True)
class OtherGateway:
    post: Callable[[str, dict[str, object]], dict[str, object]]

    def charge(self, amount: Money) -> ChargeResult:
        cents = int((amount * 100).to_integral_value())
        answer = self.post("/charges", {"amount_cents": cents, "currency": "EUR"})
        match answer["ok"]:
            case True:
                return Charged(reference=str(answer["id"]))
            case False:
                return Declined(reason=str(answer["error"]))
            case other:
                raise UnknownGatewayAnswerError(f"gateway ok {other!r}")


# [/snippet]
