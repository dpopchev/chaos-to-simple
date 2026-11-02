"""The counter plan: every section's {paths=N} titles checked against data/route.csv."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

from scripts.utils.counter import Value, ends_at, monotone, paths_of, reveal_at, storyboard_ok

ROOT = Path(__file__).resolve().parents[2]
TITLE = re.compile(r"^## (.*?) \{paths=(\?|\d+)\}$", re.MULTILINE)
ROUTE = list(csv.DictReader((ROOT / "data/route.csv").read_text(encoding="ascii").splitlines()))
COUNTER = {row["section"]: row["counter"] for row in ROUTE}


def index_text(section: str) -> str:
    """The text of the one index.md of the section numbered NN."""
    (path,) = ROOT.glob(f"{section}-*/index.md")
    return path.read_text(encoding="utf-8")


def frames(section: str) -> list[tuple[str, Value]]:
    """The (title, counter) pair of each counted frame of a section, in order."""
    return [(t, v if v == "?" else int(v)) for t, v in TITLE.findall(index_text(section))]


def before(section: str, title: str) -> list[Value]:
    """The counters of the frames ahead of the frame with that title."""
    out: list[Value] = []
    for name, value in frames(section):
        if name == title:
            return out
        out.append(value)
    return out


@pytest.mark.view
@pytest.mark.parametrize("section", sorted(COUNTER))
def test_each_section_ends_at_its_route_counter(section: str) -> None:
    assert ends_at(paths_of(index_text(section)), COUNTER[section])


@pytest.mark.view
def test_the_bits_section_opens_on_the_storyboard() -> None:
    assert storyboard_ok(paths_of(index_text("01")))


@pytest.mark.view
def test_the_checkout_done_frame_inherits_64() -> None:
    assert frames("01")[8] == ("Checkout done", 64)


@pytest.mark.view
@pytest.mark.parametrize("section", ["01", "02", "03", "04", "05", "07"])
def test_the_counter_never_falls_inside_a_section(section: str) -> None:
    assert monotone(paths_of(index_text(section)))


@pytest.mark.view
def test_the_simple_section_reveals_72_at_the_number() -> None:
    assert reveal_at(frames("06"), "The number", 72)


@pytest.mark.view
def test_the_simple_frames_before_the_number_carry_512() -> None:
    assert set(before("06", "The number")) == {512}


@pytest.mark.view
def test_the_room_frames_before_the_honest_count_carry_64() -> None:
    assert before("03", "The honest count") == [64, 64, 64]


@pytest.mark.view
def test_the_core_title_counts_the_invariant_tests() -> None:
    source = (ROOT / "06-simple/tests/test_core_paths.py").read_text(encoding="utf-8")
    body = source.split("class TestEveryCorePath:")[1]
    measured = 64 * len(re.findall(r"^    def test_", body, re.MULTILINE))
    titles = [t for t, _ in frames("06") if t.startswith("Sixty-four paths")]
    assert titles == [f"Sixty-four paths, three invariants: {measured} tests"]
