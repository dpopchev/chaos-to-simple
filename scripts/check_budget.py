"""make budget: fail when a section holds a different number of frames than data/budget.csv.

    python -m scripts.check_budget --root .
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.budget import compare, frames_of, load_budget


def read_counts(root: Path) -> dict[str, int]:
    """Count the frames of every NN-*/index.md under root, keyed by its two-digit prefix."""
    return {
        path.parent.name[:2]: frames_of(path.read_text(encoding="utf-8"))
        for path in sorted(root.glob("[0-9][0-9]-*/index.md"))
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    budget = load_budget(args.root / "data" / "budget.csv")
    gaps = compare(budget, read_counts(args.root))
    for section, planned, counted in gaps:
        sys.stdout.write(f"budget: section {section} has {counted} frames, planned {planned}\n")
    if not gaps:
        sys.stdout.write("ok    budget\n")
    return 1 if gaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
