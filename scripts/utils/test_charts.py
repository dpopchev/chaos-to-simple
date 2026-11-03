"""Test that no helper under scripts/utils/ draws a vertical bar or a pie."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

UTILS = Path(__file__).resolve().parent
VERTICAL = re.compile(r"\.(bar|pie)\(")


@pytest.mark.model
def test_no_helper_draws_a_vertical_bar_or_a_pie() -> None:
    offenders = {
        path.name
        for path in UTILS.glob("*.py")
        if not path.name.startswith("test_") and VERTICAL.search(path.read_text(encoding="utf-8"))
    }
    assert offenders == set()
