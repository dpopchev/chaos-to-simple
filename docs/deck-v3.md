# Deck v3: the review remarks of 2026-11-02

Source: the developer's paste at the plan of E-010 on 2026-11-02; the four blocks below are that review's tables, verbatim.

## Story gaps A1-A9

```text
#    Frame    Problem    Fix
A1    11 Step 6    Three bubbles plus the diff on one frame; the chat question "how many tests would make you sure?" is gone from the deck entirely, so the open loop never opens    Add frame "Checkout done": the Dev bubble, the Marketing reply, the chat question. Step 6 keeps the Accounting bubble only
A2    13 Finance    Chart, a two-line summary, a pictogram and the squeeze bubble; the loss and the next request land in the same breath    Chart title carries the totals ("October: 6,070 BGN of shipping never charged, 1,214 parcels"); drop the text block; the squeeze bubble becomes the frame's last line, read after a pause
A3    18 and 19    """The agenda was a map"" and ""Where we are"" are the same figure twice"    One frame: the matrix with 02 highlighted and the line glued. Frees a frame for A1
A4    17    Text only; the two parties are the storyboard's actors, so show them that way    Marketing and Logistics bubbles in the exhibit style, plus a Dev bubble "Which test do I write?": two above the line, one below, which is the whole 02 point
A5    34 I3    The caption "charge before reserve: the order was the bug, nobody decided it" is gone; the link to q5 is missing    Re-add the caption and one line: "decided in the room two weeks earlier (q5); the code had not heard"
A6    37 CQS    Three type lines and nothing else; the frame reads as a fragment    Two definitions (query: pure, returns a value; command: effect, answers with a value) above the three types, the refrain below
A7    43 Eight worlds    Only the world(bits) helper remains; the outcomes are gone, so the title has no evidence    Generate build/06-simple/worlds.txt by running the shell against the eight fake worlds: bits, outcome, charged, mailed. Eight rows, four distinct outcomes, measured. Keep world() as a six-line snippet beside it
A8    2 and 3    Captions describe the picture ("the shop in the middle; the customer on top")    2: "Every arrow becomes a line in one function" (Conway). 3: "The number under each stop is the paths we have to reason about" (introduces the footer)
A9    4, 16, 20, 26, 33, 40    Section frames are red text on white, the only unstyled frames    Section page template: the agenda strip with the current stop highlighted and the section's believed line as its opening question ("I believed: a green badge means tested"). Six dead frames become beats at no time cost
```

## Figures B1-B8

```text
#    Frame    Fix
B1    18 Stacey    Figure at 40% width. Remove the x-axis band labels and the sub-captions under the axis (they repeat the in-arc texts and suggest vertical bands on a radial chart); grow the figure to 85% height. BOOM label reads "9x the program (Brooks 1975)": write "program to product: 9x (Brooks, 1975)" so it parses
B2    15 Grid    No legend; the orange cell is 000101 (code bits: the threshold condition was true) while the xfail test says "45 of goods"; a listener will ask. Legend: green tested, orange the path finance found, grey never run; caption "bits read as the six conditions, left b5 to right b0". Keep code bits everywhere (03's panels already use them) and update tested.csv to 000101
B3    25 Board    Three empty columns look broken, and rows b3 to b5 have an empty first cell. Give the stage columns faded headers "04 home", "05 answer", "06 test" with "later" in grey, or grow the board rightwards per stage; first cell shows the bit when no question was raised
B4    21 Journey    Labels unreadable at slide size. Mermaid themeVariables fontSize 20px, seven tasks at most, 90% width; or draw it with the agenda-strip renderer for a consistent look
B5    22 Room    Nineteen lines of monospace. Render room.txt through the bubble renderer with coloured speaker labels, or at least colour the speaker names (a short Lua filter over the exhibit block)
B6    23 Retro    Highlight the q3 row (the dispute); who column in actor colours
B7    31 Homes    Diff in tiny type beside large pills. Show only the added body (eight lines) since the removed lines were seen on 27; drop the text table, keep the pills grouped by context
B8    45 Number    Acceptable; leader lines on the third bar still cross. Put the four small labels in a legend box to the right instead of leaders
```

## Code on slides C1-C8

```text
#    Frame    Fix
C1    5 Step 0    subtotal = goods exists only to plant the bug and appears at week 1. Move it to step 3 (its marker becomes 3): the bug is visibly born with the threshold request, and the first-fix diff removes a line the audience saw arrive. Also shipping = Decimal(5) at step 0 needs one word in the Customer bubble: "I pay the books and 5 BGN postage"
C2    5 to 11    The # what if it is declined? comments are the narrator's, not week-1 past me's. Strip them from the storyboard diffs (filter flag) and show them first on frame 34
C3    5 to 11, 28, 31, 38, 46    '--- a / +++ b / @@ headers are noise on a slide. Storyboard: no header; stage diffs: file names as a caption line, no hunk headers
C4    38 Ports    Three case _ as unreachable: assert_never(unreachable) blocks are 6 of 21 lines. Drop them from the slide (pyright's reportMatchNotExhaustive covers exhaustiveness; keep the cases in the repo if you prefer and hide them with a diff filter pattern)
C5    41 Paths    request, priced = request_from_bits(bits), price(request_from_bits(bits), TODAY) computes the request twice and reads badly. Two class fixtures, request(bits) and priced(request); each test becomes two lines. Titles of 41 and 42 should agree: "Sixty-four paths, three invariants: 192 tests"
C6    46 Epilogue    The diff wraps the signature over six lines (formatted at 88) and includes a comment edit. Keep line length 100 so the signature stays one line, and make the # b2 comment identical in both files: the diff becomes the three lines that matter
C7    29 Dispute    Coupon.is_valid_on belongs to q1, not the dispute. Show the b2 sentence from the retro, shipping_fee, and the "Values, never flags" takeaway; Coupon moves to the notes
C8    12 Coverage    """2 passed, 9 deselected"" leaks the other tests. Run the two tests from their own file or add --no-summary-style trimming so the line reads ""2 passed"""
```

## Build and data D1-D4

```text
D1. The counter plan in counter.csv gains the new frame: 01 stays 1 2 4 8 16 32 64 with the "Checkout done" frame inheriting 64.
D2. Budget: 01 to 12 frames, 02 to 2; totals unchanged (41 content, 45 minutes).
D3. Q&A frame: the repository bullet has no link; add the URL or a placeholder you fill on Wednesday, and the board at stage 06 stays.
D4. tested.csv: bug row 000101 (see B2); a test pins that the grid's marked cell equals the xfail test's path in code bits.
```

## Frame map

Page 1 is the title page; the six section titles (`# `) are pages of their own; the other pages are the `## ` titles of 0*-*/index.md in sorted order. The page numbers are the ones the remarks cite.

| Page | Section | Frame |
|---|---|---|
| 1 | title | title page |
| 2 | 00 | The business map |
| 3 | 00 | Agenda, in the order the bits fall |
| 4 | 01 | Six if statements, 64 paths (section) |
| 5 | 01 | Step 0: no ifs |
| 6 | 01 | Step 1: one if |
| 7 | 01 | Step 2: two ifs |
| 8 | 01 | Step 3: three ifs |
| 9 | 01 | Step 4: four ifs |
| 10 | 01 | Step 5: five ifs |
| 11 | 01 | Step 6: six ifs |
| 12 | 01 | Two tests. Coverage says 100% |
| 13 | 01 | Finance found it, not the tests |
| 14 | 01 | The path nobody ran |
| 15 | 01 | A path is a six-bit number |
| 16 | 02 | Stacey matrix: agreement on the What, certainty on the How (section) |
| 17 | 02 | I wanted to write a test |
| 18 | 02 | The agenda was a map |
| 19 | 02 | Where we are: question 02 |
| 20 | 03 | From chaos to complex (section) |
| 21 | 03 | The journey of one order |
| 22 | 03 | The room |
| 23 | 03 | The retro |
| 24 | 03 | The honest count |
| 25 | 03 | Nine decisions, none deleted, all moved |
| 26 | 04 | Complicated on the What: one language, bounded contexts (section) |
| 27 | 04 | Color-coded, the ifs get names |
| 28 | 04 | The first fix |
| 29 | 04 | The dispute closes |
| 30 | 04 | A bit as a type |
| 31 | 04 | Bounded contexts: every bit has a home |
| 32 | 04 | Bounded contexts, the moves |
| 33 | 05 | Complicated on the How: decoupling, cohesion, FP vs OO, CQS (section) |
| 34 | 05 | I3: cards charged for parcels the warehouse did not have |
| 35 | 05 | Past me reached for a class |
| 36 | 05 | The bit nobody wrote down |
| 37 | 05 | Command Query Separation draws the seam |
| 38 | 05 | The ports, as a picture |
| 39 | 05 | A boundary that passes values adds paths; one that passes flags multiplies them |
| 40 | 06 | Simple: functional core, imperative shell (section) |
| 41 | 06 | Sixty-four paths, one test each |
| 42 | 06 | Sixty-four paths, each invariant a test |
| 43 | 06 | Eight worlds, four outcomes |
| 44 | 06 | The wounds close by name |
| 45 | 06 | The number |
| 46 | 06 | Epilogue: marketing's seventh if |
| 47 | 07 | What I should have known from the start |
| 48 | 07 | Q&A |

## Remark map

Each remark id maps to the work item whose description carries it (E-010's work items W-089 to W-097).

| Remark | Work item | Remark | Work item |
|---|---|---|---|
| A1 | W-090 | C1 | W-090 |
| A2 | W-091 | C2 | W-090, W-095 |
| A3 | W-092 | C3 | W-090, W-094 |
| A4 | W-092 | C4 | W-095 |
| A5 | W-095 | C5 | W-096 |
| A6 | W-095 | C6 | W-096 |
| A7 | W-096 | C7 | W-094 |
| A8 | W-089 | C8 | W-091 |
| A9 | W-089 | D1 | W-090 |
| B1 | W-092 | D2 | W-090, W-092 |
| B2 | W-091 | D3 | W-097 |
| B3 | W-093 | D4 | W-091 |
| B4 | W-093 | | |
| B5 | W-093 | | |
| B6 | W-093 | | |
| B7 | W-094 | | |
| B8 | W-096 | | |
