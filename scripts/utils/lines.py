"""The six should-have-known lines: load them and find the ones a section lost."""

from __future__ import annotations

import csv
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

CLOSE = "07-close"


@dataclass(frozen=True)
class Line:
    section: str
    believed: str
    learned: str


def load_lines(path: Path) -> list[Line]:
    with path.open(newline="", encoding="ascii") as fh:
        return [
            Line(row["section"], row["believed"], row["learned"]) for row in csv.DictReader(fh)
        ]


def _squeeze(text: str) -> str:
    return " ".join(text.split())


def missing(lines: list[Line], texts: Mapping[str, str]) -> list[tuple[str, str]]:
    """Return (section, where) for each line absent from its section or from 07-close.

    Runs of whitespace are collapsed before comparing; a section with no text has none.
    """
    out: list[tuple[str, str]] = []
    for line in lines:
        needle = _squeeze(line.learned)
        for where in (line.section, CLOSE):
            if needle not in _squeeze(texts.get(where, "")):
                out.append((line.section, where))
    return out
