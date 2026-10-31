"""Draw the deck's diagrams: make artifacts calls this.

python -m scripts.figures moves --rules data/rules.csv --out build/04-what/moves.png
python -m scripts.figures route --out build/00-frontmatter/route.png
python -m scripts.figures stacey --out build/02-stacey/stacey.png
python -m scripts.figures story --out build/03-chaos/story.png
python -m scripts.figures tree --out build/01-bits/tree.png
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.figures import moves, moves_figure, route, stacey, story, tree
from scripts.utils.paths import load_rules


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("what", choices=["moves", "route", "stacey", "story", "tree"])
    parser.add_argument("--out", type=Path, required=True, help="PNG file to write")
    parser.add_argument("--rules", type=Path, default=Path("data/rules.csv"), help="moves: rules")
    args = parser.parse_args(argv)

    if args.what == "moves":
        moves_figure(args.out, moves(load_rules(args.rules)))
        return 0
    {"route": route, "stacey": stacey, "story": story, "tree": tree}[args.what](args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
