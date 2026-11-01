"""The stage of the talk: the shop in the middle, who talks to it around it, drawn once."""

from __future__ import annotations

import textwrap
from collections.abc import Mapping, Sequence
from pathlib import Path

from scripts.utils import style
from scripts.utils.figures import icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, glyph
from scripts.utils.palette import Actor, colour_of
from scripts.utils.paths import CastRow, Rule

CUSTOMER_WORDS = "places an order"
BOX_W, BOX_H = 2.7, 0.8
SHOP_W, SHOP_H = 2.6, 6.8
DEPARTMENT_X, PROVIDER_X, CUSTOMER_Y = -5.4, 5.4, 4.8
WRAP = 22


def edge_words(
    actors: Mapping[str, Actor], cast: Sequence[CastRow], rules: Sequence[Rule]
) -> dict[str, str]:
    """Return what each actor but the shop says to it: a department's requests, a provider's answer.

    The customer places an order; a department's words are its cast rows joined by '; '; a
    provider's text is the sum type of its shell rule.
    """
    answer = {rule.bit: rule.code for rule in rules if rule.scope == "shell"}
    words: dict[str, str] = {}
    for key, actor in actors.items():
        rows = [c for c in cast if c.requested_by == key]
        match actor.kind:
            case "customer":
                words[key] = CUSTOMER_WORDS
            case "department":
                words[key] = "; ".join(c.words for c in rows)
            case "provider":
                words[key] = "; ".join(answer[c.bit] for c in rows)
    return words


def positions(actors: Mapping[str, Actor]) -> dict[str, tuple[float, float]]:
    """Place the shop at the origin, departments left, providers right, the customer on top."""
    spots: dict[str, tuple[float, float]] = {}
    for kind, x in (("department", DEPARTMENT_X), ("provider", PROVIDER_X)):
        keys = [k for k, a in actors.items() if a.kind == kind]
        step = 1.9 if kind == "department" else 2.2
        for i, key in enumerate(keys):
            spots[key] = (x, (len(keys) - 1) / 2 * step - i * step)
    for key, actor in actors.items():
        if actor.kind == "customer":
            spots[key] = (0.0, CUSTOMER_Y)
        elif actor.kind == "dev":
            spots[key] = (0.0, 0.0)
    return spots


def business_map(
    actors: Mapping[str, Actor], cast: Sequence[CastRow], rules: Sequence[Rule], out: Path
) -> Path:
    """Draw the business map: a box and pictogram per actor, an edge with its words to the shop."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    words = edge_words(actors, cast, rules)
    spots = positions(actors)
    font = icon_file()
    shape = "round,pad=0.05,rounding_size=0.15"
    fig, ax = plt.subplots(figsize=(11.0, 6.2), dpi=style.DPI)
    for key, actor in actors.items():
        x, y = spots[key]
        is_shop = actor.kind == "dev"
        w, h = (SHOP_W, SHOP_H) if is_shop else (BOX_W, BOX_H)
        face = colour_of(key)
        ink = label_ink(face)
        if not is_shop:
            side = 0.0 if actor.kind == "customer" else (1.0 if x < 0 else -1.0)
            if side:
                tail = (x + side * (w / 2 + 0.1), y)
                head = (-side * (SHOP_W / 2 + 0.1), y)
            else:
                tail = (x, y - h / 2 - 0.1)
                head = (x, SHOP_H / 2 + 0.1)
            ax.annotate(
                "",
                head,
                tail,
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": face if key != "mailer" else "dimgrey",
                    "linewidth": 2.0,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
                zorder=1,
            )
            ax.text(
                (tail[0] + head[0]) / 2 + (0.15 if not side else 0.0),
                (tail[1] + head[1]) / 2 + (0.0 if not side else 0.12),
                textwrap.fill(words[key], WRAP),
                ha="left" if not side else "center",
                va="center" if not side else "bottom",
                fontsize=11,
                style="italic",
                zorder=5,
            )
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2),
                w,
                h,
                boxstyle=shape,
                facecolor=face,
                edgecolor="none",
                zorder=3,
            )
        )
        if font is not None:
            ax.text(
                x - w / 2 + 0.15,
                y,
                glyph(actor.icon, FONT_AWESOME),
                ha="left",
                va="center",
                fontproperties=FontProperties(fname=font, size=18),
                color=ink,
                zorder=4,
            )
        ax.text(
            x + (0.25 if font is not None else 0.0),
            y,
            actor.label.replace(" (", "\n("),
            ha="center",
            va="center",
            fontsize=13,
            color=ink,
            zorder=4,
        )
    ax.set_xlim(-7.2, 7.2)
    ax.set_ylim(-3.6, 5.5)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
