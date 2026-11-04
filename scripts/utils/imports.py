"""Count, per source file, the names imported from the contexts, the ports and the core.

The contexts are pricing, shipping and tax; s04_what.money is a shared value type, not one.
"""

from __future__ import annotations

import ast
from collections.abc import Sequence
from dataclasses import dataclass

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
