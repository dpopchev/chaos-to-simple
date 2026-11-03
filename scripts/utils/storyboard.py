"""The storyboard of section 01: the checkout at each step, its diffs and the bubbles."""

from __future__ import annotations

import csv
import difflib
import re
import textwrap
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from scripts.utils.stagediff import compact_body

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
    """Return the compact diff v{n-1} -> v{n} under its caption; step 0 is the whole skeleton.

    The caption is 'checkout v{n-1} -> v{n}' or 'checkout v0'; the body is stagediff's
    compact_body: one context line, '---' between hunks, '+' and '-' lines only.
    """
    if n == 0:
        return "\n".join(["checkout v0", *step_lines(source, 0).splitlines()]) + "\n"
    before = step_lines(source, n - 1).splitlines(keepends=True)
    after = step_lines(source, n).splitlines(keepends=True)
    body = compact_body(before, after)
    return "".join([f"checkout v{n - 1} -> v{n}\n", *(row.rstrip("\n") + "\n" for row in body)])


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


def tally_line(n: int, tests: int = 2, lines: int | None = None) -> str:
    """Return the tally: policies, the paths they double to, the tests, then the length if given."""
    tally = f"checkout v{n}: {n} policies, {2**n} paths, {tests} tests"
    return tally if lines is None else f"{tally}, {lines} lines"


def code_length(source: str, n: int) -> int:
    """Return the non-blank line count of the checkout at step n."""
    return sum(1 for row in step_lines(source, n).splitlines() if row.strip())


def bubble(row: BubbleRow, labels: Mapping[str, str], width: int = 34) -> str:
    """Return the bubble text: actor label and date, then the words wrapped at width."""
    words = textwrap.fill(row.words, width=width)
    label = f"{row.tag} {labels[row.actor]}" if row.tag else labels[row.actor]
    head = f"{label}, {row.when}" if row.when else label
    return f"{head}\n{words}\n"
