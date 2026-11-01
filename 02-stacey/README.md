# 02-stacey: the map

Beat: a map for where bits come from. Agreement on the What and certainty on the How are
two axes; each later section is one move on the map.

| | |
|---|---|
| Minutes | 3 |
| Footer counter | stays at `64` |
| Owns | the Stacey figure is drawn by `scripts/figures.py stacey`, declared in `02-stacey/section.mk` |
| Uses | nothing |
| Produces | `build/02-stacey/stacey.png` |

## Slides

- [x] I wanted to write a test: the question, two answers
- [x] The agenda was a map: the route, with the line glued at its foot: check whether the What is agreed

## The matrix

Both axes start certain at the origin: x is the How, y is the What. Four bands follow the
distance from the origin (`data/zones.csv`):

| Band | Distance | Above the diagonal | Below the diagonal |
|---|---|---|---|
| Simple | 0.00 to 0.25 | clear boundary; clear responsibility; a plan works | clear boundary; clear responsibility; a plan works |
| Complicated | 0.25 to 0.50 | tangled requirements; clear technology: experts agree the What | clear requirements; hard technology: experts settle the How |
| Complex | 0.50 to 0.75 | move down: decide the What first | move down: settle the How first |
| Chaos (BOOM) | 0.75 and beyond | joint venture; no boundary; nobody can say how long | joint venture; no boundary; nobody can say how long |

The diagonal y = x is labelled Who (`data/labels.csv`): above it stakeholders decide and
agree, below it developers decide. The route puts 01 and 02 above the diagonal, 03 on it,
and 04 to 06 below it.

## Sources

The BOOM label carries no number until W-061 records a source for it.

## Done when

- Given `make diagrams`, when it finishes, then the quadrant chart shows four labelled
  points along the route from chaos to simple.
- Given the route slide, when section 06 ends, then the same picture can be shown again
  with the counter at 72.

## Open

- Whether to draw the route as arrows instead of points (Mermaid quadrant charts have
  points only; arrows would need a flowchart or hand drawing).
