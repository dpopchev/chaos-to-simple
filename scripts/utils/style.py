"""The one deck style every figure is drawn with.

Adwaita Sans is the deck's font; matplotlib bundles DejaVu Sans as the fallback.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure

FONT = "Adwaita Sans"
FALLBACK_FONT = "DejaVu Sans"
FIGSIZE = (8.0, 4.5)
DPI = 150


def palette() -> list[str]:
    """Six hex colours, seaborn's colorblind palette."""
    return [mcolors.to_hex(c) for c in sns.color_palette("colorblind", 6)]


def save(fig: Figure, out: Path) -> None:
    """Save fig to out at the deck dpi on white, creating parent folders, then close it."""
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)


def apply() -> None:
    """Set the deck theme: white, deck font, 16:9 at 150 dpi, no top or right spine."""
    sns.set_theme(
        style="white",
        palette=palette(),
        font=FONT,
        rc={
            "font.family": [FONT, FALLBACK_FONT],
            "figure.figsize": FIGSIZE,
            "savefig.dpi": DPI,
            "axes.spines.top": False,
            "axes.spines.right": False,
        },
    )
