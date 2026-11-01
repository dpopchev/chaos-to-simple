"""Tests for the coverage view: what the two tested rows cover and where the bug row differs."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from scripts.utils.coverage_view import columns_covered, differing_bits, draw, load_tested

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


@pytest.mark.view
def test_the_bug_row_differs_from_the_all_zero_row_in_b0_and_b2_only() -> None:
    bug = next(row for row in load_tested(TESTED_CSV) if row.kind == "bug")
    assert differing_bits(ZERO, bug.bits) == (0, 2)
