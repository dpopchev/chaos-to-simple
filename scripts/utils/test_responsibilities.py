"""Tests for the responsibilities picture: its groups, the faded boxes, the contracts."""

from __future__ import annotations

import struct
from pathlib import Path

import pytest

from scripts.utils.responsibilities import contract_of, draw, groups, muted


@pytest.mark.model
def test_responsibilities_groups_hold_three_one_and_three_boxes() -> None:
    assert tuple(len(g) for g in groups()) == (3, 1, 3)


@pytest.mark.model
def test_responsibilities_muted_pricing_lists_every_other_box() -> None:
    assert muted("pricing") == (
        "shipping",
        "tax",
        "fulfilment",
        "payment",
        "warehouse",
        "mail",
    )


@pytest.mark.model
def test_responsibilities_contract_of_pricing_is_priced() -> None:
    assert contract_of("pricing") == "Priced"


@pytest.mark.edge
def test_responsibilities_draw_writes_a_png(tmp_path: Path) -> None:
    out = draw(tmp_path / "responsibilities.png", "payment")
    assert out.read_bytes()[:4] == b"\x89PNG"


@pytest.mark.edge
def test_responsibilities_compact_is_taller(tmp_path: Path) -> None:
    out = draw(tmp_path / "offer.png", compact=True)
    width, height = struct.unpack(">II", out.read_bytes()[16:24])
    assert width / height < 2.0
