"""Every diagram of the deck, drawn in the one deck style."""

from __future__ import annotations

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
