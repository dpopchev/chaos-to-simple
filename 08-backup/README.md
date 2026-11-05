# 08-backup: 08 Backup: the mechanisms behind the seam, for the Q&A

Beat: backup frames shown only on request during the Q&A; minutes 0.

| | |
|---|---|
| Minutes | 0 |
| Footer counter | `512` on entry, `512` on exit |
| Owns | the Stacey overview frame (moved from 00) and the sixteen frames of `08-backup/index.md`: the thirteen mechanism frames, six moved from `05-how/index.md` |
| Uses | the artifacts of `05-how/section.mk` and the exhibits under `05-how/`; `data/rules.csv`, `data/questions.csv` and `data/examples.csv` for the board |
| Produces | `build/08-backup/stacey-overview.png`, `build/08-backup/zones.tex`, `build/08-backup/counting.png` and `build/08-backup/board.png` (`section.mk`) |

## Slides

- [x] Six rules add up to 7 for McCabe and multiply to 64 configurations: the sum and the product of the six ifs, moved from 01
- [x] Agreement on the What and certainty on the How guide each move: the Stacey overview with its zone definitions, moved whole from 00
- [x] Changing the call order changes the price: 45 against 44, from the same inputs
- [x] This mutable checkout leaves discount order to its callers: a class hid the call order in its state, the same bug as I3 in pricing
- [x] Explicit outcome values make the three effects easier to handle and match: Command Query Separation draws the seam by making every answer a value
- [x] Protocols accept compatible fakes without inheritance: pyright reports zero errors (a sum type per answer, a Protocol per port, the fakes)
- [x] Stock reservation must succeed before payment is attempted
- [x] Pricing, shipping and tax import no provider port; only the shell does: the import counts, dependencies point inward
- [x] Shipping receives the discounted goods, never pricing's internal choices: the moves table and the shipping_fee contract
- [x] Values carry inputs and results across the calculation boundary: the moves table
- [x] Three invariants check 64 configurations in 192 test cases
- [x] Eight test worlds produce four explicit order outcomes
- [x] Pricing, shipping and tax hold every decision of the functional core, core.py only composes
- [x] The split leaves 72 local paths instead of 512, with integration checked separately
- [x] The seventh decision adds 8 local paths in shipping, against 512 in one function
- [x] Every decision keeps its sentence, home, contract and green test on the board: the completed board, reference for the Q&A

## Done when

- Given the Q&A, when someone asks how the seam is built, then the frame answering it is one page forward from the thank-you.

## Open

- none
