"""The talk's arithmetic, pinned."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts.paths import main
from scripts.utils.paths import (
    Bar,
    CastRow,
    Incident,
    Rule,
    bars_from_rules,
    bits_by,
    cast_table,
    contexts_table,
    count_report,
    doubling_table,
    epilogue_bars,
    epilogue_report,
    grid,
    growth,
    growth_chart,
    line_of,
    load_cast,
    load_incidents,
    load_rules,
    rules_table,
    split,
    stacked_bar,
    tangled,
    wounds_selector,
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


CAST_CSV = (
    "bit,week,requested_by,words,aside,fragment\n"
    'b0,3,Marketing,"10 off, with the code",why ten,if a\n'
    "s0,,Nobody,nobody wrote it down,,call(x)\n"
)

CAST_SOURCE = "first\nif a:\n    pass\ncall(x)\n"


@pytest.fixture
def cast_rows(tmp_path: Path) -> list[CastRow]:
    path = tmp_path / "cast.csv"
    path.write_text(CAST_CSV, encoding="ascii")
    return load_cast(path)


@pytest.mark.edge
def test_cast_row_reads_every_column(cast_rows: list[CastRow]) -> None:
    assert cast_rows[0] == CastRow("b0", 3, "Marketing", "10 off, with the code", "why ten", "if a")


INCIDENTS_CSV = (
    "id,week,told_in,closed_in,closed_by,kind,cost\n"
    'I1,14,01,06,test_a,rule,"1,000 orders"\n'
    "I2,15,02,04,rules.csv b2,decision,one meeting\n"
)


@pytest.mark.edge
def test_load_incidents_reads_every_column(tmp_path: Path) -> None:
    path = tmp_path / "incidents.csv"
    path.write_text(INCIDENTS_CSV, encoding="ascii")
    assert load_incidents(path)[0] == Incident(
        "I1", "14", "01", "06", "test_a", "rule", "1,000 orders"
    )


@pytest.mark.edge
def test_exhibits_carry_the_incident_costs() -> None:
    root = REPO_RULES.parents[1]
    costs = {i.id: i.cost for i in load_incidents(root / "data" / "incidents.csv")}
    exhibits = {"I1": "01-bits", "I3": "05-how"}
    assert all(
        number in (root / folder / "data" / "incident.txt").read_text(encoding="ascii")
        for id_, folder in exhibits.items()
        for number in re.findall(r"\d[\d,]*\d|\d", costs[id_])
    )


@pytest.mark.model
def test_wounds_selector_skips_a_closed_by_that_is_no_test() -> None:
    incidents = (
        Incident("I1", "14", "01", "06", "test_a", "rule", "x"),
        Incident("I2", "15", "02", "04", "rules.csv b2", "decision", "y"),
        Incident("I3", "18", "05", "06", "test_b", "effect", "z"),
    )
    assert wounds_selector(incidents) == "test_a or test_b"


@pytest.mark.model
def test_cast_line_of_finds_the_one_line() -> None:
    assert line_of("call(x)", CAST_SOURCE) == 4


@pytest.mark.edge
def test_cast_line_of_missing_fragment_fails_loud() -> None:
    with pytest.raises(ValueError, match="matches 0 lines"):
        line_of("absent", CAST_SOURCE)


@pytest.mark.edge
def test_cast_line_of_duplicated_fragment_fails_loud() -> None:
    with pytest.raises(ValueError, match="2 lines"):
        line_of("a", "a\nb a\n")


class TestCastTableNamesTheRequester:
    @pytest.fixture
    def lines(self, cast_rows: list[CastRow]) -> list[str]:
        return cast_table(cast_rows, CAST_SOURCE).splitlines()

    @pytest.mark.model
    def test_cast_header_is_line_bit_who_words(self, lines: list[str]) -> None:
        assert lines[0].split() == ["line", "bit", "who", "words"]

    @pytest.mark.model
    def test_cast_row_gives_line_bit_who_and_words(self, lines: list[str]) -> None:
        assert lines[1].split(None, 3) == ["2", "b0", "Marketing", "10 off, with the code"]

    @pytest.mark.edge
    def test_cast_table_has_no_trailing_spaces(self, lines: list[str]) -> None:
        assert all(line == line.rstrip() for line in lines)


CONTEXTS_RULES = (
    "bit,scope,context,name,rule,code\n"
    "b0,core,pricing,coupon,A coupon,coupon\n"
    "b1,core,pricing,member,A member,member\n"
    "b2,core,shipping,zone,A zone,zone\n"
    "s0,shell,payment,charge,A charge,charge\n"
)

CONTEXTS_CAST = (
    "bit,week,requested_by,words,aside,fragment\n"
    "b0,3,Marketing,a,,x\n"
    "b1,5,Loyalty program,b,,y\n"
    "b2,6,Marketing,c,,z\n"
    "s0,,Nobody,d,,w\n"
)


class TestContextsTableJoinsRulesAndCast:
    @pytest.fixture
    def lines(self, tmp_path: Path) -> list[str]:
        rules_path = tmp_path / "rules.csv"
        cast_path = tmp_path / "cast.csv"
        rules_path.write_text(CONTEXTS_RULES, encoding="ascii")
        cast_path.write_text(CONTEXTS_CAST, encoding="ascii")
        return contexts_table(load_rules(rules_path), load_cast(cast_path)).splitlines()

    @pytest.mark.model
    def test_contexts_table_header_names_four_columns(self, lines: list[str]) -> None:
        assert lines[0].split() == ["context", "bits", "paths", "who"]

    @pytest.mark.model
    def test_contexts_table_pricing_has_two_bits_four_paths_two_requesters(
        self, lines: list[str]
    ) -> None:
        assert lines[1].split(None, 1)[1].split(None, 3) == [
            "b0",
            "b1",
            "4",
            "Marketing, Loyalty program",
        ]

    @pytest.mark.model
    def test_contexts_table_shell_context_is_asked_by_nobody(self, lines: list[str]) -> None:
        assert lines[3].split() == ["payment", "s0", "2", "Nobody"]

    @pytest.mark.edge
    def test_contexts_table_has_no_trailing_spaces(self, lines: list[str]) -> None:
        assert all(line == line.rstrip() for line in lines)


SEVENTH_RULES =Path(__file__).resolve().parents[2] / "data" / "seventh.csv"


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


class TestEpilogueBarsGrowShippingOnly:
    @pytest.fixture
    def bars(self, repo_rules: list[Rule]) -> tuple[Bar, Bar]:
        return epilogue_bars(repo_rules, load_rules(SEVENTH_RULES))

    @pytest.mark.model
    def test_epilogue_bars_grow_shipping_only(self, bars: tuple[Bar, Bar]) -> None:
        before, after = (dict(segments) for _, segments in bars)
        assert {k: after[k] - before[k] for k in before if after[k] != before[k]} == {
            "shipping": 8
        }

    @pytest.mark.model
    def test_epilogue_bars_total_22_and_30(self, bars: tuple[Bar, Bar]) -> None:
        assert [sum(value for _, value in segments) for _, segments in bars] == [22, 30]


@pytest.mark.edge
def test_epilogue_chart_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "charts" / "epilogue.png"
    main(
        [
            "epilogue-chart",
            "--rules",
            str(REPO_RULES),
            "--seventh",
            str(SEVENTH_RULES),
            "--out",
            str(out),
        ]
    )
    assert out.read_bytes().startswith(b"\x89PNG")


DOUBLING_CAST = [
    *[CastRow(f"b{n}", 3 + n, f"Team {n}", f"ask {n}", "", f"if {n}") for n in range(6)],
    CastRow("s0", None, "Nobody", "unwritten", "", "call(x)"),
]


class TestDoublingTableCountsAlong:
    @pytest.fixture
    def lines(self) -> list[str]:
        return doubling_table(DOUBLING_CAST).splitlines()

    @pytest.mark.model
    def test_doubling_last_row_is_six_bits_64_paths(self, lines: list[str]) -> None:
        assert lines[-1].split()[-2:] == ["6", "64"]

    @pytest.mark.model
    def test_doubling_has_one_row_per_core_bit(self, lines: list[str]) -> None:
        assert len(lines) == 1 + 6

    @pytest.mark.model
    def test_doubling_table_has_no_asked_for_column(self, lines: list[str]) -> None:
        assert lines[0].split() == ["week", "who", "bits", "paths"]


@pytest.mark.model
def test_doubling_upto_two_rows_has_two_rows() -> None:
    assert len(doubling_table(DOUBLING_CAST, upto=2).splitlines()) == 1 + 2


@pytest.mark.model
def test_cast_table_rows_run_down_the_source() -> None:
    cast = [
        CastRow("s0", None, "Nobody", "unwritten", "", "call(x)"),
        CastRow("b0", 3, "Marketing", "ask", "", "if a"),
    ]
    lines = cast_table(cast, CAST_SOURCE).splitlines()[1:]
    assert [line.split()[0] for line in lines] == ["2", "4"]


@pytest.mark.model
def test_growth_ends_at_week_10_with_64_paths() -> None:
    weeks = (3, 5, 6, 6, 9, 10)
    cast = [CastRow(f"b{n}", w, "Team", "ask", "", "if x") for n, w in enumerate(weeks)]
    last = growth(cast)[-1]
    assert (last.week, last.bits, last.paths) == (10, 6, 64)


@pytest.mark.model
def test_growth_skips_the_shell_rows() -> None:
    assert len(growth(DOUBLING_CAST)) == 6


@pytest.mark.edge
def test_growth_chart_writes_a_png(tmp_path: Path) -> None:
    out = growth_chart(tmp_path / "nested" / "growth.png", growth(DOUBLING_CAST))
    assert out.read_bytes().startswith(b"\x89PNG")
