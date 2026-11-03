"""The retro table: the six questions the room raised, each with the decision that closed it."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.palette import label_of
from scripts.utils.retro import Question, load_questions, question_card, retro_table

QUESTIONS = Path(__file__).resolve().parents[2] / "data/questions.csv"
# id 2 + question 31 + who 13 plus three gaps of 2, then subdomain 10 and a gap.
SUBDOMAIN_AT = 2 + 31 + 13 + 6
DECIDED_AT = SUBDOMAIN_AT + 10 + 2


def table() -> list[str]:
    return retro_table(load_questions(QUESTIONS)).splitlines()


@pytest.mark.edge
def test_load_questions_reads_the_six_rows() -> None:
    assert [q.id for q in load_questions(QUESTIONS)] == ["q1", "q2", "q3", "q4", "q5", "q6"]


@pytest.mark.model
def test_retro_table_heads_the_five_columns() -> None:
    assert table()[0].split() == ["id", "question", "who", "subdomain", "decided"]


@pytest.mark.model
def test_retro_table_names_the_raiser_by_label() -> None:
    assert "Loyalty" in retro_table(load_questions(QUESTIONS))


@pytest.mark.model
def test_retro_table_names_the_subdomain() -> None:
    rows = [line for line in table() if line.startswith("q")]
    assert [row[SUBDOMAIN_AT : SUBDOMAIN_AT + 10].strip() for row in rows] == [
        "core",
        "core",
        "supporting",
        "supporting",
        "supporting",
        "supporting",
    ]


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
    """The cap matches cap=18 on the retro include in 03-chaos/index.md."""
    assert len(table()) <= 18


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
