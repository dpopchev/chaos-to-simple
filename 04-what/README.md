# 04-what: complicated on the What

Beat: agreement comes from one language; bounded contexts put each bit in exactly one
place; contracts between contexts are values, never flags.

| | |
|---|---|
| Minutes | 5.5 |
| Footer counter | stays at `512`; the chaos function is untouched, the bits only got names |
| Owns | `s04_what/money.py`, `pricing.py` (b0 b1), `shipping.py` (b2 b3 b4), `tax.py` (b5); `tests/` with one test per green card of these contexts |
| Uses | `data/rules.csv` through the shared `build/data/rules.txt` (the glossary slide) |
| Produces | `build/04-what/*` through `section.mk` (`dispute.txt`: the q3 card) |
| Downstream | 05 and 06 import this package. Never import 05 or 06 from here. |

## Slides

- [x] Tracing each line to who asked for it reveals candidate policy boundaries: the color-coded ifs, `colorcode.png`, legend headed 'who asked' and 'home'
- [x] Reading the discounted goods, not the cart, fixes the 55 EUR coupon order: the first fix, `fix.diff`, captioned 'one name: discounted goods, a value pricing returns -- the first boundary'
- [x] Shipping owns eligibility and applies the threshold to the discounted goods: the dispute closes, `dispute.txt` (the q3 card), `snippet=fee`, captioned 'the rule belongs to shipping, Zone is a sum type: the checker counts that bit'; the Live demo sits in its notes (no Zone frame)
- [x] Checkout delegates its calculations to pricing, shipping and tax, effects still inline: `checkout_v4.py` `snippet=checkout` as plain code under 'checkout_fixed.py -> checkout_v4.py', beside the four context lines with faces
- [x] The map gives all nine decisions a home: 2 core, 6 supporting, 1 generic: the bounded contexts, the moves, the contract line under moves.png, glued to the frame

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
