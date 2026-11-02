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
from scripts.utils.palette import colour_of, label_of
from scripts.utils.paths import Rule
from scripts.utils.retro import Question

COLUMNS = ("room", "sentence", "home", "code", "test")
# Stage 03 shows the first two columns, 04 three, 05 four, 06 all five.
STAGES = {3: 2, 4: 3, 5: 4, 6: 5}
WIDTHS = (0.07, 0.38, 0.13, 0.2, 0.22)
TEST_FUNCTION = re.compile(r"^def (test_\w+)\(", re.MULTILINE)


@dataclass(frozen=True)
class BoardRow:
    """One decision of the board: the cells of its five columns."""

    bit: str
    room: str
    sentence: str
    home: str
    code: str
    tests: tuple[str, ...]


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
            room.get(rule.bit, ""),
            rule.rule,
            rule.context,
            rule.code,
            tests.get(rule.bit, ()),
        )
        for rule in rules
    )


def tests_defined(tests_dir: Path) -> dict[str, object]:
    """Return the test functions defined under tests_dir, as a namespace of test names."""
    return {
        name: True
        for path in sorted(tests_dir.glob("test_*.py"))
        for name in TEST_FUNCTION.findall(path.read_text(encoding="utf-8"))
    }


def missing_of(rows: Sequence[BoardRow], tests_dir: Path) -> list[str]:
    """Return the example names of the rows that no test under tests_dir carries."""
    return missing_tests([name for row in rows for name in row.tests], tests_defined(tests_dir))


def board(rows: Sequence[BoardRow], stage: int, out: Path, tests_dir: Path) -> Path:
    """Draw the board at stage 3, 4, 5 or 6; hidden columns stay empty grey cells."""
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage}; expected one of {tuple(STAGES)}")
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    shown = STAGES[stage]
    grey = colour_of("tangled")
    missing = set(missing_of(rows, tests_dir))
    fig, ax = plt.subplots(figsize=(12.0, 6.75), dpi=style.DPI)
    edges = [sum(WIDTHS[:i]) for i in range(len(WIDTHS) + 1)]
    height = 1.0 / (len(rows) + 1)
    gap = 0.004

    def cell(col: int, line: int, text: str, fill: str | None, size: float, ink: str) -> None:
        x, y = edges[col], 1.0 - (line + 1) * height
        ax.add_patch(
            Rectangle(
                (x + gap, y + gap),
                WIDTHS[col] - 2 * gap,
                height - 2 * gap,
                facecolor=fill or grey,
                alpha=1.0 if fill else 0.25,
                edgecolor="none",
            )
        )
        if text:
            ax.text(
                x + WIDTHS[col] / 2 if col != 1 else x + 0.01,
                y + height / 2,
                text,
                ha="center" if col != 1 else "left",
                va="center",
                fontsize=size,
                color=ink,
                linespacing=1.15,
            )

    for col, name in enumerate(COLUMNS):
        head = colour_of("shell") if col < shown else None
        cell(col, 0, name if col < shown else "", head, 12, "white")
    for line, row in enumerate(rows, start=1):
        texts = (
            row.room,
            textwrap.fill(row.sentence, 40),
            label_of(row.home) if row.home in {"pricing", "shipping", "tax", "shell"} else row.home,
            textwrap.fill(row.code, 30, break_long_words=False),
            "\n".join(row.tests),
        )
        home_fill = colour_of(row.home)
        test_fill = colour_of("payment" if missing.intersection(row.tests) else "accounting")
        fills = (colour_of("shell"), None, home_fill, None, test_fill)
        for col, text in enumerate(texts):
            if col >= shown:
                cell(col, line, "", None, 9, "white")
            elif fills[col] is None:
                cell(col, line, text, None, 12 if col == 1 else 10, "black")
            else:
                cell(col, line, text, fills[col], 9 if col != 4 else 7, "white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    style.save(fig, out)
    return out
