"""Tests for the coverage view: what the two tested rows cover and where the bug row differs."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from scripts.utils.coverage_view import (
    columns_covered,
    differing_bits,
    draw,
    grid_growth,
    growth_panels,
    load_tested,
)

TESTED_CSV = Path(__file__).resolve().parents[2] / "01-bits" / "data" / "tested.csv"
ZERO = "000000"


@pytest.mark.view
def test_both_values_of_every_column_are_covered_by_the_two_tested_rows() -> None:
    rows = [row for row in load_tested(TESTED_CSV) if row.kind == "tested"]
    assert columns_covered(rows) == (True,) * 6


@pytest.mark.view
def test_coverage_view_stacks_its_panels(tmp_path: Path) -> None:
    out = draw(load_tested(TESTED_CSV), tmp_path / "coverage-view.png")
    with Image.open(out) as img:
        width, height = img.size
    assert height > width


def _codes(kind: str) -> list[str]:
    return [row.bits for row in load_tested(TESTED_CSV) if row.kind == kind]


@pytest.mark.view
def test_grid_growth_has_seven_panels() -> None:
    assert len(growth_panels(6, _codes("tested"), _codes("bug"))) == 7


@pytest.mark.view
def test_grid_growth_marks_two_tested_cells_in_every_panel_of_two_or_more_cells() -> None:
    panels = growth_panels(6, _codes("tested"), _codes("bug"))
    assert [list(cells.values()).count("tested") for n, cells in panels[1:]] == [2] * 6


@pytest.mark.view
def test_grid_growth_marks_the_bug_cell_in_the_last_panel_only() -> None:
    panels = growth_panels(6, _codes("tested"), _codes("bug"))
    assert [list(cells.values()).count("bug") for n, cells in panels] == [0] * 6 + [1]


@pytest.mark.view
def test_grid_growth_draws_a_wide_strip(tmp_path: Path) -> None:
    out = grid_growth(6, _codes("tested"), _codes("bug"), tmp_path / "grid-growth.png")
    with Image.open(out) as img:
        width, height = img.size
    assert width > height


@pytest.mark.view
def test_the_bug_row_differs_from_the_all_zero_row_in_b0_and_b2_only() -> None:
    bug = next(row for row in load_tested(TESTED_CSV) if row.kind == "bug")
    assert differing_bits(ZERO, bug.bits) == (0, 2)
