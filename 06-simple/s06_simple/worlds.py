"""The eight shell worlds, measured by running the shell: bits, outcome, charged, mailed.

python -m s06_simple.worlds --out build/06-simple/worlds.txt
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from s04_what.money import bgn
from s04_what.shipping import Zone
from s05_how.fakes import FakeGateway, FakeInventory, FakeMailer
from s06_simple.core import Request
from s06_simple.shell import Accepted, Outcome, Rejected, checkout


# [snippet: eight]
def world(bits: int) -> tuple[FakeGateway, FakeInventory, FakeMailer]:
    return (
        FakeGateway(declines=bool(bits & 0b001)),  # s0
        FakeInventory(out_of_stock=bool(bits & 0b010)),  # s1
        FakeMailer(bounces=bool(bits & 0b100)),  # s2
    )


# [/snippet]


@dataclass(frozen=True)
class WorldRow:
    bits: int
    outcome: str
    charged: bool
    mailed: bool


def describe(outcome: Outcome) -> str:
    match outcome:
        case Rejected(reason=reason):
            return f"Rejected: {reason}"
        case Accepted(confirmed=True):
            return "Accepted, confirmed"
        case Accepted():
            return "Accepted, not confirmed"


def rows(request: Request, today: date) -> tuple[WorldRow, ...]:
    """Run the shell against each of the eight worlds and record what happened."""
    measured: list[WorldRow] = []
    for bits in range(8):
        gateway, inventory, mailer = world(bits)
        outcome = checkout(request, today, gateway, inventory, mailer)
        measured.append(WorldRow(bits, describe(outcome), bool(gateway.charged), bool(mailer.sent)))
    return tuple(measured)


def table(measured: Sequence[WorldRow]) -> str:
    """Render the rows as four aligned columns under a header line."""
    width = max(len(row.outcome) for row in measured)

    def line(bits: str, outcome: str, charged: str, mailed: str) -> str:
        return f"{bits:<4} {outcome:<{width}} {charged:<7} {mailed}"

    yes_no = {True: "yes", False: "no"}
    body = [
        line(f"{row.bits:03b}", row.outcome, yes_no[row.charged], yes_no[row.mailed])
        for row in measured
    ]
    return "\n".join([line("bits", "outcome", "charged", "mailed"), *body]) + "\n"


def plain_request() -> Request:
    return Request(
        skus=("book",),
        goods=bgn(20),
        email="a@example.com",
        coupon=None,
        member=False,
        zone=Zone.DOMESTIC,
        gift_wrap=False,
        vat_id=None,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="worlds.txt to write")
    args = parser.parse_args(argv)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(table(rows(plain_request(), date(2026, 11, 5))), encoding="ascii")
    sys.stdout.write(f"worlds.txt: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
