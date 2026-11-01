"""Find the included blocks with more non-blank lines than their cap."""

from __future__ import annotations

from collections.abc import Callable

from scripts.utils.widths import INCLUDE, snippet_text, strip_step_markers

_HEADING_PREFIX = "## "


def too_long(
    index_md: str, read: Callable[[str], str], cap: int, name: str = "index.md"
) -> tuple[str, ...]:
    """Return '<name> <heading>: <n> > <cap>: <path>[:<snippet>]' for each block past its cap.

    An include's own cap=N replaces cap; blank lines do not count.
    """
    found: list[str] = []
    heading = ""
    for line in index_md.splitlines():
        if line.startswith(_HEADING_PREFIX):
            heading = line[len(_HEADING_PREFIX) :].split(" {")[0].strip()
            continue
        include = INCLUDE.match(line)
        if not include:
            continue
        text = strip_step_markers(read(include.group("path")))
        snippet = include.group("snippet")
        if snippet:
            text = snippet_text(text, snippet)
        count = sum(1 for row in text.splitlines() if row.strip())
        limit = int(include.group("cap") or cap)
        if count > limit:
            where = f"{include.group('path')}:{snippet}" if snippet else include.group("path")
            found.append(f"{name} {heading}: {count} > {limit}: {where}")
    return tuple(found)
