"""The six lines: loaded from data/lines.csv, found in their section and in 07."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.lines import Line, load_lines, missing

LINES_CSV = (
    'section,believed,learned\n01-bits,B1,"Count, then trust."\n02-stacey,B2,Agree the What.\n'
)


@pytest.fixture
def lines() -> list[Line]:
    return [
        Line("01-bits", "B1", "Count, then trust."),
        Line("02-stacey", "B2", "Agree the What."),
    ]


@pytest.mark.edge
def test_load_lines_reads_a_quoted_line_with_a_comma(tmp_path: Path) -> None:
    path = tmp_path / "lines.csv"
    path.write_text(LINES_CSV, encoding="ascii")
    assert load_lines(path)[0] == Line("01-bits", "B1", "Count, then trust.")


@pytest.mark.model
def test_load_lines_reads_believed_and_learned(tmp_path: Path) -> None:
    path = tmp_path / "lines.csv"
    path.write_text(
        'section,believed,learned\n01-bits,A green badge means tested,"Count, then trust."\n',
        encoding="ascii",
    )
    assert load_lines(path) == [Line("01-bits", "A green badge means tested", "Count, then trust.")]


@pytest.mark.model
def test_missing_names_an_absent_believed_line(lines: list[Line]) -> None:
    texts = {
        "01-bits": "B1\nCount, then trust.",
        "02-stacey": "Agree the What.",
        "07-close": "- B1 -> Count, then trust.\n- B2 -> Agree the What.",
    }
    assert missing(lines, texts) == [("02-stacey believed", "02-stacey")]


@pytest.mark.model
def test_missing_is_empty_when_every_line_is_in_place(lines: list[Line]) -> None:
    texts = {
        "01-bits": "B1 Count, then trust.",
        "02-stacey": "B2 Agree the What.",
        "07-close": "B1 Count, then trust.\nB2 Agree the What.",
    }
    assert missing(lines, texts) == []


@pytest.mark.model
def test_missing_names_a_line_absent_from_its_section(lines: list[Line]) -> None:
    texts = {
        "01-bits": "B1 Count, then trust.",
        "02-stacey": "B2 something else",
        "07-close": "B1 B2 Count, then trust. Agree the What.",
    }
    assert missing(lines, texts) == [("02-stacey learned", "02-stacey")]


@pytest.mark.model
def test_missing_names_a_line_absent_from_07(lines: list[Line]) -> None:
    texts = {
        "01-bits": "B1 Count, then trust.",
        "02-stacey": "B2 Agree the What.",
        "07-close": "B1 B2 Count, then trust.",
    }
    assert missing(lines, texts) == [("02-stacey learned", "07-close")]


@pytest.mark.model
def test_missing_collapses_runs_of_whitespace(lines: list[Line]) -> None:
    texts = {
        "01-bits": "B1 Count,\n  then   trust.",
        "02-stacey": "B2 Agree the\nWhat.",
        "07-close": "B1 B2 Count, then trust.  Agree the What.",
    }
    assert missing(lines, texts) == []
