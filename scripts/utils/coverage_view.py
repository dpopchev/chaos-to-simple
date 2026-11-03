"""Draw what branch coverage saw: the tested bit strings by column beside the 8x8 grid."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style
from scripts.utils.palette import colour_of

BITS = 6
GRID_SIDE = 8


@dataclass(frozen=True)
class TestedRow:
    """One test of the checkout: its name, the bit string it runs, tested or bug."""

    __test__ = False

    name: str
    bits: str
    kind: str


def load_tested(path: Path) -> tuple[TestedRow, ...]:
    """Read the tests by file order; every bit string is BITS characters of 0 and 1."""
    with path.open(newline="", encoding="ascii") as fh:
        rows = tuple(TestedRow(r["name"], r["bits"], r["kind"]) for r in csv.DictReader(fh))
    for row in rows:
        if len(row.bits) != BITS or set(row.bits) - {"0", "1"}:
            raise ValueError(f"{path}: {row.name} bits {row.bits!r} is not {BITS} of 0 and 1")
    return rows


def columns_covered(rows: Sequence[TestedRow]) -> tuple[bool, ...]:
    """Mark each column, left to right, True when both 0 and 1 occur in it."""
    return tuple({row.bits[i] for row in rows} == {"0", "1"} for i in range(BITS))


def differing_bits(left: str, right: str) -> tuple[int, ...]:
    """Return the bit numbers where two strings differ, b0 being the rightmost character."""
    return tuple(b for b in range(BITS) if left[BITS - 1 - b] != right[BITS - 1 - b])


def growth_panels(
    bits: int, tested: Sequence[str], bug: Sequence[str]
) -> tuple[tuple[int, dict[str, str]], ...]:
    """Give the grids of 0 to bits bits as (n, cells): each n-bit string is tested, bug or never.

    The all-zeros and all-ones strings are tested in every panel; the last panel takes the
    tested and bug codes as grid_image does.
    """
    panels = []
    for n in range(bits + 1):
        strings = [f"{i:0{n}b}" if n else "" for i in range(2**n)]
        if n == bits:
            cells = {
                s: "bug" if s in bug else "tested" if s in tested else "never" for s in strings
            }
        else:
            edge = {"0" * n, "1" * n}
            cells = {s: "tested" if s in edge else "never" for s in strings}
        panels.append((n, cells))
    return tuple(panels)


def grid_growth(bits: int, tested: Sequence[str], bug: Sequence[str], out: Path) -> Path:
    """Draw the grids of 0 to bits bits left to right, 2^n = N under each, two rows."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fills = {
        "tested": colour_of("accounting"),
        "bug": colour_of("payment"),
        "never": colour_of("customer"),
    }
    panels = growth_panels(bits, tested, bug)
    per_row = (len(panels) + 1) // 2
    fig, ax = plt.subplots(figsize=(8.0, 4.6), dpi=style.DPI)
    slot, gap = 8.0, 3.0
    for index, (n, cells) in enumerate(panels):
        row, col = divmod(index, per_row)
        x0 = col * (slot + gap)
        y0 = -row * (slot + gap + 1.5)
        cols, rows = 2 ** ((n + 1) // 2), 2 ** (n // 2)
        size = slot / max(cols, rows)
        for i, kind in enumerate(cells.values()):
            r, c = divmod(i, cols)
            ax.add_patch(
                Rectangle(
                    (
                        x0 + (slot - cols * size) / 2 + c * size,
                        y0 - (r + 1) * size - (slot - rows * size) / 2,
                    ),
                    size * 0.92,
                    size * 0.92,
                    facecolor=fills[kind],
                    edgecolor="none",
                )
            )
        ax.text(
            x0 + slot / 2, y0 - slot - 0.8, f"2^{n} = {2**n}", ha="center", va="top", fontsize=15
        )
    ax.set_xlim(-0.2, per_row * (slot + gap) - gap + 0.2)
    ax.set_ylim(-2 * slot - gap - 1.5 - 2.2, 0.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0.3)
    style.save(fig, out)
    return out


def draw(rows: Sequence[TestedRow], out: Path) -> Path:
    """Draw the two views stacked: columns marked covered above, the grid of 64 paths below."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    green, grey = colour_of("accounting"), colour_of("customer")
    tested = [row for row in rows if row.kind == "tested"]
    covered = columns_covered(tested)
    fig, (left, right) = plt.subplots(
        2, 1, figsize=(5.0, 6.0), dpi=style.DPI, gridspec_kw={"height_ratios": [1, 1.5]}
    )
    for col in range(BITS):
        x = col * 1.1
        left.text(x, 2.9, f"b{BITS - 1 - col}", ha="center", va="center", fontsize=14)
        for line, row in enumerate(tested):
            y = 1.9 - line * 1.1
            left.add_patch(
                Rectangle((x - 0.45, y - 0.45), 0.9, 0.9, facecolor=green, edgecolor="none")
            )
            left.text(x, y, row.bits[col], ha="center", va="center", fontsize=20, color="white")
        mark = green if covered[col] else grey
        left.add_patch(Rectangle((x - 0.45, -0.55), 0.9, 0.4, facecolor=mark, edgecolor="none"))
        left.text(x, -0.35, "both", ha="center", va="center", fontsize=11, color="white")
    left.set_title("two tests, both values of every column", fontsize=15)
    left.set_xlim(-0.8, 6.0)
    left.set_ylim(-0.8, 3.3)
    left.set_aspect("equal")
    left.axis("off")

    hit = {int(row.bits, 2) for row in tested}
    for n in range(GRID_SIDE * GRID_SIDE):
        r, c = divmod(n, GRID_SIDE)
        right.add_patch(
            Rectangle(
                (c, GRID_SIDE - 1 - r),
                0.9,
                0.9,
                facecolor=green if n in hit else grey,
                edgecolor="none",
            )
        )
    right.set_title(f"{len(hit)} of {GRID_SIDE * GRID_SIDE} combinations", fontsize=15)
    right.set_xlim(-0.1, GRID_SIDE)
    right.set_ylim(-0.1, GRID_SIDE)
    right.set_aspect("equal")
    right.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
