"""The overfull frames: named from a lualatex log and the beamer tex it compiled."""

from __future__ import annotations

import pytest

from scripts.utils.overflow import overfull_frames, tight_frames

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


WRAPPED_TEX = "\n".join(
    [
        r"\begin{frame}{A policy is one bit and every bit doubles the paths:",
        "count them}",
        "text",
        r"\end{frame}",
    ]
)


@pytest.mark.model
def test_frames_reads_a_title_wrapped_over_two_lines() -> None:
    log = "Overfull \\vbox (9.0pt too high) detected at line 3\n"
    assert overfull_frames(WRAPPED_TEX, log) == (
        "A policy is one bit and every bit doubles the paths: count them",
    )


SLACK_LOG = "slack: 3 40.5pt\nslack: 7 2.9pt\nslack: 7 0.7pt\nslack: 3 3.24pt\n"


@pytest.mark.model
def test_overflow_names_a_frame_under_the_slack_threshold() -> None:
    assert tight_frames(TEX, SLACK_LOG) == ("Second frame",)
