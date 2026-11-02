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
) -> str:
    """Return the unified diff of two snippets, labelled by file name with no timestamps.

    With start, each snippet is cut to begin at its first line containing that text.
    """
    return "".join(
        difflib.unified_diff(
            _from_start(snippet_lines(from_path, from_snippet), start),
            _from_start(snippet_lines(to_path, to_snippet), start),
            fromfile=from_path.name,
            tofile=to_path.name,
        )
    )
