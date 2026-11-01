"""Render the bit inventory: make artifacts calls this, so slide numbers are never typed.

    python -m scripts.paths rules  --rules data/rules.csv --out build/data/rules.txt
    python -m scripts.paths counts --rules data/rules.csv --out build/data/counts.txt
    python -m scripts.paths splits --rules data/rules.csv --out build/data/splits.txt
    python -m scripts.paths rules  --rules data/rules.csv --columns bit,who,rule \\
        --cast data/cast.csv --out build/03-chaos/rules.txt
    python -m scripts.paths grid   --bits 6 --out build/01-bits/grid.txt
    python -m scripts.paths epilogue --rules data/rules.csv --seventh data/seventh.csv \\
        --out build/06-simple/epilogue.txt
    python -m scripts.paths epilogue-chart --rules data/rules.csv --seventh data/seventh.csv \\
        --out build/06-simple/epilogue.png
    python -m scripts.paths cast   --cast data/cast.csv --source 01-bits/s01_bits/chaos.py \\
        --out build/01-bits/cast.txt
    python -m scripts.paths effects --cast data/cast.csv --source 01-bits/s01_bits/chaos.py \\
        --out build/05-how/effects.txt
    python -m scripts.paths contexts --rules data/rules.csv --cast data/cast.csv \\
        --out build/04-what/contexts.txt
    python -m scripts.paths doubling --cast data/cast.csv [--upto N] \\
        --out build/01-bits/doubling.txt
    python -m scripts.paths growth --cast data/cast.csv --out build/03-chaos/growth.png
    python -m scripts.paths wounds --incidents data/incidents.csv
    python -m scripts.paths chart--rules data/rules.csv --out build/06-simple/paths.png
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.paths import (
    bars_from_rules,
    cast_table,
    contexts_table,
    count_report,
    doubling_table,
    effects_lines,
    epilogue_bars,
    epilogue_report,
    grid,
    growth,
    growth_chart,
    load_cast,
    load_incidents,
    load_rules,
    rules_table,
    splits_report,
    stacked_bar,
    wounds_selector,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "what",
        choices=[
            "rules",
            "counts",
            "splits",
            "grid",
            "chart",
            "epilogue",
            "epilogue-chart",
            "cast",
            "effects",
            "contexts",
            "doubling",
            "growth",
            "wounds",
        ],
    )
    parser.add_argument("--incidents", type=Path, default=Path("data/incidents.csv"))
    parser.add_argument("--cast", type=Path, default=Path("data/cast.csv"))
    parser.add_argument("--source", type=Path, default=Path("01-bits/s01_bits/chaos.py"))
    parser.add_argument("--rules", type=Path, default=Path("data/rules.csv"))
    parser.add_argument("--seventh", type=Path, default=Path("data/seventh.csv"))
    parser.add_argument(
        "--columns",
        default="bit,context,name,code",
        help="comma-separated columns of the rules table; 'who' joins the cast",
    )
    parser.add_argument("--bits", type=int, default=6, help="bits for the grid")
    parser.add_argument("--upto", type=int, default=None, help="first N rows of the doubling")
    parser.add_argument("--out", type=Path, default=None, help="file to write; default stdout")
    args = parser.parse_args(argv)

    if args.what == "chart":
        if args.out is None:
            parser.error("chart needs --out")
        stacked_bar(args.out, bars_from_rules(load_rules(args.rules)))
        return 0

    if args.what == "epilogue-chart":
        if args.out is None:
            parser.error("epilogue-chart needs --out")
        stacked_bar(
            args.out,
            epilogue_bars(load_rules(args.rules), load_rules(args.seventh)),
            title="paths to reason about",
        )
        return 0

    if args.what == "growth":
        if args.out is None:
            parser.error("growth needs --out")
        growth_chart(args.out, growth(load_cast(args.cast)))
        return 0

    if args.what == "rules":
        text = rules_table(
            load_rules(args.rules), tuple(args.columns.split(",")), load_cast(args.cast)
        )
    elif args.what == "cast":
        text = cast_table(load_cast(args.cast), args.source.read_text(encoding="ascii"))
    elif args.what == "effects":
        text = effects_lines(load_cast(args.cast), args.source.read_text(encoding="ascii"))
    elif args.what == "contexts":
        text = contexts_table(load_rules(args.rules), load_cast(args.cast))
    elif args.what == "doubling":
        text = doubling_table(load_cast(args.cast), args.upto)
    elif args.what == "epilogue":
        before = load_rules(args.rules)
        text = epilogue_report(before, [*before, *load_rules(args.seventh)])
    elif args.what == "wounds":
        text = wounds_selector(load_incidents(args.incidents)) + "\n"
    elif args.what == "counts":
        text = count_report(load_rules(args.rules))
    elif args.what == "splits":
        text = splits_report(load_rules(args.rules))
    else:
        text = grid(args.bits)

    if args.out is None:
        sys.stdout.write(text)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="ascii")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
