"""Test that no helper under scripts/utils/ draws with a colour the palette does not hold."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts.utils.palette import load_actors, load_contexts

UTILS = Path(__file__).resolve().parent
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")


@pytest.mark.model
def test_every_hex_literal_in_the_helpers_is_a_palette_colour() -> None:
    allowed = {
        f"#{item.color}".upper() for item in (*load_actors().values(), *load_contexts().values())
    }
    used = {
        literal.upper()
        for path in UTILS.glob("*.py")
        if not path.name.startswith("test_")
        for literal in HEX.findall(path.read_text(encoding="utf-8"))
    }
    assert used <= allowed
