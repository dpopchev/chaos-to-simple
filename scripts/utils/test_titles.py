"""The title gate: a frame title under the word minimum is named."""

from __future__ import annotations

import pytest

from scripts.utils.titles import too_short


@pytest.mark.model
def test_too_short_names_a_seven_word_title() -> None:
    text = (
        "# 01 Bits: topic titles are exempt\n\n"
        "## One two three four five six seven {paths=64}\n\n"
        "## One two three four five six seven eight {paths=64}\n"
    )
    assert too_short(text) == ("One two three four five six seven",)
