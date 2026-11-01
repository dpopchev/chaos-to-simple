"""too_long: the included blocks longer than their line cap."""

from __future__ import annotations

import pytest

from scripts.utils.lengths import too_long

BLOCK = "a\nb\nc\nd\n"


def _slide(attrs: str) -> str:
    return f"## Long one\n\n```{{.python include=a.py{attrs}}}\n```\n"


@pytest.mark.view
def test_too_long_names_a_block_over_the_cap() -> None:
    texts = {"a.py": BLOCK}
    assert too_long(_slide(""), texts.__getitem__, 3) == ("index.md Long one: 4 > 3: a.py",)


@pytest.mark.view
def test_too_long_counts_non_blank_lines_only() -> None:
    texts = {"a.py": "a\n\nb\n   \nc\n"}
    assert too_long(_slide(""), texts.__getitem__, 3) == ()


@pytest.mark.view
def test_too_long_does_not_count_a_bare_step_marker() -> None:
    texts = {"a.py": "a\n# [step: 2]\nb\nc\n"}
    assert too_long(_slide(""), texts.__getitem__, 3) == ()


@pytest.mark.view
def test_too_long_honours_the_include_cap() -> None:
    texts = {"a.py": BLOCK}
    assert too_long(_slide(" cap=4"), texts.__getitem__, 3) == ()
