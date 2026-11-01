"""Tests for the stage: the business map of the shop, its departments and its providers."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.palette import load_actors
from scripts.utils.paths import load_cast, load_rules
from scripts.utils.stage import business_map, edge_words

DATA = Path(__file__).resolve().parents[2] / "data"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


@pytest.mark.model
def test_a_provider_edge_carries_its_answer() -> None:
    words = edge_words(load_actors(), load_cast(DATA / "cast.csv"), load_rules(DATA / "rules.csv"))
    assert words["payment"] == "Charged | Declined"


@pytest.mark.model
def test_a_department_edge_carries_its_requests() -> None:
    words = edge_words(load_actors(), load_cast(DATA / "cast.csv"), load_rules(DATA / "rules.csv"))
    assert words["logistics"] == "free shipping from 50; abroad is 20, not 5"


@pytest.mark.edge
def test_business_map_writes_a_png(tmp_path: Path) -> None:
    out = business_map(
        load_actors(),
        load_cast(DATA / "cast.csv"),
        load_rules(DATA / "rules.csv"),
        tmp_path / "map.png",
    )
    assert out.read_bytes().startswith(PNG_MAGIC)
