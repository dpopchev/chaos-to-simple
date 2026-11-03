"""Count the paths through a graph of blocks in sequence, and draw three examples side by side."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from pathlib import Path

from scripts.utils import style

MONO = ["Adwaita Mono", "DejaVu Sans Mono"]
GENERAL_FORM = "paths = the product of each block's alternatives"


@dataclass(frozen=True)
class Block:
    """One decision with its alternatives: an if has two, an if/elif/else three."""

    name: str
    alternatives: tuple[str, ...]


@dataclass(frozen=True)
class Graph:
    """Blocks run in sequence; a path picks one alternative in every block."""

    title: str
    blocks: tuple[Block, ...]


TWO_IFS = Graph(
    "two ifs",
    (Block("coupon?", ("no", "yes")), Block("member?", ("no", "yes"))),
)
IF_ELIF = Graph("if / elif / else", (Block("order?", ("if", "elif", "else")),))
THREE_IFS = Graph(
    "three ifs",
    (
        Block("coupon?", ("no", "yes")),
        Block("member?", ("no", "yes")),
        Block("gift?", ("no", "yes")),
    ),
)
EXAMPLES = (TWO_IFS, IF_ELIF, THREE_IFS)


def paths_of(graph: Graph) -> int:
    """Return the product of the alternative counts of the blocks."""
    return math.prod(len(block.alternatives) for block in graph.blocks)


def bit_strings(graph: Graph) -> tuple[str, ...]:
    """Return every path as the chosen alternative index of each block, in block order."""
    choices = (range(len(block.alternatives)) for block in graph.blocks)
    return tuple("".join(map(str, path)) for path in itertools.product(*choices))


def sum_text(graph: Graph) -> str:
    """Return the count line: '2 x 2 = 4 paths', or '3 paths' for a single block."""
    counts = [str(len(block.alternatives)) for block in graph.blocks]
    if len(counts) == 1:
        return f"{paths_of(graph)} paths"
    return f"{' x '.join(counts)} = {paths_of(graph)} paths"


def rows_of(graph: Graph) -> tuple[str, str]:
    """Return the count row and the bit-string row, centred to one width for a monospace grid."""
    count_row = sum_text(graph)
    bits_row = " ".join(bit_strings(graph))
    width = max(len(count_row), len(bits_row))
    return count_row.center(width), bits_row.center(width)


def counting_figure(out: Path) -> Path:
    """Draw the examples as diamonds and arrows with count and bit strings; the form under them."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.75)
    ax.axis("off")
    arrow = {"arrowstyle": "-|>", "color": "black", "linewidth": 1.2}
    chip = {"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "grey"}
    for k, graph in enumerate(EXAMPLES):
        spine = 4 * k + 1.0
        ax.text(
            spine + 0.9, 6.55, graph.title, ha="center", va="center", fontsize=14, weight="bold"
        )
        ys = [5.3 - 1.3 * i for i in range(len(graph.blocks))]
        for i, (block, y) in enumerate(zip(graph.blocks, ys, strict=True)):
            ax.add_patch(
                Polygon(
                    [(spine - 0.8, y), (spine, y + 0.42), (spine + 0.8, y), (spine, y - 0.42)],
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.4,
                )
            )
            ax.text(spine, y, block.name, ha="center", va="center", fontsize=10)
            n = len(block.alternatives)
            for j, alt in enumerate(block.alternatives):
                cy = y + (n - 1) / 2 * 0.55 - j * 0.55
                ax.annotate("", (spine + 1.45, cy), (spine + 0.65, y), arrowprops=arrow)
                ax.text(
                    spine + 2.05, cy, f"{j} {alt}", ha="center", va="center", fontsize=11, bbox=chip
                )
            if i + 1 < len(graph.blocks):
                ax.annotate("", (spine, ys[i + 1] + 0.45), (spine, y - 0.45), arrowprops=arrow)
        for text, y in zip(rows_of(graph), (1.7, 1.15), strict=True):
            ax.text(
                spine + 0.9,
                y,
                text,
                ha="center",
                va="center",
                fontsize=9,
                family=MONO,
            )
    ax.text(6.0, 0.2, GENERAL_FORM, ha="center", va="center", fontsize=15, weight="bold")
    style.save(fig, out)
    return out
