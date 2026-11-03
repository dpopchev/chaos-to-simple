"""The Stacey matrix: radial bands of uncertainty, the Who diagonal, the stops of the route."""

from __future__ import annotations

import csv
import math
import textwrap
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise
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
COLLABORATION_WIDTH = 0.26
SIMPLE_EDGE = 0.25
COLLABORATION_ALPHA = (0.30, 0.20, 0.10, 0.04)


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


def corner_texts(labels: Mapping[str, str]) -> tuple[str, str]:
    """Return the top-left and bottom-right Who texts, drawn on every variant."""
    return labels["above"], labels["below"]


def arrow_pairs(route: Sequence[Spot], highlight: str | None) -> list[tuple[str, str]]:
    """Return the (from, to) section pairs of consecutive stops, ending at the highlighted stop."""
    pairs = [(a.section, b.section) for a, b in pairwise(route)]
    if highlight is None:
        return pairs
    return [p for p in pairs if p[1] <= highlight]


def band_anchor(zone: Zone, spots: Sequence[Spot]) -> tuple[float, float]:
    """Return the point of the band's name: mid-band, at about 70 degrees, clear of the stops."""
    # The innermost band sits higher: its name runs right of the anchor, clear of the route arrow.
    share = 0.62 if zone.r_min == 0 else 0.5
    radius = zone.r_min + share * (zone.r_max - zone.r_min)

    def clearance(deg: int) -> float:
        px = radius * math.cos(math.radians(deg))
        py = radius * math.sin(math.radians(deg))
        return min((math.hypot(px - s.x, py - s.y) for s in spots), default=math.inf)

    best = max(range(64, 77), key=lambda d: (min(clearance(d), 0.15), -abs(d - 70)))
    return radius * math.cos(math.radians(best)), radius * math.sin(math.radians(best))


def collaboration_half_width(r: float, inner: float = SIMPLE_EDGE) -> float:
    """Return the half width of the band at radius r: 0 up to inner, the full width at r = 1."""
    if r <= inner:
        return 0.0
    return COLLABORATION_WIDTH * (min(r, 1.0) - inner) / (1.0 - inner)


def collaboration_polygon(
    r_min: float, r_max: float, inner: float = SIMPLE_EDGE
) -> list[tuple[float, float]]:
    """Return the corners of the band around y = x between two radii, in data units."""
    root = math.sqrt(2)
    near = collaboration_half_width(r_min, inner)
    far = collaboration_half_width(r_max, inner)
    ends = ((r_min, near), (r_max, far))
    left = [((r - w) / root, (r + w) / root) for r, w in ends]
    right = [((r + w) / root, (r - w) / root) for r, w in reversed(ends)]
    return [*left, *right]


def collaboration_zones(zones: Sequence[Zone], top: float, inner: float) -> tuple[Zone, ...]:
    """Return the bands whose far edge carries a collaboration band wider than 0."""
    return tuple(z for z in zones if collaboration_half_width(min(z.r_max, top), inner) > 0)


def collaboration_polygons(
    zones: Sequence[Zone], top: float, inner: float
) -> tuple[list[tuple[float, float]], ...]:
    """Return one band polygon per zone with a far width above 0; Simple yields none."""
    return tuple(
        collaboration_polygon(z.r_min, min(z.r_max, top), inner)
        for z in collaboration_zones(zones, top, inner)
    )


def tex_escape(text: str) -> str:
    """Escape the LaTeX specials the zone texts can hold."""
    return "".join(
        {"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$"}.get(c, c) for c in text
    )


def zones_items(zones: Sequence[Zone]) -> str:
    """Return a LaTeX itemize listing each band's label and its above-the-Who definition."""
    items = [rf"\item \textbf{{{tex_escape(z.label)}}}: {tex_escape(z.above)}" for z in zones]
    return "\n".join([r"\begin{itemize}\footnotesize", *items, r"\end{itemize}", ""])


def draw(
    route: Sequence[Spot],
    zones: Sequence[Zone],
    labels: Mapping[str, str],
    out: Path,
    highlight: str | None = None,
    plain: bool = False,
    arrows: bool = False,
) -> Path:
    """Draw the matrix; with highlight, the stop of that section stands out and the rest fade.

    With plain, only the bands, their names, the Who diagonal, the axes and the stops are drawn.
    With arrows, a grey arrow joins each stop to the next, up to the highlighted stop.
    """
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import Circle, Polygon, Wedge

    fig, ax = plt.subplots(figsize=FIGURE, dpi=style.DPI)
    for zone, key in reversed(list(zip(zones, ZONE_COLOURS, strict=True))):
        ax.add_patch(
            Wedge(
                (0, 0), zone.r_max, 0, 90, facecolor=colour_of(key), alpha=0.28, edgecolor="white"
            )
        )
    # Zones run innermost first; Chaos is last and gets the strongest shade.
    top = LIMIT * math.sqrt(2)
    alpha_of = dict(zip((z.key for z in zones), reversed(COLLABORATION_ALPHA), strict=True))
    banded = collaboration_zones(zones, top, zones[0].r_max)
    for zone, corners in zip(
        banded, collaboration_polygons(zones, top, zones[0].r_max), strict=True
    ):
        ax.add_patch(
            Polygon(
                corners,
                facecolor="grey",
                alpha=alpha_of[zone.key],
                edgecolor="none",
                zorder=1.5,
            )
        )
    ax.text(
        0.40,
        0.94,
        "collaboration",
        ha="center",
        va="center",
        fontsize=14,
        color="dimgrey",
        rotation=45,
        zorder=6,
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
    for zone in zones:
        cx, cy = band_anchor(zone, route)
        ax.text(
            cx,
            cy,
            zone.label,
            ha="left" if zone is zones[0] else "center",
            va="center",
            fontsize=ZONE_NAME_SIZE,
            fontweight="bold",
            zorder=3,
        )
    above, below = corner_texts(labels)
    ax.text(0.02, LIMIT - 0.02, above, ha="left", va="top", fontsize=13, color="dimgrey", zorder=6)
    ax.text(
        LIMIT - 0.02, 0.02, below, ha="right", va="bottom", fontsize=13, color="dimgrey", zorder=6
    )
    if arrows:
        at = {s.section: s for s in route}
        for a, b in arrow_pairs(route, highlight):
            ax.annotate(
                "",
                xy=(at[b].x, at[b].y),
                xytext=(at[a].x, at[a].y),
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": "grey",
                    "linewidth": 2.5,
                    "shrinkA": 17,
                    "shrinkB": 24,
                    "mutation_scale": 22,
                },
                zorder=3.5,
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
    ax.text(LIMIT / 2, -0.1, labels["x_axis"], ha="center", va="top", fontsize=13, color="dimgrey")
    ax.text(
        -0.11,
        LIMIT / 2,
        labels["y_axis"],
        ha="right",
        va="center",
        fontsize=13,
        color="dimgrey",
        rotation=90,
    )
    ax.set_xlim(-0.17, LIMIT)
    ax.set_ylim(-0.17, LIMIT)
    ax.set_aspect("equal")
    ticks = [0.0, 0.25, 0.5, 0.75, 1.0]
    ax.set_xticks(ticks, ["0", "25", "50", "75", "100"], fontsize=12, color="dimgrey")
    ax.set_yticks(ticks, ["0", "25", "50", "75", "100"], fontsize=12, color="dimgrey")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color("dimgrey")
        ax.spines[side].set_bounds(0, 1.0)
        ax.spines[side].set_position(("data", 0))
    ax.tick_params(colors="dimgrey")
    fig.tight_layout()
    style.save(fig, out)
    return out
