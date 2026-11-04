"""Count, per source file, the names imported from the contexts, the ports and the core.

The contexts are pricing, shipping and tax; s04_what.money is a shared value type, not one.
"""

from __future__ import annotations

import ast
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from scripts.utils import palette, style

_CONTEXTS = ("s04_what.pricing", "s04_what.shipping", "s04_what.tax")
_PORTS = "s05_how.ports"
_CORE = "s06_simple.core"
_HEADS = ("module", "contexts", "ports", "core")


@dataclass(frozen=True)
class ImportRow:
    module: str
    from_contexts: int
    from_ports: int
    from_core: int


def _names_from(tree: ast.AST, *packages: str) -> int:
    """Return how many names the from-imports of the packages (or their submodules) bring in."""
    return sum(
        len(node.names)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.level == 0
        and node.module is not None
        and any(node.module == p or node.module.startswith(p + ".") for p in packages)
    )


def import_rows(name: str, text: str) -> ImportRow:
    """Return the import counts of one source text, read with ast."""
    tree = ast.parse(text)
    return ImportRow(
        name, _names_from(tree, *_CONTEXTS), _names_from(tree, _PORTS), _names_from(tree, _CORE)
    )


def import_edges(sources: Sequence[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    """Return (importer, imported) per (name, text): a context by its name, the ports as 'ports'."""
    targets = {**{c: c.rsplit(".", 1)[1] for c in _CONTEXTS}, _PORTS: "ports", _CORE: "core"}
    edges: list[tuple[str, str]] = []
    for name, text in sources:
        for node in ast.walk(ast.parse(text)):
            if not isinstance(node, ast.ImportFrom) or node.level != 0 or node.module is None:
                continue
            for package, target in targets.items():
                edge = (name, target)
                if node.module.startswith(package) and edge not in edges:
                    edges.append(edge)
    return tuple(edges)


_BOX_W = 3.2
_BOX_H = 0.68
_COL_GAP = 4.8
_ROW_GAP = 0.85
_ASPECT = 0.3
_MAX_UNIT = 0.6
_WIDTH = 10.0
_OUTLINED = ("checkout_v5", "shell", "core")


def figure_layout(edges: Sequence[tuple[str, str]]) -> dict[str, tuple[float, float]]:
    """Return name -> (x, y): a module sits one column right of its deepest importer.

    Columns stack their modules in order of first appearance, centred on y = 0, top first.
    """
    names = list(dict.fromkeys(name for edge in edges for name in edge))
    column = dict.fromkeys(names, 0)
    for _ in names:
        for importer, imported in edges:
            column[imported] = max(column[imported], column[importer] + 1)
    cols = sorted(set(column.values()))
    tallest = max(sum(1 for name in names if column[name] == col) for col in cols)
    height = (tallest - 1) * _ROW_GAP + 1.0
    gap = _COL_GAP
    if len(cols) > 1:  # widen the columns so a tall figure keeps a wide aspect
        gap = max(_COL_GAP, (height / _ASPECT - _BOX_W - 0.6) / (len(cols) - 1))
    layout: dict[str, tuple[float, float]] = {}
    for col in cols:
        members = [name for name in names if column[name] == col]
        for row, name in enumerate(members):
            layout[name] = (col * gap, ((len(members) - 1) / 2 - row) * _ROW_GAP)
    return layout


def import_figure(edges: Sequence[tuple[str, str]], out: Path) -> None:
    """Draw the modules as boxes and one arrow per (importer, imported) edge into out."""
    layout = figure_layout(edges)
    xs = [x for x, _ in layout.values()]
    ys = [y for _, y in layout.values()]
    x_lo, x_hi = min(xs) - _BOX_W / 2 - 0.3, max(xs) + _BOX_W / 2 + 0.3
    y_lo, y_hi = min(ys) - 0.55, max(ys) + 0.55
    unit = min(_WIDTH / (x_hi - x_lo), _MAX_UNIT)
    style.apply()
    fig, ax = plt.subplots(figsize=((x_hi - x_lo) * unit, (y_hi - y_lo) * unit), dpi=style.DPI)
    for name, (x, y) in layout.items():
        shell = name in _OUTLINED
        fill = "white" if shell else palette.colour_of("fulfilment" if name == "ports" else name)
        ax.add_patch(
            FancyBboxPatch(
                (x - _BOX_W / 2, y - _BOX_H / 2),
                _BOX_W,
                _BOX_H,
                boxstyle="round,pad=0.05",
                facecolor=fill,
                edgecolor="black",
                linewidth=2.0 if shell else 0.0,
            )
        )
        ax.text(
            x,
            y,
            name,
            ha="center",
            va="center",
            fontsize=20,
            color="black" if shell else "white",
        )
    for importer, imported in edges:
        (x0, y0), (x1, y1) = layout[importer], layout[imported]
        ax.annotate(
            "",
            (x1 - (_BOX_W / 2 + 0.1), y1),
            (x0 + (_BOX_W / 2 + 0.1), y0),
            arrowprops={"arrowstyle": "-|>", "color": "black", "linewidth": 2.0},
        )
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_lo, y_hi)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    style.save(fig, out)


@dataclass(frozen=True)
class DecisionRow:
    module: str
    ifs: int
    matches: int


def decision_rows(sources: Sequence[tuple[str, str]]) -> tuple[DecisionRow, ...]:
    """Return the if and match statements per (name, text); a conditional expression is none."""
    rows: list[DecisionRow] = []
    for name, text in sources:
        nodes = list(ast.walk(ast.parse(text)))
        rows.append(
            DecisionRow(
                name,
                sum(isinstance(node, ast.If) for node in nodes),
                sum(isinstance(node, ast.Match) for node in nodes),
            )
        )
    return tuple(rows)


def decision_chart(rows: Sequence[DecisionRow], out: Path) -> None:
    """Draw one horizontal stacked bar per module, ifs then matches, the count on each segment."""
    style.apply()
    fig, ax = plt.subplots(figsize=(4.6, 3.1), dpi=style.DPI)
    names = [row.module for row in rows]
    series = (
        ("ifs", [row.ifs for row in rows], palette.colour_of("pricing")),
        ("matches", [row.matches for row in rows], palette.colour_of("shipping")),
    )
    left = [0] * len(rows)
    for label, counts, colour in series:
        bars = ax.barh(names, counts, left=left, color=colour, edgecolor="white", label=label)
        ax.bar_label(
            bars,
            labels=[str(n) if n else "" for n in counts],
            label_type="center",
            color="white",
            fontsize=16,
        )
        left = [a + b for a, b in zip(left, counts, strict=True)]
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_xlim(0, max(left) + 0.5)
    ax.tick_params(axis="y", labelsize=16, length=0)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, fontsize=14, frameon=False)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    style.save(fig, out)


def decision_table(rows: Sequence[DecisionRow]) -> str:
    """Render 'module ifs matches' aligned, one row per file in the given order."""
    heads = ("module", "ifs", "matches")
    width = max(len(heads[0]), *(len(row.module) for row in rows))
    lines = [f"{heads[0]:<{width}}  {heads[1]}  {heads[2]}"]
    for row in rows:
        counts = (row.ifs, row.matches)
        cells = "  ".join(f"{n:>{len(head)}}" for n, head in zip(counts, heads[1:], strict=True))
        lines.append(f"{row.module:<{width}}  {cells}")
    return "\n".join(lines) + "\n"


def import_table(rows: Sequence[ImportRow]) -> str:
    """Render 'module contexts ports core' aligned, one row per file in the given order."""
    width = max(len(_HEADS[0]), *(len(row.module) for row in rows))
    lines = [f"{_HEADS[0]:<{width}}  " + "  ".join(_HEADS[1:])]
    for row in rows:
        counts = (row.from_contexts, row.from_ports, row.from_core)
        cells = "  ".join(f"{n:>{len(head)}}" for n, head in zip(counts, _HEADS[1:], strict=True))
        lines.append(f"{row.module:<{width}}  {cells}")
    return "\n".join(lines) + "\n"
