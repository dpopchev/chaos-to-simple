"""import_rows and import_table: which layer each module imports from, read with ast."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.imports import (
    DecisionRow,
    ImportRow,
    decision_rows,
    import_rows,
    import_table,
)

ROOT = Path(__file__).resolve().parents[2]
CONTEXTS = ("pricing", "shipping", "tax")
CORE = "06-simple/s06_simple/core.py"
SHELL = "06-simple/s06_simple/shell.py"


def _row(source: str) -> ImportRow:
    return import_rows(source, (ROOT / source).read_text(encoding="ascii"))


def _decisions(*sources: str) -> tuple[DecisionRow, ...]:
    return decision_rows(
        [(Path(source).stem, (ROOT / source).read_text(encoding="ascii")) for source in sources]
    )


@pytest.mark.view
def test_import_rows_reads_a_from_import() -> None:
    text = "from s04_what.money import Money, eur\nfrom s05_how.ports import Sent\nimport os\n"
    assert import_rows("x", text) == ImportRow("x", 2, 1, 0)


@pytest.mark.view
def test_import_table_shows_no_context_importing_a_port() -> None:
    contexts = [_row(f"04-what/s04_what/{name}.py") for name in CONTEXTS]
    shell = _row("05-how/s05_how/checkout_v5.py")
    facts = ([row.from_ports for row in contexts], shell.from_contexts > 0, shell.from_ports > 0)
    assert facts == ([0, 0, 0], True, True)


@pytest.mark.view
def test_import_table_aligns_one_row_per_module() -> None:
    table = import_table([ImportRow("tax", 1, 0, 0), ImportRow("checkout_v5", 8, 9, 0)])
    assert table == (
        "module       contexts  ports  core\n"
        "tax                 1      0     0\n"
        "checkout_v5         8      9     0\n"
    )


@pytest.mark.view
def test_shell_has_no_if_and_three_matches() -> None:
    assert _decisions(SHELL) == (DecisionRow("shell", 0, 3),)


@pytest.mark.view
def test_the_six_ifs_live_in_the_three_contexts() -> None:
    sources = [*(f"04-what/s04_what/{name}.py" for name in CONTEXTS), CORE]
    assert [row.ifs for row in _decisions(*sources)] == [2, 2, 1, 0]
