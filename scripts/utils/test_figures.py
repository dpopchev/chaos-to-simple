"""Tests for the deck's diagrams: each figure writes a PNG."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.figures import stacey, story

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


@pytest.mark.edge
def test_stacey_writes_a_non_empty_file(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "stacey.png"
    stacey(out)
    assert out.stat().st_size > 0


@pytest.mark.edge
def test_stacey_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "stacey.png"
    stacey(out)
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_story_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "story.png"
    story(out)
    assert out.read_bytes().startswith(PNG_MAGIC)
