"""Draw the deck's diagrams: make artifacts calls this.

python -m scripts.figures agenda --out build/00-frontmatter/agenda.png
python -m scripts.figures board --stage 3 --out build/03-chaos/board.png
python -m scripts.figures business-map --out build/00-frontmatter/business-map.png
python -m scripts.figures colorcode --out build/04-what/colorcode.png
python -m scripts.figures coverage-view --out build/01-bits/coverage-view.png
python -m scripts.figures doubling --cast data/cast.csv --out build/01-bits/doubling.png
python -m scripts.figures finance --out build/01-bits/finance.png
python -m scripts.figures grid-image --out build/01-bits/grid.png
python -m scripts.figures grid-panels --rules data/rules.csv --out build/03-chaos/grid-9.png
python -m scripts.figures moves --rules data/rules.csv --out build/04-what/moves.png
python -m scripts.figures seam --rules data/rules.csv --out build/05-how/ports.png
python -m scripts.figures stacey --out build/02-stacey/stacey.png
python -m scripts.figures stacey --highlight 02 --out build/02-stacey/stacey-02.png
python -m scripts.figures journey --out build/03-chaos/diagrams/journey.png
python -m scripts.figures tree --out build/01-bits/tree.png
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.board import board, board_rows, example_tests
from scripts.utils.colorcode import colorcode, owned_lines
from scripts.utils.coverage_view import BITS, draw, load_tested
from scripts.utils.figures import (
    journey,
    moves,
    moves_figure,
    ports_of,
    seam,
    tree,
)
from scripts.utils.finance import draw as draw_finance
from scripts.utils.finance import load_october
from scripts.utils.palette import load_actors, load_contexts
from scripts.utils.paths import (
    doubling_chart,
    grid_image,
    grid_panels,
    load_cast,
    load_incidents,
    load_rules,
)
from scripts.utils.retro import load_questions
from scripts.utils.stacey import draw as draw_stacey
from scripts.utils.stacey import load_labels, load_spots, load_zones
from scripts.utils.stage import agenda_strip, business_map, load_route


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    choices = [
        "agenda",
        "board",
        "business-map",
        "colorcode",
        "coverage-view",
        "doubling",
        "finance",
        "grid-image",
        "grid-panels",
        "moves",
        "seam",
        "journey",
        "stacey",
        "tree",
    ]
    parser.add_argument("what", choices=choices)
    parser.add_argument("--out", type=Path, required=True, help="PNG file to write")
    parser.add_argument("--rules", type=Path, default=Path("data/rules.csv"), help="moves: rules")
    parser.add_argument("--cast", type=Path, default=Path("data/cast.csv"), help="seam: cast")
    parser.add_argument("--actors", type=Path, default=Path("data/actors.csv"), help="actors")
    parser.add_argument(
        "--questions", type=Path, default=Path("data/questions.csv"), help="journey: questions"
    )
    parser.add_argument("--route", type=Path, default=Path("data/route.csv"), help="agenda: stops")
    parser.add_argument(
        "--incidents", type=Path, default=Path("data/incidents.csv"), help="agenda: incidents"
    )
    parser.add_argument("--highlight", help="agenda, stacey: the section whose stop stands out")
    parser.add_argument("--zones", type=Path, default=Path("02-stacey/data/zones.csv"))
    parser.add_argument("--labels", type=Path, default=Path("02-stacey/data/labels.csv"))
    parser.add_argument("--october", type=Path, default=Path("01-bits/data/october.csv"))
    parser.add_argument("--tested", type=Path, default=Path("01-bits/data/tested.csv"))
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("01-bits/s01_bits/chaos.py"),
        help="colorcode: the checkout source",
    )
    parser.add_argument("--room", type=int, default=None, help="doubling: the room's week")
    parser.add_argument("--stage", type=int, default=6, help="board: the stage 3, 4, 5 or 6")
    parser.add_argument("--examples", type=Path, default=Path("data/examples.csv"))
    parser.add_argument("--tests", type=Path, default=Path("06-simple/tests"), help="board: tests")
    args = parser.parse_args(argv)

    if args.what == "board":
        rows = board_rows(
            load_rules(args.rules), load_questions(args.questions), example_tests(args.examples)
        )
        board(rows, args.stage, args.out, args.tests)
        return 0
    if args.what == "colorcode":
        source = args.source.read_text(encoding="ascii")
        lines = owned_lines(source, load_cast(args.cast), load_rules(args.rules))
        colorcode(lines, load_actors(args.actors), load_contexts(), args.out)
        return 0
    if args.what == "finance":
        weeks = load_october(args.october)
        draw_finance(weeks, args.out)
        return 0
    if args.what == "coverage-view":
        draw(load_tested(args.tested), args.out)
        return 0
    if args.what == "doubling":
        doubling_chart(load_cast(args.cast), args.out, room_week=args.room)
        return 0
    if args.what == "grid-image":
        rows = load_tested(args.tested)
        grid_image(
            BITS,
            [r.bits for r in rows if r.kind == "tested"],
            [r.bits for r in rows if r.kind == "bug"],
            args.out,
        )
        return 0
    if args.what == "grid-panels":
        rules = load_rules(args.rules)
        rows = load_tested(args.tested)
        grid_panels(
            sum(r.scope == "core" for r in rules),
            sum(r.scope == "shell" for r in rules),
            [r.bits for r in rows if r.kind == "tested"],
            [r.bits for r in rows if r.kind == "bug"],
            args.out,
        )
        return 0
    if args.what == "moves":
        moves_figure(args.out, moves(load_rules(args.rules)))
        return 0
    if args.what == "business-map":
        business_map(
            load_actors(args.actors), load_cast(args.cast), load_rules(args.rules), args.out
        )
        return 0
    if args.what == "agenda":
        agenda_strip(
            load_route(args.route), load_incidents(args.incidents), args.out, args.highlight
        )
        return 0
    if args.what == "seam":
        seam(args.out, ports_of(load_rules(args.rules), load_cast(args.cast)))
        return 0
    if args.what == "stacey":
        draw_stacey(
            load_spots(args.route),
            load_zones(args.zones),
            load_labels(args.labels),
            args.out,
            args.highlight,
        )
        return 0
    if args.what == "journey":
        journey(load_questions(args.questions), load_actors(args.actors), args.out)
        return 0
    tree(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
