# 05-how: complicated on the How

Beat: the broken promise, who decides, then the code's own decisions, and where multiplication
hides. Coupling is a flag across a boundary (x), cohesion keeps bits that change together in one
place (+), mutable state adds bits nobody wrote down, and Command Query Separation draws the seam
between the pure core and the effectful shell.

| | |
|---|---|
| Minutes | 6 |
| Footer counter | stays at `512`; the seam is drawn, nothing is on either side yet |
| Owns | `data/promise.csv`, `data/bubbles.csv`, the promise and policies artifacts (`build/05-how/promise.png`, `policies.txt`, `bubble-0.txt`, `bubble-1.txt`), `s05_how/oo_checkout.py` (the counter-example), `ports.py` (result sum types and Protocols), `fakes.py` (test doubles, one bit each), `warehouse_adapter.py` (the adapter behind Reserved | OutOfStock), `build/05-how/cohesion.png`, `tests/` |
| Uses | `s04_what` (Money, Coupon, the constants). Upstream only: 04 never imports this. |
| Produces | `build/05-how/imports.txt` and `pyright.txt` |
| Downstream | 06 imports `ports` and `fakes` |

## Slides

- [x] The promise: `data/incident.txt`, `build/05-how/promise.png`, the I3 run line as evidence
  ('the red test, as evidence: reserve before charge (q5)'), thread 1
- [x] The policies: `build/05-how/policies.txt` and the Support and Fulfilment bubbles, the open
  question on releasing a reservation after a declined payment, thread 2
- [x] Cohesion: the rule cards grouped by the business question each answers
  (`build/05-how/cohesion.png`), thread 3
- [x] The boundary: the warehouse adapter snippet beside the seam picture with the shell
  (`build/05-how/ports.png`), thread 4, and the 05 line
- [x] The v5 seam frame and the Protocol-and-fakes frame live in 08-backup

## Live

`make test K=TestCallOrder`: 45 against 44 from the same inputs, one test per order.
`make test K=warehouse_adapter`: the adapter turns the warehouse's JSON into Reserved | OutOfStock.

## Done when

- Given the OO checkout, when the two methods are called in both orders, then the totals
  differ and the test says which one the rule wants.
- Given the deck, when `make talk lines` runs, then 05 shows the cohesion and boundary frames
  and ends on the line 'A boundary is an agreement about what the other side must know'.
- Given the ports, when the fakes are assigned to the Protocol types, then pyright accepts
  them without inheritance.

## Open

- Exceptions as a fourth, invisible answer (`except Exception` in the chaos code): one
  slide or a Friday post.
- Whether to show `functools.partial` / closures as the FP answer to constructor state.
