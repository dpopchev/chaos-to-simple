"""Draw the deck's diagrams: make artifacts calls this.

    python -m scripts.figures stacey --out build/02-stacey/stacey.png
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.figures import stacey


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("what", choices=["stacey"])
    parser.add_argument("--out", type=Path, required=True, help="PNG file to write")
    args = parser.parse_args(argv)

    stacey(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
