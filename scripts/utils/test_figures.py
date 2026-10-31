"""Tests for the deck's diagrams: each figure writes a PNG."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from s01_bits.two_ifs import ship
from scripts.utils.figures import TREE_LEAVES, load_route, route, stacey, story, tree

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
ROUTE_CSV = Path(__file__).resolve().parents[2] / "data" / "route.csv"


@pytest.mark.edge
def test_load_route_reads_eight_sections() -> None:
    assert [stop.section for stop in load_route(ROUTE_CSV)] == [f"0{i}" for i in range(8)]


@pytest.mark.model
def test_tree_leaves_match_ship() -> None:
    def charged(subtotal: int, coupon: bool) -> Decimal:
        return ship(Decimal(subtotal), coupon) - Decimal(subtotal) + (10 if coupon else 0)

    assert all(charged(leaf.subtotal, leaf.coupon) == leaf.fee for leaf in TREE_LEAVES)


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
def test_route_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "route.png"
    route(out)
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_tree_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "tree.png"
    tree(out)
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_story_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "story.png"
    story(out)
    assert out.read_bytes().startswith(PNG_MAGIC)
