"""The deck style, pinned."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pytest
import seaborn as sns
from matplotlib.colors import to_hex

from scripts.utils.style import FIGSIZE, FONT, apply, palette


@pytest.mark.model
def test_apply_sets_the_first_font_family_to_the_deck_font() -> None:
    apply()
    assert plt.rcParams["font.family"][0] == FONT


@pytest.mark.model
def test_apply_sets_the_figure_size() -> None:
    apply()
    assert tuple(plt.rcParams["figure.figsize"]) == FIGSIZE


@pytest.mark.model
def test_palette_has_six_colours() -> None:
    assert len(palette()) == 6


@pytest.mark.edge
def test_first_palette_colour_is_the_first_of_seaborn_colorblind() -> None:
    expected = to_hex(sns.color_palette("colorblind")[0])
    assert palette()[0] == expected
