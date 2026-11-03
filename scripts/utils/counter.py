"""The path counter of a section's frames: read from titles, checked against the plan."""

from __future__ import annotations

import itertools
import re
from collections.abc import Sequence

Value = int | str

STORYBOARD = [1, 2, 4, 8, 16, 32, 64]
_PATHS = re.compile(r"\{paths=(\?|\d+)\}")


def paths_of(index_text: str) -> list[Value]:
    """Return the {paths=N} values in frame order; '?' stays a string, numbers become int."""
    return [v if v == "?" else int(v) for v in _PATHS.findall(index_text)]


def storyboard_ok(values: Sequence[Value]) -> bool:
    """Say whether the first seven values, past leading '?', are 1, 2, 4, 8, 16, 32, 64."""
    rest = list(itertools.dropwhile(lambda v: v == "?", values))
    return rest[: len(STORYBOARD)] == STORYBOARD


def monotone(values: Sequence[Value]) -> bool:
    """Say whether the numbers never decrease, ignoring '?'."""
    numbers = [v for v in values if isinstance(v, int)]
    return all(a <= b for a, b in itertools.pairwise(numbers))


def ends_at(values: Sequence[Value], counter: str) -> bool:
    """Say whether the last value equals the route counter (compared as text)."""
    return bool(values) and str(values[-1]) == counter


def reveal_at(frames: Sequence[tuple[str, Value]], title: str, value: Value) -> bool:
    """Say whether the value first appears on the frame with that title."""
    first = next((t for t, v in frames if v == value), None)
    return first == title
