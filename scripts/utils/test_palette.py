"""Tests for the palette: actors and contexts read from their two datasets."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.icons import FONT_AWESOME, Family
from scripts.utils.palette import (
    Actor,
    Context,
    actors_tex,
    colour_of,
    icon_of,
    label_of,
    load_actors,
    load_contexts,
    text_colour,
)

DATA = Path(__file__).resolve().parents[2] / "data"


@pytest.mark.edge
def test_load_actors_reads_nine_actors() -> None:
    assert len(load_actors(DATA / "actors.csv")) == 9


@pytest.mark.edge
def test_load_actors_reads_every_column(tmp_path: Path) -> None:
    path = tmp_path / "actors.csv"
    path.write_text(
        "actor,kind,label,color,icon,context\nmarketing,department,Marketing,E69F00,bullhorn,pricing\n",
        encoding="ascii",
    )
    assert load_actors(path)["marketing"] == Actor(
        "marketing", "department", "Marketing", "E69F00", "bullhorn", "pricing"
    )


@pytest.mark.edge
def test_load_contexts_reads_five_contexts() -> None:
    assert len(load_contexts(DATA / "contexts.csv")) == 5


@pytest.mark.edge
def test_load_contexts_reads_every_column(tmp_path: Path) -> None:
    path = tmp_path / "contexts.csv"
    path.write_text("context,kind,label,color\ntax,core,Tax,1E8449\n", encoding="ascii")
    assert load_contexts(path)["tax"] == Context("tax", "core", "Tax", "1E8449")


@pytest.mark.model
def test_colour_of_an_actor_is_its_hex_with_a_hash() -> None:
    assert colour_of("marketing") == "#E69F00"


@pytest.mark.model
def test_colour_of_a_context_is_its_hex_with_a_hash() -> None:
    assert colour_of("pricing") == "#7B3F9E"


@pytest.mark.model
def test_label_of_an_actor_is_its_label() -> None:
    assert label_of("payment") == "Payment provider"


@pytest.mark.model
def test_label_of_a_context_is_its_label() -> None:
    assert label_of("shell") == "Shell (effects)"


@pytest.mark.model
def test_icon_of_an_actor_is_its_icon_name() -> None:
    assert icon_of("warehouse") == "warehouse"


@pytest.mark.model
def test_text_colour_of_a_dark_actor_is_its_colour() -> None:
    assert text_colour("logistics") == "#0072B2"


@pytest.mark.edge
def test_text_colour_refuses_the_yellow_fill() -> None:
    with pytest.raises(ValueError, match="fill"):
        text_colour("mailer")


@pytest.mark.edge
def test_colour_of_an_unknown_key_raises() -> None:
    with pytest.raises(ValueError, match="unknown"):
        colour_of("nobody")


@pytest.mark.edge
def test_icon_of_a_context_raises() -> None:
    with pytest.raises(ValueError, match="no icon"):
        icon_of("pricing")


def _tex(font: Family | None) -> list[str]:
    actors = load_actors(DATA / "actors.csv")
    contexts = load_contexts(DATA / "contexts.csv")
    return actors_tex(actors, contexts, font).splitlines()


@pytest.mark.model
def test_actors_tex_defines_one_actor_line_per_actor() -> None:
    assert sum(line.startswith("\\defineactor{") for line in _tex(FONT_AWESOME)) == 9


@pytest.mark.model
def test_actors_tex_defines_one_colour_per_actor_and_context() -> None:
    assert sum(line.startswith("\\definecolor{") for line in _tex(None)) == 14


@pytest.mark.model
def test_actors_tex_writes_the_glyph_as_a_character_code() -> None:
    line = '\\defineactor{customer}{Customer}{customer}{\\symbol{"F007}}'
    assert line in _tex(FONT_AWESOME)


@pytest.mark.edge
def test_actors_tex_without_an_icon_font_leaves_the_glyph_empty() -> None:
    assert "\\defineactor{customer}{Customer}{customer}{}" in _tex(None)
