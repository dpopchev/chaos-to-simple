"""make widths: fail naming each included line wider than the column it sits in.

    python -m scripts.check_widths --root . --full 104
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.widths import too_wide


def read_text(root: Path, path: str) -> str:
    """Read an included file under root; a missing one raises naming its path."""
    return (root / path).read_text(encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--full", type=int, default=104)
    args = parser.parse_args(argv)

    clipped: list[str] = []
    for index in sorted(args.root.glob("[0-9][0-9]-*/index.md")):
        clipped.extend(
            too_wide(
                index.read_text(encoding="utf-8"),
                lambda path: read_text(args.root, path),
                args.full,
                f"{index.parent.name}/index.md",
            )
        )
    for text in clipped:
        sys.stdout.write(f"widths: {text}\n")
    return 1 if clipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
