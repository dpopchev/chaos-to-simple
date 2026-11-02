"""Write the LaTeX section beats: make artifacts calls this.

python -m scripts.beats_tex --lines data/lines.csv --out build/00-frontmatter/beats.tex
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.beats import beats_tex
from scripts.utils.lines import load_lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--lines", type=Path, default=Path("data/lines.csv"))
    parser.add_argument("--out", type=Path, required=True, help="beats.tex to write")
    args = parser.parse_args(argv)

    text = beats_tex(load_lines(args.lines))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="ascii")
    sys.stdout.write(f"beats.tex: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
