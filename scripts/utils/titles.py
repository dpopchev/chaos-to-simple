"""The title gate: name each frame title with fewer words than an action title needs."""

from __future__ import annotations

import re

_FRAME = re.compile(r"^## (?P<title>.*?)(?: \{paths=[?\d]+\})?\s*$")


def too_short(index_md: str, minimum: int = 8) -> tuple[str, ...]:
    """Return the `## ` titles of an index with fewer words than the minimum, in order.

    The `{paths=N}` attribute is not part of the title; `# ` section titles are not frames.
    """
    titles = (m.group("title") for line in index_md.splitlines() if (m := _FRAME.match(line)))
    return tuple(title for title in titles if len(title.split()) < minimum)
