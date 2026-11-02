"""The finance chart: October's expected shipping income by week, received against missing."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils.palette import colour_of

FIGSIZE = (8.0, 3.5)
FONTSIZE = 12


@dataclass(frozen=True)
class Week:
    week: int
    monday: str
    free_orders: int
    expected_bgn: int
    received_bgn: int

    @property
    def shortfall_bgn(self) -> int:
        return self.expected_bgn - self.received_bgn


def load_october(path: Path) -> tuple[Week, ...]:
    """Read the weeks of october.csv in file order; raises FileNotFoundError naming the path."""
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(
            Week(
                int(row["week"]),
                row["monday"],
                int(row["got_free_shipping"]),
                int(row["expected_bgn"]),
                int(row["received_bgn"]),
            )
            for row in csv.DictReader(fh)
        )


def totals(weeks: Sequence[Week]) -> tuple[int, int]:
    """Return (free-shipping orders, missing BGN) summed over the weeks."""
    return (sum(w.free_orders for w in weeks), sum(w.shortfall_bgn for w in weeks))


def title(weeks: Sequence[Week]) -> str:
    """Return the chart title quoting the October totals, with thousands separators."""
    orders, bgn = totals(weeks)
    return f"October: {bgn:,} BGN of shipping never charged, {orders:,} parcels"


def draw(weeks: Sequence[Week], out: Path) -> Path:
    """Draw one stacked bar per week: received below, the shortfall above, exact BGN on each."""
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt

    top = max(w.expected_bgn for w in weeks)
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=style.DPI)
    for x, w in enumerate(weeks):
        for name, bottom, value, key, ink in (
            ("received", 0, w.received_bgn, "logistics", "white"),
            ("missing", w.received_bgn, w.shortfall_bgn, "marketing", "black"),
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
        ax.text(
            x,
            w.expected_bgn,
            f"{w.expected_bgn:,}",
            ha="center",
            va="bottom",
            fontsize=FONTSIZE,
            fontweight="bold",
        )
    ax.set_xticks(range(len(weeks)), [f"Mon {w.monday}" for w in weeks], fontsize=FONTSIZE)
    ax.set_title(title(weeks), fontsize=FONTSIZE, fontweight="bold")
    ax.set_ylim(0, top * 1.2)
    ax.set_ylabel("shipping income, BGN", fontsize=FONTSIZE)
    ax.tick_params(labelsize=FONTSIZE)
    ax.legend(frameon=False, loc="upper left", fontsize=FONTSIZE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    style.save(fig, out)
    return out
