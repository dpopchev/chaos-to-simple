"""Tests for the finance chart: the October totals, the two-line report and the drawn figure."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from scripts.utils.finance import draw, load_october, report, totals

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
def test_report_is_two_lines_with_thousands_separators() -> None:
    assert report(load_october(OCTOBER)) == (
        "1,214 orders got free shipping\n6,070 BGN of shipping income never arrived\n"
    )


@pytest.mark.view
def test_draw_makes_a_wide_figure(tmp_path: Path) -> None:
    out = draw(load_october(OCTOBER), tmp_path / "finance.png")
    with Image.open(out) as img:
        width, height = img.size
    assert width > 2 * height
