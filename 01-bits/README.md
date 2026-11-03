# 01-bits: six if statements, 64 paths

## Beat

It looks tested, it is not. Two tests reach 100% branch coverage of a function with 64
execution paths, and a bug sits on one of the other 62. The protagonist is past me: the
only backend developer at a small nameless online bookshop, wanting to ship the autumn
campaign on time, one if at a time.

## Minutes

12

## Footer counter

`?` on the opening "A policy is one bit" slide, then `1`, `2`, `4` .. `64` on the seven policy slides.

## Owns

- `s01_bits/chaos.py`: the exhibit, the checkout as past me left it
- `s01_bits/two_ifs.py`: the two-ifs zoom-in
- `tests/test_chaos.py`: the two deceptive tests, green
- `tests/test_planted_bug.py`: the planted bug, xfail strict, in a file of its own
- `tests/test_two_ifs.py`: the same two tests against the two-ifs zoom-in
- `data/october.csv`: the four October weeks of expected and received shipping income
- `tests/test_october.py`: pins its totals, 1,214 free orders and 6,070 EUR, and its calendar
- `index.md`: the thirteen slides

## Uses

- `data/bubbles.csv` (the nine bubbles) and `data/cast.csv` (the six requests and their words)
- `data/incident.txt` (finance report of incident I1)
- nothing else outside this directory; this stage of the example is standalone on purpose

## Produces

- `build/01-bits/step-0.diff` .. `step-6.diff`: the whole skeleton, then each request as a
  compact `+`/`-` diff (one context line, `---` between hunks)
- `build/01-bits/test-0.diff` .. `test-6.diff`: the two tests whole at v0, then each step's
  change to them as a compact `+`/`-` diff, shown under the request's bubble
- `build/01-bits/tally-0.txt` .. `tally-6.txt`: the tally line over each step, with the
  function length in lines
- `build/01-bits/bubble-0.txt` .. `bubble-8.txt`: the actor, the date and the words of each
  request, from `data/bubbles.csv`
- `build/01-bits/coverage.txt`: the two tests under branch coverage
- `build/01-bits/two_ifs.txt`: the two-ifs zoom-in under branch coverage
- `build/01-bits/grid.txt`: the 64 six-bit path strings

## Slides

- [x] 1. A policy is one bit, paths=?: the rule paths = 2^policies, the three counting lines, "the footer counts from here"
- [x] 2. No policy yet, paths=1: the customer's bubble full width, then `step-0.diff` beside `test-0.diff`
- [x] 3. Policy 1, paths=2: marketing's AUTUMN coupon, `tally-1.txt` over `step-1.diff`
- [x] 4. Policy 2, paths=4: the loyalty program's member discount, `tally-2.txt` over `step-2.diff`
- [x] 5. Policy 3, paths=8: free shipping from 50 EUR, `tally-3.txt` over `step-3.diff`
- [x] 6. Policy 4, paths=16: shipping abroad at 20 EUR, `tally-4.txt` over `step-4.diff`
- [x] 7. Policy 5, paths=32: gift wrap at 3 EUR, `tally-5.txt` over `step-5.diff`
- [x] 8. Policy 6, paths=64: the VAT ID rule, the accounting bubble beside `tally-6.txt` over `step-6.diff`
- [x] 9. Checkout done, paths=64: the dev and marketing bubbles over the question "How many tests would make you sure?"
- [x] 10. Two tests, coverage says 100%, paths=64: the two `test_chaos` tests beside `coverage-view.png`, `coverage-summary.txt` as the caption
- [x] 11. Finance found it, paths=64: `finance.png` titled with the October totals, marketing's squeeze bubble as the last line
- [x] 12. The path nobody ran, paths=64: the `bug` snippet of `test_planted_bug.py`, run live with `--runxfail`
- [x] 13. A path is a six-bit number, paths=64: `grid.png` beside `doubling.png`, the three counting lines, the `\theline`
- [x] 14. Four orders the memo implies, paths=64: the `memo-orders` snippet of `test_memo_orders.py` beside `memo-run.txt` (three passed, the coupon order at 55 EUR failed)

## Live

1. `make test K=test_chaos`: 2 passed; `build/01-bits/coverage.txt` runs
   `01-bits/tests/test_chaos.py` over `s01_bits.chaos`: 2 passed, nothing deselected.
2. `make test K=test_planted_bug`: 1 xfailed.
3. `uv run pytest 01-bits/tests/test_planted_bug.py --runxfail`: the assertion
   shows 54.00 against 60.00.
4. `make test K=TestMemoOrders`: 3 passed, 1 xfailed.

## Done when

- Given the two `test_chaos` tests, when run under branch coverage, then the report says 2 passed and
  `chaos.py` at 100%; `coverage-summary.txt` keeps both lines.
- Given the planted bug test in `test_planted_bug.py`, when run normally, then the suite is green (xfail) and
  `--runxfail` shows 54.00 against 60.00.
- Given the grid slide, when shown, then 000000 and 111111 can be pointed at.
- Given `index.md`, when counted, then it holds thirteen `## ` slides.

## Open

- Whether to add the one-line conditional (`x if c else y`) as a seventh, invisible bit.
- Keep `qty` on `Line` or drop it; it is not a decision, only noise.
