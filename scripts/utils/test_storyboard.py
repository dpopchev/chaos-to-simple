"""The storyboard: the checkout at each step, its diffs and the bubbles."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts.utils.paths import load_cast
from scripts.utils.storyboard import BubbleRow, bubble, step_diff, step_lines, step_view
from scripts.utils.widths import snippet_text, strip_step_markers

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (ROOT / "01-bits/s01_bits/chaos.py").read_text(encoding="ascii")
CAST = load_cast(ROOT / "data/cast.csv")
STEPS = range(1, 7)
ASIDE = re.compile(r"  # .*$", re.MULTILINE)


def added(n: int) -> list[str]:
    """The lines a step's diff adds, without the plus sign."""
    return [
        line[1:]
        for line in step_diff(SOURCE, n).splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]


def marked(n: int) -> list[str]:
    """The lines of the exhibit marked for step n, markers stripped."""
    rows = [row for row in SOURCE.splitlines() if row.endswith(f"# [step: {n}]")]
    return [ASIDE.sub("", row) for row in strip_step_markers("\n".join(rows)).splitlines()]


@pytest.mark.view
def test_step_six_is_the_full_function_stripped() -> None:
    expected = snippet_text(strip_step_markers(SOURCE), "checkout").strip()
    assert step_lines(SOURCE, 6) == ASIDE.sub("", expected)


@pytest.mark.view
@pytest.mark.parametrize("n", STEPS)
def test_each_step_adds_exactly_the_lines_marked_for_it(n: int) -> None:
    assert added(n) == marked(n)


@pytest.mark.view
@pytest.mark.parametrize("n", STEPS)
def test_each_step_adds_its_cast_fragment(n: int) -> None:
    fragment = next(row.fragment for row in CAST if row.step == n)
    assert fragment in "\n".join(added(n))


@pytest.mark.view
def test_step_view_marks_only_the_lines_of_its_step() -> None:
    view = step_view(SOURCE, 3).splitlines()[1:]
    assert [row[2:] for row in view if row.startswith("+ ")] == marked(3)


@pytest.mark.view
def test_step_zero_diff_is_the_skeleton_from_nothing() -> None:
    assert added(0) == marked(0)


@pytest.mark.view
def test_step_diff_has_no_header() -> None:
    lines = step_diff(SOURCE, 3).splitlines()
    assert not any(line.startswith(("---", "+++", "@@")) for line in lines)


@pytest.mark.view
def test_step_lines_drop_the_narrator_asides() -> None:
    assert "what if" not in step_lines(SOURCE, 6)


@pytest.mark.view
def test_bubble_reads_actor_label_date_and_words() -> None:
    row = BubbleRow(1, 3, "2026-08-11", "marketing", "Small change?")
    assert bubble(row, {"marketing": "Marketing"}) == "Marketing, 2026-08-11\nSmall change?\n"


@pytest.mark.view
def test_bubble_wraps_at_the_column_width() -> None:
    words = "Autumn campaign: 10 EUR off with the code AUTUMN. Small change? Right after it."
    row = BubbleRow(1, 3, "2026-08-11", "marketing", words)
    lines = bubble(row, {"marketing": "Marketing"}).splitlines()
    assert max(map(len, lines)) <= 34


@pytest.mark.view
def test_bubble_without_a_date_reads_the_label_alone() -> None:
    row = BubbleRow(2, 0, "", "dev", "Which test do I write?")
    assert bubble(row, {"dev": "Dev (the shop)"}) == "Dev (the shop)\nWhich test do I write?\n"
