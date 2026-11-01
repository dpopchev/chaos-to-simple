"""The deck's one palette: actors and contexts, their colours, labels and icons, from data/.

data/actors.csv and data/contexts.csv are the only home of a colour; LaTeX and matplotlib
both read them (through this module or the macros built from it).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import cache
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
ACTORS_CSV = DATA / "actors.csv"
CONTEXTS_CSV = DATA / "contexts.csv"

# A fill, never text: too pale on white.
FILL_ONLY = "F0E442"


@dataclass(frozen=True)
class Actor:
    key: str
    kind: str
    label: str
    color: str
    icon: str
    context: str


@dataclass(frozen=True)
class Context:
    key: str
    kind: str
    label: str
    color: str


def load_actors(path: Path = ACTORS_CSV) -> dict[str, Actor]:
    """Read the actors by key, in file order."""
    with path.open(newline="", encoding="ascii") as fh:
        return {
            row["actor"]: Actor(
                row["actor"], row["kind"], row["label"], row["color"], row["icon"], row["context"]
            )
            for row in csv.DictReader(fh)
        }


def load_contexts(path: Path = CONTEXTS_CSV) -> dict[str, Context]:
    """Read the contexts by key, in file order."""
    with path.open(newline="", encoding="ascii") as fh:
        return {
            row["context"]: Context(row["context"], row["kind"], row["label"], row["color"])
            for row in csv.DictReader(fh)
        }


@cache
def _actors() -> dict[str, Actor]:
    return load_actors()


@cache
def _contexts() -> dict[str, Context]:
    return load_contexts()


def colour_of(key: str) -> str:
    """Return '#RRGGBB' of an actor or a context key; raise ValueError for an unknown key."""
    if key in _actors():
        return f"#{_actors()[key].color}"
    if key in _contexts():
        return f"#{_contexts()[key].color}"
    raise ValueError(f"unknown palette key {key!r}")


def label_of(key: str) -> str:
    """Return the label of an actor or a context key; raise ValueError for an unknown key."""
    if key in _actors():
        return _actors()[key].label
    if key in _contexts():
        return _contexts()[key].label
    raise ValueError(f"unknown palette key {key!r}")


def icon_of(key: str) -> str:
    """Return the icon name of an actor; raise ValueError for a context or an unknown key."""
    if key in _actors():
        return _actors()[key].icon
    if key in _contexts():
        raise ValueError(f"{key!r} is a context and has no icon")
    raise ValueError(f"unknown palette key {key!r}")


def text_colour(key: str) -> str:
    """Return the colour of key for text; raise ValueError for the yellow, a fill only."""
    colour = colour_of(key)
    if colour.removeprefix("#").upper() == FILL_ONLY:
        raise ValueError(f"{key!r} is {colour}, a fill and never text")
    return colour
