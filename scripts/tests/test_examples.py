from __future__ import annotations

from pathlib import Path

from scripts.utils.examples import example_names, missing_tests

SAMPLE = (
    "scope,bit,name,given,then\n"
    "core,b0,coupon_valid_today,g,t\n"
    "shell,s0,happy_path_accepts,g,t\n"
)


def test_example_names_filter_by_scope(tmp_path: Path) -> None:
    path = tmp_path / "examples.csv"
    path.write_text(SAMPLE, encoding="ascii")
    assert example_names(path, "core") == ["coupon_valid_today"]
    assert example_names(path, "shell") == ["happy_path_accepts"]


def test_missing_tests_names_the_gap() -> None:
    namespace = {"test_coupon_valid_today": object()}
    names = ["coupon_valid_today", "happy_path_accepts"]
    assert missing_tests(names, namespace) == ["happy_path_accepts"]
