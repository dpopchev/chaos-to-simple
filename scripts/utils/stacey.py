"""The Stacey matrix: radial bands of uncertainty, the Who diagonal, the stops of the route."""

from __future__ import annotations

import csv
import math
import textwrap
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from scripts.utils import style
from scripts.utils.figures import icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, glyph
from scripts.utils.palette import colour_of

Side = Literal["above", "on", "below"]

ZONE_COLOURS = ("accounting", "logistics", "marketing", "payment")
LIMIT = 1.1
FIGURE = (8.0, 8.1)
ZONE_NAME_SIZE = 15
ZONE_TEXT_SIZE = 12


@dataclass(frozen=True)
class Zone:
    """One band of the matrix, from r_min up to r_max; the last band is open above r_min."""

    key: str
    r_min: float
    r_max: float
    label: str
    above: str
    below: str


@dataclass(frozen=True)
class Spot:
    """One stop of the route placed on the matrix."""

    section: str
    label: str
    icon: str
    counter: str
    x: float
    y: float


def load_zones(path: Path) -> tuple[Zone, ...]:
    """Read the bands from zones.csv, innermost first."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Zone(
                r["zone"], float(r["r_min"]), float(r["r_max"]), r["label"], r["above"], r["below"]
            )
            for r in csv.DictReader(fh)
        )


def load_labels(path: Path) -> dict[str, str]:
    """Read the free texts of the matrix from labels.csv by key."""
    with path.open(newline="", encoding="ascii") as fh:
        return {r["key"]: r["text"] for r in csv.DictReader(fh)}


def load_spots(path: Path) -> tuple[Spot, ...]:
    """Read the stops that carry coordinates from route.csv, in section order."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Spot(r["section"], r["label"], r["icon"], r["counter"], float(r["x"]), float(r["y"]))
            for r in csv.DictReader(fh)
            if r["x"] and r["y"]
        )


def zone_of(x: float, y: float, zones: Sequence[Zone]) -> str:
    """Return the key of the band holding the point, by its radius from the origin.

    A band owns its r_min and not its r_max; the last band has no upper edge.
    """
    radius = math.hypot(x, y)
    inner = [z for z in zones[:-1] if radius < z.r_max]
    return inner[0].key if inner else zones[-1].key


def band_colour(x: float, y: float, zones: Sequence[Zone]) -> str:
    """Return the palette key colouring the band that holds the point."""
    keys = [z.key for z in zones]
    return ZONE_COLOURS[keys.index(zone_of(x, y, zones))]


def side_of(x: float, y: float) -> Side:
    """Return where the point lies against the diagonal y = x."""
    if math.isclose(x, y, abs_tol=1e-9):
        return "on"
    return "above" if y > x else "below"


def draw(
    route: Sequence[Spot],
    zones: Sequence[Zone],
    labels: Mapping[str, str],
    out: Path,
    highlight: str | None = None,
) -> Path:
    """Draw the matrix; with highlight, the stop of that section stands out and the rest fade."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import Circle, Wedge

    fig, ax = plt.subplots(figsize=FIGURE, dpi=style.DPI)
    for zone, key in reversed(list(zip(zones, ZONE_COLOURS, strict=True))):
        radius = 2.0 if zone is zones[-1] else zone.r_max
        ax.add_patch(
            Wedge((0, 0), radius, 0, 90, facecolor=colour_of(key), alpha=0.28, edgecolor="white")
        )
    ax.plot([0, LIMIT], [0, LIMIT], color="dimgrey", linewidth=2, linestyle="--", zorder=2)
    ax.text(
        LIMIT - 0.04,
        LIMIT - 0.08,
        labels["diagonal"],
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color="dimgrey",
        rotation=45,
        zorder=6,
    )
    quote = labels["boom_quote"]
    for zone in zones:
        mid = (zone.r_min + (zone.r_max if zone is not zones[-1] else 1.0)) / 2
        if zone is zones[0]:
            # The innermost band is narrow: its name and above text hug the y axis.
            cx, cy, align, wrap = 0.012, 0.215, "left", 12
        else:
            cx = max(mid * math.cos(math.radians(76)), 0.15)
            cy = mid * math.sin(math.radians(76))
            align, wrap = "center", 22
        size = ZONE_TEXT_SIZE
        # The band name sits in its arc above the in-arc text; the last is followed by the quote.
        ax.text(
            cx,
            cy,
            zone.label,
            ha=align,
            va="bottom",
            fontsize=ZONE_NAME_SIZE,
            fontweight="bold",
            zorder=3,
        )
        top = cy
        if zone is zones[-1] and quote:
            ax.text(cx, top, quote, ha=align, va="top", fontsize=size, zorder=3)
            top -= 0.04
        ax.text(
            cx,
            top,
            textwrap.fill(zone.above, wrap, break_long_words=False),
            ha=align,
            va="top",
            fontsize=size,
            style="italic",
            zorder=3,
        )
    ax.text(
        0.02,
        LIMIT - 0.02,
        labels["above"],
        ha="left",
        va="top",
        fontsize=13,
        color="dimgrey",
        zorder=6,
    )
    ax.text(
        LIMIT - 0.02,
        0.02,
        labels["below"],
        ha="right",
        va="bottom",
        fontsize=13,
        color="dimgrey",
        zorder=6,
    )
    font = icon_file()
    for spot in route:
        faded = highlight is not None and spot.section != highlight
        face = colour_of(band_colour(spot.x, spot.y, zones))
        alpha = 0.25 if faded else 1.0
        ax.add_patch(
            Circle(
                (spot.x, spot.y),
                0.045,
                facecolor=face,
                alpha=alpha,
                zorder=4,
                edgecolor="black" if spot.section == highlight else "none",
                linewidth=3,
            )
        )
        if font is not None and not faded:
            ax.text(
                spot.x,
                spot.y,
                glyph(spot.icon, FONT_AWESOME),
                ha="center",
                va="center",
                fontproperties=FontProperties(fname=font, size=17),
                color=label_ink(face),
                zorder=5,
            )
        beside = side_of(spot.x, spot.y) == "below"
        ax.text(
            spot.x + 0.06 if beside else spot.x,
            spot.y if beside else spot.y - 0.07,
            textwrap.fill(f"{spot.section} {spot.label}", 9)
            if beside
            else f"{spot.section} {spot.label}",
            ha="left" if beside else "center",
            va="center" if beside else "top",
            fontsize=12,
            fontweight="bold",
            alpha=alpha,
            zorder=5,
            bbox={"facecolor": "white", "alpha": 0.7 * alpha, "edgecolor": "none", "pad": 1.5},
        )
    ax.text(LIMIT / 2, -0.02, labels["x_axis"], ha="center", va="top", fontsize=13, color="dimgrey")
    ax.text(
        -0.04,
        LIMIT / 2,
        labels["y_axis"],
        ha="right",
        va="center",
        fontsize=13,
        color="dimgrey",
        rotation=90,
    )
    ax.set_xlim(-0.08, LIMIT)
    ax.set_ylim(-0.07, LIMIT)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
