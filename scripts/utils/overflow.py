"""Name the beamer frames a lualatex log reports as overfull."""

from __future__ import annotations

import re

_BEGIN = re.compile(r"\\begin\{frame\}(?:<[^>]*>)?(?:\[[^\]]*\])?(?:\{(?P<title>.*)\})?")
_END = r"\end{frame}"
_OVERFULL = re.compile(r"Overfull \\vbox \([^)]*\) detected at line (?P<line>\d+)")


def _frames(tex: str) -> list[tuple[int, str]]:
    """Return (closing line number, title) for each frame, in deck order."""
    frames: list[tuple[int, str]] = []
    title = ""
    for number, text in enumerate(tex.splitlines(), start=1):
        begin = _BEGIN.search(text)
        if begin:
            title = begin.group("title") or ""
        elif text.strip() == _END:
            frames.append((number, title))
    return frames


def overfull_frames(tex: str, log: str) -> tuple[str, ...]:
    """Return the titles of the frames whose closing line an Overfull vbox warning points into."""
    frames = _frames(tex)
    hit = {
        next((title for end, title in frames if end >= int(m.group("line"))), "")
        for m in _OVERFULL.finditer(log)
    }
    return tuple(title for _, title in frames if title in hit)
