"""Write the LaTeX actor macros: make artifacts calls this.

python -m scripts.actors_tex --out build/00-frontmatter/actors.tex
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.icons import FONT_AWESOME, fc_list, font_available
from scripts.utils.palette import ACTORS_CSV, CONTEXTS_CSV, actors_tex, load_actors, load_contexts


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--actors", type=Path, default=ACTORS_CSV)
    parser.add_argument("--contexts", type=Path, default=CONTEXTS_CSV)
    parser.add_argument("--out", type=Path, required=True, help="actors.tex to write")
    args = parser.parse_args(argv)

    icon_font = FONT_AWESOME if font_available(FONT_AWESOME, fc_list) else None
    text = actors_tex(load_actors(args.actors), load_contexts(args.contexts), icon_font)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="ascii")
    sys.stdout.write(f"actors.tex: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
