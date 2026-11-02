# 03-chaos: from chaos to complex

Beat: you cannot shrink a count you do not know. Domain storytelling and example mapping
find the three bits hiding behind the effects; the honest count is 9 bits, 512 paths.

| | |
|---|---|
| Minutes | 5.5 |
| Footer counter | `64` on entry, `512` from "The honest count" |
| Owns | `data/room.txt` (the room chat log), `data/questions.csv` at the repository root (the six questions) |
| Uses | `data/rules.csv`, `data/examples.csv` (shared: 04 and 06 read them too) |
| Produces | nothing of its own; includes the shared `build/data/rules.txt` and `build/data/counts.txt` |

## Slides

- [x] The journey of one order: `build/03-chaos/diagrams/journey.png`
- [x] The room: the chat log, `03-chaos/data/room.txt`
- [x] The retro: the six questions as a table, `build/03-chaos/retro.txt`
- [x] The honest count: `build/data/counts.txt`
- [x] First change: bit, who, rule, with the line glued at its foot: `build/data/rules.txt`

## Live

Tell the story with one concrete case (name, two books, coupon, Sofia address). No code
runs in this section.

## Done when

- Given the story diagram, when told aloud, then each of the six red cards falls out of
  a numbered sentence.
- Given `data/rules.csv`, when `make artifacts` runs, then the counts slide says
  `2^9 = 512`.

## Open

- A real domain storytelling picture (egon.io export) instead of the sequence diagram.
- Whether to show the example map as four coloured columns (needs a drawn figure) or keep
  the generated table.
