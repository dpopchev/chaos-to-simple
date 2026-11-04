# 06-simple: functional core, imperative shell

Beat: the responsibilities make a change safer. Calculate the offer apart from carrying
out the order, then the evidence the business recognizes: 64 core paths, 8 shell worlds,
72 to reason about instead of 512.

| | |
|---|---|
| Minutes | 8 |
| Footer counter | `512` on entry, `72` on the last slide |
| Owns | `s06_simple/core.py` (`Request`, `Priced`, `price`), `shell.py` (`checkout`, `Accepted | Rejected`), `worlds.py` (`world`, `rows`, `table`: the measured eight worlds), `tests/` (64 paths, 10 green cards, 8 worlds, 4 shell cards) |
| Uses | `s04_what` (the contexts), `s05_how` (ports and fakes), `data/examples.csv` (test names are pinned to it) |
| Produces | `build/06-simple/responsibilities.png`, `price.txt`, `cards.txt`, `seventh.diff`, `build/data/splits.txt` via `section.mk`; the five mechanism frames (Request / Priced, 192 tests, eight worlds, ifs and imports, 512 to 72 chart) sit in 08-backup |

## Slides

Four planned frames (W-193 writes the first two, W-194 the rest), each with speaker notes.

- [x] The offer: `build/06-simple/responsibilities.png` beside `snippet=price` (core.py), the line "the team can discuss and exercise pricing without ..."
- [x] The evidence: `build/06-simple/cards.txt` (I1, I2, I3) and `build/data/splits.txt`, the counter reveals 72
- [ ] The seventh if, rewritten by W-194
- [ ] The close, by W-194

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
