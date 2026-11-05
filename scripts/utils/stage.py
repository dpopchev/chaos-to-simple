"""The stage of the talk: the shop in the middle, who talks to it around it, drawn once."""

from __future__ import annotations

import csv
import textwrap
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style
from scripts.utils.figures import arrow_style, icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, glyph, icon_size
from scripts.utils.palette import Actor, Context, colour_of, kind_style, load_contexts
from scripts.utils.paths import CastRow, Incident, Rule
from scripts.utils.stacey import ZONE_COLOURS, Zone, band_colour, load_zones

CUSTOMER_WORDS = "places an order"
BOX_W, BOX_H = 2.7, 0.8
SHOP_W, SHOP_H = 3.9, 6.4
DEPARTMENT_W, DEPARTMENT_MARGIN = 4.3, 0.1
DEPARTMENT_X, PROVIDER_X, CUSTOMER_Y = -5.4, 5.9, SHOP_H / 2 + 1.5
WRAP = 22
LEGEND_Y = -SHOP_H / 2 - 0.65
REQUEST_WRAP = 28
REQUEST_FONT = 12
LINE_STEP = 0.44
FIGSIZE_MAP = (12.8, 6.0)


def department_box_height(lines: int) -> float:
    """Return the height of a department box that holds this many request lines."""
    return BOX_H + LINE_STEP * lines


def request_text(requests: Sequence[str]) -> str:
    """Return the requests as bullets, one per request, a long one wrapped onto more lines."""
    return "\n".join(
        textwrap.fill(r, REQUEST_WRAP, initial_indent="\N{BULLET} ", subsequent_indent="  ")
        for r in requests
    )


@dataclass(frozen=True)
class Stop:
    """One section of the talk: its pictogram, label and counter, the incident it tells."""

    section: str
    label: str
    icon: str
    counter: str
    incident: str
    x: float | None = None
    y: float | None = None


def load_route(path: Path) -> tuple[Stop, ...]:
    """Read the stops of the agenda from data/route.csv, in section order."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Stop(
                row["section"],
                row["label"],
                row["icon"],
                row["counter"],
                row["incident"],
                float(row["x"]) if row["x"] else None,
                float(row["y"]) if row["y"] else None,
            )
            for row in csv.DictReader(fh)
        )


def incident_marks(incidents: Iterable[Incident]) -> dict[str, str]:
    """Return the incident id each section tells, keyed by section."""
    return {i.told_in: i.id for i in incidents}


ZONES_CSV = Path(__file__).resolve().parents[2] / "02-stacey" / "data" / "zones.csv"
GREY = "#7F7F7F"
STOP_W, STOP_H, PITCH = 0.9, 1.5, 1.05


def stop_face(stop: Stop, zones: Sequence[Zone]) -> str:
    """Return the colour of the Stacey band the stop sits in, grey for a stop off the matrix."""
    if stop.x is None or stop.y is None:
        return GREY
    return colour_of(band_colour(stop.x, stop.y, zones))


FADED = 0.25


def stop_alpha(section: str, highlight: str | None) -> float:
    """Return 1.0 for the highlighted stop or when none is highlighted, FADED otherwise."""
    return 1.0 if highlight is None or section == highlight else FADED


def agenda_strip(
    route: Sequence[Stop],
    incidents: Iterable[Incident],
    out: Path,
    highlight: str | None = None,
    zones: Sequence[Zone] | None = None,
) -> Path:
    """Draw the agenda: a box per stop left to right, pictogram and label inside, counter below.

    A stop is coloured by its Stacey band (the zones of 02-stacey by default); a legend under
    the strip explains the incident mark and the four bands.

    A stop whose section an incident is told in carries that incident's mark on its corner.
    With a highlight, that stop gets a black edge and every other stop fades with its counter.
    """
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    marks = incident_marks(incidents)
    bands = tuple(zones) if zones is not None else load_zones(ZONES_CSV)
    font = icon_file()
    fig, ax = plt.subplots(figsize=(11.0, 4.0), dpi=style.DPI)
    for i, stop in enumerate(route):
        x = i * PITCH
        face = stop_face(stop, bands)
        ink = label_ink(face)
        alpha = stop_alpha(stop.section, highlight)
        picked = highlight is not None and stop.section == highlight
        ax.add_patch(
            FancyBboxPatch(
                (x - STOP_W / 2, -STOP_H / 2),
                STOP_W,
                STOP_H,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=face,
                edgecolor="black" if picked else "none",
                linewidth=3 if picked else 0,
                alpha=alpha,
                zorder=3,
            )
        )
        if font is not None:
            ax.text(
                x,
                0.3,
                glyph(stop.icon, FONT_AWESOME),
                ha="center",
                va="center",
                fontproperties=FontProperties(fname=font, size=26),
                color=ink,
                alpha=alpha,
                zorder=4,
            )
        ax.text(
            x,
            -0.3,
            f"{stop.section}\n{textwrap.fill(stop.label, 9)}",
            ha="center",
            va="center",
            fontsize=10,
            color=ink,
            alpha=alpha,
            zorder=4,
        )
        if font is not None:
            ax.text(
                x - 0.3,
                -STOP_H / 2 - 0.22,
                glyph("code-branch", FONT_AWESOME),
                ha="center",
                va="center",
                fontproperties=FontProperties(fname=font, size=12),
                alpha=alpha,
                zorder=4,
            )
        ax.text(
            x + (0.1 if font is not None else 0.0),
            -STOP_H / 2 - 0.22,
            stop.counter,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            alpha=alpha,
            zorder=4,
        )
        if i + 1 < len(route):
            ax.annotate(
                "",
                (x + PITCH - STOP_W / 2 - 0.04, 0),
                (x + STOP_W / 2 + 0.04, 0),
                arrowprops={"arrowstyle": "-|>", "color": "dimgrey", "linewidth": 1.5},
                zorder=2,
            )
        if stop.section in marks:
            ax.text(
                x + STOP_W / 2 - 0.05,
                STOP_H / 2 + 0.05,
                marks[stop.section],
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color="white",
                bbox={"boxstyle": "circle,pad=0.3", "facecolor": "black", "edgecolor": "none"},
                zorder=5,
            )
    ax.text(
        -0.45,
        -1.6,
        "I1",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="white",
        bbox={"boxstyle": "circle,pad=0.3", "facecolor": "black", "edgecolor": "none"},
    )
    ax.text(-0.2, -1.6, "I1 I2 I3: the incident told at this stop", va="center", fontsize=11)
    for j, zone in enumerate(bands):
        cx = -0.55 + j * 2.1
        ax.add_patch(
            FancyBboxPatch(
                (cx, -2.0),
                0.35,
                0.25,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor=colour_of(ZONE_COLOURS[j]),
                edgecolor="none",
            )
        )
        ax.text(cx + 0.45, -1.875, zone.label, va="center", fontsize=11)
    ax.set_xlim(-0.6, (len(route) - 1) * PITCH + 0.6)
    ax.set_ylim(-2.2, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out


def edge_words(
    actors: Mapping[str, Actor], cast: Sequence[CastRow], rules: Sequence[Rule]
) -> dict[str, str]:
    """Return what each actor but the shop says to it: a department's requests, a provider's answer.

    The customer places an order; a department's words are its cast rows joined by '; '; a
    provider's text is the sum type of its shell rule.
    """
    answer = {rule.bit: rule.code for rule in rules if rule.scope == "shell"}
    words: dict[str, str] = {}
    for key, actor in actors.items():
        rows = [c for c in cast if c.requested_by == key]
        match actor.kind:
            case "customer":
                words[key] = CUSTOMER_WORDS
            case "department":
                words[key] = "; ".join(c.words for c in rows)
            case "provider":
                words[key] = "; ".join(answer[c.bit] for c in rows)
    return words


def department_bullets(
    actors: Mapping[str, Actor], cast: Sequence[CastRow]
) -> dict[str, tuple[str, ...]]:
    """Return each department's requests, one per cast row, in cast order."""
    return {
        key: tuple(c.words for c in cast if c.requested_by == key)
        for key, actor in actors.items()
        if actor.kind == "department"
    }


def department_heights(bullets: Mapping[str, tuple[str, ...]]) -> dict[str, float]:
    """Return each department box's height, from the lines its requests take wrapped."""
    return {
        key: department_box_height(request_text(requests).count("\n") + 1)
        for key, requests in bullets.items()
    }


def department_centres(heights: Sequence[float]) -> tuple[float, ...]:
    """Return the box centres top to bottom, evenly gapped so the column spans the shop."""
    span = SHOP_H - 2 * DEPARTMENT_MARGIN
    gap = (span - sum(heights)) / max(len(heights) - 1, 1)
    centres: list[float] = []
    top = SHOP_H / 2 - DEPARTMENT_MARGIN
    for h in heights:
        centres.append(top - h / 2)
        top -= h + gap
    return tuple(centres)


def positions(
    actors: Mapping[str, Actor], heights: Mapping[str, float]
) -> dict[str, tuple[float, float]]:
    """Place the shop at the origin, departments left, providers right, the customer on top.

    The departments are spaced by their box heights so their column spans the shop.
    """
    spots: dict[str, tuple[float, float]] = {}
    departments = [k for k, a in actors.items() if a.kind == "department"]
    centres = department_centres([heights[k] for k in departments])
    for key, cy in zip(departments, centres, strict=True):
        spots[key] = (DEPARTMENT_X, cy)
    keys = [k for k, a in actors.items() if a.kind == "provider"]
    for i, key in enumerate(keys):
        spots[key] = (PROVIDER_X, (len(keys) - 1) / 2 * 2.2 - i * 2.2)
    for key, actor in actors.items():
        if actor.kind == "customer":
            spots[key] = (0.0, CUSTOMER_Y)
        elif actor.kind == "dev":
            spots[key] = (0.0, 0.0)
    return spots


def map_legend() -> tuple[tuple[str, str], ...]:
    """Return the strategic legend of the map: each line's words and how its box is drawn."""
    return (
        ("core subdomain: the shop wins the sale", "core"),
        ("supporting subdomain: the shop's own rules", "supporting"),
        ("generic subdomain: bought, adapted", "generic"),
    )


BAND_H, BAND_GAP = 0.95, 0.12
CHIP_H = 0.4


def band_title(ctx: Context) -> str:
    """Return the band's title: the context label and its subdomain kind in brackets."""
    return f"{ctx.label} ({ctx.kind})"


def inner_bands(
    contexts: Mapping[str, Context], actors: Mapping[str, Actor]
) -> tuple[tuple[Context, tuple[str, ...]], ...]:
    """Return the in-house contexts no provider owns, each with its owner keys."""
    bands: list[tuple[Context, tuple[str, ...]]] = []
    for ctx in contexts.values():
        owners = tuple(o for o in ctx.owner.split(";") if o)
        if ctx.kind not in ("core", "supporting", "generic"):
            continue
        if any(o in actors and actors[o].kind == "provider" for o in owners):
            continue
        bands.append((ctx, owners))
    return tuple(bands)


def business_map(
    actors: Mapping[str, Actor],
    cast: Sequence[CastRow],
    rules: Sequence[Rule],
    out: Path,
    undivided: bool = False,
) -> Path:
    """Draw the business map: a box and pictogram per actor, an edge with its words to the shop.

    The shop is the outlined core; a department asks, a provider is called and answers back.
    With undivided the shop holds one tangled 'checkout()' band and the kind legend is left out.
    """
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    words = edge_words(actors, cast, rules)
    bullets = department_bullets(actors, cast)
    spots = positions(actors, department_heights(bullets))
    font = icon_file()
    shape = "round,pad=0.05,rounding_size=0.15"
    generic = kind_style("generic")
    fig, ax = plt.subplots(figsize=FIGSIZE_MAP, dpi=style.DPI)
    for key, actor in actors.items():
        x, y = spots[key]
        is_shop = actor.kind == "dev"
        text_y = y + SHOP_H / 2 - 0.4 if is_shop else y
        is_department = actor.kind == "department"
        w, h = (SHOP_W, SHOP_H) if is_shop else (BOX_W, BOX_H)
        w = DEPARTMENT_W if is_department else w
        request_block = request_text(bullets[key]) if is_department else ""
        if is_department:
            h = department_box_height(request_block.count("\n") + 1)
        actor_colour = colour_of(key)
        is_provider = actor.kind == "provider"
        face = "white" if is_shop else generic.face if is_provider else actor_colour
        ink = "black" if is_shop or is_provider else label_ink(face)
        if not is_shop:
            side = 0.0 if actor.kind == "customer" else (1.0 if x < 0 else -1.0)
            both = actor.kind == "provider"
            lift = 0.18 if both else 0.0
            if side:
                tail = (x + side * (w / 2 + 0.1), y + lift)
                head = (-side * (SHOP_W / 2 + 0.1), y + lift)
            else:
                tail = (x, y - h / 2 - 0.1)
                head = (x, SHOP_H / 2 + 0.1)
            arrow = {
                "color": actor_colour if key != "mailer" else "dimgrey",
                "linewidth": 2.0,
                "shrinkA": 0,
                "shrinkB": 0,
            }
            answer = arrow_style("outcome" if both else "call")
            ax.annotate("", head, tail, arrowprops={**arrow, **answer}, zorder=1)
            if both:
                call = ((tail[0], y - lift), (head[0], y - lift))
                ax.annotate("", *call, arrowprops={**arrow, **arrow_style("call")}, zorder=1)
            if not is_department:
                ax.text(
                    (tail[0] + head[0]) / 2 + (0.15 if not side else 0.0),
                    (tail[1] + head[1]) / 2 + (0.0 if not side else 0.12),
                    textwrap.fill(words[key], WRAP),
                    ha="left" if not side else "center",
                    va="center" if not side else "bottom",
                    fontsize=11,
                    style="italic",
                    zorder=5,
                )
        ax.add_patch(
            FancyBboxPatch(
                (x - w / 2, y - h / 2),
                w,
                h,
                boxstyle=shape,
                facecolor=face,
                edgecolor="black" if is_shop else "none",
                linewidth=3 if is_shop else 0,
                zorder=3,
            )
        )
        if font is not None:
            ax.text(
                x - w / 2 + 0.15,
                text_y,
                glyph(actor.icon, FONT_AWESOME),
                ha="left",
                va="center",
                fontproperties=FontProperties(fname=font, size=icon_size(13)),
                color=ink,
                zorder=4,
            )
        if is_department:
            ax.text(
                x - w / 2 + 0.65,
                y,
                request_block,
                ha="left",
                va="center",
                fontsize=REQUEST_FONT,
                color=ink,
                zorder=4,
            )
        else:
            ax.text(
                x + (0.25 if font is not None else 0.0),
                text_y,
                actor.label.replace(" (", "\n(") if not is_shop else actor.label,
                ha="center",
                va="center",
                fontsize=13 if not is_shop else 12,
                color=ink,
                zorder=4,
            )
    bands = () if undivided else inner_bands(load_contexts(), actors)
    top = SHOP_H / 2 - 0.85
    if undivided:
        cy = top - BAND_H / 2
        ax.add_patch(
            FancyBboxPatch(
                (-SHOP_W / 2 + 0.2, cy - BAND_H / 2),
                SHOP_W - 0.4,
                BAND_H,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=colour_of("tangled"),
                edgecolor="none",
                zorder=4,
            )
        )
        ax.text(0, cy, "checkout()", ha="center", va="center", fontsize=12, zorder=5)
    for i, (ctx, owners) in enumerate(bands):
        kind = kind_style(ctx.kind)
        cy = top - BAND_H / 2 - i * (BAND_H + BAND_GAP)
        ax.add_patch(
            FancyBboxPatch(
                (-SHOP_W / 2 + 0.2, cy - BAND_H / 2),
                SHOP_W - 0.4,
                BAND_H,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=kind.face,
                edgecolor=kind.edge,
                linestyle=kind.linestyle,
                linewidth=2.5 if kind.edge != "none" else 0,
                zorder=4,
            )
        )
        ax.text(0, cy + 0.27, band_title(ctx), ha="center", va="center", fontsize=12, zorder=5)
        widths = [0.5 + 0.09 * len(actors[o].label if o in actors else o) for o in owners]
        left = -(sum(widths) + 0.1 * (len(owners) - 1)) / 2
        for o, cw in zip(owners, widths, strict=True):
            label = actors[o].label if o in actors else o.capitalize()
            ax.add_patch(
                FancyBboxPatch(
                    (left, cy - 0.3 - CHIP_H / 2 + 0.12),
                    cw,
                    CHIP_H,
                    boxstyle="round,pad=0.02,rounding_size=0.1",
                    facecolor=colour_of(o) if o in actors else GREY,
                    edgecolor="none",
                    zorder=5,
                )
            )
            chip_ink = label_ink(colour_of(o) if o in actors else GREY)
            if font is not None and o in actors:
                ax.text(
                    left + 0.17,
                    cy - 0.18,
                    glyph(actors[o].icon, FONT_AWESOME),
                    ha="center",
                    va="center",
                    fontproperties=FontProperties(fname=font, size=icon_size(8)),
                    color=chip_ink,
                    zorder=6,
                )
            ax.text(
                left + cw / 2 + 0.1,
                cy - 0.18,
                label,
                ha="center",
                va="center",
                fontsize=8,
                color=chip_ink,
                zorder=6,
            )
            left += cw + 0.1
    for i, (text, kind_name) in enumerate(() if undivided else map_legend()):
        kind = kind_style(kind_name)
        lx = -7.4 + i * 5.0
        ax.add_patch(
            FancyBboxPatch(
                (lx, LEGEND_Y - 0.15),
                0.5,
                0.3,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                facecolor=kind.face,
                edgecolor=kind.edge,
                linestyle=kind.linestyle,
                linewidth=2.5 if kind.edge != "none" else 0,
            )
        )
        ax.text(lx + 0.65, LEGEND_Y, text, ha="left", va="center", fontsize=10)
    ax.set_xlim(-7.6, 7.6)
    ax.set_ylim(LEGEND_Y - 0.5, CUSTOMER_Y + 0.9)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
