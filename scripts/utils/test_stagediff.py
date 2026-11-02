"""snippet_diff: the unified diff of one named snippet between two files."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.stagediff import snippet_diff

OLD = "x = 1\n# [snippet: s]\n    a = 1  # [step: 2]\n    b = 2\n# [/snippet]\n"
NEW = "# [snippet: s]\n    a = 1\n    b = 3\n# [/snippet]\ny = 2\n"


def _pair(tmp_path: Path) -> tuple[Path, Path]:
    old, new = tmp_path / "old.py", tmp_path / "new.py"
    old.write_text(OLD, encoding="ascii")
    new.write_text(NEW, encoding="ascii")
    return old, new


@pytest.mark.view
def test_snippet_diff_marks_the_changed_line(tmp_path: Path) -> None:
    old, new = _pair(tmp_path)
    assert "+b = 3" in snippet_diff(old, "s", new, "s").splitlines()


@pytest.mark.view
def test_snippet_diff_leaves_the_step_marker_out(tmp_path: Path) -> None:
    old, new = _pair(tmp_path)
    assert "step" not in snippet_diff(old, "s", new, "s")


@pytest.mark.view
def test_snippet_diff_start_cuts_both_snippets_at_the_first_matching_line(tmp_path: Path) -> None:
    old, new = _pair(tmp_path)
    assert snippet_diff(old, "s", new, "s", start="b =").splitlines()[1:] == ["-b = 2", "+b = 3"]


@pytest.mark.view
def test_snippet_diff_opens_with_the_file_names(tmp_path: Path) -> None:
    old, new = _pair(tmp_path)
    assert snippet_diff(old, "s", new, "s").splitlines()[0] == "old.py -> new.py"


@pytest.mark.view
def test_snippet_diff_has_no_hunk_header(tmp_path: Path) -> None:
    old, new = _pair(tmp_path)
    headers = ("---", "+++", "@@")
    assert [r for r in snippet_diff(old, "s", new, "s").splitlines() if r.startswith(headers)] == []


@pytest.mark.view
def test_snippet_diff_added_only_keeps_the_plus_lines(tmp_path: Path) -> None:
    old, new = _pair(tmp_path)
    assert snippet_diff(old, "s", new, "s", added_only=True).splitlines() == [
        "old.py -> new.py",
        "+b = 3",
    ]
