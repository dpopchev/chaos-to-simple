"""make overflow: name the beamer frames the lualatex log reports as overfull.

    python -m scripts.overflow --tex local/state/overflow/talk.tex \\
        --log local/state/overflow/talk.log
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.overflow import overfull_frames


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--tex", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args(argv)

    frames = overfull_frames(
        args.tex.read_text(encoding="utf-8"), args.log.read_text(encoding="utf-8", errors="replace")
    )
    for title in frames:
        sys.stdout.write(f"overflow: {title}\n")
    return 1 if frames else 0


if __name__ == "__main__":
    raise SystemExit(main())
