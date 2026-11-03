"""The storyboard of section 01: the checkout at each step, its diffs and the bubbles."""

from __future__ import annotations

import csv
import difflib
import re
import textwrap
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

from scripts.utils.board import TEST_FUNCTION
from scripts.utils.stagediff import compact_body

STEPS = 7
TODAY = date(2026, 11, 5)
CENT = Decimal("0.01")

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


def tally_line(
    version: int, policies: int, paths: int, tests: int, lines: int | None = None
) -> str:
    """Return the tally: policies, paths and tests of a version, then the length if given."""
    tally = f"checkout v{version}: {policies} policies, {paths} paths, {tests} tests"
    return tally if lines is None else f"{tally}, {lines} lines"


def count_tests(texts: Iterable[str]) -> int:
    """Return how many distinct test functions and classes the test file texts define."""
    found = (name for text in texts for pair in TEST_FUNCTION.findall(text) for name in pair)
    return len({name for name in found if name})


def code_length(source: str, n: int) -> int:
    """Return the non-blank line count of the checkout at step n."""
    return sum(1 for row in step_lines(source, n).splitlines() if row.strip())


def _order_fields(n: int) -> list[str]:
    """Return the Order keyword lines of the everything test at step n."""
    table = [
        (1, "coupon_valid_until=TODAY"),
        (2, "member=True"),
        (4, "international=True"),
        (5, "gift_wrap=True"),
        (6, 'vat_id="BG123456789"'),
    ]
    return [f"        {field}," for step, field in table if step <= n]


def run_checkout(source: str, n: int, everything: bool = True) -> Decimal:
    """Exec the step-n checkout and return its total (the one effect).

    The order is the two-line order with everything up to step n, or the regular one-line order.
    """
    from s01_bits import chaos  # 01-bits is on the path only under pytest

    if everything:
        fields = {
            "coupon_valid_until": TODAY if n >= 1 else None,
            "member": n >= 2,
            "international": n >= 4,
            "gift_wrap": n >= 5,
            "vat_id": "BG123456789" if n >= 6 else None,
        }
        lines = [chaos.Line("book", Decimal(60)), chaos.Line("pen", Decimal(40))]
    else:
        fields = {}
        lines = [chaos.Line("book", Decimal(40))]
    order = chaos.Order(lines=lines, email="a@example.com", **fields)
    namespace = dict(vars(chaos))
    exec(step_lines(source, n), namespace)
    return namespace["checkout"](order, TODAY, lambda _: None, lambda _: None, lambda *_: None)


def step_test(source: str, n: int) -> str:
    """Return the two tests as they stood at step n, without the narrator comments.

    Both expected totals are computed by running the step-n checkout.
    """
    expected = run_checkout(source, n).quantize(CENT)
    regular = run_checkout(source, n, everything=False).quantize(CENT)
    head = [
        "def test_regular_order() -> None:",
        '    order = Order(lines=[Line("book", Decimal(40))], email="a@example.com")',
        "    total = checkout(order, TODAY, charge, reserve, send)",
        f'    assert total == Decimal("{regular}")',
        "",
        "",
        "def test_order_with_everything() -> None:",
        "    order = Order(",
        '        lines=[Line("book", Decimal(60)), Line("pen", Decimal(40))],',
        '        email="a@example.com",',
        *_order_fields(n),
        "    )",
        "    total = checkout(order, TODAY, charge, reserve, send)",
        f'    assert total == Decimal("{expected}")',
    ]
    return "\n".join(head) + "\n"


def bubble(row: BubbleRow, labels: Mapping[str, str], width: int = 34) -> str:
    """Return the bubble text: actor label and date, then the words wrapped at width."""
    words = textwrap.fill(row.words, width=width)
    label = f"{row.tag} {labels[row.actor]}" if row.tag else labels[row.actor]
    head = f"{label}, {row.when}" if row.when else label
    return f"{head}\n{words}\n"
