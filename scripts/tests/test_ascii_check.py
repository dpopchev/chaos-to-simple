from __future__ import annotations

from pathlib import Path

from scripts.utils.ascii_check import candidate_files, findings, scan


def test_candidate_files_skip_build_and_optionally_slides(tmp_path: Path) -> None:
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "x.txt").write_text("x", encoding="ascii")
    (tmp_path / "01-bits").mkdir()
    (tmp_path / "01-bits" / "index.md").write_text("# slide", encoding="ascii")
    (tmp_path / "01-bits" / "README.md").write_text("# readme", encoding="ascii")
    (tmp_path / "Makefile").write_text("all:", encoding="ascii")
    names = [p.relative_to(tmp_path).as_posix() for p in candidate_files(tmp_path)]
    assert names == ["01-bits/README.md", "01-bits/index.md", "Makefile"]
    slides_skipped = candidate_files(tmp_path, skip_slides=True)
    names = [p.relative_to(tmp_path).as_posix() for p in slides_skipped]
    assert names == ["01-bits/README.md", "Makefile"]


def test_findings_report_line_and_column(tmp_path: Path) -> None:
    clean = tmp_path / "clean.py"
    clean.write_text("x = 1\n", encoding="ascii")
    dirty = tmp_path / "dirty.md"
    dirty.write_bytes(b"ok\nbad \xe2\x80\x94 dash\n")
    assert findings(clean) == []
    assert findings(dirty) == [f"{dirty}:2:5: U+2014"]
    assert scan([clean, dirty]) == [f"{dirty}:2:5: U+2014"]
