"""Tests for the block-graph path count: the product, the bit strings and the drawn figure."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from scripts.utils.counting import (
    IF_ELIF,
    THREE_IFS,
    TWO_IFS,
    bit_strings,
    counting_figure,
    paths_of,
    rows_of,
)


@pytest.mark.model
def test_counting_paths() -> None:
    assert paths_of(TWO_IFS) == 4


@pytest.mark.model
def test_counting_elif() -> None:
    assert paths_of(IF_ELIF) == 3


@pytest.mark.model
def test_counting_three_ifs() -> None:
    assert paths_of(THREE_IFS) == 8


@pytest.mark.model
def test_counting_bit_strings() -> None:
    assert bit_strings(TWO_IFS) == ("00", "01", "10", "11")


@pytest.mark.model
def test_counting_elif_strings() -> None:
    assert bit_strings(IF_ELIF) == ("0", "1", "2")


@pytest.mark.model
def test_counting_rows_align() -> None:
    count_row, bits_row = rows_of(THREE_IFS)
    assert len(count_row) == len(bits_row)


@pytest.mark.view
def test_counting_figure_is_wide(tmp_path: Path) -> None:
    out = counting_figure(tmp_path / "counting.png")
    with Image.open(out) as img:
        assert img.width > img.height
