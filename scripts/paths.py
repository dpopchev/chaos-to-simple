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
    python -m scripts.paths doubling --cast data/cast.csv [--upto N] \\
        --out build/01-bits/doubling.txt
    python -m scripts.paths next --bits 6 --out build/01-bits/next.txt
    python -m scripts.paths storyboard --source 01-bits/s01_bits/chaos.py \\
        --bubbles 01-bits/data/bubbles.csv --actors data/actors.csv --out build/01-bits
    python -m scripts.paths bubbles --bubbles 02-stacey/data/bubbles.csv --actors data/actors.csv \\
        --out build/02-stacey
    python -m scripts.paths retro--questions data/questions.csv --out build/03-chaos/retro.txt
    python -m scripts.paths retro --only q3 --questions data/questions.csv \\
        --out build/04-what/dispute.txt
    python -m scripts.paths diff --from A.py --to B.py --snippet S [--to-snippet T]
        [--start TEXT] [--added-only] [--compact] [--hide PATTERN]
        [--label-from A --label-to B] --out F.diff
    python -m scripts.paths wounds --incidents data/incidents.csv
    python -m scripts.paths postmortem --incidents data/incidents.csv --out F.txt
    python -m scripts.paths chart--rules data/rules.csv --out build/06-simple/paths.png
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.palette import load_actors
from scripts.utils.paths import (
    bars_from_rules,
    cast_table,
    count_report,
    doubling_table,
    epilogue_bars,
    epilogue_report,
    grid,
    load_cast,
    load_incidents,
    load_rules,
    next_doubling,
    postmortem_table,
    rules_table,
    splits_report,
    stacked_bar,
    wounds_selector,
)
from scripts.utils.retro import load_questions, question_card, retro_table
from scripts.utils.stagediff import snippet_diff
from scripts.utils.storyboard import STEPS, bubble, load_bubbles, step_view, tally_line


def write_storyboard(source: Path, bubbles: Path, actors: Path, out_dir: Path) -> None:
    """Write step-0..6.diff and bubble-0..8.txt into out_dir."""
    text = source.read_text(encoding="ascii")
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in range(STEPS):
        (out_dir / f"step-{n}.diff").write_text(step_view(text, n), encoding="ascii")
        (out_dir / f"tally-{n}.txt").write_text(tally_line(n) + "\n", encoding="ascii")
    write_bubbles(bubbles, actors, out_dir)


def write_bubbles(bubbles: Path, actors: Path, out_dir: Path) -> None:
    """Write bubble-N.txt, one per row of the bubbles CSV, into out_dir."""
    labels = {key: actor.label for key, actor in load_actors(actors).items()}
    out_dir.mkdir(parents=True, exist_ok=True)
    for n, row in enumerate(load_bubbles(bubbles)):
        (out_dir / f"bubble-{n}.txt").write_text(bubble(row, labels), encoding="ascii")


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
            "doubling",
            "next",
            "wounds",
            "postmortem",
            "retro",
            "storyboard",
            "bubbles",
            "diff",
        ],
    )
    parser.add_argument("--from", dest="from_path", type=Path, default=None)
    parser.add_argument("--to", dest="to_path", type=Path, default=None)
    parser.add_argument("--snippet", default=None, help="snippet of --from (and of --to)")
    parser.add_argument("--to-snippet", default=None, help="snippet of --to when it differs")
    parser.add_argument("--start", default=None, help="diff: start at the first line with TEXT")
    parser.add_argument("--added-only", action="store_true", help="diff: keep only the + lines")
    parser.add_argument("--compact", action="store_true", help="diff: +/- only, --- for a gap")
    parser.add_argument("--hide", default=None, help="diff: drop snippet lines matching PATTERN")
    parser.add_argument("--label-from", default=None, help="diff: caption left of ->")
    parser.add_argument("--label-to", default=None, help="diff: caption right of ->")
    parser.add_argument("--only", default=None, help="retro: the card of this question id")
    parser.add_argument("--questions", type=Path, default=Path("data/questions.csv"))
    parser.add_argument("--bubbles", type=Path, default=Path("01-bits/data/bubbles.csv"))
    parser.add_argument("--actors", type=Path, default=Path("data/actors.csv"))
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
            figsize=(4.5, 4.5),
            fontsize=10,
        )
        return 0

    if args.what == "storyboard":
        if args.out is None:
            parser.error("storyboard needs --out, a directory")
        write_storyboard(args.source, args.bubbles, args.actors, args.out)
        return 0

    if args.what == "bubbles":
        if args.out is None:
            parser.error("bubbles needs --out, a directory")
        write_bubbles(args.bubbles, args.actors, args.out)
        return 0

    if args.what == "diff":
        if args.out is None or args.from_path is None or args.to_path is None or not args.snippet:
            parser.error("diff needs --from, --to, --snippet and --out")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        to_snippet = args.to_snippet or args.snippet
        diff = snippet_diff(
            args.from_path,
            args.snippet,
            args.to_path,
            to_snippet,
            args.start,
            args.added_only,
            args.hide,
            (args.label_from, args.label_to) if args.label_from and args.label_to else None,
            args.compact,
        )
        args.out.write_text(diff, encoding="ascii")
        return 0

    if args.what == "rules":
        text = rules_table(
            load_rules(args.rules), tuple(args.columns.split(",")), load_cast(args.cast)
        )
    elif args.what == "cast":
        text = cast_table(load_cast(args.cast), args.source.read_text(encoding="ascii"))
    elif args.what == "doubling":
        text = doubling_table(load_cast(args.cast), args.upto)
    elif args.what == "next":
        text = next_doubling(args.bits) + "\n"
    elif args.what == "epilogue":
        before = load_rules(args.rules)
        text = epilogue_report(before, [*before, *load_rules(args.seventh)])
    elif args.what == "retro":
        questions = load_questions(args.questions)
        if args.only is None:
            text = retro_table(questions)
        else:
            text = question_card(next(q for q in questions if q.id == args.only))
    elif args.what == "wounds":
        text = wounds_selector(load_incidents(args.incidents)) + "\n"
    elif args.what == "postmortem":
        text = postmortem_table(load_incidents(args.incidents))
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
