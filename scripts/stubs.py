"""make stubs: write a placeholder for each manifest path that no make rule builds.

    python -m scripts.stubs --manifest data/artifacts.csv --built <paths> [--strict]

--strict writes nothing: it prints each path without a rule and exits 1.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.stubs import load_manifest, missing, strict, write_stub


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--manifest", type=Path, default=Path("data/artifacts.csv"))
    parser.add_argument("--built", nargs="*", default=[])
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    manifest = load_manifest(args.manifest)
    if args.strict:
        ruleless = strict(manifest, args.built)
        for path in ruleless:
            sys.stdout.write(f"stubs: no rule builds {path}\n")
        return 1 if ruleless else 0
    for entry in missing(manifest, args.built):
        write_stub(Path(entry.path), entry.kind)
        sys.stdout.write(f"[WARN] stub written: {entry.path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
