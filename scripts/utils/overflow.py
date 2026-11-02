"""Name the beamer frames a lualatex log reports as overfull."""

from __future__ import annotations

import re

_BEGIN = re.compile(r"\\begin\{frame\}(?:<[^>]*>)?(?:\[[^\]]*\])?(?:\{(?P<title>.*)\})?")
_END = r"\end{frame}"
_OVERFULL = re.compile(r"Overfull \\vbox \([^)]*\) detected at line (?P<line>\d+)")
_SLACK = re.compile(r"^slack: (?P<line>\d+) (?P<pt>-?\d+(?:\.\d+)?)pt", re.MULTILINE)
SLACK_THRESHOLD_PT = 3.0  # the developer's Decision on W-087


def _frames(tex: str) -> list[tuple[int, str]]:
    """Return (closing line number, title) for each frame, in deck order."""
    frames: list[tuple[int, str]] = []
    title = ""
    pending = ""
    for number, line in enumerate(tex.splitlines(), start=1):
        text = f"{pending} {line.strip()}" if pending else line
        if (pending or "\\begin{frame}" in line) and text.count("{") > text.count("}"):
            pending = text.rstrip()
            continue
        pending = ""
        begin = _BEGIN.search(text)
        if begin:
            title = begin.group("title") or ""
        elif text.strip() == _END:
            frames.append((number, title))
    return frames


def tight_frames(tex: str, log: str, threshold: float = SLACK_THRESHOLD_PT) -> tuple[str, ...]:
    """Return the titles of the frames whose least slack is under the threshold, in deck order.

    A frame can be typeset more than once, so its slack is the minimum over its lines.
    """
    frames = _frames(tex)
    least: dict[str, float] = {}
    for m in _SLACK.finditer(log):
        title = next((t for end, t in frames if end >= int(m.group("line"))), "")
        least[title] = min(float(m.group("pt")), least.get(title, float("inf")))
    return tuple(title for _, title in frames if least.get(title, threshold) < threshold)


def overfull_frames(tex: str, log: str) -> tuple[str, ...]:
    """Return the titles of the frames whose closing line an Overfull vbox warning points into."""
    frames = _frames(tex)
    hit = {
        next((title for end, title in frames if end >= int(m.group("line"))), "")
        for m in _OVERFULL.finditer(log)
    }
    return tuple(title for _, title in frames if title in hit)
