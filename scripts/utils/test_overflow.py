"""The overfull frames: named from a lualatex log and the beamer tex it compiled."""

from __future__ import annotations

import pytest

from scripts.utils.overflow import overfull_frames

TEX = "\n".join(
    [
        r"\begin{frame}{First frame}",
        "text",
        r"\end{frame}",
        "",
        r"\begin{frame}[fragile]{Second frame}",
        "more text",
        r"\end{frame}",
    ]
)

LOG = "Overfull \\vbox (99.0pt too high) detected at line 7\n"


@pytest.mark.model
def test_overfull_frames_names_each_frame() -> None:
    assert overfull_frames(TEX, LOG) == ("Second frame",)
