"""Find the included code and text lines wider than the column they sit in."""

from __future__ import annotations

import re
import sys
import textwrap
from collections.abc import Callable
from pathlib import Path

# The deck's code size is \footnotesize (preamble.tex AtBeginEnvironment Shaded).
BASE_POINTS = 8
POINTS = {"small": 9, "footnotesize": 8, "scriptsize": 7, "tiny": 5}

_HEADING = re.compile(r"^## (?P<title>.*?)(?:\s*\{[^}]*\})?\s*$")
_COLUMN = re.compile(r'\.column\s+width="(?P<pct>\d+(?:\.\d+)?)%"')
_CLOSE = re.compile(r"^:{3,}\s*$")
INCLUDE = re.compile(
    r"^```\{[^}]*\binclude=(?P<path>[^\s}]+)(?:\s+snippet=(?P<snippet>[\w-]+))?(?:\s+cap=(?P<cap>\d+))?"
)
_FVSET = re.compile(r"\\fvset\{fontsize=\\(?P<size>\w+)")


_STEP_MARKER = re.compile(r"\s*# \[step: \d\]\s*$")


def read_include(root: Path, path: str, strict: bool) -> str:
    """Read an included file under root; a missing one is a stub, empty, unless strict.

    A stub prints '[WARN] stub include: <path>' as the include filter does;
    strict raises FileNotFoundError naming the path.
    """
    target = root / path
    if target.exists():
        return target.read_text(encoding="utf-8")
    if strict:
        raise FileNotFoundError(f"include not found: {path}")
    sys.stdout.write(f"[WARN] stub include: {path}\n")
    return ""


def strip_step_markers(text: str) -> str:
    """Drop a trailing '# [step: N]' from each line, as the include filter does."""
    return "\n".join(_STEP_MARKER.sub("", row) for row in text.splitlines())


def snippet_text(text: str, name: str) -> str:
    """Return the lines between a snippet's markers, dedented as the filter does."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if inside and "[/snippet]" in line:
            inside = False
        elif inside:
            out.append(line)
        elif f"[snippet: {name}]" in line:
            inside = True
    return textwrap.dedent("\n".join(out))


def too_wide(
    index_md: str, read: Callable[[str], str], full: int, name: str = "index.md"
) -> tuple[str, ...]:
    """Return '<name> <heading>: <n> > <budget>: <line>' for each included line past its column.

    full is the char count of a full-width line at the deck's code size; a column
    of W% gets full * W / 100, scaled by 8 / the point size of the slide's \\fvset.
    """
    found: list[str] = []
    heading = ""
    percent = 100.0
    scale = 1.0
    for line in index_md.splitlines():
        head = _HEADING.match(line)
        if head:
            heading, percent, scale = head.group("title"), 100.0, 1.0
            continue
        fvset = _FVSET.search(line)
        if fvset and fvset.group("size") in POINTS:
            scale = BASE_POINTS / POINTS[fvset.group("size")]
        column = _COLUMN.search(line)
        if column:
            percent = float(column.group("pct"))
        elif _CLOSE.match(line):
            percent = 100.0
        include = INCLUDE.match(line)
        if include:
            text = strip_step_markers(read(include.group("path")))
            if include.group("snippet"):
                text = snippet_text(text, include.group("snippet"))
            budget = int(full * percent / 100 * scale)
            found.extend(
                f"{name} {heading}: {len(row)} > {budget}: {row}"
                for row in text.splitlines()
                if len(row) > budget
            )
    return tuple(found)
