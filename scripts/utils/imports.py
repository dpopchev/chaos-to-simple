"""Count, per source file, the names imported from the contexts, the ports and the core."""

from __future__ import annotations

import ast
from collections.abc import Sequence
from dataclasses import dataclass

_CONTEXTS = "s04_what"
_PORTS = "s05_how.ports"
_CORE = "s06_simple.core"
_HEADS = ("module", "contexts", "ports", "core")


@dataclass(frozen=True)
class ImportRow:
    module: str
    from_contexts: int
    from_ports: int
    from_core: int


def _names_from(tree: ast.AST, package: str) -> int:
    """Return how many names the from-imports of package (or its submodules) bring in."""
    return sum(
        len(node.names)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.level == 0
        and node.module is not None
        and (node.module == package or node.module.startswith(package + "."))
    )


def import_rows(name: str, text: str) -> ImportRow:
    """Return the import counts of one source text, read with ast."""
    tree = ast.parse(text)
    return ImportRow(
        name, _names_from(tree, _CONTEXTS), _names_from(tree, _PORTS), _names_from(tree, _CORE)
    )


def import_table(rows: Sequence[ImportRow]) -> str:
    """Render 'module contexts ports core' aligned, one row per file in the given order."""
    width = max(len(_HEADS[0]), *(len(row.module) for row in rows))
    lines = [f"{_HEADS[0]:<{width}}  " + "  ".join(_HEADS[1:])]
    for row in rows:
        counts = (row.from_contexts, row.from_ports, row.from_core)
        cells = "  ".join(f"{n:>{len(head)}}" for n, head in zip(counts, _HEADS[1:], strict=True))
        lines.append(f"{row.module:<{width}}  {cells}")
    return "\n".join(lines) + "\n"
