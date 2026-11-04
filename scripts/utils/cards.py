"""The evidence cards: each incident as agreed example, customer outcome and passing check."""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Example:
    """An agreed example of data/examples.csv."""

    bit: str
    name: str
    given: str
    then: str


@dataclass(frozen=True)
class Closure:
    """The columns of an incident that a card reads."""

    closed_by: str
    decision: str
    bit: str


def read_text(path: Path) -> str:
    """Return a file's text; a missing file raises naming the path."""
    return path.read_text(encoding="ascii")


def write_text(path: Path, text: str) -> None:
    """Write a file's text, creating its folder."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii")


def parse_closures(text: str) -> tuple[Closure, ...]:
    """Return the incidents of a csv text in order."""
    rows = csv.DictReader(io.StringIO(text))
    return tuple(Closure(r["closed_by"], r["decision"], r["bit"]) for r in rows)


def parse_examples(text: str) -> tuple[Example, ...]:
    """Return the examples of a csv text in order."""
    rows = csv.DictReader(io.StringIO(text))
    return tuple(Example(r["bit"], r["name"], r["given"], r["then"]) for r in rows)


def is_test(closed_by: str) -> bool:
    """Tell a test name (test_x or TestX) from a decision reference."""
    return closed_by.startswith(("test_", "Test"))


def example_name(closed_by: str) -> str:
    """Return the example name a test name stands for: test_a_b and TestAB give a_b."""
    if closed_by.startswith("test_"):
        return closed_by.removeprefix("test_")
    words = re.findall(r"[A-Z][a-z0-9]*", closed_by.removeprefix("Test"))
    return "_".join(w.lower() for w in words)


def _example_of(closure: Closure, examples: tuple[Example, ...]) -> Example:
    """Return the example of the closure: by name for a test, else the first of its bit."""
    wanted = example_name(closure.closed_by) if is_test(closure.closed_by) else None
    for example in examples:
        if example.bit == closure.bit and wanted in (None, example.name):
            return example
    raise ValueError(f"no agreed example for {closure.closed_by} on bit {closure.bit}")


def _sentence(decision: str) -> str:
    """Return the decision up to its first comma, its first letter capitalised."""
    head = decision.partition(",")[0].strip()
    return head[:1].upper() + head[1:]


def _last_line(closure: Closure, wounds: str) -> str:
    """Return the check line, confirmed against the PASSED lines; a missing one raises."""
    if not is_test(closure.closed_by):
        return f"decided: {closure.closed_by}, {_sentence(closure.decision)}"
    passed = [row for row in wounds.splitlines() if row.startswith("PASSED")]
    if not any(f"::{closure.closed_by}" in row for row in passed):
        raise ValueError(f"no PASSED line for {closure.closed_by}")
    return f"check: {closure.closed_by} PASSED"


def cards_text(incidents: str, examples: str, wounds: str) -> str:
    """Return one three-line card per incident, cards apart by a blank line.

    Raises ValueError for a test with no agreed example or no PASSED line.
    """
    found = parse_examples(examples)
    cards = []
    for closure in parse_closures(incidents):
        example = _example_of(closure, found)
        cards.append(
            "\n".join(
                (
                    f"agreed example: {example.given} -> {example.then}",
                    f"customer outcome: {closure.decision}",
                    _last_line(closure, wounds),
                )
            )
        )
    return "\n\n".join(cards) + "\n"
