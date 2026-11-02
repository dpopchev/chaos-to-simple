"""The deck style, pinned."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from scripts.utils.style import FIGSIZE, FONT, apply, save


@pytest.mark.model
def test_apply_sets_the_first_font_family_to_the_deck_font() -> None:
    apply()
    assert plt.rcParams["font.family"][0] == FONT


@pytest.mark.model
def test_apply_sets_the_figure_size() -> None:
    apply()
    assert tuple(plt.rcParams["figure.figsize"]) == FIGSIZE


@pytest.mark.edge
def test_save_writes_a_non_empty_png_under_a_new_folder(tmp_path: Path) -> None:
    apply()
    fig, _ = plt.subplots()
    out = tmp_path / "new" / "fig.png"
    save(fig, out)
    assert out.stat().st_size > 0
