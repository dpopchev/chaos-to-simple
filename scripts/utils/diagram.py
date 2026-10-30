"""Draw a warning placeholder PNG where a Mermaid render is missing (mmdc is absent)."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def write_placeholder(out: Path, message: str) -> None:
    """Write a PNG of the centered message to out, creating its parent directory."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    ax.axis("off")
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=14, wrap=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    write_placeholder(args.out, args.message)
    logger.info("done: placeholder -> %s", args.out)


if __name__ == "__main__":
    main()
