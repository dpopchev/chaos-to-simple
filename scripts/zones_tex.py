"""Write the band definitions beside the overview: make artifacts calls this.

python -m scripts.zones_tex --zones 02-stacey/data/zones.csv --out build/00-frontmatter/zones.tex
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.stacey import load_zones, zones_items


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--zones", type=Path, default=Path("02-stacey/data/zones.csv"))
    parser.add_argument("--out", type=Path, required=True, help="zones.tex to write")
    args = parser.parse_args(argv)

    text = zones_items(load_zones(args.zones))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="ascii")
    sys.stdout.write(f"zones.tex: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
