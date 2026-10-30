"""Find bytes above 127 in the files the writing conventions keep ASCII."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".venv",
    "build",
    "local",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
}
SUFFIXES = {".py", ".md", ".yaml", ".yml", ".toml", ".lua", ".tex", ".csv", ".mk", ".mmd", ".txt"}
NAMES = {"Makefile", ".python-version", ".gitignore"}
SLIDES = "index.md"


def candidate_files(root: Path, skip_slides: bool = False) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in parts) or not path.is_file():
            continue
        if skip_slides and path.name == SLIDES:
            continue
        if path.suffix in SUFFIXES or path.name in NAMES:
            out.append(path)
    return out


def findings(path: Path) -> list[str]:
    text = path.read_bytes().decode("utf-8", errors="replace")
    out: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for col, char in enumerate(line, start=1):
            if ord(char) > 127:
                out.append(f"{path}:{lineno}:{col}: U+{ord(char):04X}")
    return out


def scan(paths: Iterable[Path]) -> list[str]:
    return [finding for path in paths for finding in findings(path)]
