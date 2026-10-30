"""The placeholder diagram stands in for a Mermaid render while mmdc is absent."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.diagram import write_placeholder


@pytest.mark.edge
def test_write_placeholder_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "diagram.png"
    write_placeholder(out, "mmdc is missing")
    assert out.stat().st_size > 0
