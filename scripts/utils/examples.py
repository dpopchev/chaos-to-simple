"""The example map as data: every green card in data/examples.csv names one test."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from pathlib import Path


def example_names(path: Path, scope: str) -> list[str]:
    with path.open(newline="", encoding="ascii") as fh:
        return [row["name"] for row in csv.DictReader(fh) if row["scope"] == scope]


def missing_tests(names: Iterable[str], namespace: Mapping[str, object]) -> list[str]:
    """Names without a test_<name> in the namespace (a test module's globals())."""
    return [name for name in names if f"test_{name}" not in namespace]
