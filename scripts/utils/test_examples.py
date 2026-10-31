from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.examples import CardCounts, card_counts, example_names, missing_tests
from scripts.utils.paths import load_rules

ROOT = Path(__file__).resolve().parents[2]

SAMPLE = (
    "scope,bit,name,given,then\n"
    "core,b0,coupon_valid_today,g,t\n"
    "shell,s0,happy_path_accepts,g,t\n"
)


@pytest.fixture
def examples_csv(tmp_path: Path) -> Path:
    path = tmp_path / "examples.csv"
    path.write_text(SAMPLE, encoding="ascii")
    return path


@pytest.mark.edge
def test_example_names_of_core(examples_csv: Path) -> None:
    assert example_names(examples_csv, "core") == ["coupon_valid_today"]


@pytest.mark.edge
def test_example_names_of_shell(examples_csv: Path) -> None:
    assert example_names(examples_csv, "shell") == ["happy_path_accepts"]


def _room() -> tuple[CardCounts, CardCounts]:
    rules = load_rules(ROOT / "data" / "rules.csv")
    names = [*example_names(ROOT / "data" / "examples.csv", "core")]
    names += example_names(ROOT / "data" / "examples.csv", "shell")
    questions = (ROOT / "03-chaos" / "data" / "questions.md").read_text(encoding="ascii")
    tests = (ROOT / "01-bits" / "tests" / "test_chaos.py").read_text(encoding="ascii")
    return card_counts(rules, names, questions, tests)


@pytest.mark.edge
def test_card_counts_after_the_room_are_9_blue_6_red() -> None:
    _, after = _room()
    assert (after.blue, after.red) == (9, 6)


@pytest.mark.edge
def test_card_counts_before_the_room_are_6_blue_0_red() -> None:
    before, _ = _room()
    assert (before.blue, before.red) == (6, 0)


@pytest.mark.model
def test_missing_tests_names_the_gap() -> None:
    namespace = {"test_coupon_valid_today": object()}
    names = ["coupon_valid_today", "happy_path_accepts"]
    assert missing_tests(names, namespace) == ["happy_path_accepts"]
