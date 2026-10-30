from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.ascii_check import candidate_files, findings, scan


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "x.txt").write_text("x", encoding="ascii")
    (tmp_path / "01-bits").mkdir()
    (tmp_path / "01-bits" / "index.md").write_text("# slide", encoding="ascii")
    (tmp_path / "01-bits" / "README.md").write_text("# readme", encoding="ascii")
    (tmp_path / "Makefile").write_text("all:", encoding="ascii")
    return tmp_path


@pytest.mark.edge
def test_candidate_files_skip_build(tree: Path) -> None:
    names = [p.relative_to(tree).as_posix() for p in candidate_files(tree)]
    assert names == ["01-bits/README.md", "01-bits/index.md", "Makefile"]


@pytest.mark.edge
def test_candidate_files_optionally_skip_slides(tree: Path) -> None:
    kept = candidate_files(tree, skip_slides=True)
    assert [p.relative_to(tree).as_posix() for p in kept] == ["01-bits/README.md", "Makefile"]


class TestFindingsReportLineAndColumn:
    @pytest.fixture
    def clean(self, tmp_path: Path) -> Path:
        path = tmp_path / "clean.py"
        path.write_text("x = 1\n", encoding="ascii")
        return path

    @pytest.fixture
    def dirty(self, tmp_path: Path) -> Path:
        path = tmp_path / "dirty.md"
        path.write_bytes(b"ok\nbad \xe2\x80\x94 dash\n")
        return path

    @pytest.mark.edge
    def test_a_clean_file_has_none(self, clean: Path) -> None:
        assert findings(clean) == []

    @pytest.mark.edge
    def test_a_dirty_file_names_line_column_and_code_point(self, dirty: Path) -> None:
        assert findings(dirty) == [f"{dirty}:2:5: U+2014"]

    @pytest.mark.edge
    def test_scan_keeps_only_the_dirty_findings(self, clean: Path, dirty: Path) -> None:
        assert scan([clean, dirty]) == [f"{dirty}:2:5: U+2014"]
