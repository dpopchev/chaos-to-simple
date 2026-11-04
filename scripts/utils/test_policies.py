"""The policies table: each provider's answer beside the shop's decision, Fulfilment the owner."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.paths import load_cast, load_rules
from scripts.utils.policies import policies_table
from scripts.utils.retro import load_questions

DATA = Path(__file__).resolve().parents[2] / "data"


def body_rows() -> list[str]:
    """Return the first line of each body row: the header and the wrapped lines are left out."""
    text = policies_table(
        load_rules(DATA / "rules.csv"),
        load_questions(DATA / "questions.csv"),
        load_cast(DATA / "cast.csv"),
    )
    return [line for line in text.splitlines()[1:] if not line.startswith(" ")]


@pytest.mark.model
def test_policies_table_has_three_body_rows() -> None:
    assert len(body_rows()) == 3


@pytest.mark.model
def test_policies_every_body_row_ends_with_fulfilment() -> None:
    assert all(row.endswith("Fulfilment") for row in body_rows())
