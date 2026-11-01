"""The stub writer: the manifest, the paths without a rule, the placeholder files."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.stubs import Entry, load_manifest, missing, strict, write_stub

MANIFEST_CSV = "path,kind,producer\nbuild/a.png,png,scripts.figures a\nbuild/b.txt,txt,pytest -k\n"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@pytest.fixture
def manifest() -> list[Entry]:
    return [Entry("build/a.png", "png", "p"), Entry("build/b.txt", "txt", "q")]


@pytest.mark.edge
def test_load_manifest_reads_a_row_with_a_spaced_producer(tmp_path: Path) -> None:
    path = tmp_path / "artifacts.csv"
    path.write_text(MANIFEST_CSV, encoding="ascii")
    assert load_manifest(path)[1] == Entry("build/b.txt", "txt", "pytest -k")


@pytest.mark.model
def test_missing_drops_a_path_that_has_a_rule(manifest: list[Entry]) -> None:
    assert missing(manifest, ["build/a.png"]) == (Entry("build/b.txt", "txt", "q"),)


@pytest.mark.model
def test_strict_names_each_path_without_a_rule(manifest: list[Entry]) -> None:
    assert strict(manifest, []) == ("build/a.png", "build/b.txt")


@pytest.mark.model
def test_strict_is_empty_when_every_path_has_a_rule(manifest: list[Entry]) -> None:
    assert strict(manifest, ["build/a.png", "build/b.txt"]) == ()


@pytest.mark.edge
def test_write_stub_draws_a_png(tmp_path: Path) -> None:
    out = tmp_path / "deep" / "a.png"
    write_stub(out, "png")
    assert out.read_bytes().startswith(PNG_SIGNATURE)


@pytest.mark.edge
def test_write_stub_writes_the_warning_line_for_a_txt(tmp_path: Path) -> None:
    out = tmp_path / "b.txt"
    write_stub(out, "txt")
    assert out.read_text(encoding="ascii") == f"[WARN] not implemented yet: {out}\n"


@pytest.mark.edge
def test_write_stub_writes_the_warning_line_for_a_diff(tmp_path: Path) -> None:
    out = tmp_path / "c.diff"
    write_stub(out, "diff")
    assert out.read_text(encoding="ascii").startswith("[WARN] not implemented yet: ")


@pytest.mark.edge
def test_write_stub_rejects_an_unknown_kind(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown kind"):
        write_stub(tmp_path / "x.bin", "bin")
