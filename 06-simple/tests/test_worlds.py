"""The eight worlds measured by running the shell: a table of bits, outcome, charged, mailed."""

from __future__ import annotations

from datetime import date

import pytest

from s06_simple.core import Request
from s06_simple.worlds import WorldRow, rows, table


@pytest.fixture
def measured(plain: Request, today: date) -> tuple[WorldRow, ...]:
    return rows(plain, today)


def test_eight_worlds_give_four_distinct_outcomes(measured: tuple[WorldRow, ...]) -> None:
    assert len({row.outcome for row in measured}) == 4


def test_the_table_has_eight_rows(measured: tuple[WorldRow, ...]) -> None:
    """The header and one line per world."""
    assert len(table(measured).splitlines()) == 1 + 8


def test_no_world_with_the_stock_gone_is_charged(measured: tuple[WorldRow, ...]) -> None:
    assert [row.bits for row in measured if row.bits & 0b010 and row.charged] == []
