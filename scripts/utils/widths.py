"""Find the included code and text lines wider than the column they sit in."""

from __future__ import annotations

import re
import sys
import textwrap
from collections.abc import Callable
from pathlib import Path

# --full counts chars at \footnotesize, 8pt (BASE_POINTS). A block renders by its
# kind (preamble.tex): .text at \exhibitsize, 7pt; any other include at \snippetsize, 5pt.
BASE_POINTS = 8
EXHIBIT_POINTS = 7
SNIPPET_POINTS = 5

_HEADING = re.compile(r"^## (?P<title>.*?)(?:\s*\{[^}]*\})?\s*$")
_COLUMN = re.compile(r'\.column\s+width="(?P<pct>\d+(?:\.\d+)?)%"')
_CLOSE = re.compile(r"^:{3,}\s*$")
INCLUDE = re.compile(r"^```\{[^}]*\binclude=(?P<path>[^\s}]+)(?P<attrs>[^}]*)")
_ATTRIBUTE = re.compile(r"\s+(?P<name>snippet|cap|start-line|end-line)=(?P<value>[\w-]+)")
_TEXT_FENCE = re.compile(r"^```\{[^}]*\.text\b")
# A fence with no class renders as plain verbatim at body size, not at \snippetsize.
_CLASSLESS_FENCE = re.compile(r"^```\{(?![^}]*\s\.\w)(?!\.)[^}]*\}")


_STEP_MARKER = re.compile(r"\s*# \[step: \d\]\s*$")


def include_attributes(include: re.Match[str]) -> dict[str, str]:
    """Map the attributes after an include's path (snippet, cap, start-line, end-line) by name.

    Any order; an attribute the include does not write is absent.
    """
    return {m.group("name"): m.group("value") for m in _ATTRIBUTE.finditer(include.group("attrs"))}


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


def line_range(text: str, start: str | None, end: str | None) -> str:
    """Keep the 1-based inclusive start-line..end-line of text, as the filter does."""
    rows = text.splitlines()
    first = int(start) - 1 if start else 0
    last = int(end) if end else len(rows)
    return "\n".join(rows[first:last])


def too_wide(
    index_md: str, read: Callable[[str], str], full: int, name: str = "index.md"
) -> tuple[str, ...]:
    """Return '<name> <heading>: <n> > <budget>: <line>' for each included line past its column.

    full is the char count of a full-width line at the deck's code size; a column
    of W% gets full * W / 100, scaled by 8 / the point size of the block's kind.
    """
    found: list[str] = []
    heading = ""
    percent = 100.0
    for line in index_md.splitlines():
        head = _HEADING.match(line)
        if head:
            heading, percent = head.group("title"), 100.0
            continue
        column = _COLUMN.search(line)
        if column:
            percent = float(column.group("pct"))
        elif _CLOSE.match(line):
            percent = 100.0
        include = INCLUDE.match(line)
        if include:
            text = strip_step_markers(read(include.group("path")))
            attrs = include_attributes(include)
            if "snippet" in attrs:
                text = snippet_text(text, attrs["snippet"])
            text = line_range(text, attrs.get("start-line"), attrs.get("end-line"))
            if _TEXT_FENCE.match(line):
                points = EXHIBIT_POINTS
            elif _CLASSLESS_FENCE.match(line):
                points = BASE_POINTS
            else:
                points = SNIPPET_POINTS
            budget = int(full * percent / 100 * BASE_POINTS / points)
            found.extend(
                f"{name} {heading}: {len(row)} > {budget}: {row}"
                for row in text.splitlines()
                if len(row) > budget
            )
    return tuple(found)
