# scripts: tested helpers the build calls

Thin command-line entry points at the top, logic in `utils/`, tests in `tests/`.
Nothing here knows about a particular section; a section calls these from its
`section.mk` with its own paths.

| Entry point | Logic | Used by |
|---|---|---|
| `python -m scripts.paths rules\|counts\|grid\|chart` | `utils/paths.py` | Makefile (`build/data/*.txt`), `01-bits/section.mk` (grid), `06-simple/section.mk` (chart) |
| `python -m scripts.check_ascii` | `utils/ascii_check.py` | `make ascii` |
| (library only) | `utils/examples.py` | `06-simple/tests` to pin test names to `data/examples.csv` |

Rules: pure functions in `utils/`, I/O at the edges, every `utils` module has a test
file, tests use `tmp_path` and never touch `build/`.
