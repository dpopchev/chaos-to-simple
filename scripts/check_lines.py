"""make lines: fail when a should-have-known line is missing from its section or from 07.

    python -m scripts.check_lines --root .
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.lines import load_lines, missing


def read_indexes(root: Path) -> dict[str, str]:
    """Read every NN-*/index.md under root, keyed by its section directory."""
    return {
        path.parent.name: path.read_text(encoding="utf-8")
        for path in sorted(root.glob("[0-9][0-9]-*/index.md"))
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    lines = load_lines(args.root / "data" / "lines.csv")
    gaps = missing(lines, read_indexes(args.root))
    for section, where in gaps:
        sys.stdout.write(f"lines: the {section} line is missing from {where}/index.md\n")
    return 1 if gaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
