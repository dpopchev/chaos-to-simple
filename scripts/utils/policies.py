"""The policies table: each provider's answer beside the shop's decision, Fulfilment the owner."""

from __future__ import annotations

import textwrap
from collections.abc import Callable, Sequence

from scripts.utils.palette import label_of
from scripts.utils.paths import CastRow, Rule
from scripts.utils.retro import Question

COLUMNS = ("provider", "answers", "the shop decides", "owner")
# A story role, not an actor of data/actors.csv: written as is, never looked up.
OWNER = "Fulfilment"
# Column widths: 16 + 30 + 34 + 10 plus three gaps of 2 is 96, under the 100-column limit.
WIDTHS = (16, 30, 34, 10)
GAP = "  "


def _row(cells: Sequence[str], widths: Sequence[int]) -> list[str]:
    """Wrap each cell to its width and join the wrapped lines side by side."""
    wrapped = [
        textwrap.wrap(cell, width) or [""] for cell, width in zip(cells, widths, strict=True)
    ]
    height = max(len(lines) for lines in wrapped)
    return [
        GAP.join(
            (lines[i] if i < len(lines) else "").ljust(width)
            for lines, width in zip(wrapped, widths, strict=True)
        ).rstrip()
        for i in range(height)
    ]


def _shop_decides(decision: str) -> str:
    """Return the part of a decision after its semicolon, its first letter capitalised."""
    text = decision.partition(";")[2].strip()
    return text[:1].upper() + text[1:]


def policies_table(
    rules: Sequence[Rule],
    questions: Sequence[Question],
    cast: Sequence[CastRow],
    label: Callable[[str], str] = label_of,
) -> str:
    """Return the table of provider, answer, shop's decision and owner, one row per shell rule.

    The owner is the literal Fulfilment. A shell rule's provider is the actor its cast row
    names; its decision is the one of the question raised on the same bit.
    """
    provider = {c.bit: c.requested_by for c in cast}
    decision = {q.bit: q.decision for q in questions}
    lines = _row(COLUMNS, WIDTHS)
    for rule in rules:
        if rule.scope != "shell":
            continue
        cells = (
            label(provider[rule.bit]),
            rule.rule,
            _shop_decides(decision[rule.bit]),
            OWNER,
        )
        lines += _row(cells, WIDTHS)
    return "\n".join(lines) + "\n"
