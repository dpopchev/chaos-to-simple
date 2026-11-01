"""make lengths: fail naming each included block with more lines than its cap.

    python -m scripts.check_lengths --root . --cap 14
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.lengths import too_long


def read_text(root: Path, path: str) -> str:
    """Read an included file under root; a missing one raises naming its path."""
    return (root / path).read_text(encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--cap", type=int, default=14)
    args = parser.parse_args(argv)

    long: list[str] = []
    for index in sorted(args.root.glob("[0-9][0-9]-*/index.md")):
        long.extend(
            too_long(
                index.read_text(encoding="utf-8"),
                lambda path: read_text(args.root, path),
                args.cap,
                f"{index.parent.name}/index.md",
            )
        )
    for text in long:
        sys.stdout.write(f"lengths: {text}\n")
    return 1 if long else 0


if __name__ == "__main__":
    raise SystemExit(main())
