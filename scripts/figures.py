"""Draw the deck's diagrams: make artifacts calls this.

python -m scripts.figures agenda --out build/00-frontmatter/agenda.png
python -m scripts.figures business-map --out build/00-frontmatter/business-map.png
python -m scripts.figures coverage-view --out build/01-bits/coverage-view.png
python -m scripts.figures doubling --cast data/cast.csv --out build/01-bits/doubling.png
python -m scripts.figures finance --out build/01-bits/finance.png
python -m scripts.figures grid-image --out build/01-bits/grid.png
python -m scripts.figures moves --rules data/rules.csv --out build/04-what/moves.png
python -m scripts.figures seam --rules data/rules.csv --out build/05-how/ports.png
python -m scripts.figures stacey --out build/02-stacey/stacey.png
python -m scripts.figures stacey --highlight 02 --out build/02-stacey/stacey-02.png
python -m scripts.figures story --out build/03-chaos/story.png
python -m scripts.figures tree --out build/01-bits/tree.png
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.coverage_view import BITS, draw, load_tested
from scripts.utils.figures import (
    moves,
    moves_figure,
    ports_of,
    seam,
    story,
    tree,
)
from scripts.utils.finance import draw as draw_finance
from scripts.utils.finance import load_october, report
from scripts.utils.palette import load_actors
from scripts.utils.paths import doubling_chart, grid_image, load_cast, load_incidents, load_rules
from scripts.utils.stacey import draw as draw_stacey
from scripts.utils.stacey import load_labels, load_spots, load_zones
from scripts.utils.stage import agenda_strip, business_map, load_route


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    choices = [
        "agenda",
        "business-map",
        "coverage-view",
        "doubling",
        "finance",
        "grid-image",
        "moves",
        "seam",
        "stacey",
        "story",
        "tree",
    ]
    parser.add_argument("what", choices=choices)
    parser.add_argument("--out", type=Path, required=True, help="PNG file to write")
    parser.add_argument("--rules", type=Path, default=Path("data/rules.csv"), help="moves: rules")
    parser.add_argument("--cast", type=Path, default=Path("data/cast.csv"), help="seam: cast")
    parser.add_argument("--actors", type=Path, default=Path("data/actors.csv"), help="actors")
    parser.add_argument("--route", type=Path, default=Path("data/route.csv"), help="agenda: stops")
    parser.add_argument(
        "--incidents", type=Path, default=Path("data/incidents.csv"), help="agenda: incidents"
    )
    parser.add_argument("--highlight", help="stacey: the section whose stop stands out")
    parser.add_argument("--zones", type=Path, default=Path("02-stacey/data/zones.csv"))
    parser.add_argument("--labels", type=Path, default=Path("02-stacey/data/labels.csv"))
    parser.add_argument("--october", type=Path, default=Path("01-bits/data/october.csv"))
    parser.add_argument("--tested", type=Path, default=Path("01-bits/data/tested.csv"))
    args = parser.parse_args(argv)

    if args.what == "finance":
        weeks = load_october(args.october)
        draw_finance(weeks, args.out)
        args.out.with_suffix(".txt").write_text(report(weeks), encoding="ascii")
        return 0
    if args.what == "coverage-view":
        draw(load_tested(args.tested), args.out)
        return 0
    if args.what == "doubling":
        doubling_chart(load_cast(args.cast), args.out)
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
    if args.what == "moves":
        moves_figure(args.out, moves(load_rules(args.rules)))
        return 0
    if args.what == "business-map":
        business_map(
            load_actors(args.actors), load_cast(args.cast), load_rules(args.rules), args.out
        )
        return 0
    if args.what == "agenda":
        agenda_strip(load_route(args.route), load_incidents(args.incidents), args.out)
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
    {"story": story, "tree": tree}[args.what](args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
