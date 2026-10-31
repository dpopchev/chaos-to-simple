"""The example map as data: every green card in data/examples.csv names one test."""

from __future__ import annotations

import ast
import csv
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.utils.paths import Rule


@dataclass(frozen=True)
class CardCounts:
    blue: int
    red: int
    green: int
    yellow: int


def _is_xfail(decorator: ast.expr) -> bool:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    return isinstance(target, ast.Attribute) and target.attr == "xfail"


def passing_tests(source: str) -> int:
    """Count the test functions of a module that are not marked xfail."""
    return sum(
        1
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.FunctionDef)
        and node.name.startswith("test_")
        and not any(_is_xfail(d) for d in node.decorator_list)
    )


def card_counts(
    rules: Sequence[Rule], examples: Sequence[str], questions_md: str, tests_py: str
) -> tuple[CardCounts, CardCounts]:
    """The cards of the example map before the room and after it, measured from the files."""
    core = sum(1 for r in rules if r.scope == "core")
    questions = len(re.findall(r"^\d+\. ", questions_md, flags=re.MULTILINE))
    before = CardCounts(core, 0, passing_tests(tests_py), 1)
    after = CardCounts(len(rules), questions, len(examples), 1)
    return before, after


def example_names(path: Path, scope: str) -> list[str]:
    with path.open(newline="", encoding="ascii") as fh:
        return [row["name"] for row in csv.DictReader(fh) if row["scope"] == scope]


def missing_tests(names: Iterable[str], namespace: Mapping[str, object]) -> list[str]:
    """Names without a test_<name> in the namespace (a test module's globals())."""
    return [name for name in names if f"test_{name}" not in namespace]
