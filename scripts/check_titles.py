"""make titles: fail naming each content frame title with fewer than eight words.

python -m scripts.check_titles --root .
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.titles import too_short

FRONTMATTER = "00-frontmatter"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--minimum", type=int, default=8)
    args = parser.parse_args(argv)

    found = 0
    for path in sorted(args.root.glob("[0-9][0-9]-*/index.md")):
        if path.parent.name == FRONTMATTER:
            continue
        for title in too_short(path.read_text(encoding="utf-8"), args.minimum):
            found += 1
            name = path.parent.name
            sys.stdout.write(f"titles: {name} '{title}' has under {args.minimum} words\n")
    if not found:
        sys.stdout.write("ok    titles\n")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
