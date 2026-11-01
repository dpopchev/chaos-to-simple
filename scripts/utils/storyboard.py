"""The storyboard of section 01: the checkout at each step, its diffs and the bubbles."""

from __future__ import annotations

import csv
import difflib
import re
import textwrap
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

STEPS = 7

_MARKER = re.compile(r"\s*# \[step: (?P<n>\d)\]\s*$")


@dataclass(frozen=True)
class BubbleRow:
    step: int
    week: int
    when: str
    actor: str
    words: str


def load_bubbles(path: Path) -> list[BubbleRow]:
    """Read the nine bubbles in file order."""
    with path.open(newline="", encoding="ascii") as fh:
        return [
            BubbleRow(int(r["step"]), int(r["week"]), r["when"], r["actor"], r["words"])
            for r in csv.DictReader(fh)
        ]


def step_lines(source: str, n: int) -> str:
    """Return the checkout at step n: the lines marked at most n, markers stripped."""
    kept: list[str] = []
    for row in source.splitlines():
        found = _MARKER.search(row)
        if found and int(found.group("n")) <= n:
            kept.append(_MARKER.sub("", row))
    return "\n".join(kept)


def step_diff(source: str, n: int) -> str:
    """Return the unified diff from step n-1 to step n, headers without a timestamp.

    Step 0 diffs from nothing: the skeleton itself.
    """
    before = step_lines(source, n - 1).splitlines() if n > 0 else []
    after = step_lines(source, n).splitlines()
    old = f"step-{n - 1}" if n > 0 else "/dev/null"
    diff = difflib.unified_diff(before, after, fromfile=old, tofile=f"step-{n}", lineterm="")
    return "\n".join(diff) + "\n"


def bubble(row: BubbleRow, labels: Mapping[str, str], width: int = 34) -> str:
    """Return the bubble text: actor label and date, then the words wrapped at width."""
    words = textwrap.fill(row.words, width=width)
    return f"{labels[row.actor]}, {row.when}\n{words}\n"
