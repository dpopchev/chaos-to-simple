"""Every diagram of the deck, drawn in the one deck style."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from scripts.utils import style

# (label, x0, y0) of each zone on the unit square; x is certainty on the How,
# y is agreement on the What. Simple sits at the high-high corner.
ZONES = (
    ("simple", 0.5, 0.5),
    ("complicated on the What", 0.5, 0.0),
    ("complicated on the How", 0.0, 0.5),
    ("complex, chaos in the corner", 0.0, 0.0),
)


ACTORS = ("Customer", "Shop", "Warehouse", "Payment provider", "Mailer")

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


# (short name, footer counter) of each section, left to right.
SECTIONS = (
    ("00 pride", "?"),
    ("01 bits", "64"),
    ("02 which problem", "64"),
    ("03 the room", "512"),
    ("04 homes", "512"),
    ("05 the seam", "512"),
    ("06 simple", "72"),
    ("07 six lines", "72"),
)

# section index -> the incident on the arrow into it.
INCIDENTS = {
    1: "I1: free shipping under 50",
    3: "I2: before or after the discount?",
    5: "I3: charged, no parcel",
}


@dataclass(frozen=True)
class Stop:
    """One section of the talk: its Stacey zone, footer counter and the move into it."""

    section: str
    zone: str
    counter: str
    move: str


def load_route(path: Path) -> tuple[Stop, ...]:
    """Read the stops of the route from data/route.csv, in section order."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Stop(row["section"], row["zone"], row["counter"], row["move"])
            for row in csv.DictReader(fh)
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

    colours = style.palette()
    fill = {"tested": colours[2], "bug": colours[3], "never": "#8c8c8c"}
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


def route(out: Path) -> None:
    """Draw the route of the talk: eight section boxes in two rows, the incidents on the arrows."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    colours = style.palette()
    counter_colour = {"?": colours[3], "64": colours[0], "512": colours[1], "72": colours[2]}
    per_row = 4
    step, half_w, half_h = 3.4, 1.25, 0.55
    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    spots = [(i % per_row * step, -(i // per_row) * 2.6) for i in range(len(SECTIONS))]
    for i, (name, counter) in enumerate(SECTIONS):
        x, y = spots[i]
        ax.add_patch(
            FancyBboxPatch(
                (x - half_w, y - half_h),
                2 * half_w,
                2 * half_h,
                boxstyle="round,pad=0.05,rounding_size=0.2",
                facecolor=counter_colour[counter],
                edgecolor="none",
            )
        )
        ax.text(x, y, f"{name}\n{counter}", ha="center", va="center", fontsize=12, color="white")
    for i in range(1, len(SECTIONS)):
        (x0, y0), (x1, y1) = spots[i - 1], spots[i]
        props = {"arrowstyle": "-|>", "color": "grey", "linewidth": 1.5}
        if y1 != y0:
            mid = (y0 + y1) / 2
            ax.plot([x0, x0, x1], [y0 - half_h - 0.1, mid, mid], color="grey", linewidth=1.5)
            start, end = (x1, mid), (x1, y1 + half_h + 0.1)
        else:
            start, end = (x0 + half_w + 0.15, y0), (x1 - half_w - 0.15, y1)
        ax.annotate("", end, start, arrowprops=props)
        if i in INCIDENTS:
            head, tail = INCIDENTS[i].split(": ")
            ax.text(
                (start[0] + end[0]) / 2,
                y1 + half_h + 0.2,
                f"{head}\n{tail}",
                ha="center",
                va="bottom",
                fontsize=10,
                style="italic",
            )
    ax.set_xlim(-half_w - 0.2, 3 * step + half_w + 0.2)
    ax.set_ylim(-3.2, 1.6)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)


def story(out: Path) -> None:
    """Draw the domain story as a sequence: five lifelines, nine sentences top to bottom."""
    style.apply()
    import matplotlib.pyplot as plt

    colours = style.palette()
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
            color="white",
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

    colours = style.palette()
    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    for i, (label, x0, y0) in enumerate(ZONES):
        ax.add_patch(
            Rectangle((x0, y0), 0.5, 0.5, facecolor=colours[i], alpha=0.35, edgecolor="white")
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
