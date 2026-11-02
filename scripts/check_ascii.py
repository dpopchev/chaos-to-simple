"""make ascii: fail when code, config, data or prose carries a byte above 127.

python -m scripts.check_ascii --root .              everything, slides included
python -m scripts.check_ascii --root . --skip-slides once the slides are in Bulgarian
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.ascii_check import candidate_files, scan


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--skip-slides", action="store_true", help="do not check index.md files")
    args = parser.parse_args(argv)

    files = candidate_files(args.root, skip_slides=args.skip_slides)
    problems = scan(files)
    for problem in problems:
        sys.stdout.write(problem + "\n")
    sys.stdout.write(f"ascii: {len(files)} files checked, {len(problems)} findings\n")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
