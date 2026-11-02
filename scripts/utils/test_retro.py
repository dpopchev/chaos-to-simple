"""The retro table: the six questions the room raised, each with the decision that closed it."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.palette import label_of
from scripts.utils.retro import Question, load_questions, question_card, retro_table

QUESTIONS = Path(__file__).resolve().parents[2] / "data/questions.csv"
# id 2 + question 35 + who 15 plus three gaps of 2.
DECIDED_AT = 2 + 35 + 15 + 6


def table() -> list[str]:
    return retro_table(load_questions(QUESTIONS)).splitlines()


@pytest.mark.edge
def test_load_questions_reads_the_six_rows() -> None:
    assert [q.id for q in load_questions(QUESTIONS)] == ["q1", "q2", "q3", "q4", "q5", "q6"]


@pytest.mark.model
def test_retro_table_heads_the_four_columns() -> None:
    assert table()[0].split() == ["id", "question", "who", "decided"]


@pytest.mark.model
def test_retro_table_names_the_raiser_by_label() -> None:
    assert "Loyalty program" in retro_table(load_questions(QUESTIONS))


def decided_column() -> str:
    """The decided column of the table, its wrapped lines joined."""
    return " ".join(line[DECIDED_AT:].strip() for line in table())


@pytest.mark.model
def test_retro_table_keeps_both_positions_of_question_three() -> None:
    assert "Marketing: before, so more customers qualify. Logistics: after." in decided_column()


@pytest.mark.model
def test_retro_table_keeps_the_decision_of_question_three() -> None:
    assert "Decided in the room: after the discount" in decided_column()


@pytest.mark.view
def test_retro_table_fits_the_deck_frame() -> None:
    assert max(len(line) for line in table()) <= 104


@pytest.mark.view
def test_retro_table_is_within_the_block_cap() -> None:
    assert len(table()) <= 14


@pytest.mark.model
def test_question_card_holds_the_decision() -> None:
    q3 = load_questions(QUESTIONS)[2]
    lines = question_card(q3, label_of).splitlines()
    assert (lines[0].startswith("q3"), any("after the discount" in line for line in lines[1:])) == (
        True,
        True,
    )


@pytest.mark.model
def test_retro_table_uses_the_injected_label() -> None:
    questions = [Question("q1", "Why?", "dev", "b0", "decided", "Because.")]
    assert "DEV" in retro_table(questions, label=str.upper)
