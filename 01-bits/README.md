# 01-bits: six if statements, 64 paths

## Beat

It looks tested, it is not. Two tests reach 100% branch coverage of a function with 64
execution paths, and a bug sits on one of the other 62. The protagonist is past me: the
only backend developer at a small nameless online bookshop, wanting to ship the autumn
campaign on time, one if at a time.

## Minutes

7

## Footer counter

`?` on entry, `64` from the "Count along: one if, one bit" slide on.

## Owns

- `s01_bits/chaos.py`: the exhibit, the checkout as past me left it
- `s01_bits/two_ifs.py`: the two-ifs zoom-in
- `tests/test_chaos.py`: two deceptive tests and the planted bug, xfail strict
- `tests/test_two_ifs.py`: the same two tests against the two-ifs zoom-in
- `data/october.csv`: the four October weeks of expected and received shipping income
- `tests/test_october.py`: pins its totals, 1,214 free orders and 6,070 BGN, and its calendar
- `index.md`: the seven slides

## Uses

- `data/bubbles.csv` (the nine bubbles) and `data/cast.csv` (the six requests and their words)
- `data/incident.txt` (finance report of incident I1)
- nothing else outside this directory; this stage of the example is standalone on purpose

## Produces

- `build/01-bits/step-0.diff` .. `step-6.diff`: the checkout growing one request at a time
- `build/01-bits/bubble-0.txt` .. `bubble-8.txt`: the actor, the date and the words of each
  request, from `data/bubbles.csv`
- `build/01-bits/coverage.txt`: the two tests under branch coverage
- `build/01-bits/two_ifs.txt`: the two-ifs zoom-in under branch coverage
- `build/01-bits/grid.txt`: the 64 six-bit path strings

## Slides

- [x] 1. Step 0, no ifs, paths=1: the customer's bubble over the skeleton diff
- [x] 2. Step 1, one if, paths=2: marketing's AUTUMN coupon, `step-1.diff`
- [x] 3. Step 2, two ifs, paths=4: the loyalty program's member discount, `step-2.diff`
- [x] 4. Step 3, three ifs, paths=8: free shipping from 50 BGN, `step-3.diff`
- [x] 5. Step 4, four ifs, paths=16: shipping abroad at 20 BGN, `step-4.diff`
- [x] 6. Step 5, five ifs, paths=32: gift wrap at 3 BGN, `step-5.diff`
- [x] 7. Step 6, six ifs, paths=64: the VAT ID rule, with the dev and marketing bubbles, `step-6.diff`
- [x] 8. Two tests, coverage says 100%, paths=64: the two `test_chaos` tests beside `coverage-view.png`, `coverage-summary.txt` as the caption

## Live

1. `make test K=test_chaos`: 2 passed, 1 xfailed; `build/01-bits/coverage.txt` runs only
   `test_regular_order` and `test_order_with_everything` over `s01_bits.chaos`: 2 passed.
2. `uv run pytest 01-bits/tests -k free_shipping_after_discount --runxfail`: the assertion
   shows 54.00 against 60.00.

## Done when

- Given the two `test_chaos` tests, when run under branch coverage, then the report says 2 passed and
  `chaos.py` at 100%; `coverage-summary.txt` keeps both lines.
- Given the planted bug test, when run normally, then the suite is green (xfail) and
  `--runxfail` shows 54.00 against 60.00.
- Given the grid slide, when shown, then 000000 and 111111 can be pointed at.
- Given `index.md`, when counted, then it holds seven `## ` slides.

## Open

- Whether to add the one-line conditional (`x if c else y`) as a seventh, invisible bit.
- Keep `qty` on `Line` or drop it; it is not a decision, only noise.
