# 03-chaos: from chaos to complex

Beat: you cannot shrink a count you do not know. Domain storytelling and example mapping
find the three bits hiding behind the effects; the honest count is 9 bits, 512 paths.

| | |
|---|---|
| Minutes | 5.5 |
| Footer counter | `64` on entry, `512` from "The honest count" |
| Owns | `diagrams/story.mmd` (the domain story as a sequence diagram), `data/questions.md` (the red cards and where each was answered) |
| Uses | `data/rules.csv`, `data/examples.csv` (shared: 04 and 06 read them too) |
| Produces | nothing of its own; includes the shared `build/data/rules.txt` and `build/data/counts.txt` |

## Slides

- [x] The room: one story, nine sentences: `build/03-chaos/story.png`
- [x] The six questions, decided: the red cards, with the three effects in rows 4-6
- [x] The six questions, as a map: `build/03-chaos/example_map.png`
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
