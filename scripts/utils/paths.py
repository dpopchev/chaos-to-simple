"""Path arithmetic for the talk.

The bit inventory lives in data/rules.csv. This module turns it into the numbers
and tables the slides include: how many paths one function has, how many the
split has, the 64-path grid, and the stacked bar.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, fields
from pathlib import Path

from scripts.utils.palette import label_of


@dataclass(frozen=True)
class Rule:
    bit: str
    scope: str
    context: str
    name: str
    rule: str
    code: str


def load_rules(path: Path) -> list[Rule]:
    names = [f.name for f in fields(Rule)]
    with path.open(newline="", encoding="ascii") as fh:
        return [Rule(**{name: row[name] for name in names}) for row in csv.DictReader(fh)]


@dataclass(frozen=True)
class CastRow:
    bit: str
    step: int
    week: int | None
    requested_by: str
    words: str
    aside: str
    fragment: str


def load_cast(path: Path) -> list[CastRow]:
    """Read the cast; an empty week cell (a shell effect nobody asked for) is None."""
    with path.open(newline="", encoding="ascii") as fh:
        return [
            CastRow(
                row["bit"],
                int(row["step"]),
                int(row["week"]) if row["week"] else None,
                row["requested_by"],
                row["words"],
                row["aside"],
                row["fragment"],
            )
            for row in csv.DictReader(fh)
        ]


@dataclass(frozen=True)
class Incident:
    id: str
    week: str
    told_in: str
    closed_in: str
    closed_by: str
    kind: str
    cost: str


def load_incidents(path: Path) -> tuple[Incident, ...]:
    names = [f.name for f in fields(Incident)]
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(Incident(**{name: row[name] for name in names}) for row in csv.DictReader(fh))


def wounds_selector(incidents: Iterable[Incident]) -> str:
    """The pytest -k selector of the incidents closed by a test, in csv order."""
    return " or ".join(i.closed_by for i in incidents if i.closed_by.startswith("test_"))


def line_of(fragment: str, source: str) -> int:
    """The 1-based line of source holding fragment; raises ValueError unless exactly one does."""
    hits = [n for n, text in enumerate(source.splitlines(), start=1) if fragment in text]
    if len(hits) != 1:
        raise ValueError(f"fragment {fragment!r} matches {len(hits)} lines, want exactly 1")
    return hits[0]


def effects_lines(cast: Sequence[CastRow], source: str) -> str:
    """The source lines of the shell effects (the s* bits), each prefixed by its line number."""
    lines = source.splitlines()
    placed = sorted((line_of(c.fragment, source), c) for c in cast if c.bit.startswith("s"))
    width = max((len(str(n)) for n, _ in placed), default=0)
    return "".join(f"{str(n).rjust(width)}  {lines[n - 1].strip()}\n" for n, _ in placed)


def cast_table(cast: Sequence[CastRow], source: str) -> str:
    """The cast of the ifs by source line: the line, the bit, who asked and their words."""
    placed = sorted(((line_of(c.fragment, source), c) for c in cast), key=lambda p: p[0])
    rows = [("line", "bit", "who", "words")]
    rows += [(str(line), c.bit, label_of(c.requested_by), c.words) for line, c in placed]
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    return "\n".join(lines) + "\n"


def doubling_table(cast: Sequence[CastRow], upto: int | None = None) -> str:
    """The first upto core bits (all when None) in csv order: week, who, bits, 2**bits paths."""
    core = [c for c in cast if c.bit.startswith("b")][:upto]
    rows = [("week", "who", "bits", "paths")]
    for bits, c in enumerate(core, start=1):
        rows.append((str(c.week), label_of(c.requested_by),str(bits), str(tangled(bits))))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class Growth:
    week: int
    bits: int
    paths: int


def growth(cast: Sequence[CastRow]) -> tuple[Growth, ...]:
    """One point per core bit in week order: the bits so far and the 2**bits paths they make."""
    weeks = [c.week for c in cast if c.bit.startswith("b") and c.week is not None]
    return tuple(Growth(w, bits, tangled(bits)) for bits, w in enumerate(weeks, start=1))


def contexts_table(rules: Sequence[Rule], cast: Sequence[CastRow]) -> str:
    """Each context with its bits, its 2**n paths and who asked for them, in rules order."""
    requester = {c.bit: label_of(c.requested_by) for c in cast}
    rows = [("context", "bits", "paths", "who")]
    for context in bits_by(rules, "context"):
        bits = [r.bit for r in rules if r.context == context]
        who = list(dict.fromkeys(requester[b] for b in bits))
        rows.append((context, " ".join(bits), str(tangled(len(bits))), ", ".join(who)))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    return "\n".join(lines) + "\n"


def tangled(bits: int) -> int:
    """Decisions in one function multiply: n bits are 2**n paths."""
    return 2**bits


def split(groups: Iterable[int]) -> int:
    """Decisions behind a value boundary add: the sum of 2**bits per group."""
    return sum(2**g for g in groups)


def bits_by(rules: Sequence[Rule], key: str) -> dict[str, int]:
    """Bits per value of a Rule field, in order of first appearance."""
    counts: dict[str, int] = {}
    for rule in rules:
        value = getattr(rule, key)
        counts[value] = counts.get(value, 0) + 1
    return counts


def rules_table(
    rules: Sequence[Rule],
    columns: Sequence[str] = ("bit", "context", "name", "code"),
    cast: Sequence[CastRow] = (),
) -> str:
    """The glossary of the chosen columns; 'who' is the requester joined from cast by bit."""
    requester = {c.bit: label_of(c.requested_by) for c in cast}

    def cell(rule: Rule, column: str) -> str:
        return requester[rule.bit] if column == "who" else getattr(rule, column)

    rows = [tuple(columns), *[tuple(cell(r, c) for c in columns) for r in rules]]
    widths = [max(len(row[i]) for row in rows) for i in range(len(columns))]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    return "\n".join(lines) + "\n"


def count_report(rules: Sequence[Rule]) -> str:
    """The scope table and the honest count of one function, ending at 2^n."""
    core = [r for r in rules if r.scope == "core"]
    shell = [r for r in rules if r.scope == "shell"]
    contexts = bits_by(core, "context")
    lines = ["scope  context   bits        paths"]
    for context, n in contexts.items():
        names = " ".join(r.bit for r in core if r.context == context)
        lines.append(f"core   {context:<9} {names:<11} {tangled(n):>5}")
    shell_names = " ".join(r.bit for r in shell)
    lines.append(f"shell  effects   {shell_names:<11} {tangled(len(shell)):>5}")
    lines.append("")
    n = len(rules)
    lines.append(f"one function, {n} bits:  2^{n} = {tangled(n)}")
    return "\n".join(lines) + "\n"


def splits_report(rules: Sequence[Rule]) -> str:
    """The two splits: core | shell and contexts | shell."""
    core = [r for r in rules if r.scope == "core"]
    shell = [r for r in rules if r.scope == "shell"]
    contexts = bits_by(core, "context")
    parts = [tangled(n) for n in contexts.values()] + [tangled(len(shell))]
    lines = [
        f"core | shell:           2^{len(core)} + 2^{len(shell)}"
        f" = {tangled(len(core))} + {tangled(len(shell))} = {split([len(core), len(shell)])}",
        f"contexts | shell:       {' + '.join(str(p) for p in parts)} = {sum(parts)}",
    ]
    return "\n".join(lines) + "\n"


def path_counts(rules: Sequence[Rule]) -> tuple[int, int, int]:
    """Paths by the three ways of counting: one function, core + shell, contexts + shell."""
    core = [r for r in rules if r.scope == "core"]
    shell = [r for r in rules if r.scope == "shell"]
    contexts = bits_by(core, "context")
    return (
        tangled(len(rules)),
        split([len(core), len(shell)]),
        split(contexts.values()) + tangled(len(shell)),
    )


def epilogue_report(before: Sequence[Rule], after: Sequence[Rule]) -> str:
    """One line per way of counting: paths before, after and the delta."""
    labels = ("one function:", "core | shell:", "contexts | shell:")
    lines = []
    for label, old, new in zip(labels, path_counts(before), path_counts(after), strict=True):
        lines.append(f"{label:<18}{old:>4} -> {new:>4}  ({new - old:+d})")
    return "\n".join(lines) + "\n"


def grid(bits: int, columns: int = 8) -> str:
    """Every path as a bit string, so 64 stops being an abstraction."""
    cells = [f"{n:0{bits}b}" for n in range(tangled(bits))]
    rows = [" ".join(cells[i : i + columns]) for i in range(0, len(cells), columns)]
    return "\n".join(rows) + "\n"


Segment = tuple[str, int]
Bar = tuple[str, Sequence[Segment]]


def bars_from_rules(rules: Sequence[Rule]) -> list[Bar]:
    """The three bars of the closing chart, derived from the inventory."""
    core = [r for r in rules if r.scope == "core"]
    shell = [r for r in rules if r.scope == "shell"]
    contexts = bits_by(core, "context")
    return [
        ("one function", [(f"{len(rules)} bits tangled", tangled(len(rules)))]),
        (
            "core + shell",
            [
                (f"core {len(core)} bits", tangled(len(core))),
                (f"shell {len(shell)} bits", tangled(len(shell))),
            ],
        ),
        (
            "contexts + shell",
            [
                *[(context, tangled(n)) for context, n in contexts.items()],
                ("shell", tangled(len(shell))),
            ],
        ),
    ]


def epilogue_bars(rules: Sequence[Rule], seventh: Sequence[Rule]) -> tuple[Bar, Bar]:
    """The contexts + shell bar before and after the seventh rule joins, shell segment last.

    Segments follow the context order of the deck palette (style.CONTEXTS), so
    stacked_bar's colours match context_colour.
    """
    before = bars_from_rules(rules)[2]
    after = bars_from_rules([*rules, *seventh])[2]
    return (("before", before[1]), ("after", after[1]))


def growth_chart(out: Path, points: Sequence[Growth]) -> Path:
    """Draw bits and paths over the weeks as two lines, every point labelled with its count.

    Points sharing a week get their labels pushed apart, so none sits on another.
    """
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt

    colours = style.palette()
    weeks = [p.week for p in points]
    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    for name, values, colour in (
        ("paths", [p.paths for p in points], colours[1]),
        ("bits", [p.bits for p in points], colours[0]),
    ):
        ax.plot(weeks, values, marker="o", color=colour, label=name)
        for i, (week, value) in enumerate(zip(weeks, values, strict=True)):
            second = i > 0 and weeks[i - 1] == week
            first = i + 1 < len(weeks) and weeks[i + 1] == week
            dx = 8 if second else -8 if first else 0
            ha = "left" if second else "right" if first else "center"
            ax.annotate(
                str(value),
                (week, value),
                textcoords="offset points",
                xytext=(dx, -14 if name == "bits" else 8),
                ha=ha,
                fontsize=9,
                color=colour,
            )
    ax.set_xlabel("week")
    ax.set_ylabel("count")
    ax.set_xticks(range(min(weeks), max(weeks) + 1))
    ax.set_ylim(-6, max(p.paths for p in points) * 1.12)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    style.save(fig, out)
    return out


def bar_headroom(top: int) -> float:
    """The upper y limit of a stacked bar chart, with room above the tallest bar for its total."""
    return top * 1.2


def slice_label_point(x: float, bottom: float, value: float) -> tuple[float, float]:
    """Where a thin slice's label sits: beside the bar, level with the slice's middle."""
    return (x + 0.33, bottom + value / 2)


def spread_apart(ys: Sequence[float], gap: float) -> list[float]:
    """Push ascending label heights upward until neighbours sit at least gap apart."""
    placed: list[float] = []
    for y in ys:
        placed.append(max(y, placed[-1] + gap) if placed else y)
    return placed


def stacked_bar(
    out: Path,
    bars: Sequence[Bar],
    title: str = "paths to reason about",
    figsize: tuple[float, float] = (8.0, 3.5),
    fontsize: int = 11,
) -> None:
    """A stacked bar per way of counting, every segment labelled with its exact count.

    A segment under 8% of the top gets its label beside the bar, level with the slice.
    """
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt

    colours = style.palette()
    top = max(sum(value for _, value in segments) for _, segments in bars)
    fig, ax = plt.subplots(figsize=figsize, dpi=style.DPI)
    gap = bar_headroom(top) * 1.5 * fontsize / (0.75 * figsize[1] * 72)
    aside: list[tuple[str, tuple[float, float]]] = []
    for x, (label, segments) in enumerate(bars):
        bottom = 0
        for i, (name, value) in enumerate(segments):
            ax.bar(
                x,
                value,
                bottom=bottom,
                width=0.6,
                color=colours[i % len(colours)],
                edgecolor="white",
                linewidth=0.8,
            )
            middle = bottom + value / 2
            if value >= 0.2 * top:
                ax.text(
                    x, middle, f"{name}:\n{value}", ha="center", va="center", fontsize=fontsize
                )
            elif value >= 0.08 * top:
                ax.text(x, middle, f"{name}: {value}", ha="center", va="center", fontsize=fontsize)
            else:
                aside.append((f"{name}: {value}", slice_label_point(x, bottom, value)))
            bottom += value
        points = [point for _, point in aside]
        for (text, (lx, ly)), y in zip(
            aside, spread_apart([py for _, py in points], gap), strict=True
        ):
            ax.annotate(
                text,
                (lx - 0.03, ly),
                xytext=(lx + 0.05, y),
                ha="left",
                va="center",
                fontsize=fontsize,
                arrowprops={"arrowstyle": "-", "color": "0.5", "linewidth": 0.8},
            )
        aside.clear()
        ax.text(
            x, bottom, str(bottom), ha="center", va="bottom", fontsize=fontsize, fontweight="bold"
        )
        ax.text(x, -0.02 * top, label, ha="center", va="top", fontsize=fontsize)
    ax.set_xticks([])
    ax.set_xlim(-0.5, len(bars) - 0.2)
    ax.set_ylim(0, bar_headroom(top))
    ax.set_ylabel(title, fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    style.save(fig, out)
