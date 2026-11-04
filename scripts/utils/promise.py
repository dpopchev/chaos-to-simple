"""The promise: what the customer got against what the room agreed, two rows of three steps."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style
from scripts.utils.figures import icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, glyph
from scripts.utils.palette import ACTORS_CSV, colour_of, load_actors

TITLES = {"customer": "what the customer got", "room": "what the room agreed, q5"}
ROWS = ("customer", "room")
BOX_W, BOX_H, PITCH = 2.4, 1.1, 3.4
INCIDENT = "black"


@dataclass(frozen=True)
class Step:
    """One step of a row: who acts and the words under the box."""

    row: str
    step: int
    actor: str
    words: str


def load_steps(path: Path) -> tuple[Step, ...]:
    """Read the steps from promise.csv, in file order."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Step(r["row"], int(r["step"]), r["actor"], r["words"]) for r in csv.DictReader(fh)
        )


def swapped_pair(steps: Sequence[Step]) -> tuple[int, ...]:
    """Return the step numbers whose actor is in both rows but at another step, in order."""
    by_row = {row: {s.step: s.actor for s in steps if s.row == row} for row in ROWS}
    first, second = by_row[ROWS[0]], by_row[ROWS[1]]
    shared = set(first.values()) & set(second.values())
    return tuple(n for n in sorted(first) if first[n] in shared and first[n] != second.get(n))


def draw(steps: Sequence[Step], out: Path, actors: Path = ACTORS_CSV) -> Path:
    """Draw the two rows of boxes, the swapped pair framed in the incident colour."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    palette = load_actors(actors)
    swapped = swapped_pair(steps)
    font = icon_file()
    fig, ax = plt.subplots(figsize=(11.0, 4.6), dpi=style.DPI)
    for r, row in enumerate(ROWS):
        y = -r * 2.4
        ax.text(-2.0, y, TITLES[row], ha="right", va="center", fontsize=14, fontweight="bold")
        for s in (s for s in steps if s.row == row):
            x = (s.step - 1) * PITCH
            face = colour_of(s.actor)
            ink = label_ink(face)
            framed = s.step in swapped
            ax.add_patch(
                FancyBboxPatch(
                    (x - BOX_W / 2, y - BOX_H / 2),
                    BOX_W,
                    BOX_H,
                    boxstyle="round,pad=0.02,rounding_size=0.1",
                    facecolor=face,
                    edgecolor=INCIDENT if framed else "none",
                    linewidth=4 if framed else 0,
                    zorder=3,
                )
            )
            if font is not None:
                ax.text(
                    x - 0.75,
                    y,
                    glyph(palette[s.actor].icon, FONT_AWESOME),
                    ha="center",
                    va="center",
                    fontproperties=FontProperties(fname=font, size=22),
                    color=ink,
                    zorder=4,
                )
            ax.text(
                x + 0.2,
                y,
                palette[s.actor].label,
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
                color=ink,
                zorder=4,
            )
            ax.text(x, y - BOX_H / 2 - 0.25, s.words, ha="center", va="top", fontsize=13)
            if s.step < 3:
                ax.annotate(
                    "",
                    xy=(x + PITCH - BOX_W / 2 - 0.05, y),
                    xytext=(x + BOX_W / 2 + 0.05, y),
                    arrowprops={"arrowstyle": "-|>", "color": "dimgrey", "linewidth": 1.5},
                    zorder=2,
                )
    ax.set_xlim(-7.5, 2 * PITCH + BOX_W / 2 + 0.2)
    ax.set_ylim(-3.6, 0.8)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
