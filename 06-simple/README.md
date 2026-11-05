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

Six frames, each with speaker notes.

- [x] We calculate the offer without carrying out the order: `build/06-simple/responsibilities.png` beside `snippet=price` (core.py), the caption "this has a name: functional core, imperative shell -- the team exercises pricing without ..."
- [x] Agreed promises now have concrete examples and traceable evidence: `build/06-simple/row-b2.png` (the free-shipping row with its evidence), `build/06-simple/cards.txt` (I1, I2, I3) and `build/data/splits.txt`, the counter reveals 72
- [x] A pricing change to 15% leaves the shipping code unchanged: the change rehearsal, the member discount diff on the muted pictures, then `snippet=crossing` (`tests/test_member15.py`): the 57 EUR member order ships free at 10% and pays 5 at 15%
- [x] A stable payment contract lets us replace the provider: the change rehearsal, the gateway swap on the muted pictures
- [x] Digital-only orders add one delivery-charge rule to shipping: a fourth bit: the seventh request, dated week 15 of the shop's calendar and narrowed to the delivery-charge rule for a digital-only order, run RED (`seventh-red.txt`: the agreed example against the shipped fee, a strict xfail in `tests/test_seventh.py`) then GREEN (`seventh-green.txt`) beside `seventh.diff`
- [x] The next if starts with ownership and discovery: the closing frame, ending on the 06 line

## Live

`uv run pytest 06-simple/tests -q`: 64 + 11 + 13 tests in well under a second. Then show
`git grep -n "if " 06-simple/s06_simple/shell.py` returning nothing.

## Done when

- Given `test_core_paths.py`, when run, then 64 parametrized cases pass with ids `000000`..`111111`.
- Given `data/examples.csv`, when a `name` has no `test_<name>` here, then
  `test_every_*_example_has_a_test` fails and names it.
- Given the eight fake configurations, when the stock is gone, then the gateway was never called.

## Open

- The epilogue arithmetic (512 -> 1024, +64, +8) moved to the 13th frame of 08-backup.
- Compensation (release the reservation on a declined payment): a bit in the shell, a
  Friday post, not a slide.
- Hypothesis for the core instead of `range(64)`: same count, stronger invariants.
