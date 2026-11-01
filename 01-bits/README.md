# 01-bits: six if statements, 64 paths

## Beat

It looks tested, it is not. Two tests reach 100% branch coverage of a function with 64
execution paths, and a bug sits on one of the other 62. The protagonist is past me: the
only backend developer at a small nameless online bookshop, wanting to ship the autumn
campaign on time, one if at a time.

## Minutes

9

## Footer counter

`?` on entry, `64` from the "Count along: one if, one bit" slide on.

## Owns

- `s01_bits/chaos.py`: the exhibit, the checkout as past me left it
- `s01_bits/two_ifs.py`: the two-ifs zoom-in
- `tests/test_chaos.py`: two deceptive tests and the planted bug, xfail strict
- `tests/test_two_ifs.py`: the same two tests against the two-ifs zoom-in
- `index.md`: the nine slides

## Uses

- `data/cast.csv` (the six requests and their words), rendered to `build/01-bits/cast.txt`
- `data/incident.txt` (finance report of incident I1)
- nothing else outside this directory; this stage of the example is standalone on purpose

## Produces

- `build/01-bits/cast.txt`: the cast table beside the checkout
- `build/01-bits/coverage.txt`: the two tests under branch coverage
- `build/01-bits/two_ifs.txt`: the two-ifs zoom-in under branch coverage
- `build/01-bits/grid.txt`: the 64 six-bit path strings

## Slides

- [x] 1. The checkout as found: `snippet=checkout` beside the cast
- [x] 2. Two tests. Coverage says 100%: `snippet=two-tests` and the coverage report
- [x] 3. Finance found it, not the tests: incident I1
- [x] 4. One of the other sixty-two: `snippet=bug`, run live
- [x] 5. Four paths, the same two tests: `snippet=ship`, `snippet=ship-tests`, two-ifs report
- [x] 6. Count along: one if, one bit, to 64 (`{paths=64}`)
- [x] 7. A path is a six-bit number: the grid
- [x] 8. Rule 1: how ifs count
- [x] 9. Parked for section 03, with the line glued at its foot (`\theline`)

## Live

1. `make test K=test_chaos`: 2 passed, 1 xfailed.
2. `uv run pytest 01-bits/tests -k free_shipping_after_discount --runxfail`: the assertion
   shows 54.00 against 60.00.

## Done when

- Given the two `test_chaos` tests, when run under branch coverage, then the report says 100%.
- Given the planted bug test, when run normally, then the suite is green (xfail) and
  `--runxfail` shows 54.00 against 60.00.
- Given the grid slide, when shown, then 000000 and 111111 can be pointed at.
- Given `index.md`, when counted, then it holds nine `## ` slides.

## Open

- Whether to add the one-line conditional (`x if c else y`) as a seventh, invisible bit.
- Keep `qty` on `Line` or drop it; it is not a decision, only noise.
