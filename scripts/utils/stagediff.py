"""Diff one named snippet between two files, as the slides show an edit between stages."""

from __future__ import annotations

import difflib
from pathlib import Path

from scripts.utils.widths import snippet_text, strip_step_markers


def snippet_lines(path: Path, name: str) -> list[str]:
    """Return a file's snippet with step markers stripped and dedented, one string per line."""
    text = snippet_text(strip_step_markers(path.read_text(encoding="ascii")), name)
    return [f"{row}\n" for row in text.splitlines()]


def snippet_diff(from_path: Path, from_snippet: str, to_path: Path, to_snippet: str) -> str:
    """Return the unified diff of two snippets, labelled by file name with no timestamps."""
    return "".join(
        difflib.unified_diff(
            snippet_lines(from_path, from_snippet),
            snippet_lines(to_path, to_snippet),
            fromfile=from_path.name,
            tofile=to_path.name,
        )
    )
