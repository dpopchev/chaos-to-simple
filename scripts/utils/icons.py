"""Map an icon name to its glyph in the two installed icon fonts, and draw a probe of them.

The codepoints were read from the font files' cmaps with fontTools on 2026-11-02:
Font Awesome 7 Free Solid (otf-font-awesome, /usr/share/fonts/OTF) and Hack Nerd Font
(~/.local/share/fonts). Nerd Fonts moves the Font Awesome icons newer than version 4 out
of their Font Awesome codepoints (warehouse, store, layer-group), so the two differ.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Collection
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, assert_never

from scripts.utils import style

Family = Literal["Font Awesome 7 Free", "Hack Nerd Font"]
FONT_AWESOME: Family = "Font Awesome 7 Free"
NERD: Family = "Hack Nerd Font"
FAMILIES: tuple[Family, ...] = (FONT_AWESOME, NERD)

# fontconfig pattern -> the font files it matches, one per line.
Find = Callable[[str], str]
# font file -> the codepoints it draws.
Charmap = Callable[[Path], Collection[int]]


@dataclass(frozen=True)
class Codepoints:
    """Where one icon sits in each icon font."""

    font_awesome: int
    nerd: int


# The nine actors.csv icons, in actors.csv order, then the eight route.csv icons.
ACTOR_ICONS = (
    "user",
    "code",
    "bullhorn",
    "star",
    "truck",
    "calculator",
    "credit-card",
    "warehouse",
    "envelope",
)
ROUTE_ICONS = (
    "store",
    "code-branch",
    "map",
    "comments",
    "home",
    "cut",
    "layer-group",
    "flag-checkered",
)

ROLE_ICONS = ("clipboard-check", "headset")

# home and cut are Font Awesome 5 names; Font Awesome 7 and Nerd Fonts call them house
# and scissors; Nerd Fonts keeps code-branch as fa-code_fork.
ICONS: dict[str, Codepoints] = {
    "user": Codepoints(0xF007, 0xF007),
    "code": Codepoints(0xF121, 0xF121),
    "bullhorn": Codepoints(0xF0A1, 0xF0A1),
    "star": Codepoints(0xF005, 0xF005),
    "truck": Codepoints(0xF0D1, 0xF0D1),
    "calculator": Codepoints(0xF1EC, 0xF1EC),
    "credit-card": Codepoints(0xF09D, 0xF09D),
    "warehouse": Codepoints(0xF494, 0xED92),
    "envelope": Codepoints(0xF0E0, 0xF0E0),
    "store": Codepoints(0xF54E, 0xEE17),
    "code-branch": Codepoints(0xF126, 0xF126),
    "map": Codepoints(0xF279, 0xF279),
    "comments": Codepoints(0xF086, 0xF086),
    "home": Codepoints(0xF015, 0xF015),
    "cut": Codepoints(0xF0C4, 0xF0C4),
    "layer-group": Codepoints(0xF5FD, 0xEEA8),
    "flag-checkered": Codepoints(0xF11E, 0xF11E),
    "clipboard-check": Codepoints(0xF46C, 0xED7A),
    "headset": Codepoints(0xF590, 0xEE59),
}

# The face of each family that holds the icons.
STYLES: dict[Family, str] = {FONT_AWESOME: "Solid", NERD: "Regular"}


# An icon beside a label is drawn this many times the label's point size, so it is never
# shorter than the label's capitals.
ICON_SCALE = 1.3


def icon_size(label_size: float) -> float:
    """Return the point size of an icon drawn beside a label of label_size points."""
    return label_size * ICON_SCALE


class UnknownIconError(ValueError):
    """An icon name ICONS does not map."""


class FontMissingError(LookupError):
    """fontconfig finds no file for an icon font."""


def make_family(raw: str) -> Family:
    """Return the icon font named raw; raise ValueError for any other name."""
    for family in FAMILIES:
        if raw == family:
            return family
    raise ValueError(f"unknown icon font {raw!r}; expected one of {FAMILIES}")


def glyph(name: str, family: Family) -> str:
    """Return the character that draws icon name in family; raise UnknownIconError if unmapped."""
    if name not in ICONS:
        raise UnknownIconError(f"unknown icon {name!r}; expected one of {sorted(ICONS)}")
    points = ICONS[name]
    match family:
        case "Font Awesome 7 Free":
            return chr(points.font_awesome)
        case "Hack Nerd Font":
            return chr(points.nerd)
        case _:
            assert_never(family)


def pattern(family: Family) -> str:
    """Return the fontconfig pattern of the icon face of family."""
    return f"{family}:style={STYLES[family]}"


def font_available(family: Family, find: Find) -> bool:
    """Tell whether fontconfig finds the icon face of family."""
    return bool(find(pattern(family)).strip())


def ft2font_charmap(path: Path) -> Collection[int]:
    """Return the codepoints the font file draws, read with matplotlib's FreeType."""
    from matplotlib.ft2font import FT2Font

    return FT2Font(str(path)).get_charmap().keys()


def icon_points(family: Family) -> set[int]:
    """Return the codepoints of every ICONS entry in family."""
    return {p.font_awesome if family == FONT_AWESOME else p.nerd for p in ICONS.values()}


def font_file(family: Family, find: Find, charmap: Charmap = ft2font_charmap) -> Path:
    """Return the first font file of the icon face of family that draws every icon.

    A file sorted first that lacks a glyph (a Regular file beside the Solid one) is skipped;
    raise FontMissingError naming the files tried when none draws them all.
    """
    files = sorted(line for line in find(pattern(family)).splitlines() if line.strip())
    if not files:
        raise FontMissingError(f"fontconfig finds no file for {pattern(family)!r}")
    needed = icon_points(family)
    for name in files:
        if needed <= set(charmap(Path(name))):
            return Path(name)
    raise FontMissingError(f"no file draws every icon of {family!r}; tried {', '.join(files)}")


def probe(out_png: Path, family: Family, font: Path) -> Path:
    """Draw the nine actor icons of family from the font file, each over its name."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties

    icon_face = FontProperties(fname=font, size=36)
    fig, ax = plt.subplots(figsize=(9.0, 2.0), dpi=style.DPI)
    for i, name in enumerate(ACTOR_ICONS):
        ax.text(i, 0.6, glyph(name, family), ha="center", va="center", fontproperties=icon_face)
        ax.text(i, 0.0, name, ha="center", va="center", fontsize=9)
    ax.set_xlim(-0.6, len(ACTOR_ICONS) - 0.4)
    ax.set_ylim(-0.4, 1.1)
    ax.set_title(f"{family} ({font.name})", fontsize=10)
    ax.axis("off")
    style.save(fig, out_png)
    return out_png


def fc_list(fc_pattern: str) -> str:
    """Return the font files fontconfig lists for fc_pattern, one per line.

    Raises CalledProcessError naming the command and its stderr on a non-zero exit.
    """
    command = ["fc-list", "--format", "%{file}\n", fc_pattern]
    done = subprocess.run(command, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise subprocess.CalledProcessError(done.returncode, command, done.stdout, done.stderr)
    return done.stdout
