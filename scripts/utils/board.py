"""The rules board: nine rows, five columns revealed stage by stage, from the room to the tests."""

from __future__ import annotations

import csv
import re
import textwrap
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style
from scripts.utils.examples import missing_tests
from scripts.utils.figures import HOMES
from scripts.utils.palette import colour_of, label_of
from scripts.utils.paths import Rule
from scripts.utils.retro import Question
from scripts.utils.stage import Stop

COLUMNS = ("room", "sentence", "home", "code", "test")
# Stage 03 shows the first two columns, 04 three, 05 four, 06 all five.
STAGES = {3: 2, 4: 3, 5: 4, 6: 5}
ROOM_SUFFIXES = ("\nraised", ": sentence")
HEADER_SECTIONS = ("03", "03", "04", "05", "06")
WIDTHS = (0.07, 0.38, 0.13, 0.2, 0.22)
TEST_FUNCTION = re.compile(r"^(?:def (test_\w+)\(|class (Test\w+)[(:])", re.MULTILINE)


@dataclass(frozen=True)
class BoardRow:
    """One decision of the board: the cells of its five columns."""

    bit: str
    room: str
    sentence: str
    home: str
    code: str
    tests: tuple[str, ...]


def column_widths(stage: int, n: int) -> tuple[float, ...]:
    """Return n column widths; at stage 3 a waiting column takes a third, the sentence the rest."""
    widths = WIDTHS[:n]
    if stage != 3:
        return widths
    waiting = tuple(w / 3 if col >= STAGES[stage] else w for col, w in enumerate(widths))
    freed = sum(widths) - sum(waiting)
    return (waiting[0], waiting[1] + freed, *waiting[2:])


def example_tests(path: Path) -> dict[str, tuple[str, ...]]:
    """Read the test names of every bit from data/examples.csv, in file order."""
    names: dict[str, list[str]] = {}
    with path.open(newline="", encoding="ascii") as fh:
        for row in csv.DictReader(fh):
            names.setdefault(row["bit"], []).append(row["name"])
    return {bit: tuple(found) for bit, found in names.items()}


def board_rows(
    rules: Sequence[Rule],
    questions: Sequence[Question],
    tests: dict[str, tuple[str, ...]],
) -> tuple[BoardRow, ...]:
    """Join each rule with the question of its bit and the example names of its bit."""
    room = {question.bit: question.id for question in questions}
    return tuple(
        BoardRow(
            rule.bit,
            room.get(rule.bit, rule.bit),
            rule.rule,
            rule.context,
            rule.code,
            tests.get(rule.bit, ()),
        )
        for rule in rules
    )


def headers(route: Sequence[Stop]) -> tuple[str, ...]:
    """Head the five columns by the route labels; the two room columns share section 03."""
    label = {stop.section: f"{stop.section} {stop.label}" for stop in route}
    suffix = {0: ROOM_SUFFIXES[0], 1: ROOM_SUFFIXES[1]}
    return tuple(label[s] + suffix.get(col, "") for col, s in enumerate(HEADER_SECTIONS))


def header_text(col: int, stage: int, heads: Sequence[str]) -> str:
    """Name column col by the stage that reveals it; a column past stage gets 'later' below."""
    name = heads[col]
    return name if col < STAGES[stage] else f"{name}\nlater"


def tests_defined(tests_dir: Path) -> dict[str, object]:
    """Return the test functions defined under tests_dir, as a namespace of test names."""
    return {
        name: True
        for path in sorted(tests_dir.glob("test_*.py"))
        for found in TEST_FUNCTION.findall(path.read_text(encoding="utf-8"))
        for name in found
        if name
    }


def missing_of(rows: Sequence[BoardRow], tests_dir: Path) -> list[str]:
    """Return the example names of the rows that no test under tests_dir carries."""
    return missing_tests([name for row in rows for name in row.tests], tests_defined(tests_dir))


def figure_size(stage: int) -> tuple[float, float]:
    """Return the figure size in inches; stage 3 is wide and short to fill its frame's width."""
    return (12.0, 4.3) if stage == 3 else (12.0, 6.75)


def board(
    rows: Sequence[BoardRow], stage: int, out: Path, tests_dir: Path, heads: Sequence[str]
) -> Path:
    """Draw the board at stage 3, 4, 5 or 6; hidden columns stay empty grey cells."""
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage}; expected one of {tuple(STAGES)}")
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    shown = STAGES[stage]
    grey = colour_of("tangled")
    missing = set(missing_of(rows, tests_dir))
    fig, ax = plt.subplots(figsize=figure_size(stage), dpi=style.DPI)
    widths = column_widths(stage, len(COLUMNS))
    edges = [sum(widths[:i]) for i in range(len(widths) + 1)]
    height = 1.0 / (len(rows) + 1)
    gap = 0.004

    def cell(col: int, line: int, text: str, fill: str | None, size: float, ink: str) -> None:
        x, y = edges[col], 1.0 - (line + 1) * height
        ax.add_patch(
            Rectangle(
                (x + gap, y + gap),
                widths[col] - 2 * gap,
                height - 2 * gap,
                facecolor=fill or grey,
                alpha=1.0 if fill else 0.25,
                edgecolor="none",
            )
        )
        if text:
            ax.text(
                x + widths[col] / 2 if col != 1 else x + 0.01,
                y + height / 2,
                text,
                ha="center" if col != 1 else "left",
                va="center",
                fontsize=size,
                color=ink,
                linespacing=1.15,
            )

    for col in range(len(COLUMNS)):
        head = colour_of("fulfilment") if col < shown else None
        ink = "white" if col < shown else "dimgray"
        narrow = stage == 3 and col >= shown
        size = 6 if narrow else (10 if stage == 3 else 12)
        cell(col, 0, header_text(col, stage, heads), head, size, ink)
    for line, row in enumerate(rows, start=1):
        texts = (
            row.room,
            textwrap.fill(row.sentence, 96 if stage == 3 else 40),
            label_of(row.home) if row.home in HOMES else row.home,
            textwrap.fill(row.code, 30, break_long_words=False),
            "\n".join(row.tests),
        )
        home_fill = colour_of(row.home)
        test_fill = colour_of("payment" if missing.intersection(row.tests) else "accounting")
        fills = (colour_of("fulfilment"), None, home_fill, None, test_fill)
        for col, text in enumerate(texts):
            if col >= shown:
                cell(col, line, "", None, 9, "white")
            elif fills[col] is None:
                size = 13 if stage == 3 else 12
                cell(col, line, text, None, size if col == 1 else 10, "black")
            else:
                cell(col, line, text, fills[col], 9 if col != 4 else 7, "white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    style.save(fig, out)
    return out
