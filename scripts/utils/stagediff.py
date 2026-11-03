"""Diff one named snippet between two files, as the slides show an edit between stages."""

from __future__ import annotations

import difflib
import re
import textwrap
from pathlib import Path

from scripts.utils.widths import snippet_text, strip_step_markers


_DEF_NAME = re.compile(r"\s*def (\w+)\(")


def snippet_lines(path: Path, name: str) -> list[str]:
    """Return a file's snippet with step markers stripped and dedented, one string per line."""
    text = snippet_text(strip_step_markers(path.read_text(encoding="ascii")), name)
    return [f"{row}\n" for row in text.splitlines()]


def _from_start(lines: list[str], start: str | None) -> list[str]:
    """Cut lines to begin at the first one containing start, then dedent the cut lines.

    All of them, undented, when start is None.
    """
    if start is None:
        return lines
    cut = lines[next(i for i, row in enumerate(lines) if start in row) :]
    return textwrap.dedent("".join(cut)).splitlines(keepends=True)


def _unhidden(lines: list[str], hide: str | None) -> list[str]:
    """Drop the lines matching the hide pattern; all of them when hide is None."""
    if hide is None:
        return lines
    pattern = re.compile(hide)
    return [row for row in lines if not pattern.search(row)]


def _tilded(body: list[str]) -> list[str]:
    """Merge each block of equally many - then + lines into ~ lines carrying the new text."""
    out: list[str] = []
    i = 0
    while i < len(body):
        if not body[i].startswith("-"):
            out.append(body[i])
            i += 1
            continue
        j = i
        while j < len(body) and body[j].startswith("-"):
            j += 1
        k = j
        while k < len(body) and body[k].startswith("+"):
            k += 1
        if k - j == j - i:
            out.extend(f"~ {row[1:]}" for row in body[j:k])
        else:
            out.extend(body[i:k])
        i = k
    return out


def _elided(body: list[str]) -> list[str]:
    """Collapse each run of more than two unchanged lines to one context line, '...', one more."""
    out: list[str] = []
    run: list[str] = []

    def flush(at_start: bool, at_end: bool) -> None:
        if len(run) <= 2:
            out.extend(run)
        else:
            if not at_start:
                out.append(run[0])
            out.append("...\n")
            if not at_end:
                out.append(run[-1])
        run.clear()

    for row in body:
        if row.startswith(" "):
            run.append(row)
        else:
            flush(not out, False)
            out.append(row)
    flush(not out, True)
    return out


def compact_body(old: list[str], new: list[str]) -> list[str]:
    """Return the - and + lines of a diff with one context line each side of a change.

    Every elided run of unchanged lines is one '---' line, at the edges too; a -/+ pair stays.
    """
    rows = list(difflib.unified_diff(old, new, n=1))[2:]
    spans = [_old_span(row) for row in rows if row.startswith("@@")]
    out: list[str] = []
    for row in rows:
        if not row.startswith("@@"):
            out.append(row)
        elif out or spans[0][0] > 1:
            out.append("---\n")
    if spans and spans[-1][1] < len(old):
        out.append("---\n")
    return out


def _old_span(header: str) -> tuple[int, int]:
    """Return the first and last old line a '@@ -s,c +s,c @@' header covers."""
    found = re.match(r"@@ -(\d+)(?:,(\d+))?", header)
    if found is None:
        raise ValueError(f"not a unified diff hunk header: {header!r}")
    start = int(found.group(1))
    count = int(found.group(2) or 1)
    return start, start + count - 1


def _scope_lead(path: Path, snippet: str, start: str | None) -> list[str]:
    """Return the def row, with a '---' row when the body does not follow it, or [].

    The def is the first one inside the snippet, else the nearest one above its marker.
    """
    text = strip_step_markers(path.read_text(encoding="ascii"))
    inside = snippet_text(text, snippet).splitlines()
    named = next((m for row in inside if (m := _DEF_NAME.match(row))), None)
    if named is None:
        above = text.splitlines()
        at = next(i for i, row in enumerate(above) if f"[snippet: {snippet}]" in row)
        named = next((m for row in reversed(above[:at]) if (m := _DEF_NAME.match(row))), None)
    if named is None:
        return []
    contiguous = start is None and (not _DEF_NAME.match(inside[0]) or len(inside) == 1)
    return [f" def {named.group(1)}(...):\n", *([] if contiguous else ["---\n"])]


def _scoped(body: list[str], lead: list[str]) -> list[str]:
    """Put the lead rows before the body unless it already opens on a def row."""
    if not lead or (body and _DEF_NAME.match(body[0][1:])):
        return body
    return [*lead, *(body[1:] if body[:1] == ["---\n"] and len(lead) == 2 else body)]


def snippet_diff(
    from_path: Path,
    from_snippet: str,
    to_path: Path,
    to_snippet: str,
    start: str | None = None,
    added_only: bool = False,
    hide: str | None = None,
    labels: tuple[str, str] | None = None,
    compact: bool = False,
    scope: bool = True,
) -> str:
    """Return the captioned diff of two snippets: '<from> -> <to>', then the body lines.

    The ---, +++ and @@ lines are left out. With start, each snippet is cut to begin at its
    first line containing that text. With added_only, only the + lines follow the caption.
    With hide, a regular expression, a snippet line matching it is dropped before diffing.
    Otherwise a -/+ pair is one '~ new' line and an unchanged run over two lines is '...'.
    With labels, the caption names them instead of the files. With compact, see compact_body.
    With scope, a body not opening on a def line opens on the to-snippet's ' def f(...):' row.
    """
    old = _unhidden(_from_start(snippet_lines(from_path, from_snippet), start), hide)
    new = _unhidden(_from_start(snippet_lines(to_path, to_snippet), start), hide)
    lead = _scope_lead(to_path, to_snippet, start) if scope and not added_only else []
    if compact and not added_only:
        caption = labels or (from_path.name, to_path.name)
        body = compact_body(old, new)
        return "".join([f"{caption[0]} -> {caption[1]}\n", *_scoped(body, lead)])
    rows = difflib.unified_diff(
        old,
        new,
        fromfile=from_path.name,
        tofile=to_path.name,
        n=max(len(old), len(new)),
    )
    kept = [row for row in rows if not row.startswith(("---", "+++", "@@"))]
    body = [row for row in kept if row[0] == "+"] if added_only else _elided(_tilded(kept))
    caption = labels or (from_path.name, to_path.name)
    return "".join([f"{caption[0]} -> {caption[1]}\n", *_scoped(body, lead)])
