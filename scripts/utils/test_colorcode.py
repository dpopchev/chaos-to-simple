"""Tests for the colour-coded checkout: line owners and the drawn frame."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.colorcode import (
    OwnedLine,
    chip_label,
    colorcode,
    legend_groups,
    owned_lines,
)
from scripts.utils.palette import load_actors, load_contexts
from scripts.utils.paths import load_cast, load_rules

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _lines() -> tuple[OwnedLine, ...]:
    source = (ROOT / "01-bits/s01_bits/chaos.py").read_text(encoding="ascii")
    return owned_lines(source, load_cast(DATA / "cast.csv"), load_rules(DATA / "rules.csv"))


def _by_text(start: str) -> OwnedLine:
    return next(line for line in _lines() if line.text.lstrip().startswith(start))


@pytest.mark.edge
def test_owned_lines_cover_the_whole_checkout_snippet() -> None:
    assert len(_lines()) == 23


@pytest.mark.model
def test_a_marked_line_has_no_step_marker_left() -> None:
    assert not any("[step:" in line.text for line in _lines())


@pytest.mark.model
def test_the_coupon_line_belongs_to_marketing() -> None:
    assert _by_text("if order.coupon_valid_until").owner == "marketing"


@pytest.mark.model
def test_the_member_line_is_in_the_pricing_context() -> None:
    assert _by_text("if order.member").context == "pricing"


@pytest.mark.model
def test_the_charge_call_belongs_to_the_payment_provider() -> None:
    assert _by_text("charge(total)").owner == "payment"


@pytest.mark.model
def test_the_charge_call_is_in_fulfilment() -> None:
    assert _by_text("charge(total)").context == "fulfilment"


@pytest.mark.model
def test_a_skeleton_line_has_no_context() -> None:
    assert _by_text("total = goods + shipping").context is None


@pytest.mark.edge
def test_colorcode_writes_a_png(tmp_path: Path) -> None:
    out = colorcode(_lines(), load_actors(), load_contexts(), tmp_path / "x" / "c.png")
    assert out.read_bytes().startswith(PNG_MAGIC)


@pytest.mark.model
def test_legend_groups_actors_and_contexts() -> None:
    groups = legend_groups(load_actors(), load_contexts())
    assert {heading: keys for heading, keys in groups} == {
        "who asked": ("customer", "marketing", "loyalty", "logistics", "accounting"),
        "home": ("pricing", "shipping", "fulfilment", "tax"),
        "the ports (generic, external teams)": ("payment", "warehouse", "mailer"),
    }


@pytest.mark.model
def test_ports_chips_carry_no_kind() -> None:
    actors, contexts = load_actors(), load_contexts()
    ports = dict(legend_groups(actors, contexts))["the ports (generic, external teams)"]
    labels = [chip_label(key, actors, contexts) for key in ports]
    assert not any("(" in label for label in labels)


@pytest.mark.model
def test_legend_names_the_kinds() -> None:
    actors, contexts = load_actors(), load_contexts()
    home = dict(legend_groups(actors, contexts))["home"]
    labels = [chip_label(key, actors, contexts) for key in home]
    assert [label.rsplit("(", 1)[1] for label in labels] == [
        "core)",
        "supporting)",
        "supporting)",
        "generic)",
    ]
