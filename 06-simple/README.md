# 06-simple: functional core, imperative shell

Beat: put the bits where they belong, count again. 64 core paths tested by enumeration,
8 shell configurations tested with fakes, 72 to reason about instead of 512.

| | |
|---|---|
| Minutes | 8 |
| Footer counter | `512` on entry, `72` on the last slide |
| Owns | `s06_simple/core.py` (`Request`, `Priced`, `price`), `shell.py` (`checkout`, `Accepted | Rejected`), `tests/` (64 paths, 10 green cards, 8 worlds, 4 shell cards) |
| Uses | `s04_what` (the contexts), `s05_how` (ports and fakes), `data/examples.csv` (test names are pinned to it) |
| Produces | `build/06-simple/pytest.txt`, `build/06-simple/paths.png` (stacked bar: 512, 64 + 8, 4 + 8 + 2 + 8) via `section.mk` |

## Slides

- [x] The core: `snippet=price`
- [x] Sixty-four paths, one test each: `snippet=from-bits`
- [x] We counted them: `build/06-simple/pytest.txt`
- [x] The shell: `snippet=checkout`
- [x] Eight worlds, four outcomes: `snippet=eight`
- [x] The wounds close by name: `snippet=wound-i1`, `snippet=wound-i3`, `build/06-simple/wounds.txt`
- [x] The number: the chart, `build/data/splits.txt` and the line "No decision is ever deleted, only moved"
- [x] Epilogue: marketing's seventh if, in two columns; the glued line sits under them

## Live

`uv run pytest 06-simple/tests -q`: 64 + 11 + 13 tests in well under a second. Then show
`git grep -n "if " 06-simple/s06_simple/shell.py` returning nothing.

## Done when

- Given `test_core_paths.py`, when run, then 64 parametrized cases pass with ids `000000`..`111111`.
- Given `data/examples.csv`, when a `name` has no `test_<name>` here, then
  `test_every_*_example_has_a_test` fails and names it.
- Given the eight fake configurations, when the stock is gone, then the gateway was never called.

## Open

- Compensation (release the reservation on a declined payment): a bit in the shell, a
  Friday post, not a slide.
- Hypothesis for the core instead of `range(64)`: same count, stronger invariants.
