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
    requested_by: str
    words: str
    fragment: str


def load_cast(path: Path) -> list[CastRow]:
    names = [f.name for f in fields(CastRow)]
    with path.open(newline="", encoding="ascii") as fh:
        return [CastRow(**{name: row[name] for name in names}) for row in csv.DictReader(fh)]


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


def cast_table(cast: Sequence[CastRow], source: str) -> str:
    """The cast of the ifs: the source line, the bit, who asked and their words."""
    rows = [("line", "bit", "who", "words")]
    rows += [(str(line_of(c.fragment, source)), c.bit, c.requested_by, c.words) for c in cast]
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    return "\n".join(lines) + "\n"


def contexts_table(rules: Sequence[Rule], cast: Sequence[CastRow]) -> str:
    """Each context with its bits, its 2**n paths and who asked for them, in rules order."""
    requester = {c.bit: c.requested_by for c in cast}
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


def rules_table(rules: Sequence[Rule]) -> str:
    """The glossary: bit, context, name and the code that carries it."""
    columns = ("bit", "context", "name", "code")
    rows = [columns, *[tuple(getattr(r, c) for c in columns) for r in rules]]
    widths = [max(len(row[i]) for row in rows) for i in range(len(columns))]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    return "\n".join(lines) + "\n"


def count_report(rules: Sequence[Rule]) -> str:
    """Three ways to count the same bits: tangled, core | shell, contexts | shell."""
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
    lines.append(
        f"core | shell:           2^{len(core)} + 2^{len(shell)}"
        f" = {tangled(len(core))} + {tangled(len(shell))} = {split([len(core), len(shell)])}"
    )
    parts = [tangled(n) for n in contexts.values()] + [tangled(len(shell))]
    lines.append(f"contexts | shell:       {' + '.join(str(p) for p in parts)} = {sum(parts)}")
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


def stacked_bar(out: Path, bars: Sequence[Bar], title: str = "paths to reason about") -> None:
    """A stacked bar per way of counting, every segment labelled with its exact count.

    A segment too thin to carry its label inside gets it in a note beside the bar.
    """
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt

    colours = style.palette()
    top = max(sum(value for _, value in segments) for _, segments in bars)
    fig, ax = plt.subplots(figsize=style.FIGSIZE, dpi=style.DPI)
    for x, (label, segments) in enumerate(bars):
        bottom = 0
        beside: list[str] = []
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
            if value >= 0.08 * top:
                label_y = bottom + value / 2
                ax.text(x, label_y, f"{name}: {value}", ha="center", va="center", fontsize=8)
            else:
                beside.append(f"{name}: {value}")
            bottom += value
        ax.text(x, bottom, str(bottom), ha="center", va="bottom", fontsize=11, fontweight="bold")
        if beside:
            ax.text(x + 0.33, bottom, "\n".join(beside), ha="left", va="bottom", fontsize=8)
        ax.text(x, -0.02 * top, label, ha="center", va="top")
    ax.set_xticks([])
    ax.set_xlim(-0.5, len(bars) - 0.2)
    ax.set_ylabel(title)
    ax.set_title(title)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    style.save(fig, out)
