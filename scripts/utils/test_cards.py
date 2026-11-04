"""The evidence cards: each incident as agreed example, customer outcome and passing check."""

from __future__ import annotations

import pytest

from scripts.utils.cards import cards_text

INCIDENTS = """id,closed_by,decision,customer_outcome,bit
I1,test_free_shipping,the threshold reads the value,pays 5 EUR shipping,b2
I2,rules.csv b2,"logistics owns the rule, decided in the room",one answer whoever asks,b2
I3,TestOutOfStockRejects,reserve before charge,told the order is rejected,s1
"""
EXAMPLES = """scope,bit,name,given,then
core,b2,free_shipping,goods 55,shipping 5
shell,s1,out_of_stock_rejects,a priced order,Rejected
"""
WOUNDS = """PASSED 06-simple/tests/test_a.py::test_free_shipping
PASSED 06-simple/tests/test_b.py::TestOutOfStockRejects::test_rejected
"""


@pytest.mark.model
def test_cards_three_cards_lead_with_the_example() -> None:
    cards = cards_text(INCIDENTS, EXAMPLES, WOUNDS).split("\n\n")
    assert [c.splitlines()[0] for c in cards] == [
        "agreed example: goods 55 -> shipping 5",
        "agreed example: goods 55 -> shipping 5",
        "agreed example: a priced order -> Rejected",
    ]


@pytest.mark.model
def test_cards_outcome_reads_the_customer_column() -> None:
    cards = cards_text(INCIDENTS, EXAMPLES, WOUNDS).split("\n\n")
    assert [c.splitlines()[1] for c in cards] == [
        "customer outcome: pays 5 EUR shipping",
        "customer outcome: one answer whoever asks",
        "customer outcome: told the order is rejected",
    ]


@pytest.mark.model
def test_cards_the_decided_incident_carries_decided() -> None:
    card = cards_text(INCIDENTS, EXAMPLES, WOUNDS).split("\n\n")[1]
    assert card.splitlines()[2] == "decided: rules.csv b2, Logistics owns the rule"
