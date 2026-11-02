"""Tests for the rules board: its rows join the data, every stage draws, stage 06 is all green."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.board import board, board_rows, example_tests, header_text, headers, missing_of
from scripts.utils.board import tests_defined as defined_tests
from scripts.utils.paths import load_rules
from scripts.utils.retro import load_questions
from scripts.utils.stage import load_route

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "06-simple" / "tests"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def rows():
    return board_rows(
        load_rules(ROOT / "data" / "rules.csv"),
        load_questions(ROOT / "data" / "questions.csv"),
        example_tests(ROOT / "data" / "examples.csv"),
    )


@pytest.mark.model
def test_stage_06_has_no_missing_test() -> None:
    assert missing_of(rows(), TESTS) == []


@pytest.mark.model
def test_tests_defined_reads_a_test_class(tmp_path: Path) -> None:
    (tmp_path / "test_x.py").write_text("class TestOutOfStock:\n    pass\n", encoding="utf-8")
    assert "TestOutOfStock" in defined_tests(tmp_path)


@pytest.mark.model
def test_board_has_nine_rows() -> None:
    assert len(rows()) == 9


@pytest.mark.model
def test_room_of_the_coupon_bit_is_question_q1() -> None:
    assert rows()[0].room == "q1"


@pytest.mark.model
def test_a_bit_without_a_question_shows_its_bit() -> None:
    assert rows()[3].room == "b3"


def route_headers() -> tuple[str, ...]:
    return headers(load_route(ROOT / "data" / "route.csv"))


@pytest.mark.model
def test_headers_carry_the_route_labels() -> None:
    assert route_headers() == (
        "03 Room: raised",
        "03 Room: sentence",
        "04 Homes",
        "05 Seam",
        "06 Core and shell",
    )


@pytest.mark.model
def test_waiting_columns_are_headed_later() -> None:
    assert header_text(2, 3, route_headers()) == "04 Homes\nlater"


@pytest.mark.edge
@pytest.mark.parametrize("stage", [3, 4, 5, 6])
def test_board_writes_a_png_at_each_stage(tmp_path: Path, stage: int) -> None:
    out = board(rows(), stage, tmp_path / "board.png", TESTS, route_headers())
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.model
def test_board_refuses_an_unknown_stage(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown stage"):
        board(rows(), 7, tmp_path / "board.png", TESTS, route_headers())
