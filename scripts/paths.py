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
    python -m scripts.paths tally --version 7 --tests-dir DIR [--only REGEX] --out F.txt
    python -m scripts.paths tally-code --name F --version 7 --policies 6 --paths 64 \\
        --source FILE --snippet S --out F.txt
    python -m scripts.paths imports --source FILE [--source FILE ...] --out F.txt
    python -m scripts.paths imports-figure --source FILE [--source FILE ...] --out F.png
    python -m scripts.paths ifs --source FILE [--source FILE ...] --out F.txt
    python -m scripts.paths retro--questions data/questions.csv --out build/03-chaos/retro.txt
    python -m scripts.paths retro --only q3 --questions data/questions.csv \\
        --out build/04-what/dispute.txt
    python -m scripts.paths diff --from A.py --to B.py --snippet S [--to-snippet T]
        [--start TEXT] [--added-only] [--compact] [--hide PATTERN]
        [--label-from A --label-to B] [--no-scope] \\
        [--name F --version N --policies P --paths N] --out F.diff
    python -m scripts.paths wounds --incidents data/incidents.csv
    python -m scripts.paths postmortem --incidents data/incidents.csv --out F.txt
    python -m scripts.paths chart--rules data/rules.csv --out build/06-simple/paths.png
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.utils.imports import (
    decision_rows,
    decision_table,
    import_edges,
    import_figure,
    import_rows,
    import_table,
)
from scripts.utils.palette import load_actors, load_contexts
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
from scripts.utils.storyboard import (
    STEPS,
    bubble,
    code_length,
    code_tally,
    count_tests,
    load_bubbles,
    step_view,
    suite_view,
    tests_tally,
)
from scripts.utils.widths import snippet_text, strip_step_markers


def write_storyboard(
    source: Path, bubbles: Path, actors: Path, out_dir: Path, wrap: int | None = 34
) -> None:
    """Write step-0..6.diff, test-0..6.diff, tally and bubble-0..8.txt into out_dir."""
    text = source.read_text(encoding="ascii")
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in range(STEPS):
        (out_dir / f"step-{n}.diff").write_text(step_view(text, n), encoding="ascii")
        (out_dir / f"test-{n}.diff").write_text(suite_view(text, n), encoding="ascii")
        tally = code_tally("checkout", n, n, 2**n, code_length(text, n))
        (out_dir / f"tally-{n}.txt").write_text(tally + "\n", encoding="ascii")
    write_bubbles(bubbles, actors, out_dir, wrap)


def tally_text(version: int, tests_dirs: Sequence[Path], only: str | None) -> str:
    """Return the tests tally of a version: tests and non-blank lines over the matched files."""
    pattern = re.compile(only) if only else None
    files = sorted(
        path
        for tests_dir in tests_dirs
        for path in tests_dir.glob("test_*.py")
        if pattern is None or pattern.search(path.name)
    )
    texts = [path.read_text(encoding="utf-8") for path in files]
    lines = sum(1 for text in texts for row in text.splitlines() if row.strip())
    return tests_tally(version, count_tests(texts), lines) + "\n"


def snippet_length(path: Path, snippet: str) -> int:
    """Return the non-blank line count of a file's snippet, step markers stripped."""
    text = snippet_text(strip_step_markers(path.read_text(encoding="ascii")), snippet)
    return sum(1 for row in text.splitlines() if row.strip())


def write_bubbles(bubbles: Path, actors: Path, out_dir: Path, wrap: int | None = 34) -> None:
    """Write bubble-N.txt, one per row of the bubbles CSV, into out_dir, words wrapped at wrap."""
    labels = {key: actor.label for key, actor in load_actors(actors).items()}
    out_dir.mkdir(parents=True, exist_ok=True)
    for n, row in enumerate(load_bubbles(bubbles)):
        (out_dir / f"bubble-{n}.txt").write_text(bubble(row, labels, wrap), encoding="ascii")


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
            "tally",
            "tally-code",
            "imports",
            "imports-figure",
            "ifs",
            "diff",
        ],
    )
    parser.add_argument("--name", default=None, help="tally-code, diff: the function's name")
    parser.add_argument("--version", type=int, default=None, help="tally: the checkout version")
    parser.add_argument("--policies", type=int, default=None, help="tally: the policy count")
    parser.add_argument("--paths", type=int, default=None, help="tally: the path count")
    parser.add_argument(
        "--tests-dir", type=Path, action="append", default=[], help="tally: a tests dir (repeat)"
    )
    parser.add_argument("--from", dest="from_path", type=Path, default=None)
    parser.add_argument("--to", dest="to_path", type=Path, default=None)
    parser.add_argument("--snippet", default=None, help="snippet of --from (and of --to)")
    parser.add_argument("--to-snippet", default=None, help="snippet of --to when it differs")
    parser.add_argument("--start", default=None, help="diff: start at the first line with TEXT")
    parser.add_argument("--added-only", action="store_true", help="diff: keep only the + lines")
    parser.add_argument("--compact", action="store_true", help="diff: +/- only, --- for a gap")
    parser.add_argument(
        "--no-scope", dest="scope", action="store_false", help="diff: no leading def row"
    )
    parser.add_argument("--hide", default=None, help="diff: drop snippet lines matching PATTERN")
    parser.add_argument("--label-from", default=None, help="diff: caption left of ->")
    parser.add_argument("--label-to", default=None, help="diff: caption right of ->")
    parser.add_argument("--only", default=None, help="retro: a question id; tally: file regex")
    parser.add_argument("--questions", type=Path, default=Path("data/questions.csv"))
    parser.add_argument("--bubbles", type=Path, default=Path("01-bits/data/bubbles.csv"))
    parser.add_argument("--actors", type=Path, default=Path("data/actors.csv"))
    parser.add_argument(
        "--wrap", type=int, default=34, help="storyboard, bubbles: bubble column width, 0 = none"
    )
    parser.add_argument("--incidents", type=Path, default=Path("data/incidents.csv"))
    parser.add_argument("--cast", type=Path, default=Path("data/cast.csv"))
    parser.add_argument(
        "--source", type=Path, action="append", default=[], help="a source file; imports repeats it"
    )
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
    source = args.source[-1] if args.source else Path("01-bits/s01_bits/chaos.py")

    if args.what == "imports":
        if args.out is None or not args.source:
            parser.error("imports needs --source (repeatable) and --out")
        rows = [import_rows(path.stem, path.read_text(encoding="ascii")) for path in args.source]
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(import_table(rows), encoding="ascii")
        return 0

    if args.what == "imports-figure":
        if args.out is None or not args.source:
            parser.error("imports-figure needs --source (repeatable) and --out")
        edges = import_edges(
            [(path.stem, path.read_text(encoding="ascii")) for path in args.source]
        )
        import_figure(edges, args.out)
        return 0

    if args.what == "ifs":
        if args.out is None or not args.source:
            parser.error("ifs needs --source (repeatable) and --out")
        found = decision_rows(
            [(path.stem, path.read_text(encoding="ascii")) for path in args.source]
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(decision_table(found), encoding="ascii")
        return 0

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
            figsize=(6.0, 3.2),
            fontsize=10,
        )
        return 0

    if args.what == "storyboard":
        if args.out is None:
            parser.error("storyboard needs --out, a directory")
        write_storyboard(source, args.bubbles, args.actors, args.out, args.wrap or None)
        return 0

    if args.what == "bubbles":
        if args.out is None:
            parser.error("bubbles needs --out, a directory")
        write_bubbles(args.bubbles, args.actors, args.out, args.wrap or None)
        return 0

    if args.what == "tally":
        if args.out is None or args.version is None:
            parser.error("tally needs --version and --out")
        if not args.tests_dir:
            parser.error("tally needs a --tests-dir")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(tally_text(args.version, args.tests_dir, args.only), encoding="ascii")
        return 0

    if args.what == "tally-code":
        if None in (args.name, args.version, args.policies, args.paths, args.snippet, args.out):
            parser.error("tally-code needs --name --version --policies --paths --snippet --out")
        lines = snippet_length(source, args.snippet)
        text = code_tally(args.name, args.version, args.policies, args.paths, lines) + "\n"
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="ascii")
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
            args.scope,
        )
        if args.name and None not in (args.version, args.policies, args.paths):
            lines = snippet_length(args.to_path, to_snippet)
            head = code_tally(args.name, args.version, args.policies, args.paths, lines)
            diff = head + "\n" + diff.partition("\n")[2]
        args.out.write_text(diff, encoding="ascii")
        return 0

    if args.what == "rules":
        text = rules_table(
            load_rules(args.rules), tuple(args.columns.split(",")), load_cast(args.cast)
        )
    elif args.what == "cast":
        text = cast_table(load_cast(args.cast), source.read_text(encoding="ascii"))
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
            text = retro_table(questions, load_rules(args.rules), load_contexts())
        else:
            text = question_card(next(q for q in questions if q.id == args.only))
    elif args.what == "wounds":
        text = wounds_selector(load_incidents(args.incidents)) + "\n"
    elif args.what == "postmortem":
        text = postmortem_table(
            load_incidents(args.incidents), load_rules(args.rules), load_contexts()
        )
    elif args.what == "counts":
        text = count_report(load_rules(args.rules), load_contexts())
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
