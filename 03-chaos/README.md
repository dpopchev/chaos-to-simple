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

- [x] Replaying one order reveals six unanswered business questions: the journey of one order, `build/03-chaos/diagrams/journey.png`
- [x] The room surfaces three unwritten rules and three unhandled provider answers: the chat log, `03-chaos/data/room.txt`
- [x] Each of the six questions gains a decision and a subdomain: the retro, the six questions as a table, `build/03-chaos/retro.txt`
- [x] Three provider answers join the six policies: nine bits, 512 paths, not 64 (frame 4): `build/03-chaos/grid-9.png`, `build/03-chaos/doubling-512.png`, `build/data/counts.txt`
- [x] Every one of the nine decisions is kept and moves to a responsible home: `build/03-chaos/board.png`, the `\theline` at its foot

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
