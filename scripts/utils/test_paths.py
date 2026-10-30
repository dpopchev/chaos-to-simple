"""The talk's arithmetic, pinned."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.paths import (
    Rule,
    bars_from_rules,
    bits_by,
    count_report,
    epilogue_report,
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


@pytest.fixture
def sample_rules(tmp_path: Path) -> list[Rule]:
    path = tmp_path / "rules.csv"
    path.write_text(SAMPLE, encoding="ascii")
    return load_rules(path)


@pytest.fixture
def repo_rules() -> list[Rule]:
    return load_rules(REPO_RULES)


@pytest.mark.model
def test_sequential_ifs_multiply() -> None:
    assert tangled(6) == 64


@pytest.mark.model
def test_nine_sequential_ifs_make_512_paths() -> None:
    assert tangled(9) == 512


@pytest.mark.model
def test_boundaries_add_the_split_paths() -> None:
    assert split([6, 3]) == 72


@pytest.mark.model
def test_three_boundaries_add_up() -> None:
    assert split([2, 3, 1]) == 14


@pytest.mark.edge
def test_load_rules_reads_every_column(sample_rules: list[Rule]) -> None:
    assert sample_rules[0] == Rule("b0", "core", "pricing", "coupon", "A coupon", "coupon")


@pytest.mark.edge
def test_bits_by_scope_counts_each_scope(sample_rules: list[Rule]) -> None:
    assert bits_by(sample_rules, "scope") == {"core": 3, "shell": 1}


@pytest.mark.edge
def test_bits_by_context_counts_each_context(sample_rules: list[Rule]) -> None:
    assert bits_by(sample_rules, "context") == {"pricing": 2, "shipping": 1, "payment": 1}


class TestCountReportNamesThreeWaysOfCounting:
    @pytest.fixture
    def report(self, sample_rules: list[Rule]) -> str:
        return count_report(sample_rules)

    @pytest.mark.edge
    def test_one_function_multiplies(self, report: str) -> None:
        assert "one function, 4 bits:  2^4 = 16" in report

    @pytest.mark.edge
    def test_scopes_add(self, report: str) -> None:
        assert "core | shell:           2^3 + 2^1 = 8 + 2 = 10" in report

    @pytest.mark.edge
    def test_contexts_add(self, report: str) -> None:
        assert "contexts | shell:       4 + 2 + 2 = 8" in report


class TestTalkNumbersComeFromRepoData:
    @pytest.fixture
    def report(self, repo_rules: list[Rule]) -> str:
        return count_report(repo_rules)

    @pytest.mark.edge
    def test_one_function_is_512(self, report: str) -> None:
        assert "2^9 = 512" in report

    @pytest.mark.edge
    def test_core_and_shell_make_72(self, report: str) -> None:
        assert "64 + 8 = 72" in report

    @pytest.mark.edge
    def test_contexts_make_22(self, report: str) -> None:
        assert "4 + 8 + 2 + 8 = 22" in report


class TestRulesTableIsAlignedText:
    @pytest.fixture
    def lines(self, repo_rules: list[Rule]) -> list[str]:
        return rules_table(repo_rules).splitlines()

    @pytest.mark.edge
    def test_header_starts_with_bit_and_context(self, lines: list[str]) -> None:
        assert lines[0].startswith("bit  context")

    @pytest.mark.edge
    def test_one_header_and_nine_rule_lines(self, lines: list[str]) -> None:
        assert len(lines) == 10

    @pytest.mark.edge
    def test_no_line_has_trailing_spaces(self, lines: list[str]) -> None:
        assert all(line == line.rstrip() for line in lines)


class TestGridListsEveryPathOnce:
    @pytest.fixture
    def rows(self) -> list[str]:
        return grid(6).splitlines()

    @pytest.fixture
    def cells(self, rows: list[str]) -> list[str]:
        return [cell for row in rows for cell in row.split()]

    @pytest.mark.model
    def test_eight_rows(self, rows: list[str]) -> None:
        assert len(rows) == 8

    @pytest.mark.model
    def test_sixty_four_distinct_cells(self, cells: list[str]) -> None:
        assert len(cells) == len(set(cells)) == 64

    @pytest.mark.model
    def test_first_cell_is_all_zeros(self, cells: list[str]) -> None:
        assert cells[0] == "000000"

    @pytest.mark.model
    def test_last_cell_is_all_ones(self, cells: list[str]) -> None:
        assert cells[-1] == "111111"


@pytest.mark.model
def test_bars_follow_the_inventory(repo_rules: list[Rule]) -> None:
    bars = bars_from_rules(repo_rules)
    totals = [sum(value for _, value in segments) for _, segments in bars]
    assert totals == [512, 72, 22]


class TestStackedBarWritesAPng:
    @pytest.fixture
    def out(self, tmp_path: Path, repo_rules: list[Rule]) -> Path:
        pytest.importorskip("matplotlib")
        path = tmp_path / "charts" / "paths.png"
        stacked_bar(path, bars_from_rules(repo_rules))
        return path

    @pytest.mark.edge
    def test_the_file_exists(self, out: Path) -> None:
        assert out.exists()

    @pytest.mark.edge
    def test_the_file_is_not_empty(self, out: Path) -> None:
        assert out.stat().st_size > 0


SEVENTH_RULES = Path(__file__).resolve().parents[2] / "data" / "seventh.csv"


class TestEpilogueCountsTheSeventhIf:
    @pytest.fixture
    def lines(self, repo_rules: list[Rule]) -> list[str]:
        after = [*repo_rules, *load_rules(SEVENTH_RULES)]
        return epilogue_report(repo_rules, after).splitlines()

    @pytest.mark.model
    def test_epilogue_one_function_doubles_to_1024(self, lines: list[str]) -> None:
        assert lines[0] == "one function:      512 -> 1024  (+512)"

    @pytest.mark.model
    def test_epilogue_core_and_shell_grow_to_136(self, lines: list[str]) -> None:
        assert lines[1] == "core | shell:       72 ->  136  (+64)"

    @pytest.mark.model
    def test_epilogue_contexts_and_shell_grow_to_30(self, lines: list[str]) -> None:
        assert lines[2] == "contexts | shell:   22 ->   30  (+8)"

    @pytest.mark.edge
    def test_epilogue_is_three_lines(self, lines: list[str]) -> None:
        assert len(lines) == 3
