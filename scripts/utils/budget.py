"""The frame budget: frames and minutes per section, compared with what each index holds."""

from __future__ import annotations

import csv
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Budget:
    section: str
    frames: int
    minutes: int


def load_budget(path: Path) -> list[Budget]:
    with path.open(newline="", encoding="ascii") as fh:
        return [
            Budget(row["section"], int(row["frames"]), int(row["minutes"]))
            for row in csv.DictReader(fh)
        ]


def frames_of(index_text: str) -> int:
    """Count the frames of an index: the lines that start with two hashes and a space."""
    return sum(1 for line in index_text.splitlines() if line.startswith("## "))


def compare(budget: list[Budget], counts: Mapping[str, int]) -> list[tuple[str, int, int]]:
    """Return (section, budgeted, counted) for each section whose count differs.

    A section with no entry in counts is counted as zero frames.
    """
    return [
        (item.section, item.frames, counts.get(item.section, 0))
        for item in budget
        if counts.get(item.section, 0) != item.frames
    ]


def minutes_total(budget: list[Budget]) -> int:
    return sum(item.minutes for item in budget)
