"""Render the bit inventory: make artifacts calls this, so slide numbers are never typed.

    python -m scripts.paths rules  --rules data/rules.csv --out build/data/rules.txt
    python -m scripts.paths counts --rules data/rules.csv --out build/data/counts.txt
    python -m scripts.paths grid   --bits 6 --out build/01-bits/grid.txt
    python -m scripts.paths epilogue --rules data/rules.csv --seventh data/seventh.csv \\
        --out build/06-simple/epilogue.txt
    python -m scripts.paths chart --rules data/rules.csv --out build/06-simple/paths.png
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.paths import (
    bars_from_rules,
    count_report,
    epilogue_report,
    grid,
    load_rules,
    rules_table,
    stacked_bar,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("what", choices=["rules", "counts", "grid", "chart", "epilogue"])
    parser.add_argument("--rules", type=Path, default=Path("data/rules.csv"))
    parser.add_argument("--seventh", type=Path, default=Path("data/seventh.csv"))
    parser.add_argument("--bits", type=int, default=6, help="bits for the grid")
    parser.add_argument("--out", type=Path, default=None, help="file to write; default stdout")
    args = parser.parse_args(argv)

    if args.what == "chart":
        if args.out is None:
            parser.error("chart needs --out")
        stacked_bar(args.out, bars_from_rules(load_rules(args.rules)))
        return 0

    if args.what == "rules":
        text = rules_table(load_rules(args.rules))
    elif args.what == "epilogue":
        before = load_rules(args.rules)
        text = epilogue_report(before, [*before, *load_rules(args.seventh)])
    elif args.what == "counts":
        text = count_report(load_rules(args.rules))
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
