"""Tests for the stage: the business map of the shop, its departments and its providers."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.palette import colour_of, load_actors
from scripts.utils.paths import load_cast, load_incidents, load_rules
from scripts.utils.stacey import load_zones
from scripts.utils.stage import (
    GREY,
    agenda_strip,
    business_map,
    edge_words,
    incident_marks,
    load_route,
    map_legend,
    stop_alpha,
    stop_face,
)

DATA = Path(__file__).resolve().parents[2] / "data"
ZONES = load_zones(DATA.parent / "02-stacey" / "data" / "zones.csv")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


@pytest.mark.model
def test_a_provider_edge_carries_its_answer() -> None:
    words = edge_words(load_actors(), load_cast(DATA / "cast.csv"), load_rules(DATA / "rules.csv"))
    assert words["payment"] == "Charged | Declined"


@pytest.mark.model
def test_a_department_edge_carries_its_requests() -> None:
    words = edge_words(load_actors(), load_cast(DATA / "cast.csv"), load_rules(DATA / "rules.csv"))
    assert words["logistics"] == "free shipping from 50; abroad is 20, not 5"


@pytest.mark.model
def test_map_legend_names_core_and_generic() -> None:
    assert map_legend() == (
        ("core subdomain: the shop and its policies", "outlined"),
        ("generic subdomain: sourced out", "filled"),
    )


@pytest.mark.edge
def test_business_map_writes_a_png(tmp_path: Path) -> None:
    out = business_map(
        load_actors(),
        load_cast(DATA / "cast.csv"),
        load_rules(DATA / "rules.csv"),
        tmp_path / "map.png",
    )
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_load_route_reads_eight_stops_in_order() -> None:
    assert [s.section for s in load_route(DATA / "route.csv")] == [f"0{i}" for i in range(8)]


@pytest.mark.edge
def test_load_route_reads_the_label_and_icon() -> None:
    stop = load_route(DATA / "route.csv")[1]
    assert (stop.label, stop.icon) == ("Bits", "code-branch")


@pytest.mark.model
def test_incident_marks_follow_told_in() -> None:
    marks = incident_marks(load_incidents(DATA / "incidents.csv"))
    assert marks == {"01": "I1", "02": "I2", "05": "I3"}


@pytest.mark.edge
def test_agenda_strip_writes_a_png(tmp_path: Path) -> None:
    out = agenda_strip(
        load_route(DATA / "route.csv"),
        load_incidents(DATA / "incidents.csv"),
        tmp_path / "agenda.png",
    )
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.model
def test_stop_face_is_the_band_colour() -> None:
    stop = load_route(DATA / "route.csv")[1]
    assert stop_face(stop, ZONES) == colour_of("payment")


@pytest.mark.model
def test_stop_face_is_grey_for_a_stop_off_the_matrix() -> None:
    stop = load_route(DATA / "route.csv")[0]
    assert stop_face(stop, ZONES) == GREY


@pytest.mark.model
def test_stop_alpha_fades_the_other_stops() -> None:
    assert (stop_alpha("01", "01"), stop_alpha("02", "01")) == (1.0, 0.25)


@pytest.mark.model
def test_stop_alpha_keeps_every_stop_without_a_highlight() -> None:
    assert stop_alpha("02", None) == 1.0
