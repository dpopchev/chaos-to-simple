"""The examples as data: every row of data/examples.csv names one test."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from pathlib import Path


def example_names(path: Path, scope: str) -> list[str]:
    with path.open(newline="", encoding="ascii") as fh:
        return [row["name"] for row in csv.DictReader(fh) if row["scope"] == scope]


def class_name(name: str) -> str:
    """Return the test class name of an example name: out_of_stock -> TestOutOfStock."""
    return "Test" + "".join(part.capitalize() for part in name.split("_"))


def missing_tests(names: Iterable[str], namespace: Mapping[str, object]) -> list[str]:
    """Names with neither a test_<name> function nor a Test<CamelName> class in the namespace."""
    return [
        name
        for name in names
        if f"test_{name}" not in namespace and class_name(name) not in namespace
    ]
