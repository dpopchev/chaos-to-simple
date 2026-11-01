"""The deck style, pinned."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pytest
import seaborn as sns
from matplotlib.colors import to_hex

from scripts.utils.style import CONTEXTS, FIGSIZE, FONT, apply, context_colour, palette, save


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


@pytest.mark.model
def test_context_colour_gives_five_distinct_colours() -> None:
    assert len({context_colour(name) for name in CONTEXTS}) == 5


@pytest.mark.model
def test_context_colour_reads_contexts_csv() -> None:
    assert context_colour("pricing") == "#7B3F9E"


@pytest.mark.edge
def test_save_writes_a_non_empty_png_under_a_new_folder(tmp_path: Path) -> None:
    apply()
    fig, _ = plt.subplots()
    out = tmp_path / "new" / "fig.png"
    save(fig, out)
    assert out.stat().st_size > 0


@pytest.mark.edge
def test_first_palette_colour_is_the_first_of_seaborn_colorblind() -> None:
    expected = to_hex(sns.color_palette("colorblind")[0])
    assert palette()[0] == expected
