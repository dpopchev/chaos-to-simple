"""Tests for the Stacey matrix: the bands, the Who diagonal and the BOOM label."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

from scripts.utils.stacey import draw, load_labels, load_spots, load_zones, side_of, zone_of

ROOT = Path(__file__).resolve().parents[2]
ZONES = load_zones(ROOT / "02-stacey" / "data" / "zones.csv")
LABELS = load_labels(ROOT / "02-stacey" / "data" / "labels.csv")
SOURCED = re.compile(r"\([^()]*\b\d{4}\)")


def stop(section: str) -> tuple[float, float]:
    with (ROOT / "data" / "route.csv").open(newline="", encoding="ascii") as fh:
        row = next(r for r in csv.DictReader(fh) if r["section"] == section)
    return float(row["x"]), float(row["y"])


@pytest.mark.model
def test_the_origin_is_simple() -> None:
    assert zone_of(0.0, 0.0, ZONES) == "simple"


@pytest.mark.model
def test_a_band_starts_at_its_r_min() -> None:
    assert zone_of(0.5, 0.0, ZONES) == "complex"


@pytest.mark.model
def test_the_last_band_is_open_ended() -> None:
    assert zone_of(1.5, 1.5, ZONES) == "boom"


@pytest.mark.model
def test_stop_01_is_above_the_diagonal() -> None:
    assert side_of(*stop("01")) == "above"


@pytest.mark.model
def test_stop_03_is_on_the_diagonal() -> None:
    assert side_of(*stop("03")) == "on"


@pytest.mark.model
def test_stop_06_is_below_the_diagonal() -> None:
    assert side_of(*stop("06")) == "below"


def sourced_or_digit_free(text: str) -> bool:
    """Tell whether a label names its source as a year in parentheses, or carries no number."""
    return SOURCED.search(text) is not None or not any(c.isdigit() for c in text)


@pytest.mark.model
def test_the_boom_quote_names_its_source_or_holds_no_digit() -> None:
    assert sourced_or_digit_free(LABELS["boom_quote"])


@pytest.mark.model
def test_stacey_writes_a_png(tmp_path: Path) -> None:
    route = load_spots(ROOT / "data" / "route.csv")
    out = draw(route, ZONES, LABELS, tmp_path / "m.png", highlight="02")
    assert out.read_bytes().startswith(b"\x89PNG")
