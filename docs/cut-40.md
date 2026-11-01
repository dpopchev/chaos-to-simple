# The 40-minute cut: the review remarks of 2026-11-01

From: the developer, received mid-burn on 2026-11-01 (W-034 and W-035, T-085 doing), noted at
local/inbox/2026-11-01-chaos-to-simple-talk-remarks.md. The four blocks below are that note's,
verbatim; the frame map and the line counts after them are derived.

## Storyline (verbatim)

```text
#    Where    Problem    Suggestion
A1    03 "The honest count" (frame 30)    The ending leaks: 64 + 8 = 72 and 22 are on screen in section 03, thirty frames before "The number".    Split the counts artifact: 03 shows the scope table and only one function, 9 bits: 2^9 = 512; the two split lines move to 06 "The number", under the chart. The counter then has a real reveal.
A2    03 "First change: a table" (31) and 04 "One language" (34)    Same table twice, and in 03 it already carries names that do not exist yet (coupon.is_valid_on, Zone.DOMESTIC, FREE_SHIPPING_FROM). The room produced sentences, not code.    scripts.paths rules --columns: 03 shows bit, who, rule (the sentences), 04 shows bit, context, name, code. One table each, chronology intact.
A3    05    I3 is about effects (charged without stock) but the instinct and the hidden bit are about pricing (apply_coupon, 45 vs 44). The false victory does not answer the incident.    Add the missing beat before the class: chaos lines 67 to 69 under the I3 exhibit, charge before reserve: the order was the bug and nobody decided it. Then the class as "the same bit in OO clothing: order hidden in state". 06's shell closes it by order (reserve, charge, send) and by name. Frame the 05 line accordingly.
A4    01 "One of the other sixty-two" (12)    Refers to 62 before the audience has counted to 64 (frame 14).    Rename "The path nobody ran"; the loop order (exhibit, instinct, count) stays.
A5    01 cast (8) and count along (14)    The cast table carries the narrator's asides ("from what? nobody asked", "two weeks before launch") and its words are repeated in the doubling table six frames later.    Cast table shows past me's record only (line, who, their words); asides go to the notes. Count along overlays become the doubling rows themselves (week, who, bits, paths), replacing the "One if: 2 paths" lines.
A6    06 epilogue (61)    Order on the slide is code, counts, then marketing's chat line. Exhibit comes first everywhere else.    Chat line on top, the digital shipping_fee as the move, the three deltas as the proof. Drop the "before" function (shown in 04); highlight the two new lines instead.
A7    03 "What it felt like, what it was" (29)    The chart tells 01's story (weeks 3 to 10, paths to 64) inside 03, after the count.    Move to 01 beside the count along, or extend its x axis to week 15 with the honest 512 so it says "it got worse before it got better". For 40 minutes: drop it, keep for the Friday post.
A8    Lines    Section 02, 03, 04, 06 have a separate "The line" frame; 01 and 05 glue it to the last slide.    Glue everywhere: a fixed two-line block at the bottom of each section's last frame, believed in grey, learned in bold. Saves four frames and makes the device recognisable.
A9    06 "The core" (54)    The docstring says "4 + 8 + 2 paths, not 64" one frame before "Sixty-four paths, one test each". Two counting modes on consecutive slides.    Docstring: "composes three contexts; every bit stays where it was named". 64 + 8 is the headline; 22 belongs to the epilogue only.
A10    01 contract    """No decision is ever deleted, only moved"" is a bullet on ""Parked for section 03"". It is the rule that makes 02 to 06 one story."    Give it its own line on that frame, repeat it verbatim on 04 "the moves" (the Sankey is literally this sentence) and on 06 "The number".
```

## Forty minutes (verbatim)

```text
Section    Now    Min    Keep    Cut or merge
00    4    2.5    message; code with the chat question as its last line; route    4 (question alone)
01    11    7    cast; tests with a two-line coverage summary; finance; the path nobody ran; count along; grid with Rule 1 as three bottom lines; parked + contract + line    7 (code again), 10 (full report), 13 (two-ifs zoom-in: the marked grid makes the point; the code stays in the repo for the post), 16 merged into grid
02    6    3    """I wanted to write a test""; the route diagram again, titled ""The agenda was a map"", with the line glued"    20 (empty quadrant), 21 (zones table, to notes), 22 (route duplicate), 23
03    8    5.5    room; six questions with the decided column (questions 4 to 6 are the three effects); example map; honest count (512 only); first change with sentences + line    28 (effects, merged), 29 (chart), 32
04    8    5.5    dispute closes (sentence, Coupon.is_valid_on, shipping_fee, "values, never flags" as the takeaway); a bit as a type; every bit has a home (with who); the moves + contract + line    34 (duplicate table), 36 (folded), 38, 41
05    9    6    I3 + lines 67 to 69; the class (two methods only); the hidden bit; CQS with the three type X = A | B lines; ports as a picture; moves table with the refrain as title + line    47 (22 lines of dataclasses), 48 (Protocol code; the picture carries it), 51 merged into 50
06    11    8    core; sixty-four paths (the parametrized test only, 9 lines); counted (64 passed); shell (checkout only); eight worlds; wounds (trimmed output); the number with the split lines and the counter to 72; epilogue in two columns (code left, before/after chart right) + line    53 (bullets; the 05 picture already drew it), 62 merged into 61, 63
07    3 + title    2.5    the six lines; "Where to go" retitled "Q&A" so the repo link stays on screen for 15 minutes    64 (section frame), 67
```

## Density (verbatim)

```text
Density and consistency
D1. Cap included snippets at about 14 lines: 05 answers (22), 06 shell (26), 06 sixty-four (21), epilogue (21) overflow a 16:9 frame at this font. Add a make check step that fails when an included snippet exceeds the cap, so it cannot regress.
D2. Code shown twice: checkout (3 and 7), shipping_fee (35 and 61), the rules table (31 and 34), the route (5 and 22). After the cuts only the route repeats, and that one is deliberate.
D3. "Rewriting the two ifs of section 01" (16) refers to the section it is in; after the merge it reads "two sequential ifs as if/elif: 4 becomes 3".
D4. Cast "line" column lists bits in bit order (52, 54, 59, 57, 61, 64); sort by line so the eye runs down the code.
D5. The 07 summary is six dense pairs; it works as a leave-behind, but read only the learned column aloud.
```

## Fifteen minutes of Q and A (verbatim)

```text
Fifteen minutes of Q&A
The last frame is the repo and the posts; it stays up for the whole Q&A.
Seed six questions for a slow chat, each answered in one breath: "64 tests is overkill", "where does async or the ORM go", "what about exceptions", "how do I convince my team", "does this scale beyond one function", "where does the digital-books if go" (the chat already answered it; replay the answer).
Keep the 45 vs 44 run and the two-ifs tree in the repo as Q&A demos; they are the first things people ask about.
```

## Frame map

The remarks number the frames of build/talk.pdf at b9ee26a, before the 40-minute cut (E-005, tag
v0.5.0): this map is built from `git show b9ee26a:<section>/index.md`, its `# ` and `## `
headings, not from today's files.

```text
n   section         heading
1   (title)         Python: From chaos to simple, one bit at a time
2   00-frontmatter  Checkout done
3   00-frontmatter  The checkout, as past me left it
4   00-frontmatter  How many tests would make you sure?
5   00-frontmatter  Agenda, in the order the bits fall
6   01-bits         (section) Six if statements, 64 paths
7   01-bits         The checkout as found
8   01-bits         The cast behind the ifs
9   01-bits         Two tests. Coverage says 100%
10  01-bits         The coverage report
11  01-bits         Finance found it, not the tests
12  01-bits         One of the other sixty-two
13  01-bits         Four paths, the same two tests
14  01-bits         Count along: one if, one bit
15  01-bits         A path is a six-bit number
16  01-bits         Rule 1: how ifs count
17  01-bits         Parked for section 03
18  02-stacey       (section) Stacey matrix: agreement on the What, certainty on the How
19  02-stacey       I wanted to write a test
20  02-stacey       Two axes, four zones
21  02-stacey       Bits on the map
22  02-stacey       The route of this talk
23  02-stacey       The line
24  03-chaos        (section) From chaos to complex
25  03-chaos        The room
26  03-chaos        The six questions
27  03-chaos        The six questions, as a map
28  03-chaos        Three effects nobody wrote down
29  03-chaos        What it felt like, what it was
30  03-chaos        The honest count
31  03-chaos        First change: a table, not a refactoring
32  03-chaos        The line
33  04-what         (section) Complicated on the What: one language, bounded contexts
34  04-what         One language
35  04-what         The dispute closes
36  04-what         A rule is a phrase, a phrase is a method
37  04-what         A bit as a type
38  04-what         Values, never flags
39  04-what         Bounded contexts: every bit has a home
40  04-what         Bounded contexts, the moves
41  04-what         The line
42  05-how          (section) Complicated on the How: decoupling, cohesion, FP vs OO, CQS
43  05-how          I3: cards charged for parcels the warehouse did not have
44  05-how          Past me reached for a class
45  05-how          The bit nobody wrote down
46  05-how          Command Query Separation draws the seam
47  05-how          The answers the world may give
48  05-how          The ports
49  05-how          The ports, as a picture
50  05-how          Refactoring moves and their sign
51  05-how          Coupling multiplies, cohesion adds
52  06-simple       (section) Simple: functional core, imperative shell
53  06-simple       The picture
54  06-simple       The core
55  06-simple       Sixty-four paths, one test each
56  06-simple       We counted them
57  06-simple       The shell
58  06-simple       Eight worlds, four outcomes
59  06-simple       The wounds close by name
60  06-simple       The number
61  06-simple       Epilogue: marketing's seventh if
62  06-simple       Epilogue, the cost in a chart
63  06-simple       The line
64  07-close        (section) Close
65  07-close        What I should have known from the start
66  07-close        Where to go from here
67  07-close        Q&A
```

00-frontmatter has no section frame; the title frame comes from 00-frontmatter/meta.yaml.

## Included lines per frame

The review counts non-blank lines. Measured with the include parser of scripts.utils.widths
(`INCLUDE`, `snippet_text`) over every index.md at b9ee26a, each included file read with
`git show b9ee26a:<path>`; the rows are the blocks over 14 raw lines and the epilogue frame. The
last column is the same block's non-blank count at d8a97f2, today's deck after the cut, or `cut`
when the frame is gone.

| Frame | file:snippet | Raw, non-blank | Today |
|---|---|---|---|
| 3 and 7 | 01-bits/s01_bits/chaos.py:checkout | 23, 22 | 22 (3 kept, 7 cut) |
| 9 | 01-bits/tests/test_chaos.py:two-tests | 22, 19 | 19 |
| 44 | 05-how/s05_how/oo_checkout.py:oo | 19, 16 | 11 |
| 47 | 05-how/s05_how/ports.py:results | 38, 21 | cut |
| 55 | 06-simple/tests/test_core_paths.py:from-bits | 23, 20 | 8 |
| 57 | 06-simple/s06_simple/shell.py:checkout | 28, 25 | 12 |
| 58 | 06-simple/tests/test_shell.py:eight | 15, 14 | 14 |
| 61 | 04-what/s04_what/shipping.py:fee | 8, 7 | dropped from the frame |
| 61 | 06-simple/s06_simple/seventh.py:fee-digital | 10, 9 | 9 |
| 61 | build/06-simple/epilogue.txt | 3, 3 | 3 |
| 61 | 06-simple/data/teaser.txt | 1, 1 | 1 |

- The non-blank counts of ports.py:results, test_core_paths.py:from-bits and shell.py:checkout
  read one lower than the brief's 22, 21 and 26: `snippet_text` drops the trailing blank line and
  the count here skips every blank line; the raw counts agree.
- build/06-simple/epilogue.txt is a build artifact, not in git: its count is today's build, the
  three delta lines the brief names.
- Frame 61 held 22 raw, 20 non-blank lines in four blocks; today's epilogue frame holds 13.
