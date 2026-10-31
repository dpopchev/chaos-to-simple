"""Draw the deck's diagrams: make artifacts calls this.

python -m scripts.figures example-map --out build/03-chaos/example_map.png
python -m scripts.figures moves --rules data/rules.csv --out build/04-what/moves.png
python -m scripts.figures route --out build/00-frontmatter/route.png
python -m scripts.figures seam --rules data/rules.csv --out build/05-how/ports.png
python -m scripts.figures stacey --out build/02-stacey/stacey.png
python -m scripts.figures story --out build/03-chaos/story.png
python -m scripts.figures tree --out build/01-bits/tree.png
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.examples import card_counts, example_names
from scripts.utils.figures import (
    example_map,
    moves,
    moves_figure,
    ports_of,
    route,
    seam,
    stacey,
    story,
    tree,
)
from scripts.utils.paths import load_rules


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    choices = ["example-map", "moves", "route", "seam", "stacey", "story", "tree"]
    parser.add_argument("what", choices=choices)
    parser.add_argument("--out", type=Path, required=True, help="PNG file to write")
    parser.add_argument("--rules", type=Path, default=Path("data/rules.csv"), help="moves: rules")
    parser.add_argument("--examples", type=Path, default=Path("data/examples.csv"))
    parser.add_argument("--questions", type=Path, default=Path("03-chaos/data/questions.md"))
    parser.add_argument("--chaos-tests", type=Path, default=Path("01-bits/tests/test_chaos.py"))
    args = parser.parse_args(argv)

    if args.what == "example-map":
        names = [
            *example_names(args.examples, "core"),
            *example_names(args.examples, "shell"),
        ]
        before, after = card_counts(
            load_rules(args.rules),
            names,
            args.questions.read_text(encoding="ascii"),
            args.chaos_tests.read_text(encoding="ascii"),
        )
        example_map(args.out, before, after)
        return 0
    if args.what == "moves":
        moves_figure(args.out, moves(load_rules(args.rules)))
        return 0
    if args.what == "seam":
        seam(args.out, ports_of(load_rules(args.rules)))
        return 0
    {"route": route, "stacey": stacey, "story": story, "tree": tree}[args.what](args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
