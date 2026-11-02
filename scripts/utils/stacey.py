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
from scripts.utils.stage import COUNTER_COLOUR

Side = Literal["above", "on", "below"]

ZONE_COLOURS = ("accounting", "logistics", "marketing", "payment")
LIMIT = 1.1
FIGURE = (8.0, 8.2)


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
        LIMIT - 0.04, LIMIT - 0.08, labels["diagonal"], ha="center", va="center", fontsize=20,
        fontweight="bold", color="dimgrey", rotation=45, zorder=6,
    )
    quote = labels["boom_quote"]
    for zone in zones:
        mid = (zone.r_min + (zone.r_max if zone is not zones[-1] else 1.0)) / 2
        ax.text(mid, -0.035, zone.label, ha="center", va="top", fontsize=15, fontweight="bold")
        below = -0.11
        if zone is zones[-1] and quote:
            # The recorded quote sits between the band's name and its below text.
            ax.text(mid, -0.08, quote, ha="center", va="top", fontsize=10)
            below = -0.125
        # Below the diagonal is below the axis: the band's below text sits under its name.
        ax.text(
            mid, below, textwrap.fill(zone.below, 22), ha="center", va="top", fontsize=9.5,
            style="italic",
        )
        if zone is zones[0]:
            # The innermost band is narrow: its above text hugs the y axis.
            ax.text(
                0.012, 0.19, textwrap.fill(zone.above, 15), ha="left", va="center", fontsize=8.5,
                style="italic", zorder=3,
            )
            continue
        ax.text(
            mid * math.cos(math.radians(76)), mid * math.sin(math.radians(76)),
            textwrap.fill(zone.above, 16), ha="center", va="center", fontsize=9, style="italic",
            zorder=3,
        )
    ax.text(
        0.02, LIMIT - 0.02, labels["above"], ha="left", va="top", fontsize=13, color="dimgrey",
        zorder=6,
    )
    ax.text(
        LIMIT - 0.02, 0.02, labels["below"], ha="right", va="bottom", fontsize=13, color="dimgrey",
        zorder=6,
    )
    font = icon_file()
    for spot in route:
        faded = highlight is not None and spot.section != highlight
        face = colour_of(COUNTER_COLOUR[spot.counter])
        alpha = 0.25 if faded else 1.0
        ax.add_patch(
            Circle(
                (spot.x, spot.y), 0.045, facecolor=face, alpha=alpha, zorder=4,
                edgecolor="black" if spot.section == highlight else "none", linewidth=3,
            )
        )
        if font is not None and not faded:
            ax.text(
                spot.x, spot.y, glyph(spot.icon, FONT_AWESOME), ha="center", va="center",
                fontproperties=FontProperties(fname=font, size=17), color=label_ink(face), zorder=5,
            )
        beside = side_of(spot.x, spot.y) == "below"
        ax.text(
            spot.x + 0.06 if beside else spot.x,
            spot.y if beside else spot.y - 0.07,
            textwrap.fill(f"{spot.section} {spot.label}", 9) if beside else
            f"{spot.section} {spot.label}",
            ha="left" if beside else "center", va="center" if beside else "top",
            fontsize=12, fontweight="bold", alpha=alpha, zorder=5,
            bbox={"facecolor": "white", "alpha": 0.7 * alpha, "edgecolor": "none", "pad": 1.5},
        )
    ax.text(
        LIMIT / 2, -0.27, labels["x_axis"], ha="center", va="top", fontsize=13, color="dimgrey"
    )
    ax.text(
        -0.04, LIMIT / 2, labels["y_axis"], ha="right", va="center", fontsize=13, color="dimgrey",
        rotation=90,
    )
    ax.set_xlim(-0.08, LIMIT)
    ax.set_ylim(-0.3, LIMIT)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
