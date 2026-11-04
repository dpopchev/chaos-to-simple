"""Tests for the cohesion figure: rule cards grouped by the question each answers."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.cohesion import Group, draw, groups
from scripts.utils.palette import load_actors, load_contexts
from scripts.utils.paths import load_rules

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def _groups() -> tuple[Group, ...]:
    actors = {
        **load_actors(DATA / "actors.csv"),
        **load_actors(ROOT / "05-how" / "data" / "roles.csv"),
    }
    return groups(load_rules(DATA / "rules.csv"), load_contexts(DATA / "contexts.csv"), actors)


@pytest.mark.model
def test_cohesion_groups_are_four_in_question_order() -> None:
    assert [g.context for g in _groups()] == ["pricing", "shipping", "tax", "fulfilment"]


@pytest.mark.model
def test_cohesion_fulfilment_holds_the_three_shell_rules() -> None:
    assert [r.name for r in _groups()[3].rules] == ["charge", "reserve", "confirm"]


@pytest.mark.edge
def test_cohesion_draw_writes_a_png(tmp_path: Path) -> None:
    out = draw(_groups(), tmp_path / "cohesion.png")
    assert out.read_bytes()[:4] == b"\x89PNG"
