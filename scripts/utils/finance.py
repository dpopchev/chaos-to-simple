"""The finance chart: October's expected shipping income by week, received against missing."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils.palette import colour_of

FIGSIZE = (8.0, 3.5)
FONTSIZE = 12
PARCEL_EUR = 5
LEGEND = (
    "expected: the bar, 5 EUR on every parcel",
    "received: what the code charged (R1)",
    "missing: what finance expected (R2)",
)


@dataclass(frozen=True)
class Week:
    week: int
    monday: str
    free_orders: int
    expected_eur: int
    received_eur: int
    free_with_coupon: int
    free_without_coupon: int

    @property
    def shortfall_eur(self) -> int:
        return self.expected_eur - self.received_eur


def load_october(path: Path) -> tuple[Week, ...]:
    """Read the weeks of october.csv in file order; raises FileNotFoundError naming the path."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Week(
                int(row["week"]),
                row["monday"],
                int(row["got_free_shipping"]),
                int(row["expected_eur"]),
                int(row["received_eur"]),
                int(row["free_with_coupon"]),
                int(row["free_without_coupon"]),
            )
            for row in csv.DictReader(fh)
        )


def totals(weeks: Sequence[Week]) -> tuple[int, int]:
    """Return (free-shipping orders, missing EUR) summed over the weeks."""
    return (sum(w.free_orders for w in weeks), sum(w.shortfall_eur for w in weeks))


def cues(weeks: Sequence[Week]) -> str:
    """Return the coupon cue table, one row per week and a total, within 49 columns."""
    head = f"{'week':<6}{'<50':>6}{'free':>6}{'coupon':>8}{'none':>6}"
    rows = [
        f"{w.week:<6}{w.expected_eur // PARCEL_EUR:>6}{w.free_orders:>6}"
        f"{w.free_with_coupon:>8}{w.free_without_coupon:>6}"
        for w in weeks
    ]
    total = (
        f"{'total':<6}{sum(w.expected_eur for w in weeks) // PARCEL_EUR:>6}"
        f"{sum(w.free_orders for w in weeks):>6}"
        f"{sum(w.free_with_coupon for w in weeks):>8}"
        f"{sum(w.free_without_coupon for w in weeks):>6}"
    )
    closing = ("every free parcel carried the coupon;", "none without it")
    return "\n".join([head, *rows, total, "", *closing]) + "\n"


def title(weeks: Sequence[Week]) -> str:
    """Return the chart title quoting the October totals, with thousands separators."""
    orders, eur = totals(weeks)
    return f"October: {eur:,} EUR of shipping nowhere to be found, {orders:,} parcels"


def draw(weeks: Sequence[Week], out: Path) -> Path:
    """Draw one stacked bar per week: received below, the shortfall above, exact EUR on each."""
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt

    top = max(w.expected_eur for w in weeks)
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=style.DPI)
    for x, w in enumerate(weeks):
        for name, bottom, value, key, ink in (
            (LEGEND[1], 0, w.received_eur, "logistics", "white"),
            (LEGEND[2], w.received_eur, w.shortfall_eur, "marketing", "black"),
        ):
            ax.bar(
                x,
                value,
                bottom=bottom,
                width=0.6,
                color=colour_of(key),
                edgecolor="white",
                linewidth=0.8,
                label=name if x == 0 else None,
            )
            ax.text(
                x,
                bottom + value / 2,
                f"{value:,}",
                ha="center",
                va="center",
                fontsize=FONTSIZE,
                color=ink,
            )
        ax.bar(
            x,
            w.expected_eur,
            width=0.6,
            fill=False,
            edgecolor="black",
            linewidth=1.5,
            label=LEGEND[0] if x == 0 else None,
        )
        ax.text(
            x,
            w.expected_eur,
            f"{w.expected_eur:,}",
            ha="center",
            va="bottom",
            fontsize=FONTSIZE,
            fontweight="bold",
        )
    ax.set_xticks(range(len(weeks)), [f"Mon {w.monday}" for w in weeks], fontsize=FONTSIZE)
    ax.set_title(title(weeks), fontsize=FONTSIZE, fontweight="bold")
    ax.set_ylim(0, top * 1.55)
    ax.set_ylabel("shipping income, EUR", fontsize=FONTSIZE)
    ax.tick_params(labelsize=FONTSIZE)
    by_name = dict(zip(*reversed(ax.get_legend_handles_labels()), strict=True))
    handles = [by_name[name] for name in LEGEND]
    ax.legend(handles, LEGEND, frameon=False, loc="upper left", fontsize=FONTSIZE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    style.save(fig, out)
    return out
