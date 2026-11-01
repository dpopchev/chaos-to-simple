"""The artifact manifest and its stubs: a placeholder for each path that has no rule yet."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

TEXT_KINDS = ("txt", "diff", "tex")
PNG_SIZE = (1600, 900)


@dataclass(frozen=True)
class Entry:
    path: str
    kind: str
    producer: str


def load_manifest(path: Path) -> list[Entry]:
    with path.open(newline="", encoding="ascii") as fh:
        return [Entry(row["path"], row["kind"], row["producer"]) for row in csv.DictReader(fh)]


def missing(manifest: Iterable[Entry], built: Iterable[str]) -> tuple[Entry, ...]:
    """Return the manifest entries whose path is not in built, in manifest order."""
    ruled = set(built)
    return tuple(entry for entry in manifest if entry.path not in ruled)


def strict(manifest: Iterable[Entry], built: Iterable[str]) -> tuple[str, ...]:
    """Return the manifest paths that no rule builds."""
    return tuple(entry.path for entry in missing(manifest, built))


def write_stub(path: Path, kind: str) -> None:
    """Write the placeholder of one kind at path, creating its folders.

    A png reads STUB and the path; a txt, diff or tex holds one warning line.
    Raises ValueError for a kind that has no placeholder.
    """
    if kind != "png" and kind not in TEXT_KINDS:
        raise ValueError(f"unknown kind {kind!r}; expected png or one of {TEXT_KINDS}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if kind == "png":
        image = Image.new("RGB", PNG_SIZE, "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((10, 10, PNG_SIZE[0] - 10, PNG_SIZE[1] - 10), outline="red", width=8)
        draw.text((60, 60), f"STUB\n{path}", fill="black", font_size=64)
        image.save(path)
        return
    path.write_text(f"[WARN] not implemented yet: {path}\n", encoding="ascii")
