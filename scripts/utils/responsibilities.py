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
TITLE_FONT, BODY_FONT = 16, 14
BOX_H = 1.3
FRAME = (1.8, 0.5, 4.4, 7.1)
OFFER_X, OFFER_W = 2.0, 4.0
SHELL_X, SHELL_W = 8.2, 4.4
PROVIDER_X, PROVIDER_W = 15.6, 3.6
OFFER_Y = (5.0, 3.35, 1.7)
PROVIDER_Y = (5.6, 3.6, 1.6)
MID_Y = 3.6


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


def draw(out: Path, highlight: str | None = None) -> Path:
    """Draw the picture; with a highlight every other box and arrow fades and its arrows go bold."""
    style.apply()
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    from matplotlib.patches import FancyBboxPatch

    offer, shell, providers = groups()
    contexts, actors = load_contexts(), load_actors()
    faded = muted(highlight)
    shape = "round,pad=0.05,rounding_size=0.15"
    font = icon_file()
    fig, ax = plt.subplots(figsize=(15.4, 6.4), dpi=style.DPI)

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
            fontsize=BODY_FONT,
            style="italic",
            fontweight="bold" if bold else "normal",
            alpha=1.0 if kept else FADED,
            zorder=5,
        )

    fx, fy, fw, fh = FRAME
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
    ax.text(mid_x, 7.0, OFFER_TITLE, ha="center", fontsize=TITLE_FONT, fontweight="bold")
    ax.text(mid_x, 6.45, OFFER_NOTE, ha="center", fontsize=BODY_FONT, style="italic")
    for name, y in zip(offer, OFFER_Y, strict=True):
        face = colour_of(name)
        box(OFFER_X, y, OFFER_W, BOX_H, name, face, "none")
        ax.text(
            OFFER_X + OFFER_W / 2,
            y,
            f"{contexts[name].label}\n{contexts[name].result}",
            ha="center",
            va="center",
            fontsize=BODY_FONT,
            color=label_ink(face),
            alpha=alpha(name),
            zorder=4,
        )

    order = shell[0]
    face = colour_of(order)
    ink = label_ink(face)
    box(SHELL_X, MID_Y, SHELL_W, 4.8, order, face, "none")
    shell_x = SHELL_X + SHELL_W / 2
    for dy, text, size, how in (
        (1.8, SHELL_TITLE, TITLE_FONT, "bold"),
        (1.25, SHELL_NOTE, BODY_FONT, "normal"),
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
            SHELL_X + 0.7,
            MID_Y + 0.35 - i * 0.65,
            f"{i + 1}. {step}",
            ha="left",
            va="center",
            fontsize=BODY_FONT + 2,
            color=ink,
            alpha=alpha(order),
            zorder=4,
        )

    arrow(0.1, fx - 0.05, MID_Y, offer, "Request")
    arrow(fx + fw + 0.05, SHELL_X - 0.05, MID_Y, (*offer, order), CORE_CONTRACT)
    ax.text(
        PROVIDER_X + PROVIDER_W / 2, 7.0, OUTSIDE_TITLE, ha="center", fontsize=TITLE_FONT,
        fontweight="bold",
    )  # fmt: skip
    generic = kind_style("generic")
    for name, y in zip(providers, PROVIDER_Y, strict=True):
        actor = next(a for a in actors.values() if a.context == name)
        box(PROVIDER_X, y, PROVIDER_W, BOX_H, name, generic.face, generic.edge)
        if font is not None:
            ax.text(
                PROVIDER_X + 0.6,
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
            PROVIDER_X + (1.0 if font is not None else 0.0) + 0.1,
            y,
            actor.label.replace(" ", "\n", 1),
            ha="left" if font is not None else "center",
            va="center",
            fontsize=BODY_FONT,
            fontweight="bold",
            color="black",
            alpha=alpha(name),
            zorder=4,
        )
        arrow(
            SHELL_X + SHELL_W + 0.1,
            PROVIDER_X - 0.1,
            y,
            (order, name),
            contract_of(name).replace(" | ", " |\n"),
        )
    ax.set_xlim(0, 19.4)
    ax.set_ylim(0, 7.7)
    ax.axis("off")
    fig.tight_layout()
    style.save(fig, out)
    return out
