"""Every diagram of the deck, drawn in the one deck style."""

from __future__ import annotations

import textwrap
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from scripts.utils import style
from scripts.utils.icons import FONT_AWESOME, FontMissingError, fc_list, font_file, glyph
from scripts.utils.palette import Actor, colour_of, context_colour, icon_of, label_of
from scripts.utils.paths import CastRow, Rule
from scripts.utils.retro import Question


@dataclass(frozen=True)
class JourneyStep:
    """One step of Maria's order: the actor who acts, what it does, the bit it decides."""

    actor: str
    text: str
    bit: str | None


# Maria orders two books with the autumn coupon to an address in Sofia.
JOURNEY = (
    JourneyStep("customer", "Maria picks two books", None),
    JourneyStep("marketing", "the autumn coupon applies", "b0"),
    JourneyStep("loyalty", "the member discount applies", "b1"),
    JourneyStep("logistics", "free shipping from 50?", "b2"),
    JourneyStep("payment", "the card is charged", "s0"),
    JourneyStep("warehouse", "the parcel is reserved", "s1"),
    JourneyStep("mailer", "the confirmation is sent", "s2"),
)


@dataclass(frozen=True)
class Leaf:
    """One path of the two-if tree: its code (coupon bit, free-shipping bit), input, fee, state."""

    code: str
    subtotal: int
    coupon: bool
    fee: int
    state: Literal["tested", "bug", "never"]


# The four leaves of the two-if tree of docs/storyline.md; the test pins each fee to ship().
TREE_LEAVES = (
    Leaf("00", 40, False, 5, "tested"),
    Leaf("01", 60, False, 0, "never"),
    Leaf("10", 55, True, 0, "bug"),
    Leaf("11", 100, True, 0, "tested"),
)


LEAF_LABELS = {
    "00": "00 tested\n40, no coupon\nfee 5",
    "01": "01 never ran\n60, no coupon\nfee 0, right\nby luck",
    "10": "10 bug (I1)\n55 + coupon\nfee 0,\nshould be 5",
    "11": "11 tested\n100 + coupon\nfee 0",
}


def tree(out: Path) -> Path:
    """Draw the two-if tree: four leaves, green tested, red bug, grey never ran."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    fill = {
        "tested": colour_of("accounting"),
        "bug": colour_of("payment"),
        "never": colour_of("customer"),
    }
    fig, ax = plt.subplots(figsize=(6.0, 4.5), dpi=style.DPI)
    xs = {leaf.code: i * 1.5 for i, leaf in enumerate(TREE_LEAVES)}
    top = (1.5 * 1.5, 0.0)
    mids = {"0": (0.75, -1.4), "1": (3.75, -1.4)}
    box = {"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "grey"}
    ax.text(*top, "coupon valid?", ha="center", va="center", fontsize=11, bbox=box)
    for bit, (mx, my) in mids.items():
        ax.annotate(
            "",
            (mx, my + 0.3),
            (top[0], top[1] - 0.3),
            arrowprops={"arrowstyle": "-|>", "color": "grey"},
        )
        ax.text(
            top[0] + (mx - top[0]) / 2,
            -0.7,
            "no" if bit == "0" else "yes",
            fontsize=10,
            ha="center",
        )
        ax.text(mx, my, "free shipping\nearned?", ha="center", va="center", fontsize=10, bbox=box)
    for leaf in TREE_LEAVES:
        mx, my = mids[leaf.code[0]]
        x, y = xs[leaf.code], -3.3
        ax.annotate(
            "", (x, y + 0.65), (mx, my - 0.4), arrowprops={"arrowstyle": "-|>", "color": "grey"}
        )
        ax.text(
            (mx + x) / 2, -2.4, "no" if leaf.code[1] == "0" else "yes", fontsize=10, ha="center"
        )
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.68, y - 0.65),
                1.36,
                1.3,
                boxstyle="round,pad=0.03,rounding_size=0.1",
                facecolor=fill[leaf.state],
                edgecolor="none",
            )
        )
        ax.text(x, y, LEAF_LABELS[leaf.code], ha="center", va="center", fontsize=8, color="white")
    ax.set_xlim(-0.8, 5.3)
    ax.set_ylim(-4.1, 0.5)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out


HOMES = ("pricing", "shipping", "tax", "fulfilment")


@dataclass(frozen=True)
class Move:
    """One home of checkout()'s bits and how many bits moved into it."""

    home: str
    bits: int


def moves(rules: Sequence[Rule]) -> tuple[Move, ...]:
    """Count the bits per home in the order pricing, shipping, tax, fulfilment; shell rows group."""
    homes = [rule.context if rule.scope == "core" else "fulfilment" for rule in rules]
    return tuple(Move(home, homes.count(home)) for home in HOMES)


@dataclass(frozen=True)
class Port:
    """One edge of the shell: the context it talks to and the sum type it answers with."""

    context: str
    code: str
    actor: str


def ports_of(rules: Sequence[Rule], cast: Sequence[CastRow]) -> tuple[Port, ...]:
    """Read the shell rows in csv order as ports: provider's label, its sum type, its actor key."""
    asked = {c.bit: c.requested_by for c in cast}
    return tuple(
        Port(label_of(asked[rule.bit]), rule.code, asked[rule.bit])
        for rule in rules
        if rule.scope == "shell"
    )


def seam_boxes(ports: Sequence[Port]) -> tuple[str, ...]:
    """Return the face colour of each port box: its actor's palette colour."""
    return tuple(colour_of(port.actor) for port in ports)


def label_ink(face: str) -> str:
    """Return black on a light face and white on a dark one, by relative luminance."""
    r, g, b = (int(face[i : i + 2], 16) / 255 for i in (1, 3, 5))
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    luminance = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    return "black" if luminance > 0.3 else "white"


def icon_file() -> Path | None:
    """Return the Font Awesome 7 Free Solid file, or None when fontconfig finds none."""
    try:
        return font_file(FONT_AWESOME, fc_list)
    except FontMissingError:
        return None


def seam(out: Path, ports: Sequence[Port]) -> Path:
    """Draw the core box, a port box per Port, and each answer's sum type on its arrow."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    n = len(ports)
    mid = (n - 1) / 2
    core_right, port_left, port_w, port_h = 3.4, 7.2, 2.6, 0.7
    colour = context_colour("fulfilment")
    shape = "round,pad=0.05,rounding_size=0.15"
    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    ax.add_patch(
        FancyBboxPatch(
            (0.2, mid - 1.2), 3.2, 2.4, boxstyle=shape, facecolor=colour_of("dev"), edgecolor="none"
        )
    )
    ax.text(1.8, mid, "core\npure rules", ha="center", va="center", fontsize=16, color="white")
    faces = seam_boxes(ports)
    font = icon_file()
    for row, (port, face) in enumerate(zip(ports, faces, strict=True)):
        y = n - 1 - row
        ink = label_ink(face)
        ax.add_patch(
            FancyBboxPatch(
                (port_left, y - port_h / 2),
                port_w,
                port_h,
                boxstyle=shape,
                facecolor=face,
                edgecolor="none",
            )
        )
        if font is not None:
            ax.text(
                port_left + 0.1,
                y,
                glyph(icon_of(port.actor), FONT_AWESOME),
                ha="left",
                va="center",
                fontproperties=FontProperties(fname=font, size=16),
                color=ink,
            )
        ax.text(
            port_left + port_w / 2 + (0.2 if font is not None else 0.0),
            y,
            port.context,
            ha="center",
            va="center",
            fontsize=16 if font is None else 14,
            color=ink,
        )
        ax.annotate(
            "",
            (core_right + 0.15, y),
            (port_left - 0.1, y),
            arrowprops={"arrowstyle": "-|>", "color": colour, "linewidth": 1.8},
        )
        ax.text(
            (core_right + port_left) / 2,
            y + 0.12,
            port.code,
            ha="center",
            va="bottom",
            fontsize=12,
            style="italic",
        )
    ax.set_xlim(0, 10.2)
    ax.set_ylim(-0.7, n - 0.3)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out


def band_groups(moves: Sequence[Move]) -> tuple[tuple[str, int], ...]:
    """Count the bands under the core and the shell labels."""
    shell = sum(1 for move in moves if move.home == "fulfilment")
    return (("core: the What", len(moves) - shell), ("shell: the How, the ports", shell))


def moves_figure(out: Path, moves: Sequence[Move]) -> Path:
    """Draw checkout() as one box and one band per home, its width by bits, its count on it."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Rectangle

    unit, band_x, band_h = 1.5, 5.0, 0.7
    n = len(moves)
    fig, ax = plt.subplots(figsize=(11.0, 3.6), dpi=style.DPI)
    mid = (n - 1) / 2
    ax.add_patch(
        FancyBboxPatch(
            (0.2, mid - 0.8),
            2.6,
            1.6,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            facecolor=colour_of("dev"),
            edgecolor="none",
        )
    )
    ax.text(1.5, mid, "checkout()", ha="center", va="center", fontsize=16, color="white")
    for row, move in enumerate(moves):
        y = n - 1 - row
        colour = context_colour(move.home)
        ax.annotate(
            "",
            (band_x - 0.1, y),
            (2.9, mid),
            arrowprops={"arrowstyle": "-|>", "color": colour, "linewidth": 1.8},
        )
        ax.add_patch(
            Rectangle((band_x, y - band_h / 2), move.bits * unit, band_h, facecolor=colour)
        )
        ax.text(
            band_x + move.bits * unit / 2,
            y,
            str(move.bits),
            ha="center",
            va="center",
            fontsize=20,
            color="white",
        )
        ax.text(band_x + move.bits * unit + 0.2, y, move.home, ha="left", va="center", fontsize=16)
    bracket_x = band_x + max(move.bits for move in moves) * unit + 3.4
    top = n - 1
    for label, count in band_groups(moves):
        if count == 0:
            continue
        bottom = top - count + 1
        ax.plot(
            [bracket_x - 0.15, bracket_x, bracket_x, bracket_x - 0.15],
            [top + 0.3, top + 0.3, bottom - 0.3, bottom - 0.3],
            color="black",
            linewidth=1.5,
        )
        ax.text(
            bracket_x + 0.2,
            (top + bottom) / 2,
            label,
            ha="left",
            va="center",
            fontsize=14,
        )
        top = bottom - 1
    ax.set_xlim(0, bracket_x + 7.5)
    ax.set_ylim(-0.7, n - 0.3)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out


def question_ids(
    steps: Sequence[JourneyStep], questions: Sequence[Question]
) -> tuple[str | None, ...]:
    """Return the id of the question raised on each step's bit, None where none was."""
    raised = {q.bit: q.id for q in questions}
    return tuple(raised.get(step.bit) if step.bit else None for step in steps)


def mood(steps: Sequence[JourneyStep], questions: Sequence[Question]) -> tuple[int, ...]:
    """Return the certainty level per step: a question drops 2 on an s-bit, 1 on a b-bit."""
    level = 0
    levels: list[int] = []
    for step, qid in zip(steps, question_ids(steps, questions), strict=True):
        if qid:
            level -= 2 if step.bit and step.bit.startswith("s") else 1
        levels.append(level)
    return tuple(levels)


def journey(questions: Sequence[Question], actors: Mapping[str, Actor], out: Path) -> Path:
    """Draw the journey of one order: an actor box per step, the mood line above it.

    The mood line drops at each step that raised a question, labelled with the question id.
    """
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    pitch, box_w, box_h = 1.7, 1.6, 1.3
    levels = mood(JOURNEY, questions)
    ids = question_ids(JOURNEY, questions)
    font = icon_file()
    fig, ax = plt.subplots(figsize=(12.0, 5.0), dpi=style.DPI)
    xs = [i * pitch for i in range(len(JOURNEY))]
    ys = [1.5 + 0.3 * (level + 9) for level in levels]
    ax.plot([-box_w / 2, *xs], [ys[0], *ys], color="dimgrey", linewidth=2.5, zorder=2)
    for i, step in enumerate(JOURNEY):
        actor = actors[step.actor]
        face = colour_of(step.actor)
        ink = label_ink(face)
        ax.add_patch(
            FancyBboxPatch(
                (xs[i] - box_w / 2, -box_h / 2),
                box_w,
                box_h,
                boxstyle="round,pad=0.03,rounding_size=0.1",
                facecolor=face,
                edgecolor="none",
                zorder=3,
            )
        )
        if font is not None:
            ax.text(
                xs[i],
                0.27,
                glyph(actor.icon, FONT_AWESOME),
                ha="center",
                va="center",
                fontproperties=FontProperties(fname=font, size=22),
                color=ink,
                zorder=4,
            )
        ax.text(
            xs[i],
            -0.3 if font is not None else 0.0,
            textwrap.fill(actor.label.replace(" (the shop)", ""), 11),
            ha="center",
            va="center",
            fontsize=12,
            color=ink,
            zorder=4,
        )
        ax.text(
            xs[i],
            -box_h / 2 - 0.1,
            textwrap.fill(step.text, 16),
            ha="center",
            va="top",
            fontsize=14,
            zorder=4,
        )
        qid = ids[i]
        ax.plot(
            xs[i],
            ys[i],
            "o",
            color=colour_of("payment") if qid else "dimgrey",
            markersize=11 if qid else 7,
            zorder=3,
        )
        if qid:
            ax.text(
                xs[i],
                ys[i] - 0.28,
                qid,
                ha="center",
                va="top",
                fontsize=16,
                fontweight="bold",
                color=colour_of("payment"),
                zorder=4,
            )
    ax.text(
        -box_w / 2,
        max(ys) + 0.55,
        "the customer's certainty",
        fontsize=14,
        style="italic",
        color="dimgrey",
    )
    ax.set_xlim(-box_w / 2 - 0.2, xs[-1] + box_w / 2 + 0.2)
    ax.set_ylim(-2.4, max(ys) + 0.9)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
