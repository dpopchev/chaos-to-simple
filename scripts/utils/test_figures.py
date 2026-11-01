"""Tests for the deck's diagrams: each figure writes a PNG."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from s01_bits.two_ifs import ship
from scripts.utils.examples import CardCounts
from scripts.utils.figures import (
    TREE_LEAVES,
    example_map,
    moves,
    moves_figure,
    ports_of,
    seam,
    seam_boxes,
    stacey,
    story,
    tree,
)
from scripts.utils.paths import load_cast, load_rules

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
CAST_CSV = Path(__file__).resolve().parents[2] / "data" / "cast.csv"
RULES_CSV = Path(__file__).resolve().parents[2] / "data" / "rules.csv"


@pytest.mark.model
def test_moves_sum_to_nine() -> None:
    assert sum(move.bits for move in moves(load_rules(RULES_CSV))) == 9


@pytest.mark.model
def test_ports_of_reads_three_sum_types() -> None:
    ports = ports_of(load_rules(RULES_CSV), load_cast(CAST_CSV))
    assert [(p.context, p.code) for p in ports] == [
        ("Payment provider", "Charged | Declined"),
        ("Warehouse", "Reserved | OutOfStock"),
        ("Mailer", "Sent | Bounced"),
    ]


@pytest.mark.model
def test_seam_box_colour_is_the_actor_colour() -> None:
    ports = ports_of(load_rules(RULES_CSV), load_cast(CAST_CSV))
    assert seam_boxes(ports) == ("#D55E00", "#56B4E9", "#F0E442")


@pytest.mark.edge
def test_seam_writes_a_png(tmp_path: Path) -> None:
    out = seam(tmp_path / "seam.png", ports_of(load_rules(RULES_CSV), load_cast(CAST_CSV)))
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_moves_figure_writes_a_png(tmp_path: Path) -> None:
    out = moves_figure(tmp_path / "moves.png", moves(load_rules(RULES_CSV)))
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_example_map_writes_a_png(tmp_path: Path) -> None:
    out = example_map(tmp_path / "map.png", CardCounts(2, 0, 1, 1), CardCounts(3, 2, 4, 1))
    assert out.read_bytes().startswith(PNG_MAGIC)


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
def test_tree_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "tree.png"
    tree(out)
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_story_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "story.png"
    story(out)
    assert out.read_bytes().startswith(PNG_MAGIC)
