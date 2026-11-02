"""Tests for the deck's diagrams: each figure writes a PNG."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from s01_bits.two_ifs import ship
from scripts.utils.figures import (
    JOURNEY,
    TREE_LEAVES,
    JourneyStep,
    journey,
    mood,
    moves,
    moves_figure,
    ports_of,
    question_ids,
    seam,
    seam_boxes,
    tree,
)
from scripts.utils.palette import load_actors
from scripts.utils.paths import load_cast, load_rules
from scripts.utils.retro import Question

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
CAST_CSV = Path(__file__).resolve().parents[2] / "data" / "cast.csv"
RULES_CSV = Path(__file__).resolve().parents[2] / "data" / "rules.csv"
QUESTIONS = [
    Question("q4", "declined?", "dev", "s0", "decided", "rejected"),
    Question("q1", "expired?", "accounting", "b0", "decided", "through its last day"),
]


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


@pytest.mark.model
def test_tree_leaves_match_ship() -> None:
    def charged(subtotal: int, coupon: bool) -> Decimal:
        return ship(Decimal(subtotal), coupon) - Decimal(subtotal) + (10 if coupon else 0)

    assert all(charged(leaf.subtotal, leaf.coupon) == leaf.fee for leaf in TREE_LEAVES)


@pytest.mark.edge
def test_tree_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "tree.png"
    tree(out)
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.edge
def test_journey_writes_a_png(tmp_path: Path) -> None:
    out = tmp_path / "nested" / "journey.png"
    journey(QUESTIONS, load_actors(), out)
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.model
def test_mood_drops_one_level_at_each_questioned_step() -> None:
    steps = (JourneyStep("customer", "x", None), JourneyStep("payment", "y", "s0"))
    assert mood(steps, QUESTIONS) == (0, -1)


@pytest.mark.model
def test_mood_stays_level_where_no_question_was_raised() -> None:
    steps = (JourneyStep("customer", "x", None), JourneyStep("accounting", "y", None))
    assert mood(steps, QUESTIONS) == (0, 0)


@pytest.mark.model
def test_question_ids_label_the_questioned_steps() -> None:
    steps = (JourneyStep("customer", "x", None), JourneyStep("payment", "y", "s0"))
    assert question_ids(steps, QUESTIONS) == (None, "q4")


@pytest.mark.model
def test_journey_steps_each_name_a_palette_actor() -> None:
    assert {s.actor for s in JOURNEY} <= set(load_actors())
