"""Every diagram of the deck, drawn in the one deck style."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from scripts.utils import style
from scripts.utils.examples import CardCounts
from scripts.utils.icons import FONT_AWESOME, FontMissingError, fc_list, font_file, glyph
from scripts.utils.palette import colour_of, icon_of, label_of
from scripts.utils.paths import CastRow, Rule

# Palette keys of the four Stacey zones, in ZONES order.
ZONE_KEYS = ("logistics", "marketing", "accounting", "payment")

# (label, x0, y0) of each zone on the unit square; x is certainty on the How,
# y is agreement on the What. Simple sits at the high-high corner.
ZONES = (
    ("simple", 0.5, 0.5),
    ("complicated on the What", 0.5, 0.0),
    ("complicated on the How", 0.0, 0.5),
    ("complex, chaos in the corner", 0.0, 0.0),
)


ACTORS = ("Customer", "Shop", "Warehouse", "Payment provider", "Mailer")
# Palette key of each lifeline, in ACTORS order.
STORY_KEYS = ("customer", "dev", "warehouse", "payment", "mailer")

# (sender, receiver, text, is_answer): the nine sentences of the domain story, top to bottom.
SENTENCES = (
    (0, 1, "1. places an order: cart, coupon, address, VAT ID", False),
    (1, 1, "2. prices the order: six rules", False),
    (1, 2, "3. reserves the parcel", False),
    (2, 1, "4. Reserved or OutOfStock", True),
    (1, 3, "5. charges the total", False),
    (3, 1, "6. Charged or Declined", True),
    (1, 4, "7. sends the confirmation", False),
    (4, 1, "8. Sent or Bounced", True),
    (1, 0, "9. Accepted or Rejected", True),
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


@dataclass(frozen=True)
class Move:
    """One home of checkout()'s bits and how many bits moved into it."""

    home: str
    bits: int


def moves(rules: Sequence[Rule]) -> tuple[Move, ...]:
    """Count the bits per home in the order pricing, shipping, tax, shell; shell rows group."""
    homes = [rule.context if rule.scope == "core" else "shell" for rule in rules]
    return tuple(Move(home, homes.count(home)) for home in style.CONTEXTS[:4])


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
    colour = style.context_colour("shell")
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


def moves_figure(out: Path, moves: Sequence[Move]) -> Path:
    """Draw checkout() as one box and one band per home, its width by bits, its count on it."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Rectangle

    unit, band_x, band_h = 1.5, 5.0, 0.7
    n = len(moves)
    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
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
        colour = style.context_colour(move.home)
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
        ax.text(
            band_x + move.bits * unit + 0.2, y, move.home, ha="left", va="center", fontsize=16
        )
    ax.set_xlim(0, 11.5)
    ax.set_ylim(-0.7, n - 0.3)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out


CARDS_PER_ROW = 7


def example_map(out: Path, before: CardCounts, after: CardCounts) -> Path:
    """Draw the example map twice, before and after the room, a coloured rectangle per card.

    Each panel puts the yellow story card on top, then rows of blue, red and green cards; the
    rows each colour needs are the larger of the two panels, so the panels line up.
    """
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    kinds = (
        ("blue", colour_of("logistics")),
        ("red", colour_of("payment")),
        ("green", colour_of("accounting")),
    )
    rows_of = {
        name: max(1, -(-max(getattr(before, name), getattr(after, name)) // CARDS_PER_ROW))
        for name, _ in kinds
    }
    fig, axes = plt.subplots(1, 2, figsize=style.FIGSIZE, dpi=style.DPI)
    panels = ((axes[0], "before the room", before), (axes[1], "after the room", after))
    for ax, title, counts in panels:
        ax.add_patch(
            Rectangle(
                (0, 0), 3.2, 0.8, facecolor=colour_of("mailer"), edgecolor="white", linewidth=1.5
            )
        )
        ax.text(1.6, 0.4, "story", ha="center", va="center", fontsize=10)
        row = 1.4
        for name, colour in kinds:
            for n in range(getattr(counts, name)):
                x, y = (n % CARDS_PER_ROW) * 1.0, row + (n // CARDS_PER_ROW) * 1.0
                ax.add_patch(
                    Rectangle((x, y), 0.85, 0.8, facecolor=colour, edgecolor="white", linewidth=1.5)
                )
            row += rows_of[name] + 0.2
        ax.set_title(
            f"{title}\n{counts.blue} blue, {counts.red} red, {counts.green} green, 1 yellow",
            fontsize=11,
        )
        ax.set_xlim(-0.1, CARDS_PER_ROW)
        ax.set_ylim(row, -0.1)
        ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out


def story(out: Path) -> None:
    """Draw the domain story as a sequence: five lifelines, nine sentences top to bottom."""
    style.apply()
    import matplotlib.pyplot as plt

    colours = [colour_of(key) for key in STORY_KEYS]
    n = len(SENTENCES)
    fig, ax = plt.subplots(figsize=(11.0, 6.2), dpi=style.DPI)
    top = 0.5
    bottom = -(n + 0.5)
    for i, name in enumerate(ACTORS):
        ax.plot([i, i], [top, bottom], color=colours[i], linewidth=1)
        ax.text(
            i,
            top + 0.15,
            name,
            ha="center",
            va="bottom",
            fontsize=15,
            color="black" if STORY_KEYS[i] == "mailer" else "white",
            bbox={"boxstyle": "round,pad=0.4", "facecolor": colours[i], "edgecolor": "none"},
        )
    for row, (src, dst, text, answer) in enumerate(SENTENCES):
        y = -(row + 0.5)
        colour = colours[src]
        style_line = "--" if answer else "-"
        props = {"arrowstyle": "-|>", "color": colour, "linestyle": style_line, "linewidth": 1.8}
        if src == dst:
            loop = {**props, "connectionstyle": "arc3,rad=-1.6"}
            ax.annotate("", (dst, y - 0.4), (src, y), arrowprops=loop)
            ax.text(src + 0.25, y - 0.2, text, ha="left", va="center", fontsize=12)
            continue
        ax.annotate("", (dst, y), (src, y), arrowprops=props)
        ax.text((src + dst) / 2, y + 0.12, text, ha="center", va="bottom", fontsize=12)
    ax.set_xlim(-0.6, len(ACTORS) - 0.4)
    ax.set_ylim(bottom, top + 0.9)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)


def stacey(out: Path) -> None:
    """Draw the Stacey matrix: four zones over certainty on the How and agreement on the What."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    for i, (label, x0, y0) in enumerate(ZONES):
        ax.add_patch(
            Rectangle(
                (x0, y0), 0.5, 0.5, facecolor=colour_of(ZONE_KEYS[i]), alpha=0.35, edgecolor="white"
            )
        )
        ax.text(x0 + 0.25, y0 + 0.25, label, ha="center", va="center", fontsize=18)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("certainty on the How  (low -> high)", fontsize=14)
    ax.set_ylabel("agreement on the What  (low -> high)", fontsize=14)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    style.save(fig, out)
