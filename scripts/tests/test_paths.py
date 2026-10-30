"""The talk's arithmetic, pinned."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.paths import (
    Rule,
    bars_from_rules,
    bits_by,
    count_report,
    grid,
    load_rules,
    rules_table,
    split,
    stacked_bar,
    tangled,
)

REPO_RULES = Path(__file__).resolve().parents[2] / "data" / "rules.csv"

SAMPLE = (
    "bit,scope,context,name,rule,code\n"
    "b0,core,pricing,coupon,A coupon,coupon\n"
    "b1,core,pricing,member,A member,member\n"
    "b2,core,shipping,zone,A zone,zone\n"
    "s0,shell,payment,charge,A charge,charge\n"
)


def test_sequential_ifs_multiply_and_boundaries_add() -> None:
    assert tangled(6) == 64
    assert tangled(9) == 512
    assert split([6, 3]) == 72
    assert split([2, 3, 1]) == 14


def test_load_rules_reads_every_column(tmp_path: Path) -> None:
    path = tmp_path / "rules.csv"
    path.write_text(SAMPLE, encoding="ascii")
    rules = load_rules(path)
    assert rules[0] == Rule("b0", "core", "pricing", "coupon", "A coupon", "coupon")
    assert bits_by(rules, "scope") == {"core": 3, "shell": 1}
    assert bits_by(rules, "context") == {"pricing": 2, "shipping": 1, "payment": 1}


def test_count_report_names_the_three_ways_of_counting(tmp_path: Path) -> None:
    path = tmp_path / "rules.csv"
    path.write_text(SAMPLE, encoding="ascii")
    report = count_report(load_rules(path))
    assert "one function, 4 bits:  2^4 = 16" in report
    assert "core | shell:           2^3 + 2^1 = 8 + 2 = 10" in report
    assert "contexts | shell:       4 + 2 + 2 = 8" in report


def test_the_talk_numbers_come_from_the_repo_data() -> None:
    report = count_report(load_rules(REPO_RULES))
    assert "2^9 = 512" in report
    assert "64 + 8 = 72" in report
    assert "4 + 8 + 2 + 8 = 22" in report


def test_rules_table_is_aligned_text() -> None:
    table = rules_table(load_rules(REPO_RULES))
    lines = table.splitlines()
    assert lines[0].startswith("bit  context")
    assert len(lines) == 10
    assert all(line == line.rstrip() for line in lines)


def test_grid_lists_every_path_once() -> None:
    rows = grid(6).splitlines()
    cells = [cell for row in rows for cell in row.split()]
    assert len(rows) == 8
    assert len(cells) == 64 == len(set(cells))
    assert cells[0] == "000000" and cells[-1] == "111111"


def test_bars_follow_the_inventory() -> None:
    bars = bars_from_rules(load_rules(REPO_RULES))
    totals = [sum(value for _, value in segments) for _, segments in bars]
    assert totals == [512, 72, 22]


def test_stacked_bar_writes_a_png(tmp_path: Path) -> None:
    pytest.importorskip("matplotlib")
    out = tmp_path / "charts" / "paths.png"
    stacked_bar(out, bars_from_rules(load_rules(REPO_RULES)))
    assert out.exists() and out.stat().st_size > 0
