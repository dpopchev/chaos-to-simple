# 05-how: complicated on the How

Beat: the code's own decisions, and where multiplication hides. Coupling is a flag across
a boundary (x), cohesion keeps bits that change together in one place (+), mutable state
adds bits nobody wrote down, and Command Query Separation draws the seam between the
pure core and the effectful shell.

| | |
|---|---|
| Minutes | 8 |
| Footer counter | stays at `512`; the seam is drawn, nothing is on either side yet |
| Owns | `s05_how/oo_checkout.py` (the counter-example), `ports.py` (result sum types and Protocols), `fakes.py` (test doubles, one bit each), `tests/` |
| Uses | `s04_what` (Money, Coupon, the constants). Upstream only: 04 never imports this. |
| Produces | nothing; no `section.mk` |
| Downstream | 06 imports `ports` and `fakes` |

## Slides

- [x] Coupling multiplies, cohesion adds: the refrain
- [x] Object with a mutable total: `snippet=oo`
- [x] The bit nobody wrote down: `snippet=order-bit`
- [x] Command Query Separation draws the seam
- [x] The answers the world may give: `snippet=results`
- [x] The ports: `snippet=ports`
- [x] Refactoring moves and their sign, with the line glued at its foot

## Live

`uv run pytest 05-how/tests -k order -v`: 45 against 44 from the same inputs.

## Done when

- Given the OO checkout, when the two methods are called in both orders, then the totals
  differ and the test says which one the rule wants.
- Given the ports, when the fakes are assigned to the Protocol types, then pyright accepts
  them without inheritance.

## Open

- Exceptions as a fourth, invisible answer (`except Exception` in the chaos code): one
  slide or a Friday post.
- Whether to show `functools.partial` / closures as the FP answer to constructor state.
