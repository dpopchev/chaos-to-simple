"""The responsibilities picture: calculate the offer, carry out the order, the outside providers."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path

from scripts.utils import style
from scripts.utils.figures import icon_file, label_ink
from scripts.utils.icons import FONT_AWESOME, glyph
from scripts.utils.palette import (
    Actor,
    Context,
    colour_of,
    kind_style,
    load_actors,
    load_contexts,
)
from scripts.utils.paths import load_rules

RULES_CSV = Path(__file__).resolve().parents[2] / "data" / "rules.csv"
FADED = 0.25
OFFER_TITLE, OFFER_NOTE = "calculate the offer", "functional core: price()"
SHELL_TITLE, SHELL_NOTE = "carry out the order", "imperative shell: checkout()"
OUTSIDE_TITLE = "outside capabilities"
CORE_CONTRACT = "Priced"
BOX_H = 1.3
OFFER_Y = (5.0, 3.35, 1.7)
PROVIDER_Y = (5.6, 3.6, 1.6)
MID_Y = 3.6


@dataclass(frozen=True)
class Layout:
    """The picture's size, type sizes and column positions in axes units."""

    figsize: tuple[float, float]
    xmax: float
    title_font: int
    body_font: int
    frame: tuple[float, float, float, float]
    offer: tuple[float, float]
    shell: tuple[float, float]
    provider: tuple[float, float]


WIDE = Layout((15.4, 6.4), 19.4, 16, 14, (1.8, 0.5, 4.4, 7.1), (2.0, 4.0), (8.2, 4.4), (15.6, 3.6))
COMPACT = Layout(
    (11.8, 6.5), 22.1, 18, 16, (1.7, 0.5, 5.2, 7.1), (2.0, 4.6), (9.2, 6.0), (18.4, 3.6)
)


@dataclass(frozen=True)
class Model:
    """The picture's boxes in three groups and the contract each box's boundary carries."""

    groups: tuple[tuple[str, ...], ...]
    contracts: dict[str, str]


def build(rules_csv: Path, contexts: dict[str, Context], actors: dict[str, Actor]) -> Model:
    """Read the groups and contracts from the rules, contexts and actors."""
    rules = load_rules(rules_csv)
    offer = tuple(dict.fromkeys(r.context for r in rules if r.scope == "core"))
    shell = tuple(dict.fromkeys(r.context for r in rules if r.scope == "shell"))
    providers = tuple(
        c.key
        for c in contexts.values()
        if any(o in actors and actors[o].kind == "provider" for o in c.owner.split(";"))
    )
    answers = [r.code for r in rules if r.scope == "shell"]
    contracts = {name: CORE_CONTRACT for name in offer}
    contracts.update({name: contexts[name].result for name in shell})
    contracts.update(zip(providers, answers, strict=True))
    return Model((offer, shell, providers), contracts)


@cache
def _model() -> Model:
    return build(RULES_CSV, load_contexts(), load_actors())


def groups() -> tuple[tuple[str, ...], ...]:
    """Return the box names of the offer group, the order box and the providers."""
    return _model().groups


def boxes() -> tuple[str, ...]:
    """Return every box name, left to right."""
    return tuple(name for group in groups() for name in group)


def _checked(name: str) -> str:
    if name not in boxes():
        raise ValueError(f"unknown box {name!r}; expected one of {boxes()}")
    return name


def muted(highlight: str | None) -> tuple[str, ...]:
    """Return the names drawn faded: every box but the highlighted one, none without one."""
    if highlight is None:
        return ()
    return tuple(name for name in boxes() if name != _checked(highlight))


def contract_of(name: str) -> str:
    """Return the contract crossing the boundary of this box; raise ValueError if unknown."""
    return _model().contracts[_checked(name)]


def draw(out: Path, highlight: str | None = None, compact: bool = False) -> Path:
    """Draw the picture; a highlight fades the other boxes, compact is taller with larger type."""
    style.apply()
    lay = COMPACT if compact else WIDE
    title_font, body_font = lay.title_font, lay.body_font
    offer_x, offer_w = lay.offer
    shell_x0, shell_w = lay.shell
    provider_x, provider_w = lay.provider
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    offer, shell, providers = groups()
    contexts, actors = load_contexts(), load_actors()
    faded = muted(highlight)
    shape = "round,pad=0.05,rounding_size=0.15"
    font = icon_file()
    fig, ax = plt.subplots(figsize=lay.figsize, dpi=style.DPI)

    def alpha(name: str) -> float:
        return FADED if name in faded else 1.0

    def box(x: float, y: float, w: float, h: float, name: str, face: str, edge: str) -> None:
        picked = name == highlight
        ax.add_patch(
            FancyBboxPatch(
                (x, y - h / 2),
                w,
                h,
                boxstyle=shape,
                facecolor=face,
                edgecolor="black" if picked else edge,
                linewidth=4 if picked else 0,
                alpha=alpha(name),
                zorder=3,
            )
        )

    def arrow(x0: float, x1: float, y: float, touches: tuple[str, ...], words: str) -> None:
        bold = highlight in touches
        kept = highlight is None or bold
        ax.annotate(
            "",
            (x1, y),
            (x0, y),
            arrowprops={
                "arrowstyle": "-|>",
                "color": "black" if bold else "dimgrey",
                "linewidth": 5.0 if bold else 2.0,
                "alpha": 1.0 if kept else FADED,
                "shrinkA": 0,
                "shrinkB": 0,
            },
            zorder=2,
        )
        ax.text(
            (x0 + x1) / 2,
            y + 0.2,
            words,
            ha="center",
            va="bottom",
            fontsize=body_font,
            style="italic",
            fontweight="bold" if bold else "normal",
            alpha=1.0 if kept else FADED,
            zorder=5,
        )

    fx, fy, fw, fh = lay.frame
    ax.add_patch(
        FancyBboxPatch(
            (fx, fy),
            fw,
            fh,
            boxstyle=shape,
            facecolor="none",
            edgecolor="dimgrey",
            linewidth=2,
            linestyle="dashed",
            zorder=1,
        )
    )
    mid_x = fx + fw / 2
    ax.text(mid_x, 7.0, OFFER_TITLE, ha="center", fontsize=title_font, fontweight="bold")
    ax.text(mid_x, 6.45, OFFER_NOTE, ha="center", fontsize=body_font, style="italic")
    for name, y in zip(offer, OFFER_Y, strict=True):
        face = colour_of(name)
        box(offer_x, y, offer_w, BOX_H, name, face, "none")
        ax.text(
            offer_x + offer_w / 2,
            y,
            f"{contexts[name].label}\n{contexts[name].result}",
            ha="center",
            va="center",
            fontsize=body_font,
            color=label_ink(face),
            alpha=alpha(name),
            zorder=4,
        )

    order = shell[0]
    face = colour_of(order)
    ink = label_ink(face)
    box(shell_x0, MID_Y, shell_w, 4.8, order, face, "none")
    shell_x = shell_x0 + shell_w / 2
    for dy, text, size, how in (
        (1.8, SHELL_TITLE, title_font, "bold"),
        (1.25, SHELL_NOTE, body_font, "normal"),
    ):
        ax.text(
            shell_x,
            MID_Y + dy,
            text,
            ha="center",
            va="center",
            fontsize=size,
            fontweight=how,
            style="italic" if how == "normal" else "normal",
            color=ink,
            alpha=alpha(order),
            zorder=4,
        )
    for i, step in enumerate(("reserve", "charge", "confirm")):
        ax.text(
            shell_x0 + 0.7,
            MID_Y + 0.35 - i * 0.65,
            f"{i + 1}. {step}",
            ha="left",
            va="center",
            fontsize=body_font + 2,
            color=ink,
            alpha=alpha(order),
            zorder=4,
        )

    arrow(0.1, fx - 0.05, MID_Y, offer, "Request")
    arrow(fx + fw + 0.05, shell_x0 - 0.05, MID_Y, (*offer, order), CORE_CONTRACT)
    ax.text(
        provider_x + provider_w / 2, 7.0, OUTSIDE_TITLE, ha="center", fontsize=title_font,
        fontweight="bold",
    )  # fmt: skip
    generic = kind_style("generic")
    for name, y in zip(providers, PROVIDER_Y, strict=True):
        actor = next(a for a in actors.values() if a.context == name)
        box(provider_x, y, provider_w, BOX_H, name, generic.face, generic.edge)
        if font is not None:
            ax.text(
                provider_x + 0.6,
                y,
                glyph(actor.icon, FONT_AWESOME),
                ha="center",
                va="center",
                fontproperties=FontProperties(fname=font, size=24),
                color="black",
                alpha=alpha(name),
                zorder=4,
            )
        ax.text(
            provider_x + (1.0 if font is not None else 0.0) + 0.1,
            y,
            actor.label.replace(" ", "\n", 1),
            ha="left" if font is not None else "center",
            va="center",
            fontsize=body_font,
            fontweight="bold",
            color="black",
            alpha=alpha(name),
            zorder=4,
        )
        arrow(
            shell_x0 + shell_w + 0.1,
            provider_x - 0.1,
            y,
            (order, name),
            contract_of(name).replace(" | ", " |\n"),
        )
    ax.set_xlim(0, lay.xmax)
    ax.set_ylim(0, 7.7)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
