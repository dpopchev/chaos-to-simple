"""The path counter: read from the frame titles, checked against the storyboard."""

from __future__ import annotations

import pytest

from scripts.utils.counter import ends_at, monotone, paths_of, reveal_at, storyboard_ok

INDEX = "## One {paths=1}\n\ntext\n\n## Two {paths=2}\n## Odd {paths=?}\n## Big {paths=64}\n"


@pytest.mark.edge
def test_paths_of_reads_numbers_as_int_and_keeps_the_question_mark() -> None:
    assert paths_of(INDEX) == [1, 2, "?", 64]


@pytest.mark.edge
def test_paths_of_skips_a_title_without_a_counter() -> None:
    assert paths_of("## Plain\n## Two {paths=2}\n") == [2]


@pytest.mark.model
def test_storyboard_ok_accepts_the_doubling() -> None:
    assert storyboard_ok([1, 1, 2, 4, 8, 16, 32, 64, 64])


@pytest.mark.model
def test_storyboard_ok_skips_a_leading_question_mark() -> None:
    assert storyboard_ok(["?", 1, 1, 2, 4, 8, 16, 32, 64, 64])


@pytest.mark.model
def test_storyboard_ok_refuses_a_skipped_step() -> None:
    assert not storyboard_ok([1, 2, 8, 16, 32, 64, 128])


@pytest.mark.model
def test_storyboard_ok_refuses_too_few_frames() -> None:
    assert not storyboard_ok([1, 2, 4])


@pytest.mark.model
def test_monotone_ignores_the_question_mark() -> None:
    assert monotone([1, "?", 2, 2, 4])


@pytest.mark.model
def test_monotone_refuses_a_drop() -> None:
    assert not monotone([1, 4, 2])


@pytest.mark.model
def test_ends_at_compares_the_last_value_with_the_counter() -> None:
    assert ends_at([1, 64], "64")


@pytest.mark.model
def test_ends_at_refuses_another_counter() -> None:
    assert not ends_at([1, 64], "72")


@pytest.mark.model
def test_ends_at_refuses_no_values() -> None:
    assert not ends_at([], "64")


@pytest.mark.model
def test_reveal_at_is_true_when_the_value_first_appears_on_that_title() -> None:
    frames = [("A", 64), ("The number", 72), ("B", 72)]
    assert reveal_at(frames, "The number", 72)


@pytest.mark.model
def test_reveal_at_is_false_when_the_value_came_earlier() -> None:
    frames = [("A", 72), ("The number", 72)]
    assert not reveal_at(frames, "The number", 72)


@pytest.mark.model
def test_reveal_at_is_false_when_the_value_never_appears() -> None:
    assert not reveal_at([("A", 64)], "A", 72)
