# 02-stacey: the map

Beat: a map for where bits come from. Agreement on the What and certainty on the How are
two axes; each later section is one move on the map.

| | |
|---|---|
| Minutes | 6 |
| Footer counter | stays at `64` |
| Owns | `diagrams/stacey.mmd` (Mermaid quadrant chart with the talk's route as points) |
| Uses | nothing |
| Produces | `build/02-stacey/diagrams/stacey.png` through the generic diagram rule in the Makefile |

## Slides

- [x] Two axes, four zones: the chart
- [x] Bits on the map: the table
- [x] The route of this talk

## Done when

- Given `make diagrams`, when it finishes, then the quadrant chart shows four labelled
  points along the route from chaos to simple.
- Given the route slide, when section 06 ends, then the same picture can be shown again
  with the counter at 72.

## Open

- Whether to draw the route as arrows instead of points (Mermaid quadrant charts have
  points only; arrows would need a flowchart or hand drawing).
