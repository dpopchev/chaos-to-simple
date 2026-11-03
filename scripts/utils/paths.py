"""Path arithmetic for the talk.

The bit inventory lives in data/rules.csv. This module turns it into the numbers
and tables the slides include: how many paths one function has, how many the
split has, the 64-path grid, and the stacked bar.
"""

from __future__ import annotations

import csv
import re
import textwrap
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, fields
from pathlib import Path

from scripts.utils.palette import Context, colour_of, label_of


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
    date: str
    told_in: str
    decided_in: str
    closed_in: str
    closed_by: str
    kind: str
    cost: str
    decision: str
    principle: str
    subdomain: str


def load_incidents(path: Path) -> tuple[Incident, ...]:
    names = [f.name for f in fields(Incident)]
    with path.open(newline="", encoding="ascii") as fh:
        return tuple(Incident(**{name: row[name] for name in names}) for row in csv.DictReader(fh))


def wounds_selector(incidents: Iterable[Incident]) -> str:
    """The pytest -k selector of the incidents closed by a test, in csv order."""
    return " or ".join(i.closed_by for i in incidents if i.closed_by.startswith(("test_", "Test")))


POSTMORTEM_WIDTHS = (3, 10, 32, 27, 24)  # 3 + 10 + 32 + 27 + 24 + four gaps of 2 is 104
POSTMORTEM_HEADER = ("id", "kind", "decision", "principle", "closed by")


def _wrap_cell(cell: str, width: int) -> list[str]:
    """Wrap a cell; a long name breaks after an underscore or before a capital."""
    if " " in cell or len(cell) <= width:
        return textwrap.wrap(cell, width) or [""]
    lines = [""]
    for part in re.split(r"(?<=_)|(?<=[a-z])(?=[A-Z])", cell):
        if lines[-1] and len(lines[-1]) + len(part) > width:
            lines.append("")
        lines[-1] += part
    return lines


def _postmortem_row(cells: Sequence[str]) -> list[str]:
    """Wrap each cell to its column and join the wrapped lines side by side."""
    wrapped = [_wrap_cell(c, w) for c, w in zip(cells, POSTMORTEM_WIDTHS, strict=True)]
    return [
        "  ".join(
            (lines[i] if i < len(lines) else "").ljust(w)
            for lines, w in zip(wrapped, POSTMORTEM_WIDTHS, strict=True)
        ).rstrip()
        for i in range(max(len(lines) for lines in wrapped))
    ]


def postmortem_table(incidents: Iterable[Incident]) -> str:
    """The post-mortem: one row per incident, with its decision, principle and closing test."""
    lines = _postmortem_row(POSTMORTEM_HEADER)
    for i in incidents:
        lines += _postmortem_row((i.id, i.subdomain, i.decision, i.principle, i.closed_by))
    return "\n".join(lines) + "\n"


def line_of(fragment: str, source: str) -> int:
    """The 1-based line of source holding fragment; raises ValueError unless exactly one does."""
    hits = [n for n, text in enumerate(source.splitlines(), start=1) if fragment in text]
    if len(hits) != 1:
        raise ValueError(f"fragment {fragment!r} matches {len(hits)} lines, want exactly 1")
    return hits[0]


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


def next_doubling(bits: int) -> str:
    """Price the next if: the paths today and the paths one more bit would make."""
    return f"{tangled(bits)} paths today, one more if: {tangled(bits + 1)}"


def doubling_table(cast: Sequence[CastRow], upto: int | None = None) -> str:
    """The first upto core bits (all when None) in csv order: week, who, bits, 2**bits paths."""
    core = [c for c in cast if c.bit.startswith("b")][:upto]
    rows = [("week", "who", "bits", "paths")]
    for bits, c in enumerate(core, start=1):
        rows.append((str(c.week), label_of(c.requested_by), str(bits), str(tangled(bits))))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in rows
    ]
    if upto is None:
        lines.append("tested: 2")
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


def room_curve(
    points: Sequence[Growth], room_week: int, shell_bits: int = 3
) -> tuple[list[int], list[int]]:
    """The growth steps held flat to the room week, then the jump with the shell bits counted."""
    weeks = [p.week for p in points]
    paths = [p.paths for p in points]
    room = tangled(points[-1].bits + shell_bits)
    return [*weeks, room_week, room_week], [*paths, paths[-1], room]


def doubling_chart(
    cast: Sequence[CastRow], out: Path, tested: int = 2, room_week: int | None = None
) -> Path:
    """Draw paths per week as a step line and the flat tested line beside it, near-square.

    room_week, when set, holds the curve flat to that week and jumps to the room's 512 on a
    log2 axis, so every doubling stays visible.
    """
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt

    points = growth(cast)
    weeks = [p.week for p in points]
    paths = [p.paths for p in points]
    end = room_week if room_week is not None else weeks[-1]
    curve = colour_of("marketing")
    flat = colour_of("payment")
    fig, ax = plt.subplots(figsize=(6.0, 6.0), dpi=style.DPI)
    if room_week is None:
        ax.step([*weeks, end], [*paths, paths[-1]], where="post", color=curve, linewidth=3)
    else:
        room_weeks, room_paths = room_curve(points, room_week)
        ax.plot(room_weeks, room_paths, drawstyle="steps-post", color=curve, linewidth=3)
        ax.plot([room_week], [room_paths[-1]], "o", color=curve, markersize=8)
        ax.set_yscale("log", base=2)
        ax.set_yticks([2**n for n in range(1, 10)])
        ax.set_yticklabels([str(2**n) for n in range(1, 10)])
        ax.annotate(
            str(room_paths[-1]),
            (room_week, room_paths[-1]),
            textcoords="offset points",
            xytext=(-8, -4),
            ha="right",
            va="top",
            fontsize=14,
            color=curve,
        )
    ax.plot(weeks, paths, "o", color=curve, markersize=8)
    ax.hlines(tested, weeks[0] - 0.5, end, color=flat, linewidth=3)
    for week, value in zip(weeks, paths, strict=True):
        ax.annotate(
            str(value),
            (week, value),
            textcoords="offset points",
            xytext=(-6, 8),
            ha="right",
            fontsize=14,
            color=curve,
        )
    ax.text(end, tested * 1.35, f"tested: {tested}", ha="right", fontsize=16, color=flat)
    ax.text(weeks[0], paths[-1] * 0.92, "paths", fontsize=16, color=curve)
    ax.set_xlabel("week", fontsize=16)
    ax.set_ylabel("paths", fontsize=16)
    ax.tick_params(labelsize=14)
    ax.set_xticks(range(weeks[0], end + 1))
    ax.set_xlim(weeks[0] - 0.5, end + 0.5)
    if room_week is None:
        ax.set_ylim(0, paths[-1] * 1.15)
    else:
        ax.minorticks_off()
        ax.set_ylim(1.5, room_curve(points, room_week)[1][-1] * 1.4)
    fig.tight_layout()
    style.save(fig, out)
    return out


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


def count_report(rules: Sequence[Rule], contexts: Mapping[str, Context]) -> str:
    """The kind table and the honest count of one function, ending at 2^n.

    Each row carries its context's kind from contexts.csv; the shell is fulfilment.
    """
    core = [r for r in rules if r.scope == "core"]
    shell = [r for r in rules if r.scope == "shell"]
    lines = ["kind        context      bits        paths"]
    for context, n in bits_by(core, "context").items():
        names = " ".join(r.bit for r in core if r.context == context)
        lines.append(f"{contexts[context].kind:<10}  {context:<12} {names:<11} {tangled(n):>5}")
    shell_names = " ".join(r.bit for r in shell)
    kind = contexts["fulfilment"].kind
    lines.append(f"{kind:<10}  {'fulfilment':<12} {shell_names:<11} {tangled(len(shell)):>5}")
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


def cell_kinds(bits: int, tested: Sequence[str], bug: Sequence[str]) -> tuple[str, ...]:
    """Name each of the 2**bits paths by number: "bug", "tested" or "untested"."""
    hit = {int(b, 2) for b in tested}
    broken = {int(b, 2) for b in bug}
    return tuple(
        "bug" if n in broken else "tested" if n in hit else "untested" for n in range(tangled(bits))
    )


def grid_image(bits: int, tested: Sequence[str], bug: Sequence[str], out: Path) -> Path:
    """Draw every path as a cell with its bit string: tested green, the bug red, the rest grey."""
    from scripts.utils import style
    from scripts.utils.coverage_view import GRID_SIDE

    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch, Rectangle

    fills = {
        "tested": colour_of("accounting"),
        "bug": colour_of("payment"),
        "untested": colour_of("customer"),
    }
    fig, ax = plt.subplots(figsize=(6.0, 6.4), dpi=style.DPI)
    for n, kind in enumerate(cell_kinds(bits, tested, bug)):
        r, c = divmod(n, GRID_SIDE)
        y = GRID_SIDE - 1 - r
        ax.add_patch(Rectangle((c, y), 0.94, 0.94, facecolor=fills[kind], edgecolor="none"))
        ax.text(
            c + 0.47,
            y + 0.47,
            f"{n:0{bits}b}",
            ha="center",
            va="center",
            fontsize=11,
            family="monospace",
            color="black" if kind == "untested" else "white",
            fontweight="normal" if kind == "untested" else "bold",
        )
    ax.set_xlim(0, GRID_SIDE)
    ax.set_ylim(0, GRID_SIDE)
    ax.set_aspect("equal")
    ax.axis("off")
    legend = (
        Patch(facecolor=fills["tested"], label="tested"),
        Patch(facecolor=fills["bug"], label="the path finance found"),
        Patch(facecolor=fills["untested"], label="never run"),
    )
    fig.legend(handles=legend, loc="lower center", ncol=3, frameon=False, fontsize=11)
    fig.tight_layout(pad=0.2, rect=(0, 0.06, 1, 1))
    style.save(fig, out)
    return out


def panel_titles(shell_bits: int) -> tuple[str, ...]:
    """One title per shell configuration, the bits s2 s1 s0 counted up from all zero."""
    return tuple(f"{n:0{shell_bits}b}" for n in range(tangled(shell_bits)))


SHELL_WORLDS = {"s0": "card declined", "s1": "stock gone", "s2": "mail bounced"}


def world_name(bits: str, rules: Sequence[Rule]) -> str:
    """Name a panel by its set shell effects, the bits written s2 s1 s0 left to right."""
    shell = [r.bit for r in rules if r.scope == "shell"]
    set_bits = [bit for n, bit in enumerate(shell) if bits[-1 - n] == "1"]
    return ", ".join(SHELL_WORLDS[bit] for bit in reversed(set_bits)) or "all answered"


def panels_suptitle(core_bits: int, shell_bits: int) -> str:
    """Say what the panels are: the core grid once per world of the shell effects."""
    worlds = tangled(shell_bits)
    cells = tangled(core_bits)
    return (
        f"the {cells} paths of 01, once per world of the three effects: "
        f"{worlds} x {cells} = {worlds * cells}"
    )


def stock_gone(title: str) -> bool:
    """Whether the panel is a configuration where the warehouse answers OutOfStock (s1 set)."""
    return title[-2] == "1"


def grid_panels(
    core_bits: int,
    shell_bits: int,
    tested: Sequence[str],
    bug: Sequence[str],
    out: Path,
    rules: Sequence[Rule],
) -> Path:
    """Draw one 8x8 panel per shell configuration; panel 0 marks the tested and bug cells.

    Every stock-gone panel is framed in the payment colour and titled by its bits and world.
    """
    from scripts.utils import style
    from scripts.utils.coverage_view import GRID_SIDE

    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fills = {
        "tested": colour_of("accounting"),
        "bug": colour_of("payment"),
        "untested": colour_of("customer"),
    }
    titles = panel_titles(shell_bits)
    columns = 4
    rows = len(titles) // columns
    fig, axes = plt.subplots(rows, columns, figsize=(6.4, 3.8), dpi=style.DPI)
    for n, (ax, title) in enumerate(zip(axes.flat, titles, strict=True)):
        kinds = cell_kinds(core_bits, tested if n == 0 else [], bug if n == 0 else [])
        for k, kind in enumerate(kinds):
            r, c = divmod(k, GRID_SIDE)
            ax.add_patch(
                Rectangle((c, GRID_SIDE - 1 - r), 0.9, 0.9, facecolor=fills[kind], edgecolor="none")
            )
        framed = stock_gone(title)
        if framed:
            ax.add_patch(
                Rectangle(
                    (-0.35, -0.35),
                    GRID_SIDE + 0.6,
                    GRID_SIDE + 0.6,
                    fill=False,
                    edgecolor=colour_of("payment"),
                    linewidth=3.5,
                )
            )
        ax.set_xlim(-0.5, GRID_SIDE + 0.5)
        ax.set_ylim(-0.5, GRID_SIDE + 0.5)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(
            textwrap.fill(world_name(title, rules), 22),
            fontsize=7,
            fontweight="bold",
            color=colour_of("payment") if framed else "black",
        )
    fig.suptitle(panels_suptitle(core_bits, shell_bits), fontsize=9, fontweight="bold")
    fig.tight_layout(pad=0.3, h_pad=2.6, rect=(0, 0, 1, 0.94))
    style.save(fig, out)
    return out


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
                ("fulfilment", tangled(len(shell))),
            ],
        ),
    ]


def epilogue_bars(rules: Sequence[Rule], seventh: Sequence[Rule]) -> tuple[Bar, Bar]:
    """The contexts + shell bar before and after the seventh rule joins, shell segment last.

    Segments follow the context order of the deck palette (palette.CONTEXTS), so
    stacked_bar's colours match context_colour.
    """
    before = bars_from_rules(rules)[2]
    after = bars_from_rules([*rules, *seventh])[2]
    return (("before", before[1]), ("after", after[1]))


def bar_headroom(top: int) -> float:
    """The upper y limit of a stacked bar chart, with room above the tallest bar for its total."""
    return top * 1.2


def is_small(value: int, top: int) -> bool:
    """Whether a slice is too thin for a label inside it: under 8% of the top."""
    return value < 0.08 * top


def small_slices(bars: Sequence[Bar], top: int) -> tuple[Segment, ...]:
    """The thin slices in bar order, a slice of the same name and value once."""
    thin = (seg for _, segments in bars for seg in segments if is_small(seg[1], top))
    merged: dict[tuple[str, int], str] = {}
    for name, value in thin:
        key = (name.split()[0], value)  # the first word picks the colour (segment_colour)
        merged[key] = min(merged.get(key, name), name, key=len)
    return tuple((name, key[1]) for key, name in merged.items())


def legend_entries(bars: Sequence[Bar], top: int) -> tuple[str, ...]:
    """The 'name: value' text of each slice under 8% of the top, in bar order."""
    return tuple(f"{name}: {value}" for name, value in small_slices(bars, top))


def segment_colour(name: str) -> str:
    """Return the palette colour of a bar segment: its context, the shell, the core or the tangle.

    A segment is named by a context key, "shell", "core N bits", "shell N bits" or
    "N bits tangled"; the core as a whole is the shop's own (dev) colour.
    """
    words = name.split()
    if words[-1] == "tangled":
        return colour_of("tangled")
    return colour_of({"core": "dev", "shell": "fulfilment"}.get(words[0], words[0]))


FIT = 0.85  # an in-bar label may fill this share of its bar's width


def stacked_bar(
    out: Path,
    bars: Sequence[Bar],
    title: str = "paths to reason about",
    figsize: tuple[float, float] = (8.0, 3.5),
    fontsize: int = 11,
) -> None:
    """A stacked bar per way of counting, every segment labelled with its exact count.

    A segment under 8% of the top is named in a legend box right of the bars, no leader line.
    """
    from scripts.utils import style

    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    top = max(sum(value for _, value in segments) for _, segments in bars)
    small = small_slices(bars, top)
    fig, ax = plt.subplots(figsize=figsize, dpi=style.DPI)
    ax.set_xticks([])
    ax.set_xlim(-0.5, len(bars) - 0.2)
    ax.set_ylim(0, bar_headroom(top))
    ax.set_ylabel(title, fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    if small:
        ax.legend(
            handles=[
                Patch(facecolor=segment_colour(name), edgecolor="white", label=f"{name}: {value}")
                for name, value in small
            ],
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=True,
            fontsize=fontsize,
        )
    fig.tight_layout()
    fig.canvas.draw()  # a first draw gives text extents a renderer
    bar_px = ax.transData.transform((0.3, 0))[0] - ax.transData.transform((-0.3, 0))[0]
    for x, (label, segments) in enumerate(bars):
        bottom = 0
        for name, value in segments:
            ax.bar(
                x,
                value,
                bottom=bottom,
                width=0.6,
                color=segment_colour(name),
                edgecolor="white",
                linewidth=0.8,
            )
            middle = bottom + value / 2
            ink = "white" if name.startswith("core") else "black"  # the core is the black dev
            if not is_small(value, top):
                wrapped = value >= 0.2 * top
                label_text = ax.text(
                    x,
                    middle,
                    f"{name}:\n{value}" if wrapped else f"{name}: {value}",
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                    color=ink,
                )
                if label_text.get_window_extent().width > FIT * bar_px:
                    label_text.set_text(f"{name}:\n{value}")
                slice_px = (
                    ax.transData.transform((0, bottom + value))[1]
                    - ax.transData.transform((0, bottom))[1]
                )
                size = fontsize
                while (
                    label_text.get_window_extent().width > FIT * bar_px
                    or label_text.get_window_extent().height > FIT * slice_px
                ):
                    size -= 1
                    label_text.set_fontsize(size)
            bottom += value
        ax.text(
            x, bottom, str(bottom), ha="center", va="bottom", fontsize=fontsize, fontweight="bold"
        )
        ax.text(x, -0.02 * top, label, ha="center", va="top", fontsize=fontsize)
    fig.tight_layout()
    style.save(fig, out)
