# 05-how: complicated on the How

Beat: the code's own decisions, and where multiplication hides. Coupling is a flag across
a boundary (x), cohesion keeps bits that change together in one place (+), mutable state
adds bits nobody wrote down, and Command Query Separation draws the seam between the
pure core and the effectful shell.

| | |
|---|---|
| Minutes | 6 |
| Footer counter | stays at `512`; the seam is drawn, nothing is on either side yet |
| Owns | `s05_how/oo_checkout.py` (the counter-example), `ports.py` (result sum types and Protocols), `fakes.py` (test doubles, one bit each), `tests/` |
| Uses | `s04_what` (Money, Coupon, the constants). Upstream only: 04 never imports this. |
| Produces | nothing; no `section.mk` |
| Downstream | 06 imports `ports` and `fakes` |

## Slides

- [x] I3: the incident, then the test against `checkout_v4` (`snippet=i3`) over its captured run
  (`build/05-how/i3-run.txt`), captioned 'support raised the flag, the test points at the shell:
  reserve before charge (q5)'
- [x] The bit nobody wrote down: `snippet=order-bit`, the order test before the class
- [x] Past me reached for a class: `snippet=oo`, captioned 'same bug, pricing edition: the order
  hidden in state'
- [x] Command Query Separation draws the seam: two definitions, `snippet=types`, the refrain
- [x] A sum type per answer and a Protocol per port: `snippet=results` beside `snippet=fakes`
  over the pyright line that accepts the fakes (`build/05-how/pyright.txt`)
- [x] The ports, as a picture
- [x] Dependencies point inward: the import counts of `build/05-how/imports.txt`, measured from
  the files
- [x] A boundary that passes values adds paths: the moves table, with the line glued at its foot

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
