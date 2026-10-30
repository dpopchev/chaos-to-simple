from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.examples import example_names, missing_tests

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


@pytest.mark.model
def test_missing_tests_names_the_gap() -> None:
    namespace = {"test_coupon_valid_today": object()}
    names = ["coupon_valid_today", "happy_path_accepts"]
    assert missing_tests(names, namespace) == ["happy_path_accepts"]
