# 04-what: complicated on the What

Beat: agreement comes from one language; bounded contexts put each bit in exactly one
place; contracts between contexts are values, never flags.

| | |
|---|---|
| Minutes | 5.5 |
| Footer counter | stays at `512`; the chaos function is untouched, the bits only got names |
| Owns | `s04_what/money.py`, `pricing.py` (b0 b1), `shipping.py` (b2 b3 b4), `tax.py` (b5); `tests/` with one test per green card of these contexts |
| Uses | `data/rules.csv` through the shared `build/data/rules.txt` (the glossary slide) |
| Produces | nothing; no `section.mk` |
| Downstream | 05 and 06 import this package. Never import 05 or 06 from here. |

## Slides

- [x] The dispute closes: `snippet=coupon`, `snippet=fee`, the takeaway "Values, never flags"
- [x] A bit as a type: `snippet=zone`
- [x] Bounded contexts: every bit has a home
- [x] Bounded contexts, the moves: the contract line under moves.png, glued to the frame

## Live

Delete the `INTERNATIONAL` case in `base_fee` and run `uv run pyright`: the type checker
counts the bit. Put it back.

## Done when

- Given the contexts' tests, when run, then each green card of b0..b5 in `data/examples.csv`
  has a passing test here or in 06.
- Given `shipping_fee`, when read, then no parameter is a flag about another context.

## Open

- Physical vs digital lines as a second sum type (gift wrap on a digital-only order is an
  illegal state). Adds a slide; cut if over time.
- `Money` is a type alias over `Decimal`; a proper value class is a Friday post.
