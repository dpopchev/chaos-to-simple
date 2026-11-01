"""Tests for the Stacey matrix: the bands, the Who diagonal and the BOOM label."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.utils.stacey import boom_label, load_labels, load_zones, side_of, zone_of

ROOT = Path(__file__).resolve().parents[2]
ZONES = load_zones(ROOT / "02-stacey" / "data" / "zones.csv")
LABELS = load_labels(ROOT / "02-stacey" / "data" / "labels.csv")


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


@pytest.mark.model
def test_the_boom_label_holds_no_digit_while_the_quote_is_empty() -> None:
    assert not any(c.isdigit() for c in boom_label(LABELS, ZONES))
