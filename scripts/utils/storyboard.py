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
_ASIDE = re.compile(r"  # .*$")
_HEADERS = ("---", "+++", "@@")


@dataclass(frozen=True)
class BubbleRow:
    step: int
    week: int
    when: str
    actor: str
    words: str
    tag: str = ""


def load_bubbles(path: Path) -> list[BubbleRow]:
    """Read the nine bubbles in file order."""
    with path.open(newline="", encoding="ascii") as fh:
        return [
            BubbleRow(int(r["step"]), int(r["week"]), r["when"], r["actor"], r["words"], r["tag"])
            for r in csv.DictReader(fh)
        ]


def step_lines(source: str, n: int) -> str:
    """Return the checkout at step n: the lines marked at most n, markers stripped."""
    kept: list[str] = []
    for row in source.splitlines():
        found = _MARKER.search(row)
        if found and int(found.group("n")) <= n:
            kept.append(_ASIDE.sub("", _MARKER.sub("", row)))
    return "\n".join(kept)


def step_view(source: str, n: int) -> str:
    """Return the whole checkout at step n under its caption, the lines of step n marked '+ '.

    The caption is 'checkout v{n-1} -> v{n}', or 'checkout v0' for step 0; the other lines
    take two spaces, so each body line keeps its source indentation after the prefix.
    """
    caption = f"checkout v{n - 1} -> v{n}" if n > 0 else "checkout v0"
    body: list[str] = []
    for row in source.splitlines():
        found = _MARKER.search(row)
        if found and int(found.group("n")) <= n:
            mark = "+ " if int(found.group("n")) == n else "  "
            body.append(mark + _ASIDE.sub("", _MARKER.sub("", row)))
    return "\n".join([caption, *body]) + "\n"


def step_diff(source: str, n: int) -> str:
    """Return the unified diff from step n-1 to step n, without file or hunk headers.

    Step 0 diffs from nothing: the skeleton itself.
    """
    before = step_lines(source, n - 1).splitlines() if n > 0 else []
    after = step_lines(source, n).splitlines()
    old = f"step-{n - 1}" if n > 0 else "/dev/null"
    diff = difflib.unified_diff(before, after, fromfile=old, tofile=f"step-{n}", lineterm="")
    body = [line for line in diff if not line.startswith(_HEADERS)]
    return "\n".join(body) + "\n"


def tally_line(n: int, tests: int = 2) -> str:
    """Return the tally over the step view: policies, the paths they double to, the tests."""
    return f"checkout v{n}: {n} policies, {2**n} paths, {tests} tests"


def bubble(row: BubbleRow, labels: Mapping[str, str], width: int = 34) -> str:
    """Return the bubble text: actor label and date, then the words wrapped at width."""
    words = textwrap.fill(row.words, width=width)
    label = f"{row.tag} {labels[row.actor]}" if row.tag else labels[row.actor]
    head = f"{label}, {row.when}" if row.when else label
    return f"{head}\n{words}\n"
