"""too_wide: the included lines wider than the column they sit in."""

from __future__ import annotations

import pytest

from scripts.utils.widths import too_wide

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


@pytest.mark.view
def test_too_wide_names_a_line_past_its_column() -> None:
    texts = {"a.py": "short\n" + "x" * 60 + "\n"}
    assert too_wide(SLIDE, texts.__getitem__, 104) == (
        f"index.md Beside a figure: 60 > 52: {'x' * 60}",
    )
