"""too_long: the included blocks longer than their line cap."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.check_lengths import main
from scripts.utils.lengths import too_long

BLOCK = "a\nb\nc\nd\n"


def _slide(attrs: str) -> str:
    return f"## Long one\n\n```{{.python include=a.py{attrs}}}\n```\n"


@pytest.mark.view
def test_too_long_names_a_block_over_the_cap() -> None:
    texts = {"a.py": BLOCK}
    assert too_long(_slide(""), texts.__getitem__, 3) == ("index.md Long one: 4 > 3: a.py",)


@pytest.mark.view
def test_too_long_counts_non_blank_lines_only() -> None:
    texts = {"a.py": "a\n\nb\n   \nc\n"}
    assert too_long(_slide(""), texts.__getitem__, 3) == ()


@pytest.mark.view
def test_too_long_does_not_count_a_bare_step_marker() -> None:
    texts = {"a.py": "a\n# [step: 2]\nb\nc\n"}
    assert too_long(_slide(""), texts.__getitem__, 3) == ()


@pytest.mark.edge
def test_lengths_skips_a_missing_include(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("STRICT", raising=False)
    (tmp_path / "01-x").mkdir()
    (tmp_path / "01-x" / "index.md").write_text(_slide(""), encoding="utf-8")
    code = main(["--root", str(tmp_path)])
    assert (code, capsys.readouterr().out) == (0, "[WARN] stub include: a.py\n")


@pytest.mark.view
def test_start_line_end_line_counts_only_the_range() -> None:
    texts = {"a.py": "".join(f"l{n}\n" for n in range(1, 11))}
    assert too_long(_slide(" cap=3 start-line=3 end-line=5"), texts.__getitem__, 3) == ()


@pytest.mark.view
def test_too_long_honours_the_include_cap() -> None:
    texts = {"a.py": BLOCK}
    assert too_long(_slide(" cap=4"), texts.__getitem__, 3) == ()
