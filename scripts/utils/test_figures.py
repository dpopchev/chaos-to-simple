"""Tests for the deck's diagrams: each figure writes a PNG."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from s01_bits.two_ifs import ship
from scripts.utils.examples import CardCounts
from scripts.utils.figures import (
    TREE_LEAVES,
    ZONES,
    example_map,
    load_route,
    moves,
    moves_figure,
    ports_of,
    route,
    route_layout,
    seam,
    stacey,
    story,
    tree,
)
from scripts.utils.paths import load_rules

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
ROUTE_CSV = Path(__file__).resolve().parents[2] / "data" / "route.csv"
RULES_CSV = Path(__file__).resolve().parents[2] / "data" / "rules.csv"


@pytest.mark.model
def test_moves_sum_to_nine() -> None:
    assert sum(move.bits for move in moves(load_rules(RULES_CSV))) == 9


@pytest.mark.model
def test_ports_of_reads_three_sum_types() -> None:
    assert [(p.context, p.code) for p in ports_of(load_rules(RULES_CSV))] == [
        ("payment", "Charged | Declined"),
        ("warehouse", "Reserved | OutOfStock"),
        ("mail", "Sent | Bounced"),
    ]


@pytest.mark.edge
def test_seam_writes_a_png(tmp_path: Path) -> None:
    out = seam(tmp_path / "seam.png", ports_of(load_rules(RULES_CSV)))
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_moves_figure_writes_a_png(tmp_path: Path) -> None:
    out = moves_figure(tmp_path / "moves.png", moves(load_rules(RULES_CSV)))
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_example_map_writes_a_png(tmp_path: Path) -> None:
    out = example_map(tmp_path / "map.png", CardCounts(2, 0, 1, 1), CardCounts(3, 2, 4, 1))
    assert out.read_bytes().startswith(PNG_MAGIC)


def inside(point: tuple[float, float], zone: str) -> bool:
    x, y = point
    x0, y0 = next((zx, zy) for label, zx, zy in ZONES if label == zone)
    return x0 <= x <= x0 + 0.5 and y0 <= y <= y0 + 0.5


@pytest.mark.model
def test_route_layout_puts_06_in_simple() -> None:
    assert inside(route_layout(load_route(ROUTE_CSV))[6], "simple")


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
