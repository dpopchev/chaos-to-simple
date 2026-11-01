"""Probe an icon font with matplotlib: make spike-fa calls this.

python -m scripts.icons probe --font "Font Awesome 7 Free" --out build/spike/fa-probe.png
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.icons import FAMILIES, fc_list, font_file, make_family, probe


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("what", choices=["probe"])
    parser.add_argument("--font", required=True, choices=FAMILIES, help="icon font family")
    parser.add_argument("--out", type=Path, required=True, help="PNG file to write")
    args = parser.parse_args(argv)

    family = make_family(args.font)
    probe(args.out, family, font_file(family, fc_list))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
