# 01-bits: six if statements, 64 paths

Beat: it looks tested, it is not. Two tests reach 100% branch coverage of a function
with 64 execution paths, and a bug sits on one of the other 62.

| | |
|---|---|
| Minutes | 8 |
| Footer counter | `?` on entry, `64` from the "Three numbers" slide |
| Owns | `s01_bits/chaos.py` (the exhibit), `tests/test_chaos.py` (two deceptive tests and the planted bug, xfail strict) |
| Uses | nothing outside this directory; this stage of the example is standalone on purpose |
| Produces | `build/01-bits/coverage.txt` (the two tests under branch coverage), `build/01-bits/grid.txt` (64 bit strings) via `section.mk` |

## Slides

- [x] The checkout as found: `snippet=checkout`
- [x] Two tests: `snippet=two-tests`
- [x] The report, as measured by the build
- [x] Three numbers: tests 2, branch coverage 100%, cyclomatic 7, paths 64
- [x] A path is a six-bit number: the grid
- [x] One of the other sixty-two: `snippet=bug`, run live
- [x] Rule 1: how ifs count

## Live

1. `uv run pytest 01-bits/tests -k all_flags --cov=s01_bits --cov-branch` in a terminal: 2 passed, 100%.
2. `uv run pytest 01-bits/tests -k threshold --runxfail`: the assertion shows 54.00 against 60.00.

## Done when

- Given the two `all_flags` tests, when run under branch coverage, then the report says 100%.
- Given the planted bug test, when run normally, then the suite is green (xfail) and
  `--runxfail` shows 54.00 against 60.00.
- Given the grid slide, when shown, then 000000 and 111111 can be pointed at.

## Open

- Whether to add the one-line conditional (`x if c else y`) as a seventh, invisible bit.
- Keep `qty` on `Line` or drop it; it is not a decision, only noise.
