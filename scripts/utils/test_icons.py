"""Tests for the icon map: an icon name to its glyph in each icon font, and the probe figure."""

from __future__ import annotations

from pathlib import Path

import pytest
from matplotlib import font_manager

from scripts.utils.icons import (
    ACTOR_ICONS,
    FONT_AWESOME,
    ICONS,
    NERD,
    ROUTE_ICONS,
    FontMissingError,
    UnknownIconError,
    fc_list,
    font_available,
    font_file,
    glyph,
    make_family,
    probe,
)

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOLID = "/fonts/a b-Solid.otf\n"


@pytest.mark.model
def test_icons_cover_the_actor_and_route_icons() -> None:
    assert set(ICONS) == {*ACTOR_ICONS, *ROUTE_ICONS}


@pytest.mark.model
def test_glyph_reads_the_font_awesome_codepoint() -> None:
    assert glyph("warehouse", FONT_AWESOME) == chr(0xF494)


@pytest.mark.model
def test_glyph_reads_the_nerd_font_codepoint() -> None:
    assert glyph("warehouse", NERD) == chr(0xED92)


@pytest.mark.model
def test_glyph_refuses_an_unknown_icon() -> None:
    with pytest.raises(UnknownIconError, match="no-such"):
        glyph("no-such", NERD)


@pytest.mark.edge
def test_make_family_accepts_a_known_family() -> None:
    assert make_family("Hack Nerd Font") == NERD


@pytest.mark.edge
def test_make_family_refuses_an_unknown_family() -> None:
    with pytest.raises(ValueError, match="Comic Sans"):
        make_family("Comic Sans")


@pytest.mark.model
def test_font_available_when_fontconfig_finds_a_file() -> None:
    assert font_available(FONT_AWESOME, lambda pattern: SOLID)


@pytest.mark.model
def test_font_unavailable_when_fontconfig_finds_nothing() -> None:
    assert not font_available(FONT_AWESOME, lambda pattern: "")


@pytest.mark.model
def test_font_available_asks_for_the_icon_face() -> None:
    asked: list[str] = []
    font_available(FONT_AWESOME, lambda pattern: asked.append(pattern) or "")
    assert asked == ["Font Awesome 7 Free:style=Solid"]


@pytest.mark.model
def test_font_file_keeps_a_path_with_spaces() -> None:
    assert font_file(FONT_AWESOME, lambda pattern: SOLID) == Path("/fonts/a b-Solid.otf")


@pytest.mark.model
def test_font_file_refuses_a_missing_font() -> None:
    with pytest.raises(FontMissingError, match="Hack Nerd Font"):
        font_file(NERD, lambda pattern: "")


@pytest.mark.edge
def test_fc_list_finds_no_file_for_an_unknown_family() -> None:
    assert fc_list("no such family 7f3a:style=Solid") == ""


@pytest.mark.edge
@pytest.mark.filterwarnings("ignore:Glyph")
def test_probe_writes_a_png(tmp_path: Path) -> None:
    fallback = Path(font_manager.findfont("DejaVu Sans"))
    out = probe(tmp_path / "probe.png", NERD, fallback)
    assert out.read_bytes().startswith(PNG_MAGIC)
