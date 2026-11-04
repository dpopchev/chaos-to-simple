"""The cohesion groups: the rule cards grouped by the business question each answers."""

from __future__ import annotations

import textwrap
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style
from scripts.utils.figures import icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, UnknownIconError, glyph
from scripts.utils.palette import Actor, Context
from scripts.utils.paths import Rule

COL_W, PITCH, CARD_H = 3.2, 3.5, 1.15
WRAP = 26
ORDER = ("pricing", "shipping", "tax", "fulfilment")


@dataclass(frozen=True)
class Group:
    """One context: its question, its rule cards, its owners and its result."""

    context: str
    question: str
    color: str
    rules: tuple[Rule, ...]
    owners: tuple[Actor, ...]
    result: str


def groups(
    rules: Sequence[Rule], contexts: Mapping[str, Context], actors: Mapping[str, Actor]
) -> tuple[Group, ...]:
    """Return one Group per context with a question, in file order of contexts.

    Core rows belong to their context; shell rows belong to fulfilment.
    """
    return tuple(
        Group(
            ctx.key,
            ctx.question,
            f"#{ctx.color}",
            tuple(
                r
                for r in rules
                if r.context == ctx.key or (ctx.key == "fulfilment" and r.scope == "shell")
            ),
            tuple(a for a in actors.values() if a.context == ctx.key),
            ctx.result,
        )
        for ctx in (contexts[key] for key in ORDER)
        if ctx.question
    )


def draw(items: Sequence[Group], out: Path) -> Path:
    """Draw one column per group: the question, a card per rule, the owners and the result."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    font = icon_file()
    top = max(len(g.rules) for g in items)
    fig, ax = plt.subplots(figsize=(13.0, 6.2), dpi=style.DPI)
    for i, g in enumerate(items):
        x = i * PITCH
        ink = label_ink(g.color)
        ax.text(
            x,
            0.2,
            "\n".join(textwrap.wrap(g.question, WRAP)),
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color=g.color if ink == "white" else "black",
        )
        for j, rule in enumerate(g.rules):
            y = -j * (CARD_H + 0.15) - CARD_H / 2
            ax.add_patch(
                FancyBboxPatch(
                    (x - COL_W / 2, y - CARD_H / 2),
                    COL_W,
                    CARD_H,
                    boxstyle="round,pad=0.02,rounding_size=0.1",
                    facecolor=g.color,
                    edgecolor="none",
                    zorder=3,
                )
            )
            ax.text(
                x,
                y,
                "\n".join(textwrap.wrap(rule.rule, WRAP + 6)),
                ha="center",
                va="center",
                fontsize=9.5,
                color=ink,
                zorder=4,
            )
        foot = -top * (CARD_H + 0.15) - 0.1
        for k, owner in enumerate(g.owners):
            ox = x - 0.4 * (len(g.owners) - 1) / 2 + 0.4 * k
            ink = f"#{owner.color}" if owner.color.upper() != "F0E442" else "black"
            try:
                mark = glyph(owner.icon, FONT_AWESOME)
            except UnknownIconError:
                # An icon icons.py does not draw: the owner's name stands in.
                ax.text(ox, foot - 0.3, owner.label, ha="center", va="center", fontsize=12)
                continue
            if font is not None:
                ax.text(
                    ox,
                    foot - 0.3,
                    mark,
                    ha="center",
                    va="center",
                    fontproperties=FontProperties(fname=font, size=20),
                    color=ink,
                )
        ax.text(
            x,
            foot - 0.85,
            f"result: {g.result}",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )
    ax.set_xlim(-COL_W / 2 - 0.1, (len(items) - 1) * PITCH + COL_W / 2 + 0.1)
    ax.set_ylim(-top * (CARD_H + 0.15) - 1.4, 1.5)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
