"""Diff one named snippet between two files, as the slides show an edit between stages."""

from __future__ import annotations

import difflib
from pathlib import Path

from scripts.utils.widths import snippet_text, strip_step_markers


def snippet_lines(path: Path, name: str) -> list[str]:
    """Return a file's snippet with step markers stripped and dedented, one string per line."""
    text = snippet_text(strip_step_markers(path.read_text(encoding="ascii")), name)
    return [f"{row}\n" for row in text.splitlines()]


def _from_start(lines: list[str], start: str | None) -> list[str]:
    """Cut lines to begin at the first one containing start; all of them when start is None."""
    if start is None:
        return lines
    return lines[next(i for i, row in enumerate(lines) if start in row) :]


def snippet_diff(
    from_path: Path,
    from_snippet: str,
    to_path: Path,
    to_snippet: str,
    start: str | None = None,
    added_only: bool = False,
) -> str:
    """Return the captioned diff of two snippets: '<from> -> <to>', then the body lines.

    The ---, +++ and @@ lines are left out. With start, each snippet is cut to begin at its
    first line containing that text. With added_only, only the + lines follow the caption.
    """
    rows = difflib.unified_diff(
        _from_start(snippet_lines(from_path, from_snippet), start),
        _from_start(snippet_lines(to_path, to_snippet), start),
        fromfile=from_path.name,
        tofile=to_path.name,
    )
    body = [row for row in rows if not row.startswith(("---", "+++", "@@"))]
    if added_only:
        body = [row for row in body if row.startswith("+")]
    return "".join([f"{from_path.name} -> {to_path.name}\n", *body])
