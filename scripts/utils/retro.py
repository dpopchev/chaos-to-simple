"""The retro table: the questions the room raised, each with the decision that closed it."""

from __future__ import annotations

import csv
import re
import textwrap
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils.palette import label_of

COLUMNS = ("id", "question", "who", "decided")
# Column widths for the deck frame: 2 + 35 + 15 + 46 plus three gaps of 2 is 104.
QUESTION_WIDTH = 35
WHO_WIDTH = 15
DECIDED_WIDTH = 46
GAP = "  "


@dataclass(frozen=True)
class Question:
    id: str
    question: str
    raised_by: str
    bit: str
    status: str
    decision: str


def load_questions(path: Path) -> list[Question]:
    """Read the questions in file order."""
    with path.open(newline="", encoding="ascii") as fh:
        return [
            Question(
                row["id"],
                row["question"],
                row["raised_by"],
                row["bit"],
                row["status"],
                row["decision"],
            )
            for row in csv.DictReader(fh)
        ]


def _wrap(cell: str, width: int) -> list[str]:
    """Wrap a cell, breaking at a clause end (. ; :) before breaking inside a clause."""
    lines: list[str] = []
    current = ""
    for clause in re.split(r"(?<=[.;:]) ", cell):
        if current and len(current) + 1 + len(clause) <= width:
            current = f"{current} {clause}"
            continue
        lines += [current] if current else []
        pieces = textwrap.wrap(clause, width) or [""]
        lines += pieces[:-1]
        current = pieces[-1]
    return [*lines, current]


def _row(cells: Sequence[str], widths: Sequence[int]) -> list[str]:
    """Wrap each cell to its width and join the wrapped lines side by side."""
    wrapped = [_wrap(cell, width) for cell, width in zip(cells, widths, strict=True)]
    height = max(len(lines) for lines in wrapped)
    return [
        GAP.join(
            (lines[i] if i < len(lines) else "").ljust(width)
            for lines, width in zip(wrapped, widths, strict=True)
        ).rstrip()
        for i in range(height)
    ]


def retro_table(questions: Sequence[Question], label: Callable[[str], str] = label_of) -> str:
    """The table of id, question, who raised it and what was decided; long cells wrap."""
    widths = (2, QUESTION_WIDTH, WHO_WIDTH, DECIDED_WIDTH)
    lines = _row(COLUMNS, widths)
    for q in questions:
        lines += _row((q.id, q.question, label(q.raised_by), q.decision), widths)
    return "\n".join(lines) + "\n"
