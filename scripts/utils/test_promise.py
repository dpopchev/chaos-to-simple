"""Tests for the promise figure: the two sequences and the pair the order swaps."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.promise import draw, load_steps, swapped_pair

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "05-how" / "data" / "promise.csv"


@pytest.mark.model
def test_promise_load_steps_reads_six_steps() -> None:
    assert len(load_steps(CSV)) == 6


@pytest.mark.model
def test_promise_swapped_pair_is_one_and_two() -> None:
    assert swapped_pair(load_steps(CSV)) == (1, 2)


@pytest.mark.edge
def test_promise_draw_writes_a_png(tmp_path: Path) -> None:
    out = draw(load_steps(CSV), tmp_path / "promise.png")
    assert out.read_bytes()[:4] == b"\x89PNG"
