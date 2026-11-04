# 05-how: complicated on the How

Beat: the broken promise, who decides, then the code's own decisions, and where multiplication
hides. Coupling is a flag across a boundary (x), cohesion keeps bits that change together in one
place (+), mutable state adds bits nobody wrote down, and Command Query Separation draws the seam
between the pure core and the effectful shell.

| | |
|---|---|
| Minutes | 6 |
| Footer counter | stays at `512`; the seam is drawn, nothing is on either side yet |
| Owns | `data/promise.csv`, `data/bubbles.csv`, the promise and policies artifacts (`build/05-how/promise.png`, `policies.txt`, `bubble-0.txt`, `bubble-1.txt`), `s05_how/oo_checkout.py` (the counter-example), `ports.py` (result sum types and Protocols), `fakes.py` (test doubles, one bit each), `tests/` |
| Uses | `s04_what` (Money, Coupon, the constants). Upstream only: 04 never imports this. |
| Produces | `build/05-how/imports.txt` and `pyright.txt` |
| Downstream | 06 imports `ports` and `fakes` |

## Slides

- [x] The promise: `data/incident.txt`, `build/05-how/promise.png`, the I3 run line as evidence
  ('the red test, as evidence: reserve before charge (q5)'), thread 1
- [x] The policies: `build/05-how/policies.txt` and the Support and Fulfilment bubbles, the open
  question on releasing a reservation after a declined payment, thread 2
- [ ] The seam: each effect answers with a value, reserve first (`build/05-how/ports.png`, v5 diff)
- [ ] The contract: a Protocol per port and the fakes over the pyright line that accepts them

## Live

`make test K=TestCallOrder`: 45 against 44 from the same inputs, one test per order.

## Done when

- Given the OO checkout, when the two methods are called in both orders, then the totals
  differ and the test says which one the rule wants.
- Given the ports, when the fakes are assigned to the Protocol types, then pyright accepts
  them without inheritance.

## Open

- Exceptions as a fourth, invisible answer (`except Exception` in the chaos code): one
  slide or a Friday post.
- Whether to show `functools.partial` / closures as the FP answer to constructor state.
