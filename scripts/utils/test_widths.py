"""too_wide: the included lines wider than the column they sit in."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.utils.widths import read_include, too_wide

SLIDE = """## Beside a figure

:::: columns
::: {.column width="50%"}
```{.python include=a.py}
```
:::
::: {.column width="50%"}
![](x.png)
:::
::::
"""


@pytest.mark.edge
def test_read_include_fails_on_a_missing_file_when_strict(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match=r"missing\.txt"):
        read_include(tmp_path, "missing.txt", strict=True)


@pytest.mark.view
def test_too_wide_measures_a_line_without_its_step_marker() -> None:
    texts = {"a.py": "x" * 52 + "  # [step: 3]\n"}
    assert too_wide(SLIDE, texts.__getitem__, 104) == ()


@pytest.mark.view
def test_too_wide_budgets_a_text_block_at_the_exhibit_size() -> None:
    texts = {"a.py": "short\n" + "x" * 60 + "\n"}
    slide = SLIDE.replace("{.python include=a.py}", "{.text include=a.py}")
    assert too_wide(slide, texts.__getitem__, 104) == (
        f"index.md Beside a figure: 60 > 59: {'x' * 60}",
    )


@pytest.mark.view
def test_too_wide_budgets_a_code_block_at_the_snippet_size() -> None:
    texts = {"a.py": "x" * 80 + "\n"}
    assert too_wide(SLIDE, texts.__getitem__, 104) == ()


@pytest.mark.view
def test_a_classless_include_is_measured_at_body_size() -> None:
    texts = {"a.py": "x" * 53 + "\n"}
    slide = SLIDE.replace("{.python include=a.py}", "{include=a.py}")
    assert too_wide(slide, texts.__getitem__, 104) == (
        f"index.md Beside a figure: 53 > 52: {'x' * 53}",
    )


@pytest.mark.view
def test_a_quoted_dot_word_does_not_make_an_include_classed() -> None:
    texts = {"a.py": "x" * 60 + "\n"}
    slide = SLIDE.replace("{.python include=a.py}", '{heading="run it, then .x" include=a.py}')
    assert too_wide(slide, texts.__getitem__, 104) == (
        f"index.md Beside a figure: 60 > 52: {'x' * 60}",
    )


@pytest.mark.view
def test_too_wide_names_a_line_past_its_column() -> None:
    texts = {"a.py": "short\n" + "x" * 90 + "\n"}
    assert too_wide(SLIDE, texts.__getitem__, 104) == (
        f"index.md Beside a figure: 90 > 83: {'x' * 90}",
    )
