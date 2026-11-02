"""The section beats: one believed line and one strip name per section, as LaTeX."""

from __future__ import annotations

import pytest

from scripts.utils.beats import beats_tex
from scripts.utils.lines import Line

LINES = [Line("01-bits", "B1", "L1"), Line("02-stacey", "B2", "L2")]


@pytest.mark.view
def test_beats_tex_defines_one_believed_line_per_section() -> None:
    text = beats_tex(LINES)
    assert [ln for ln in text.splitlines() if "believed@" in ln] == [
        r"\expandafter\gdef\csname believed@1\endcsname{B1}",
        r"\expandafter\gdef\csname believed@2\endcsname{B2}",
    ]


@pytest.mark.view
def test_beats_tex_names_the_strip_of_each_section() -> None:
    text = beats_tex(LINES)
    assert [ln for ln in text.splitlines() if "strip@" in ln] == [
        r"\expandafter\gdef\csname strip@1\endcsname{build/00-frontmatter/agenda-01.png}",
        r"\expandafter\gdef\csname strip@2\endcsname{build/00-frontmatter/agenda-02.png}",
    ]
