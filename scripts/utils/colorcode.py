"""The checkout coloured by owner: a left bar for who asked, a right bar for the context."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style
from scripts.utils.figures import icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, glyph
from scripts.utils.palette import Actor, Context, colour_of
from scripts.utils.paths import CastRow, Rule
from scripts.utils.widths import snippet_text, strip_step_markers

_STEP = re.compile(r"# \[step: (?P<n>\d)\]\s*$")
SKELETON_OWNER = "customer"
MONO = ["Adwaita Mono", "DejaVu Sans Mono"]
WIDTH, HEIGHT = 10.0, 6.0
TOP, BOTTOM = 5.85, 1.35
TEXT_X, BAR_W = 0.45, 0.14
FONT_SIZE = 12


@dataclass(frozen=True)
class OwnedLine:
    """One checkout line: its text, the actor who asked for it, the context it belongs to."""

    text: str
    owner: str
    context: str | None


def _owner_row(step: int, text: str, cast: Sequence[CastRow]) -> CastRow | None:
    if step > 0:
        return next((row for row in cast if row.step == step), None)
    code = text.strip()
    for row in cast:
        if row.step == 0 and code.startswith(row.fragment.split("(")[0] + "("):
            return row
    return None


def owned_lines(
    source: str, cast: Sequence[CastRow], rules: Sequence[Rule]
) -> tuple[OwnedLine, ...]:
    """Return the checkout snippet's lines, markers stripped, each with its owner and context.

    A line marked step N belongs to the cast row of step N; the three effect calls of step 0
    belong to their provider by fragment; the rest is the skeleton, owned by nobody.
    """
    context_of = {rule.bit: rule.context for rule in rules}
    out: list[OwnedLine] = []
    for raw in snippet_text(source, "checkout").splitlines():
        marker = _STEP.search(raw)
        step = int(marker.group("n")) if marker else 0
        text = strip_step_markers(raw)
        row = _owner_row(step, text, cast)
        if row is None:
            out.append(OwnedLine(text, SKELETON_OWNER, None))
        else:
            out.append(OwnedLine(text, row.requested_by, context_of[row.bit]))
    return tuple(out)


def colorcode(
    lines: Sequence[OwnedLine],
    actors: Mapping[str, Actor],
    contexts: Mapping[str, Context],
    out: Path,
) -> Path:
    """Draw the lines as monospace text between two bars, with a legend of actors and contexts."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import Rectangle

    font = icon_file()
    fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=style.DPI)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.axis("off")
    pitch = (TOP - BOTTOM) / len(lines)
    for i, line in enumerate(lines):
        y = TOP - (i + 1) * pitch
        ax.add_patch(
            Rectangle((0.1, y), BAR_W, pitch, facecolor=colour_of(line.owner), edgecolor="none")
        )
        if line.context is not None:
            ax.add_patch(
                Rectangle(
                    (WIDTH - 0.1 - BAR_W, y),
                    BAR_W,
                    pitch,
                    facecolor=colour_of(line.context),
                    edgecolor="none",
                )
            )
        ax.text(
            TEXT_X,
            y + pitch / 2,
            line.text,
            family=MONO,
            fontsize=FONT_SIZE,
            va="center",
            ha="left",
            color="black",
        )
    chips = [(key, a.label, colour_of(key), a.icon) for key, a in actors.items()]
    chips += [(key, c.label, colour_of(key), "") for key, c in contexts.items() if key != "tangled"]
    per_row = 5
    cell = (WIDTH - 0.4) / per_row
    for i, (_, label, face, icon) in enumerate(chips):
        x = 0.2 + (i % per_row) * cell
        y = 1.0 - (i // per_row) * 0.42
        ax.add_patch(Rectangle((x, y - 0.14), 0.32, 0.28, facecolor=face, edgecolor="none"))
        if icon and font is not None:
            ax.text(
                x + 0.16,
                y,
                glyph(icon, FONT_AWESOME),
                ha="center",
                va="center",
                fontproperties=FontProperties(fname=font, size=10),
                color=label_ink(face),
            )
        ax.text(x + 0.4, y, label, ha="left", va="center", fontsize=9)
    style.save(fig, out)
    return out
