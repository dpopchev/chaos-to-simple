"""Tests for the finance chart: the October totals, the two-line report and the drawn figure."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from scripts.utils.finance import LEGEND, cues, draw, load_october, title, totals

OCTOBER = Path(__file__).resolve().parents[2] / "01-bits" / "data" / "october.csv"


@pytest.mark.edge
def test_load_october_reads_the_four_weeks_in_file_order() -> None:
    assert [w.week for w in load_october(OCTOBER)] == [11, 12, 13, 14]


@pytest.mark.view
def test_totals_are_the_pinned_orders() -> None:
    assert totals(load_october(OCTOBER))[0] == 1214


@pytest.mark.view
def test_totals_are_the_pinned_shortfall() -> None:
    assert totals(load_october(OCTOBER))[1] == 6070


@pytest.mark.view
def test_title_names_the_gap() -> None:
    assert title(load_october(OCTOBER)) == (
        "October: 6,070 EUR of shipping nowhere to be found, 1,214 parcels"
    )


@pytest.mark.view
def test_legend_reads_finances_count_income_and_the_difference() -> None:
    words = [name.split(":")[0] for name in LEGEND]
    code_talk = any("code" in name or "R1" in name for name in LEGEND)
    assert (words, code_talk) == (["expected", "received", "missing"], False)


@pytest.mark.view
def test_cues_count_no_free_parcel_without_the_coupon() -> None:
    total = next(r for r in cues(load_october(OCTOBER)).splitlines() if r.startswith("total"))
    assert total.endswith(" 0")


@pytest.mark.view
def test_draw_makes_a_wide_figure(tmp_path: Path) -> None:
    out = draw(load_october(OCTOBER), tmp_path / "finance.png")
    with Image.open(out) as img:
        width, height = img.size
    assert width > 2 * height
