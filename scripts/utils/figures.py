"""Every diagram of the deck, drawn in the one deck style."""

from __future__ import annotations

from pathlib import Path

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
