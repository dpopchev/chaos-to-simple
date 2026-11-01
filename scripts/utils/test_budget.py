"""The frame budget: loaded from data/budget.csv, compared with the frames each index holds."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.budget import Budget, compare, frames_of, load_budget, minutes_total


@pytest.fixture
def budget() -> list[Budget]:
    return [Budget("00", 2, 3), Budget("01", 11, 10)]


@pytest.mark.model
def test_load_budget_reads_section_frames_and_minutes(tmp_path: Path) -> None:
    path = tmp_path / "budget.csv"
    path.write_text("section,frames,minutes\n00,2,3\n01,11,10\n", encoding="ascii")
    assert load_budget(path) == [Budget("00", 2, 3), Budget("01", 11, 10)]


@pytest.mark.model
def test_frames_of_counts_the_lines_that_start_with_two_hashes() -> None:
    assert frames_of("# Title\n\n## One\n\ntext\n\n## Two\n") == 2


@pytest.mark.edge
def test_frames_of_ignores_a_deeper_heading_and_an_indented_one() -> None:
    assert frames_of("### Three\n  ## indented\n## One\n") == 1


@pytest.mark.model
def test_compare_names_a_section_whose_count_differs(budget: list[Budget]) -> None:
    assert compare(budget, {"00": 2, "01": 9}) == [("01", 11, 9)]


@pytest.mark.model
def test_compare_is_empty_when_every_count_matches(budget: list[Budget]) -> None:
    assert compare(budget, {"00": 2, "01": 11}) == []


@pytest.mark.edge
def test_compare_counts_a_section_with_no_index_as_zero(budget: list[Budget]) -> None:
    assert compare(budget, {"00": 2}) == [("01", 11, 0)]


@pytest.mark.model
def test_minutes_total_sums_the_minutes(budget: list[Budget]) -> None:
    assert minutes_total(budget) == 13
