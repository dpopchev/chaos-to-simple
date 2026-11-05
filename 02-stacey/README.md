# 02-stacey: the map

Beat: a map for where bits come from. Agreement on the What and certainty on the How are
two axes; each later section is one move on the map.

| | |
|---|---|
| Minutes | 3 (3 frames) |
| Footer counter | stays at `64` |
| Owns | the Stacey figure is drawn by `scripts/figures.py stacey`, declared in `02-stacey/section.mk`; `02-stacey/tests/test_readings.py` holds the R1 and R2 tests (snippets `r1`, `r2`) run against `s01_bits.chaos` |
| Uses | nothing |
| Produces | `build/02-stacey/stacey.png` |

## Slides

- [x] Free shipping from 50 has two plausible meanings: the sentence, the code's condition, finance's test and the two-readings table (the cart before or after the coupon)
- [x] Marketing and Logistics disagree about what the customer should pay: the question, the R1 Marketing and R2 Logistics bubbles, the line 'one function, one reading: the code picked R1 and nobody chose', a rule, the dev bubble below
- [x] Stakeholders must choose the rule before developers can fix it: `stacey-02.png` at 85% height, with the line glued at its foot: check whether the What is agreed

## The matrix

Both axes start certain at the origin: x is the How, y is the What. Four bands follow the
distance from the origin (`data/zones.csv`):

| Band | Distance | Above the diagonal | Below the diagonal |
|---|---|---|---|
| Simple | 0.00 to 0.25 | clear boundary; clear responsibility; a plan works | clear boundary; clear responsibility; a plan works |
| Complicated | 0.25 to 0.50 | tangled requirements; clear technology: experts agree the What | clear requirements; hard technology: experts settle the How |
| Complex | 0.50 to 0.75 | move down: decide the What first | move down: settle the How first |
| Chaos | 0.75 and beyond | joint venture; no boundary; nobody can say how long | joint venture; no boundary; nobody can say how long |

Each band's name is drawn inside its arc. Nothing is drawn under the x axis but its label;
the below column of `zones.csv` is kept for the notes, not drawn.

The diagonal y = x is labelled Who (`data/labels.csv`): above it stakeholders decide (the
text stands upright at the top of the y axis), below it developers decide. The route puts 01 and 02 above the diagonal, 03 on it,
and 04 to 06 below it.

The collaboration wedge: one flat grey wedge from the origin, half of each side of the Who
line (22.5 to 67.5 degrees), with the word collaboration along the Who line from the Chaos
arc. The point: only Simple has a clear boundary; everywhere else the work is collaboration.

## Sources

The candidate sources and what each states are in `data/boom-sources.md` (W-061).

Decision: the BOOM label quotes Brooks, The Mythical Man-Month, ch. 1 "The Tar Pit" (1975): a programming systems product costs nine times the program; `data/labels.csv` boom_quote reads "program to product: 9x (Brooks, 1975)"; the 8:1 hunch is not used, since no source read states it.

## Done when

- Given `make talk budget`, when they finish, then 02 holds three frames: the deduction table,
  the marketing and logistics bubbles above a rule with the dev bubble 'Which test do I write?'
  below it, then the matrix with 02 highlighted at 85% height and the line glued under it.
- Given `make diagrams`, when it finishes, then the quadrant chart shows four labelled
  points along the route from chaos to simple.
- Given the route slide, when section 06 ends, then the same picture can be shown again
  with the counter at 72.

## Open

- Whether to draw the route as arrows instead of points (Mermaid quadrant charts have
  points only; arrows would need a flowchart or hand drawing).
