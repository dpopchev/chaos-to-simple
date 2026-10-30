"""The one deck style every figure is drawn with.

Adwaita Sans is the deck's font; matplotlib bundles DejaVu Sans as the fallback.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.colors as mcolors
import seaborn as sns

FONT = "Adwaita Sans"
FALLBACK_FONT = "DejaVu Sans"
FIGSIZE = (8.0, 4.5)
DPI = 150


def palette() -> list[str]:
    """Six hex colours, seaborn's colorblind palette."""
    return [mcolors.to_hex(c) for c in sns.color_palette("colorblind", 6)]


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
