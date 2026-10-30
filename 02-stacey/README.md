# 02-stacey: the map

Beat: a map for where bits come from. Agreement on the What and certainty on the How are
two axes; each later section is one move on the map.

| | |
|---|---|
| Minutes | 5 |
| Footer counter | stays at `64` |
| Owns | the Stacey figure is drawn by `scripts/figures.py stacey`, declared in `02-stacey/section.mk` |
| Uses | nothing |
| Produces | `build/02-stacey/stacey.png` |

## Slides

- [x] I wanted to write a test: the question, two answers
- [x] Two axes, four zones: the matrix
- [x] Bits on the map: the table
- [x] The route of this talk
- [x] The line: check whether the What is agreed

## Done when

- Given `make diagrams`, when it finishes, then the quadrant chart shows four labelled
  points along the route from chaos to simple.
- Given the route slide, when section 06 ends, then the same picture can be shown again
  with the counter at 72.

## Open

- Whether to draw the route as arrows instead of points (Mermaid quadrant charts have
  points only; arrows would need a flowchart or hand drawing).
