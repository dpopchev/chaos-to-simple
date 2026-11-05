"""The storyboard: the checkout at each step, its diffs and the bubbles."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts.paths import tally_text
from scripts.utils.paths import load_cast
from scripts.utils.storyboard import (
    BubbleRow,
    bubble,
    code_tally,
    count_tests,
    step_diff,
    step_lines,
    step_test,
    step_view,
    suite_view,
    wrap_row,
)
from scripts.utils.widths import snippet_text, strip_step_markers

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (ROOT / "01-bits/s01_bits/chaos.py").read_text(encoding="ascii")
CAST = load_cast(ROOT / "data/cast.csv")
STEPS = range(1, 7)
ASIDE = re.compile(r"  # .*$", re.MULTILINE)


def added(n: int) -> list[str]:
    """The lines a step's diff adds, without the plus sign."""
    return [
        line[1:]
        for line in step_diff(SOURCE, n).splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]


def marked(n: int) -> list[str]:
    """The lines of the exhibit marked for step n, markers stripped."""
    rows = [row for row in SOURCE.splitlines() if row.endswith(f"# [step: {n}]")]
    return [ASIDE.sub("", row) for row in strip_step_markers("\n".join(rows)).splitlines()]


@pytest.mark.view
def test_step_six_is_the_full_function_stripped() -> None:
    expected = snippet_text(strip_step_markers(SOURCE), "checkout").strip()
    assert step_lines(SOURCE, 6) == ASIDE.sub("", expected)


@pytest.mark.view
@pytest.mark.parametrize("n", STEPS)
def test_each_step_adds_exactly_the_lines_marked_for_it(n: int) -> None:
    assert added(n) == marked(n)


@pytest.mark.view
@pytest.mark.parametrize("n", STEPS)
def test_each_step_adds_its_cast_fragment(n: int) -> None:
    fragment = next(row.fragment for row in CAST if row.step == n)
    assert fragment in "\n".join(added(n))


@pytest.mark.view
def test_step_view_adds_exactly_the_lines_of_its_step() -> None:
    view = step_view(SOURCE, 3).splitlines()[1:]
    assert [row[1:] for row in view if row.startswith("+")] == marked(3)


@pytest.mark.view
def test_step_diff_is_compact() -> None:
    rows = step_view(SOURCE, 3).splitlines()[1:]
    assert [row[0] for row in rows if row != "---" and row[0] in "+~"] == ["+", "+", "+"]


@pytest.mark.view
def test_step_diff_has_no_merged_line() -> None:
    assert not any(row.startswith("~") for row in step_view(SOURCE, 3).splitlines())


@pytest.mark.view
def test_step_zero_view_is_the_whole_skeleton() -> None:
    skeleton = ["+" + row for row in step_lines(SOURCE, 0).splitlines()]
    assert step_view(SOURCE, 0).splitlines()[1:] == skeleton


@pytest.mark.view
def test_step_view_keeps_only_the_scope_and_the_changes() -> None:
    body = step_view(SOURCE, 3).splitlines()[1:]
    assert body == [" def checkout(...):", *("+" + row for row in marked(3))]


@pytest.mark.view
def test_step_view_heading_says_policy_for_one() -> None:
    assert step_view(SOURCE, 1).splitlines()[0] == "checkout v1: 1 policy, 2 paths, 11 lines"


@pytest.mark.view
def test_step_view_heading_counts_policies_paths_and_lines() -> None:
    assert step_view(SOURCE, 6).splitlines()[0] == "checkout v6: 6 policies, 64 paths, 22 lines"


@pytest.mark.view
def test_test_view_heading_counts_the_tests_and_lines() -> None:
    assert suite_view(SOURCE, 6).splitlines()[0] == "tests v6: 2 tests, 18 lines"


@pytest.mark.view
def test_wide_row_wraps_before_and() -> None:
    row = next(r for r in step_diff(SOURCE, 1).splitlines() if "coupon_valid_until is not" in r)
    assert [len(part) <= 60 for part in wrap_row(row, 60)] == [True, True]


@pytest.mark.view
def test_step_zero_diff_is_the_skeleton_from_nothing() -> None:
    assert added(0) == marked(0)


@pytest.mark.view
def test_step_diff_has_no_header() -> None:
    lines = step_diff(SOURCE, 3).splitlines()
    assert not any(line.startswith(("---", "+++", "@@")) for line in lines)


@pytest.mark.view
def test_step_lines_drop_the_narrator_asides() -> None:
    assert "what if" not in step_lines(SOURCE, 6)


def flat(text: str) -> str:
    """The text without narrator comments, whitespace normalised."""
    return " ".join(ASIDE.sub("", text).split())


@pytest.mark.view
def test_step_test_matches_test_chaos() -> None:
    tests = (ROOT / "01-bits/tests/test_chaos.py").read_text(encoding="ascii")
    assert flat(step_test(SOURCE, 6)) == flat(snippet_text(tests, "two-tests"))


@pytest.mark.view
def test_step_test_expected_at_step_3() -> None:
    assert 'assert total == Decimal("81.00")' in step_test(SOURCE, 3)


@pytest.mark.view
def test_step_test_regular_order_at_step_0() -> None:
    regular = step_test(SOURCE, 0).split("def test_order_with_everything")[0]
    assert 'assert total == Decimal("45.00")' in regular


@pytest.mark.view
def test_bubble_reads_actor_label_date_and_words() -> None:
    row = BubbleRow(1, 3, "2026-08-11", "marketing", "Small change?")
    assert bubble(row, {"marketing": "Marketing"}) == "Marketing, 2026-08-11\nSmall change?\n"


@pytest.mark.view
def test_bubble_wraps_at_the_column_width() -> None:
    words = "Autumn campaign: 10 EUR off with the code AUTUMN. Small change? Right after it."
    row = BubbleRow(1, 3, "2026-08-11", "marketing", words)
    lines = bubble(row, {"marketing": "Marketing"}, width=34).splitlines()
    assert max(map(len, lines)) <= 34


@pytest.mark.view
def test_bubble_stays_on_one_line() -> None:
    words = "Autumn campaign: 10 EUR off with the code AUTUMN. Small change? Yes."
    row = BubbleRow(1, 3, "2026-08-11", "marketing", words)
    assert len(bubble(row, {"marketing": "Marketing"}, width=None).splitlines()) == 2


@pytest.mark.view
def test_code_tally_names_the_function() -> None:
    assert code_tally("price", 3, 1, 2, 9) == "price v3: 1 policy, 2 paths, 9 lines"


@pytest.mark.view
def test_tally_text_counts_tests_and_lines(tmp_path: Path) -> None:
    (tmp_path / "test_a.py").write_text("def test_one():\n    pass\n", encoding="ascii")
    (tmp_path / "test_b.py").write_text("def test_two():\n    pass\n", encoding="ascii")
    assert tally_text(1, [tmp_path], None) == "tests v1: 2 tests, 4 lines\n"


@pytest.mark.view
def test_tally_counts_tests_dir(tmp_path: Path) -> None:
    (tmp_path / "test_a.py").write_text("def test_one():\n    pass\n\ndef test_two():\n    pass\n")
    texts = [path.read_text() for path in sorted(tmp_path.glob("test_*.py"))]
    assert count_tests(texts) == 2


@pytest.mark.view
def test_count_tests_counts_methods_in_a_class() -> None:
    text = "class TestOrder:\n    def test_a(self): pass\n    def test_b(self): pass\n"
    assert count_tests([text]) == 2


@pytest.mark.view
def test_bubble_head_carries_the_tag() -> None:
    row = BubbleRow(0, 0, "", "marketing", "Of the cart.", "R1")
    assert bubble(row, {"marketing": "Marketing"}) == "R1 Marketing\nOf the cart.\n"


@pytest.mark.view
def test_bubble_without_a_date_reads_the_label_alone() -> None:
    row = BubbleRow(2, 0, "", "dev", "Which test do I write?")
    assert bubble(row, {"dev": "Dev (the shop)"}) == "Dev (the shop)\nWhich test do I write?\n"
