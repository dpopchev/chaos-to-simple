# Board -- chaos-to-simple
record: local
open path: E-014 > W-131 > T-294   | blocked: 0 | todo roots: 1 | done: 433 | pruned: 4

## Tree

```text
E-014         [doing]    Deck v5: one legend of three kinds, the Stacey overview, compact diffs with their tests
  W-130  issue  [done]     00: one legend of three kinds, the map redrawn -- T-291 [done], T-292 [done], T-293 [done], T-330 [done]
  W-131  issue  [doing]    03/06: the kinds in the retro, the post-mortem and the epilogue -- T-294 [doing]   <- ACTIVE LEAF, T-295 [todo], T-296 [todo]
  W-132  issue  [todo]     04: the moves and the colour code under the kinds -- T-297 [todo], T-298 [todo], T-299 [todo]
  W-133  issue  [todo]     00/02: the Stacey overview on page 3, the plain matrix on page 20 -- T-300 [todo], T-301 [todo], T-302 [todo]
  W-134  issue  [todo]     03: the new view after the room -- T-303 [todo], T-304 [todo]
  W-135  issue  [todo]     01: how the paths are counted, as a block diagram -- T-305 [todo], T-306 [todo]
  W-136  issue  [todo]     01: the storyboard as compact +/- diffs with the length in the tally -- T-307 [todo], T-308 [todo], T-309 [todo]
  W-137  issue  [todo]     01: the tests under each request, page 14 in step -- T-310 [todo], T-311 [todo]
  W-138  issue  [todo]     01: finance finds it, the condition, the test -- T-312 [todo], T-313 [todo], T-314 [todo]
  W-139  issue  [todo]     01: the grid that doubles, the badge named -- T-315 [todo], T-316 [todo]
  W-140  issue  [todo]     02: two readings, two tests that cannot both pass -- T-317 [todo], T-318 [todo]
  W-141  issue  [todo]     03: why the order was replayed, where the room clashed -- T-319 [todo], T-320 [todo], T-321 [todo]
  W-142  issue  [todo]     04: the fix is v7, the contexts v8, each under its tally -- T-322 [todo], T-323 [todo], T-324 [todo]
  W-143  issue  [todo]     05: v8 to v9 compact, every snippet with its home and its test -- T-325 [todo], T-326 [todo]
  W-144  issue  [todo]     06: v9 to v10 compact, the long snippet cut, every snippet with its home and its test -- T-327 [todo], T-328 [todo], T-329 [todo]
W-145  bug    [todo]     (standalone) Figure rules miss the palette files, so a colour or label change leaves stale figures   (filed during T-330) -- T-331 [todo]
```

## Closed

### E-001 [done] Deck infrastructure: the drafts become one beamer PDF through make

closed 2026-10-30 -- outcome: make check proves the repository (board, ruff, pyright, pytest, ascii) and make deliverable writes build/talk.pdf from 00-frontmatter..07-close with every snippet, artifact and diagram built by make. -- ledger: ledgers/E-001.md

#### W-001 issue [done] The front door: base Makefile, python layer and the 3.14 toolchain

- T-001 [done] Write the base Makefile, the python layer and the 3.14 toolchain files -> make check prints [DONE] all checks passed
- T-002 [done] Move the helper tests beside their modules under the one-assert conftest -> make test M=model K=test_bars_follow_the_inventory passes

#### W-002 issue [done] The deck builds: mk/deck.mk, lualatex and the installed fonts

- T-003 [done] Add the diagram fallback helper scripts/utils/diagram.py with its edge test -> make test M=edge K=test_write_placeholder passes
- T-004 [done] Add mk/deck.mk with the deck targets, lualatex and the installed fonts -> make deliverable prints [DONE] deliverables built: deliverable-talk
- T-005 [done] Rewrite the README build section and add CLAUDE.md with the gate deviations -> grep finds ## Gate deviations in CLAUDE.md

### E-002 [done] The deck tells the storyline: past me, the cast of the ifs, three incidents closed by name

closed 2026-10-30 -- outcome: make talk builds a deck that runs from the message of past me to the six lines, with the cast, the incidents, the counts and the lines as artifacts the build measures or checks. -- ledger: ledgers/E-002.md

#### W-007 issue [done] 01-bits: the protagonist, the cast of the ifs and the count to 64

- T-010 [done] Add the cast data and its renderer -> build/01-bits/cast.txt
- T-011 [done] Rewrite the exhibit as past me left it -> test_chaos.py with his names, the I1 report
- T-012 [done] Add the two-ifs zoom-in -> build/01-bits/two_ifs.txt
- T-013 [done] Rewrite the 01 slides to the nine-slide format -> 01-bits/index.md, nine slides

#### W-008 issue [done] 00-frontmatter: the message from past me and the route

- T-014 [done] Draw the route -> build/00-frontmatter/route.png in the deck style
- T-015 [done] Rewrite the opening -> 00-frontmatter/index.md: message, raw code, chat, route

#### W-009 issue [done] 02-stacey: which problem do I have

- T-016 [done] Rewrite the 02 slides -> 02-stacey/index.md: instinct, matrix, map, route, the line

#### W-010 issue [done] 03-chaos: the room, the dispute decided and the honest count

- T-017 [done] Rewrite the red cards -> 03-chaos/data/questions.md with question 3 decided
- T-018 [done] Rewrite the 03 slides -> 03-chaos/index.md: room, six questions, effects, 512, table, line

#### W-011 issue [done] 04-what: the words become homes

- T-019 [done] Render the contexts with their faces -> build/04-what/contexts.txt
- T-020 [done] Rewrite the 04 slides -> 04-what/index.md: the sentence, homes with faces, the line

#### W-012 issue [done] 05-how: I3, the false victory and the seam

- T-021 [done] Write the I3 report -> 05-how/data/incident.txt
- T-022 [done] Rewrite the 05 slides -> 05-how/index.md: I3, the class, the hidden bit, CQS, seam, line

#### W-013 issue [done] 06-simple: the run of 72 and the seventh if

- T-023 [done] Add the seventh if beside the core, not inside it -> 06-simple/s06_simple/seventh.py
- T-028 [done] Render the epilogue counts -> build/06-simple/epilogue.txt
- T-029 [done] Rewrite the 06 slides -> 06-simple/index.md: core, 64, the wounds, 72, epilogue, line

#### W-014 issue [done] 07-close: the six lines

- T-024 [done] Rewrite the close -> 07-close/index.md: the six lines, where to go, Q&A
- T-025 [done] Check the lines against the sections -> scripts/check_lines.py, make lines

#### W-015 issue [done] build: the targets and filter behaviour the checks assume

- T-026 [done] Rename slides to talk, add K= to test, add the lines target -> Makefile, README.md
- T-027 [done] Number a snippet by its file line -> 00-frontmatter/filters/include-code-files.lua

#### W-016 issue [done] plots: one matplotlib and seaborn style for every chart and diagram

- T-030 [pruned] Add the deck style -> scripts/utils/style.py, applied by the stacked bar   [pruned: frozen Check '-> passes' compares the literal text and the run prints '4 passed'; the work stands in 734ef74 and closes under T-034]
- T-031 [done] Draw the Stacey matrix in Python -> build/02-stacey/stacey.png
- T-032 [done] Draw the story in Python -> build/03-chaos/story.png
- T-033 [done] Drop the Mermaid rule -> mk/deck.mk, README.md, CLAUDE.md without mmdc
- T-034 [done] Close the deck style on an exit-status Check -> scripts/utils/style.py at 734ef74

### E-003 [done] The talk runs one loop: found documents, built counts, figures in one style, the believed line flipped

closed 2026-10-31 -- outcome: make talk builds the deck with the five must and six should visuals of docs/storyline.md, each built from its source by make artifacts, and make lines checks a believed / learned pair per section. -- ledger: ledgers/E-003.md

#### W-018 issue [done] 06-simple: the wounds close by name in a run built from incidents.csv

- T-037 [done] Add the incidents -> data/incidents.csv and load_incidents
- T-038 [done] Select the wounds by name -> wounds_selector and scripts.paths wounds
- T-039 [done] Run the wounds -> build/06-simple/wounds.txt
- T-040 [done] Show the wounds -> 06-simple/index.md includes build/06-simple/wounds.txt

#### W-019 issue [done] 00-frontmatter, 01-bits, 05-how, 06-simple: the exhibits as found documents

- T-041 [done] Rewrite the I1 and I3 exhibits -> 01-bits/data/incident.txt, 05-how/data/incident.txt
- T-042 [done] Write the message and the teaser -> 00-frontmatter/data/message.txt, 06-simple/data/teaser.txt
- T-043 [done] Show the found documents -> 00-frontmatter/index.md, 01-bits/index.md, 06-simple/index.md

#### W-020 issue [done] 01-bits: the doubling with faces

- T-044 [done] Add the week -> data/cast.csv week column and CastRow.week
- T-045 [done] Render the doubling -> doubling_table and scripts.paths doubling
- T-046 [done] Show the doubling -> build/01-bits/doubling.txt on Count along

#### W-021 issue [done] lines: the believed / learned pair

- T-047 [done] Read the pair -> Line(section, believed, learned) and data/lines.csv
- T-048 [done] Put the believed lines on the slides -> NN-*/index.md and 07-close/index.md
- T-049 [done] Check the pair -> missing() names an absent believed line

#### W-022 issue [done] 01-bits: the two-if tree

- T-050 [done] Pin the leaves -> TREE_LEAVES in scripts/utils/figures.py
- T-051 [done] Draw the tree -> tree(out) and scripts.figures tree
- T-052 [done] Show the tree -> build/01-bits/tree.png on Four paths

#### W-023 issue [done] 00-frontmatter: the route on the map

- T-053 [done] Add the route -> data/route.csv and load_route
- T-054 [done] Place the route on the map -> route_layout(stops)
- T-055 [done] Show the map -> 00-frontmatter/section.mk and 02-stacey/index.md

#### W-024 issue [done] 03-chaos: what it felt like vs what it was

- T-056 [done] Count the growth -> growth(cast)
- T-057 [done] Draw the growth -> growth_chart(out, points) and scripts.paths growth
- T-058 [done] Show the growth -> build/03-chaos/growth.png before The honest count

#### W-025 issue [done] 04-what: the bits move, none deleted

- T-059 [done] Add the context palette -> context_colour(name) in scripts/utils/style.py
- T-060 [done] Count the moves -> moves(rules)
- T-061 [done] Draw the moves -> moves_figure(out, moves) and scripts.figures moves
- T-062 [done] Show the moves -> build/04-what/moves.png on Bounded contexts

#### W-026 issue [done] 03-chaos: the example map before and after the room

- T-063 [done] Count the cards -> card_counts in scripts/utils/examples.py
- T-064 [done] Draw the map -> example_map(out, before, after) and scripts.figures example-map
- T-065 [done] Show the map -> build/03-chaos/example_map.png on The six questions

#### W-027 issue [done] 05-how: the core and the shell with three ports

- T-066 [done] Read the ports -> ports_of(rules)
- T-067 [done] Draw the seam -> seam(out, ports) and scripts.figures seam
- T-068 [done] Show the seam -> 05-how/section.mk and The ports

#### W-028 issue [done] 06-simple: the epilogue as stacked bars

- T-069 [done] Build the two bars -> epilogue_bars(rules, seventh)
- T-070 [done] Show the bars -> build/06-simple/epilogue.png on the epilogue

### E-004 [done] deck: the deck renders whole

closed 2026-11-01 -- outcome: The developer runs make overflow and make widths clean and sees each route box name its section. -- ledger: ledgers/E-004.md

#### W-029 bug [done] deck: four slides run past the frame bottom   (filed during T-040)

- T-071 [done] Name the overfull frames -> scripts/utils/overflow.py and make overflow
- T-072 [done] Fit the 01-bits frames -> 01-bits/index.md
- T-073 [done] Fit the 05-how and 06-simple frames -> 05-how/index.md and 06-simple/index.md

#### W-030 issue [done] 00-frontmatter: the route boxes name their sections   (filed during T-055)

- T-074 [done] Add the names -> data/route.csv name column and Stop.name
- T-075 [done] Label the boxes -> stop_label(stop) used by route(out)
- T-079 [done] Fit the route labels -> route_box_half_width(stops) used by route(out)

#### W-031 bug [done] deck: code and tables clip at the right edge, column figures too small to read   (filed during T-070)

- T-076 [done] Measure the widths -> scripts/utils/widths.py and make widths
- T-077 [done] Give the E-003 figures room -> 03-chaos, 04-what, 05-how, 06-simple index.md
- T-078 [done] Fit the older clipped lines -> 01-bits, 06-simple index.md
- T-082 [done] Fit the slides past the report -> 00-frontmatter and 01-bits fitted, make widths clean

### E-005 [done] deck: the 40-minute cut

closed 2026-11-01 -- outcome: make talk builds the 40-minute deck: one counter reveal at 06, one table per section, the line device on every section's last frame, no snippet over its cap, the repository frame up for the Q&A. -- ledger: ledgers/E-005.md

#### W-039 issue [done] lines: the believed / learned device glued to each section's last frame

- T-096 [done] Define the line block -> \theline in 00-frontmatter/preamble.tex
- T-097 [done] Glue the lines -> 01..06 index.md end on \theline, no 'The line' frame

#### W-040 issue [done] 00 and 01: the cut and the cast

- T-098 [done] Render the cast without asides -> cast_table by source line, doubling_table with upto
- T-099 [done] Render the artifacts of 01 -> doubling-1..6.txt and coverage-summary.txt from 01-bits/section.mk
- T-100 [done] Cut 00 -> 00-frontmatter/index.md three frames
- T-101 [done] Cut 01 -> 01-bits/index.md seven frames

#### W-041 issue [done] 02 and 03: the cut and the counter's reveal

- T-102 [done] Split the counts and name who asked -> scripts.paths splits and rules --columns
- T-103 [done] Cut 02 -> 02-stacey/index.md two frames
- T-104 [done] Cut 03 -> 03-chaos/index.md five frames
- T-116 [done] Show the sentences -> 03-chaos/index.md 'First change' includes build/03-chaos/rules.txt

#### W-042 issue [done] 04 and 05: the cut and the I3 beat

- T-105 [done] Trim the 05 exhibits -> oo at two methods, the types snippet in ports.py
- T-106 [done] Render the effect lines -> scripts.paths effects and build/05-how/effects.txt
- T-107 [done] Cut 04 -> 04-what/index.md four frames
- T-108 [done] Cut 05 -> 05-how/index.md six frames

#### W-043 issue [done] 06 and 07: the cut, the reveal and the Q&A

- T-109 [done] Trim the 06 exhibits -> core docstring, from-bits at the test, shell checkout at its body
- T-110 [done] Cut 06 -> 06-simple/index.md eight frames
- T-111 [done] Cut 07 -> 07-close/index.md two frames

#### W-044 issue [done] lengths: the snippet cap in make check

- T-112 [done] Count the included lines -> too_long in scripts/utils/lengths.py
- T-113 [done] Gate the lengths -> make lengths in make check

#### W-045 bug [done] deck bold renders regular: Adwaita Sans has no bold shape   (filed during T-097)

- T-114 [done] Give Adwaita Sans a bold face -> mainfontoptions and sansfontoptions in 00-frontmatter/meta.yaml

#### W-046 bug [done] count along prints its include fences instead of the doubling rows   (filed during T-101)

- T-115 [done] Fence the overlays -> 01-bits/index.md count along with raw latex begin and end fences

#### W-048 bug [done] 04 moves frame overfull: make overflow exits 1   (filed during T-108)

- T-118 [done] Fit the moves frame -> 04-what/index.md 'Bounded contexts, the moves' at moves.png height 60%

### E-006 [done] deck: talk day -- legible figures, true docs, the review on record

closed 2026-11-01 -- outcome: the talk-day deck: every figure and frame readable from the back of the room, every README matching its frames, the review and its plan recorded in docs/. -- ledger: ledgers/E-006.md

#### W-036 spike [done] talk: the 2026-11-01 review and the cut on record in docs/cut-40.md   (filed during W-034)

- T-089 [done] Write the remarks into the repository -> docs/cut-40.md
- T-090 [pruned] Draft the cut from the remarks -> docs/cut-40.md Plan section   [pruned: superseded: the developer approved the tree from the coordinator's report of 2026-11-01 and E-005 was filed directly; T-095 records the filed plan instead]
- T-095 [done] Record the filed plan -> docs/cut-40.md Plan section

#### W-037 bug [done] route.png: the 04->05 label covers its shaft and the zone caption, the 00->01 label touches box 01   (filed during W-034)

- T-091 [done] Compute the clearing offset -> route_label_offset(words, tail, head)
- T-092 [done] Place each label clear of its arrow -> route(out) calls route_label_offset

#### W-038 bug [done] epilogue chart: the 30 total overprints the chart title   (filed during W-035)

- T-093 [done] Compute the headroom -> bar_headroom(top)
- T-094 [done] Lift the axes over the totals -> stacked_bar sets ylim to bar_headroom(top) and drops the title
- T-121 [done] Place each thin-slice label beside its slice -> slice_label_point(x, bottom, value) and stacked_bar calling it

#### W-047 bug [done] 03-chaos README Done-when still names the 72 count   (filed during T-104)

- T-117 [done] Fix the Done-when -> 03-chaos/README.md names 2^9 = 512 only

#### W-049 bug [done] epilogue frame set in \tiny: the two-column layout fits only at 5pt

- T-119 [done] Wrap the two long lines -> teaser.txt and the fee-digital snippet with no line over 71 characters
- T-120 [done] Set the epilogue at \scriptsize -> 06-simple/index.md frame 'Epilogue: marketing's seventh if'

### E-007 [done] deck v2: the stage, the counter one bit at a time, the checkout changing on screen

closed 2026-11-02 -- outcome: make talk writes build/talk.pdf: 48 frames (1 title, 6 section, 41 content) that make budget accepts, STRICT=1 make talk passes with no stub left, and make check is green: board, ruff, pyright, pytest with one assert per test, ascii, lines, lengths, budget. -- ledger: ledgers/E-007.md

#### W-050 bug [done] 06 We counted them shows the whole suite's count

- T-122 [done] Restrict the counted run to the path tests -> build/06-simple/pytest-core.txt
- T-123 [done] Point the frame at the measured count -> 06-simple/index.md

#### W-051 bug [done] 06 the number and epilogue charts render small with overlapping labels

- T-124 [done] Reshape the two chart figures -> build/06-simple/paths.png wide, build/06-simple/epilogue.png near-square
- T-125 [done] Lay the two frames out in columns -> 06-simple/index.md

#### W-052 issue [done] skeleton: the new frame plan builds end to end on stubs

- T-126 [done] Add the artifact manifest, the stub writer and the strict guard -> make stubs
- T-127 [done] Add the frame budget helper -> scripts/utils/budget.py
- T-128 [done] Rewrite the eight index files to the frame plan -> 0*-*/index.md

#### W-053 spike [done] the pictogram rendering path: fontawesome5, the Font Awesome OTF or Hack Nerd Font

- T-129 [done] Probe the two renderers -> build/spike/fa-probe.pdf, build/spike/fa-probe.png
- T-130 [done] Record the decision -> 00-frontmatter/README.md

#### W-054 issue [done] one palette: actors and contexts with colours and pictograms shared by LaTeX and matplotlib

- T-131 [done] Add the actors and contexts datasets and the palette module -> scripts/utils/palette.py
- T-132 [done] Generate the actor macros -> build/00-frontmatter/actors.tex
- T-133 [done] Enforce the palette in figures -> scripts/utils/test_palette_usage.py

#### W-055 issue [done] 00: the business map and the agenda as a pictogram strip

- T-134 [done] Render the business map -> build/00-frontmatter/business-map.png
- T-135 [done] Replace the route dataset and render the agenda strip -> build/00-frontmatter/agenda.png
- T-136 [done] Finish the 00 frames -> 00-frontmatter/index.md

#### W-056 issue [done] 01: the storyboard, the function written one request at a time

- T-137 [done] Mark the steps in the exhibit and strip them on include -> 01-bits/s01_bits/chaos.py
- T-138 [done] Render the step diffs and bubbles -> build/01-bits/step-0.diff .. step-6.diff, bubble-0.txt .. bubble-8.txt
- T-139 [done] Finish the seven storyboard frames -> 01-bits/index.md frames 1 to 7
- T-186 [done] Wrap the bubble words to the bubble column -> build/01-bits/bubble-0.txt .. bubble-8.txt

#### W-057 issue [done] 01: past me's two tests and what coverage saw

- T-140 [done] Simplify past me's tests and restrict the coverage run -> build/01-bits/coverage.txt
- T-141 [done] Render the coverage view -> build/01-bits/coverage-view.png
- T-142 [done] Finish the tests frame -> 01-bits/index.md frame 8

#### W-058 issue [done] 01: finance found it, as a chart

- T-143 [done] Add the October dataset with pinned totals -> 01-bits/data/october.csv
- T-144 [done] Render the finance chart -> build/01-bits/finance.png, build/01-bits/finance.txt
- T-145 [done] Finish the finance frame with the squeeze -> 01-bits/index.md frame 9

#### W-059 issue [done] 01: the path nobody ran, and why nobody ran it

- T-146 [done] Render the marked grid image -> build/01-bits/grid.png
- T-147 [done] Render the doubling curve -> build/01-bits/doubling.png, build/01-bits/doubling.txt
- T-148 [done] Finish the red-test and grid frames -> 01-bits/index.md frames 10 and 11

#### W-060 issue [done] 02: the Stacey matrix as specified, radial with the Who diagonal

- T-149 [done] Add the zones and labels datasets and the matrix renderer -> build/02-stacey/stacey.png
- T-150 [done] Render the highlighted minimaps -> build/02-stacey/stacey-01.png .. stacey-06.png
- T-151 [done] Finish the 02 frames -> 02-stacey/index.md

#### W-061 spike [done] the source behind the BOOM label

- T-152 [done] Collect candidate sources -> 02-stacey/data/boom-sources.md
- T-153 [done] Record the decision and set the label -> 02-stacey/README.md, 02-stacey/data/labels.csv

#### W-062 issue [done] 03: the room as a journey, a log and a retro table

- T-154 [done] Replace the red cards with a dataset -> data/questions.csv
- T-155 [done] Render the retro table -> build/03-chaos/retro.txt
- T-156 [done] Draw the journey and write the room log -> build/03-chaos/diagrams/journey.png, 03-chaos/data/room.txt
- T-157 [done] Finish the 03 frames 1 to 3 -> 03-chaos/index.md

#### W-063 issue [done] 03: the explosion to 512 in the style of 01

- T-158 [done] Render the nine-bit panels -> build/03-chaos/grid-9.png
- T-159 [done] Extend the doubling curve to the room -> build/03-chaos/doubling-512.png
- T-160 [done] Finish the explosion frame -> 03-chaos/index.md frame 4

#### W-064 issue [done] the rules board, the artifact everyone sees from the room to the tests

- T-161 [done] Render the board per stage -> build/03-chaos/board.png, build/04-what/board.png, build/05-how/board.png, build/07-close/board.png
- T-162 [done] Place the board on four frames -> 03-chaos, 04-what, 05-how, 07-close index.md

#### W-065 issue [done] 04: the diff ladder begins, the checkout stays on screen

- T-163 [done] Add the staged checkouts with their tests -> 04-what/s04_what/checkout_fixed.py, 04-what/s04_what/checkout_v4.py
- T-164 [done] Render the colour-coded checkout -> build/04-what/colorcode.png
- T-165 [done] Render the diffs between stages -> build/04-what/fix.diff, build/04-what/v4.diff
- T-166 [done] Finish the 04 frames -> 04-what/index.md

#### W-066 issue [done] 05: the seam as the next edit of the same function

- T-167 [done] Add the stage-5 checkout with its tests -> 05-how/s05_how/checkout_v5.py
- T-168 [done] Render the v4-to-v5 diff -> build/05-how/v5.diff
- T-169 [done] Finish the 05 frames -> 05-how/index.md
- T-191 [done] Diff only the seam -> build/05-how/v5.diff

#### W-067 issue [done] one assert per test, enforced by the build for the exhibit tests too

- T-170 [done] Refactor the exhibit tests into one-assert functions and classes -> 01-bits/tests, 04-what/tests, 05-how/tests, 06-simple/tests
- T-171 [done] Lift the exhibit exemption from the assert gate -> conftest.py
- T-172 [done] Point the wounds run at the class names -> build/06-simple/wounds.txt

#### W-068 issue [done] 06: the last rung, the seam cut, the paths counted, the seventh if

- T-173 [done] Render the seventh-if diff -> build/06-simple/seventh.diff
- T-174 [done] Finish the 06 frames -> 06-simple/index.md

#### W-069 issue [done] lines and counter pinned to the plan

- T-175 [done] Add the counter helper -> scripts/utils/counter.py
- T-176 [done] Pin the deck's counters to the route -> scripts/utils/test_counter_plan.py

#### W-071 bug [done] 06 epilogue chart is width-capped in its 30% column, below 65% height, labels unreadable   (filed during T-125)

- T-178 [done] Wrap the fee-digital signature and give the chart a 40% column -> 06-simple/s06_simple/seventh.py, 06-simple/index.md

#### W-076 bug [done] 05 seam draws the three providers in the shell grey with no pictogram   (filed during T-133)

- T-183 [done] Colour the seam's ports by actor with their pictograms -> build/05-how/ports.png

#### W-077 bug [done] make check fails on a fresh build/: lengths and widths read stub files they do not build   (filed during T-134)

- T-184 [done] Run stubs before lengths and widths -> mk/deck.mk

#### W-078 bug [done] 05 effects listing prints the step markers of chaos.py   (filed during T-137)

- T-185 [done] Strip the step markers in effects_lines -> build/05-how/effects.txt

#### W-079 bug [done] 01 coverage view renders as an unreadable thumbnail on the tests frame   (filed during T-142)

- T-187 [done] Stack the coverage view and give it half the frame -> build/01-bits/coverage-view.png, 01-bits/index.md

#### W-080 bug [done] 01 grid frame: the grid image prints over the frame title   (filed during T-148)

- T-188 [done] Fit the grid frame under its title -> 01-bits/index.md

#### W-084 bug [done] 07 lost its Q&A bullets and notes in the skeleton rewrite   (filed during T-169)

- T-193 [done] Restore the 07 bullets and notes -> 07-close/index.md

#### W-085 bug [done] 06 epilogue: the Marketing badge prints over the frame title   (filed during T-174)

- T-194 [done] Fit the epilogue under its title -> 06-simple/index.md

### E-008 [done] backlog after deck v2: the build guards, the rebuild rule and the cleanups

closed 2026-11-02 -- outcome: make check is green on main with ruff format --check among its gates; make stubs writes epoch-dated stubs, make lengths warns on a missing include, make overflow names a frame shifted over its title, make artifacts redraws ports.png after a cast.csv edit, and scripts hold a named spread_apart test, a top-level icons import in palette.py and no growth_chart. -- ledger: ledgers/E-008.md

#### W-070 issue [done] chart labels: spread_apart gets its own test   (filed during T-124)

- T-177 [done] Pin spread_apart with a test -> scripts/utils/test_paths.py

#### W-072 bug [done] make lengths crashes on an include of a missing file the filter would render as a STUB   (filed during T-128)

- T-179 [done] Skip a missing include with a warning -> scripts/check_lengths.py

#### W-073 bug [done] 05 ports.png is not rebuilt when data/cast.csv changes   (filed during T-131)

- T-180 [done] List the cast as a prerequisite of the seam -> 05-how/section.mk

#### W-074 bug [done] make check passes on a tree that ruff format would change   (filed during T-132)

- T-181 [done] Format the tree and gate it in make check -> mk/python.mk

#### W-075 issue [done] scripts.utils.style imports palette, so palette imports icons lazily   (filed during T-132)

- T-182 [done] Break the style-palette import cycle -> scripts/utils/style.py, scripts/utils/palette.py

#### W-081 bug [pruned] make overflow passes a frame whose content beamer shifts over the title   [pruned: hypothesis refuted by T-189's probe; the real case is a frame with under 1ex slack whose [T]-column image reaches the title]   (filed during T-148)

- T-189 [pruned] Catch a frame shifted over its title -> scripts/utils/overflow.py   [pruned: hypothesis refuted by T-189's probe; the real case is a frame with under 1ex slack whose [T]-column image reaches the title]

#### W-082 issue [done] remove the dead growth chart and its paths subcommand   (filed during T-156)

- T-190 [done] Remove growth_chart and the growth subcommand -> scripts/paths.py

#### W-083 bug [done] make stubs leaves a stub newer than a new rule's inputs, so make skips the real build   (filed during T-168)

- T-192 [done] Write stubs with an epoch mtime -> scripts/utils/stubs.py

#### W-087 bug [done] make overflow passes a frame that fits its text height but whose [T]-column image reaches the title   (filed during T-189)

- T-196 [done] Print each frame's slack in the overflow build -> 00-frontmatter/slack-probe.tex
- T-197 [done] Name a frame under the slack threshold -> scripts/utils/overflow.py

### E-009 [done] backlog after v0.8.0: the strict include test and the in-tree bytecode

closed 2026-11-02 -- outcome: make check is green on main with a named test of read_include's strict failure, and make clean-python leaves no __pycache__ folder under scripts or the sections. -- ledger: ledgers/E-009.md

#### W-086 issue [done] lengths: the STRICT failure on a missing include gets its own test   (filed during T-179)

- T-195 [done] Pin the strict failure of read_include -> scripts/utils/test_widths.py

#### W-088 bug [done] stale in-tree __pycache__ keeps a grep Check red after a symbol is removed   (filed during T-190)

- T-198 [done] Remove the in-tree bytecode in make clean-python -> mk/python.mk

### E-010 [done] deck v3: the 2026-11-02 review -- story gaps, figures, code on slides, build and data

closed 2026-11-02 -- outcome: make talk writes build/talk.pdf: 48 pages (1 title, 6 templated section beats, 41 content frames with 01 at 12 and 02 at 2) carrying every remark of the 2026-11-02 review, recorded in docs/deck-v3.md, with make check, overflow, widths and lengths green. -- ledger: ledgers/E-010.md

#### W-089 issue [done] 00: the section beats and the record

- T-199 [done] Record the review remarks -> docs/deck-v3.md
- T-200 [done] Highlight one stop on the agenda strip -> build/00-frontmatter/agenda-01.png .. agenda-06.png
- T-201 [done] Template the section page -> 00-frontmatter/preamble.tex and build/00-frontmatter/beats.tex
- T-202 [done] Recaption the opening frames -> 00-frontmatter/index.md

#### W-090 issue [done] 01: the storyboard opens the loop

- T-203 [done] Move the birth of the bug to step 3 -> 01-bits/s01_bits/chaos.py and 01-bits/data/bubbles.csv
- T-204 [done] Strip the asides and the headers from the step diffs -> build/01-bits/step-0.diff .. step-6.diff
- T-205 [done] Open the loop on its own frame -> 01-bits/index.md, data/budget.csv and scripts/utils/test_counter_plan.py
- T-225 [done] Fit the step-3 diff to its column -> 01-bits/index.md

#### W-091 issue [done] 01: measured captions on the evidence frames

- T-206 [done] Run the two green tests from their own file -> 01-bits/tests/test_planted_bug.py and build/01-bits/coverage-summary.txt
- T-207 [done] Title the finance chart with its totals -> build/01-bits/finance.png and 01-bits/index.md
- T-208 [done] Legend the grid and pin the bug cell -> build/01-bits/grid.png and 01-bits/tests/test_tested_paths.py

#### W-092 issue [done] 02: the dispute as bubbles and one map

- T-209 [done] Trim the matrix -> build/02-stacey/stacey-02.png and 02-stacey/data/labels.csv
- T-210 [done] Bubble the two positions and the question -> 02-stacey/data/bubbles.csv and build/02-stacey/bubble-0.txt .. bubble-2.txt
- T-211 [done] Rewrite the 02 frames -> 02-stacey/index.md and data/budget.csv
- T-226 [done] Fit the matrix at 85% height -> 02-stacey/index.md and scripts/utils/stacey.py

#### W-093 issue [done] 03: the room readable from the back

- T-212 [done] Redraw the journey legibly -> build/03-chaos/diagrams/journey.png
- T-213 [done] Colour the speakers of an exhibit block -> 00-frontmatter/filters/speakers.lua and 03-chaos/index.md
- T-214 [done] Head the waiting board columns -> build/03-chaos/board.png

#### W-094 issue [done] 04: the homes without noise

- T-215 [done] Caption the stage diffs instead of headers -> scripts/utils/stagediff.py
- T-216 [done] Show the q3 decision on the dispute frame -> build/04-what/dispute.txt and 04-what/index.md
- T-217 [done] Show only the added body on the homes frame -> 04-what/index.md and 04-what/section.mk

#### W-095 issue [done] 05: the seam without guards

- T-218 [done] Hide the exhaustiveness guards from the ports diff -> build/05-how/v5.diff
- T-219 [done] Recaption the I3 frame and define the seam -> 05-how/index.md

#### W-096 issue [done] 06: the measured frames

- T-220 [done] Refactor the 64-path tests onto two fixtures -> 06-simple/tests/test_core_paths.py and 06-simple/index.md
- T-221 [done] Measure the eight worlds -> 06-simple/s06_simple/worlds.py and build/06-simple/worlds.txt
- T-222 [done] Keep the seventh signature on one line -> 06-simple/s06_simple/seventh.py and build/06-simple/seventh.diff
- T-223 [done] Legend the small slices of the number chart -> build/06-simple/paths.png

#### W-097 issue [done] 07: the repository link

- T-224 [done] Link the repository on the Q&A frame -> 07-close/index.md

### E-011 [done] the v0.9.0 backlog and the layout gates

closed 2026-11-02 -- outcome: make check runs widths and overflow and is green on main with the homes diff at scriptsize, no contexts subcommand, a clean number chart and the repository URL on one line. -- ledger: ledgers/E-011.md

#### W-098 issue [done] 04: the homes diff at a readable size   (filed during T-217)

- T-227 [done] Wrap the coupon line and raise the homes diff -> 04-what/s04_what/checkout_v4.py and 04-what/index.md

#### W-099 issue [done] remove the unused contexts table and its paths subcommand   (filed during T-217)

- T-228 [done] Remove contexts_table and the contexts subcommand -> scripts/utils/paths.py and scripts/paths.py

#### W-100 issue [done] 06: the number chart's core label and doubled shell entry   (filed during T-223)

- T-229 [done] Fit the core label and merge the shell entry -> scripts/utils/paths.py and scripts/utils/test_paths.py

#### W-101 issue [done] 07: the repository URL breaks across two lines   (filed during T-224)

- T-230 [done] Set the repository URL on one line -> 07-close/index.md

#### W-102 issue [done] make check runs widths and overflow

- T-231 [done] Add widths and overflow to the checks -> mk/deck.mk and README.md

### E-012 [done] Deck v4: the review of 2026-11-02 landed -- action titles, one diff renderer, the R1/R2 thread, the seam, the close, EUR

closed 2026-11-02 -- outcome: make talk builds build/talk.pdf at 50 pages (43 content frames per data/budget.csv), green on make check, every remark of docs/deck-v4.md landed by a work item or pruned by a Decision. -- ledger: ledgers/E-012.md

#### W-103 issue [done] EUR: every amount reads EUR

- T-232 [done] Record the review and the frame plan -> docs/deck-v4.md
- T-233 [done] Rename the money helper -> eur() in 04-what/s04_what/money.py and its importers
- T-234 [done] Rewrite the amounts -> EUR in the data, the exhibits, the notes and the READMEs

#### W-104 issue [done] one diff renderer: -, +, \~, ... under a version caption; the storyboard whole

- T-235 [done] Mark changed and elided lines -> snippet_diff emits \~ and ... in scripts/utils/stagediff.py
- T-236 [done] Show the whole function per step -> step_view in scripts/utils/storyboard.py
- T-237 [done] Colour the prefixes -> 00-frontmatter/filters/diffs.lua and the preamble macros
- T-238 [done] Fit the whole function -> the 01, 04, 05 and 06 includes with their captions

#### W-105 issue [done] 00: the map as a flow of policies, the agenda explained, the icons guarded

- T-239 [done] Outline the core and label the flows -> business_map in scripts/utils/stage.py
- T-240 [done] Colour the stops by band and explain the marks -> agenda_strip and stacey.draw
- T-241 [done] Put the path glyph by each counter and in the footer -> stage.py, palette.actors_tex, 00-frontmatter/preamble.tex, 00-frontmatter/index.md
- T-242 [done] Choose the icon file by its glyphs -> font_file in scripts/utils/icons.py

#### W-106 issue [done] 01: the storyboard counts policies

- T-243 [done] Count the tally -> tally_line in scripts/utils/storyboard.py and build/01-bits/tally-N.txt
- T-244 [done] Let the storyboard open on a measurement frame -> counter.storyboard_ok and test_counter_plan
- T-245 [done] Write the measurement frame and the seven policy frames -> 01-bits/index.md, data/budget.csv, 01-bits/README.md, scripts/utils/test_counter_plan.py

#### W-107 issue [done] 01: checkout done, the two tests, the six-bit number

- T-246 [done] Price the next if -> next_doubling in scripts/utils/paths.py and build/01-bits/next.txt
- T-247 [done] Rework the three frames -> 01-bits/index.md

#### W-108 issue [done] 01: finance R1 against R2, and its test

- T-248 [done] Name the readings on the chart -> finance.draw legend and title, the frame caption and notes
- T-249 [done] Show the finance test as a plain test with its run -> 01-bits/tests/test_planted_bug.py, 01-bits/section.mk, 01-bits/index.md, data/artifacts.csv

#### W-109 issue [done] 02: R1 and R2 above the line, the decision frame

- T-250 [done] Tag the readings -> a tag column in the bubbles csv and the bubble head
- T-251 [done] Enlarge the zone texts -> scripts/utils/stacey.py
- T-252 [done] Write the two frames -> 02-stacey/index.md

#### W-110 issue [done] 03: the journey as the customer certainty, the retro subdomains

- T-253 [done] Weigh the drops -> mood(steps, questions) in scripts/utils/figures.py
- T-254 [done] Add the subdomain -> data/questions.csv, Question and retro_table
- T-255 [done] Caption the room and the retro -> 03-chaos/index.md

#### W-111 issue [done] 03: the honest count panels and the board continuity

- T-256 [done] Name the worlds -> world_name(bits, rules) and the grid_panels titles
- T-257 [done] Head the board by the route -> headers(route) in scripts/utils/board.py
- T-258 [done] Caption the two frames -> 03-chaos/index.md

#### W-112 issue [done] 04: tactical to strategic in five frames

- T-259 [done] Split the legend -> legend_groups and the two columns of colorcode()
- T-260 [done] Trim the b2 comment -> 04-what/s04_what/shipping.py and 06-simple/s06_simple/seventh.py
- T-261 [done] Rewrite the five frames -> 04-what/index.md, 04-what/section.mk, data/artifacts.csv, data/budget.csv, 04-what/README.md

#### W-113 issue [done] 04: the moves frame, core = the What, shell = the How

- T-262 [done] Group the bands -> band_groups and the brackets of moves_figure
- T-263 [done] Widen the frame -> 04-what/index.md

#### W-114 issue [done] 05: the test first

- T-264 [done] Write the I3 test against v4 -> 05-how/tests/test_i3.py
- T-265 [done] Capture the run -> build/05-how/i3-run.txt in 05-how/section.mk and data/artifacts.csv
- T-266 [done] Reorder 05 -> 05-how/index.md and 05-how/README.md

#### W-115 issue [done] 05: the ports answer with values, the moves table explained

- T-267 [done] Return confirmed -> Accepted(total, confirmed) in 05-how/s05_how/checkout_v5.py
- T-268 [done] Name the moves -> the table and the ports title in 05-how/index.md

#### W-116 issue [done] 06: cut along the seam

- T-269 [done] Diff the seam and trim the run -> build/06-simple/seam.diff and pytest-core-summary.txt in 06-simple/section.mk
- T-270 [done] Write the seam frame and merge the 192 frames -> 06-simple/index.md, scripts/utils/test_counter_plan.py, 06-simple/README.md

#### W-117 issue [done] 06: the wounds as a post-mortem

- T-271 [done] Add the decision and the principle -> data/incidents.csv, Incident, data/README.md
- T-272 [done] Render the post-mortem -> postmortem_table, scripts.paths postmortem, 06-simple/section.mk, data/artifacts.csv
- T-273 [done] Show it -> 06-simple/index.md

#### W-118 issue [done] 07: the call to action and the thank-you

- T-274 [done] Write the two frames -> 07-close/index.md, data/budget.csv, 07-close/README.md
- T-275 [done] Count the pages -> build/talk.pdf at 50 and README.md

#### W-119 issue [done] action titles on every content frame, topic titles on the section pages

- T-276 [done] Write the titles -> the Planned titles section of docs/deck-v4.md
- T-277 [done] Retitle 01, 02 and 03 -> their index.md and scripts/utils/test_counter_plan.py
- T-278 [done] Retitle 04, 05, 06 and 07 -> their index.md and the counter plan
- T-279 [done] Gate the title length -> scripts/utils/titles.py, scripts/check_titles.py, make titles in mk/deck.mk

#### W-128 bug [done] 07: the call to action lacks 'reach out with your own checkout'   (filed during T-274)

- T-289 [done] Reword the third bullet -> 07-close/index.md

### E-013 [done] Deck v4 polish: the nine findings of the E-012 verification landed before the dry run

closed 2026-11-03 -- outcome: make talk writes build/talk.pdf with the seam diff in context, the step frames filled at scriptsize, the board headers in their cells, the I3 test plain, the moves notes on the cut and no orphan artifact, while a zones change rebuilds the agenda, pytest's exit is captured and every overflow line names its frame. -- ledger: ledgers/E-013.md

#### W-120 bug [done] the agenda strips are not rebuilt when 02-stacey/data/zones.csv changes   (filed during T-240)

- T-280 [done] List the zones as a prerequisite -> 00-frontmatter/section.mk

#### W-121 issue [done] 01: the step code at scriptsize in a wider column   (filed during T-245)

- T-281 [done] Widen the step code column -> 01-bits/index.md

#### W-122 bug [done] 01: the bug-run rule masks pytest's exit with || true   (filed during T-249)

- T-282 [done] Accept only a failed test -> the bug-run rule in 01-bits/section.mk

#### W-123 bug [done] the board's first header overflows its cell   (filed during T-257)

- T-283 [done] Break the first header -> scripts/utils/board.py

#### W-124 issue [done] 04: the moves notes still speak of the board   (filed during T-263)

- T-284 [done] Rewrite the moves notes -> 04-what/index.md

#### W-125 bug [done] 05: the I3 snippet shows its xfail decorator   (filed during T-264)

- T-285 [done] Move the i3 marker below the decorator -> 05-how/tests/test_i3.py

#### W-126 issue [done] 05: effects.txt is built but no slide includes it   (filed during T-266)

- T-286 [done] Remove the effects artifact -> 05-how/section.mk and data/artifacts.csv

#### W-127 bug [done] 06: the seam diff shows every line changed, against its caption   (filed during T-269)

- T-287 [done] Dedent after the start cut -> snippet_diff in scripts/utils/stagediff.py
- T-288 [done] Align v5's matches with the shell -> 05-how/s05_how/checkout_v5.py

#### W-129 bug [done] make overflow names no frame when a title wraps   (filed during T-278)

- T-290 [done] Read a wrapped frame title -> scripts/utils/overflow.py

### W-003 bug [done] (standalone) Slide artifacts carry a PytestConfigWarning about stats_file

closed 2026-10-30 -- outcome: Given a clean build/, When make deliverable runs, Then build/06-simple/pytest.txt holds no PytestConfigWarning line. -- ledger: ledgers/W-003.md

- T-006 [done] Register the pytest stats ini options for every run -> grep counts 0 PytestConfigWarning in build/06-simple/pytest.txt

### W-004 bug [done] (standalone) 00-frontmatter/README.md still names xelatex and the DejaVu fonts

closed 2026-10-30 -- outcome: Given 00-frontmatter/README.md, When grep -E 'xelatex|DejaVu' runs over it, Then it finds no line. -- ledger: ledgers/W-004.md

- T-007 [done] Update 00-frontmatter/README.md to lualatex and the Adwaita fonts -> grep counts 0 lines naming xelatex or DejaVu

### W-005 bug [done] (standalone) Slide artifacts carry the pytest slowest-durations block

closed 2026-10-30 -- outcome: Given a clean build/, When make deliverable runs, Then build/06-simple/pytest.txt holds no slowest durations line. -- ledger: ledgers/W-005.md

- T-008 [done] Drop the durations report from the two slide pytest recipes -> grep counts 0 slowest durations lines in build/06-simple/pytest.txt

### W-006 issue [done] (standalone) Slide pytest recipes repeat the pyproject addopts

closed 2026-10-30 -- outcome: Given the repository, When grep -c import-mode 01-bits/section.mk 06-simple/section.mk runs, Then it prints 0 for each file. -- ledger: ledgers/W-006.md

- T-009 [done] Keep the pytest options in pyproject only -> grep counts 0 import-mode lines in 06-simple/section.mk

### W-017 spike [done] (standalone) storyline: which of the developer's principles, data and ranked visuals the talk adopts

closed 2026-10-30 -- outcome: Given docs/storyline.md, When the developer reads its Plan section, Then it names the root, its work items and the conflicts with E-002 to decide. -- ledger: ledgers/W-017.md

- T-035 [done] Write the suggestions into the repository -> docs/storyline.md
- T-036 [done] Draft the root from the suggestions -> docs/storyline.md Plan section

### W-032 bug [done] (standalone) route.png: the arrowheads hide under the widened boxes

closed 2026-11-01 -- outcome: Given the deck, When make talk runs, Then every arrow of build/00-frontmatter/route.png ends at its box edge with its head visible. -- ledger: ledgers/W-032.md

- T-080 [done] Compute the arrow ends -> route_arrow_ends(start, end, half_w, half_h)
- T-081 [done] Draw the arrows to the edges -> route(out) calls route_arrow_ends

### W-033 bug [done] (standalone) epilogue chart: the bar labels read too small

closed 2026-11-01 -- outcome: Given the deck, When make talk runs, Then every label of the 'Epilogue, the cost in a chart' slide reads at 12 points or larger. -- ledger: ledgers/W-033.md

- T-083 [done] Enlarge the bar labels -> stacked_bar labels at fontsize 12
- T-084 [done] Look at the epilogue slide -> local/state/epilogue.png read

### W-034 bug [done] (standalone) route.png: the move labels cover the short arrows

closed 2026-11-01 -- outcome: Given the deck, When make talk runs, Then every arrow of build/00-frontmatter/route.png ends at its box edge with its head visible. -- ledger: ledgers/W-034.md

- T-085 [done] Compute the label point -> route_label_point(tail, head, offset)
- T-086 [done] Place the labels off the arrows -> route(out) calls route_label_point

### W-035 bug [done] (standalone) epilogue chart: the labels shrink to about 7 points on the slide

closed 2026-11-01 -- outcome: Given the deck, When make talk runs, Then every label of the 'Epilogue, the cost in a chart' slide reads at 12 points or larger. -- ledger: ledgers/W-035.md

- T-087 [done] Draw every chart text at 22 points -> stacked_bar texts at fontsize 22
- T-088 [done] Look at the epilogue slide at 22 points -> local/state/epilogue-22.png read

## Diagram
```mermaid
flowchart TD
  E014["E-014 doing: Deck v5: one legend of three kinds, the Stacey overview, compact diffs with their tests"]
  E014 --> W130["W-130 issue done: 00: one legend of three kinds, the map redrawn"]
  W130 --> T291["T-291 done: Add the kinds to the palette -> data/contexts.csv with kind and owner, palette.kind_style"]
  W130 --> T292["T-292 done: Draw the kinds on the business map -> stage.business_map with inner bands, the tax box and grey providers"]
  W130 --> T293["T-293 done: Caption and note frame 2 -> 00-frontmatter/index.md notes on the two arrow sides"]
  W130 --> T330["T-330 done: Restore the developer's context labels -> data/contexts.csv labels as pasted"]
  E014 --> W131["W-131 issue doing: 03/06: the kinds in the retro, the post-mortem and the epilogue"]
  W131 --> T294["T-294 doing: Reassign the retro subdomains -> data/questions.csv, the title and footnote of frame 24 -- ACTIVE LEAF"]
  W131 --> T295["T-295 todo: Add the kind column to the post-mortem -> data/incidents.csv kind, paths.postmortem_table"]
  W131 --> T296["T-296 todo: Close the epilogue on the supporting line -> 06-simple/index.md caption of frame 46"]
  E014 --> W132["W-132 issue todo: 04: the moves and the colour code under the kinds"]
  W132 --> T297["T-297 todo: Group the moves by kind -> figures.band_groups reads the kinds, the checkout box outlined grey"]
  W132 --> T298["T-298 todo: Name the kinds in the colour-code legend -> colorcode.legend_groups with a kind per home"]
  W132 --> T299["T-299 todo: Recaption frames 28 and 32 -> 04-what/index.md captions and notes"]
  E014 --> W133["W-133 issue todo: 00/02: the Stacey overview on page 3, the plain matrix on page 20"]
  W133 --> T300["T-300 todo: Draw the quarters with ticks and a plain mode -> stacey.draw(plain=) with 0 to 100 axis ticks"]
  W133 --> T301["T-301 todo: Draw the movement -> stacey.draw(arrows=), route.csv 02 in Complex, the overview and plain artifacts"]
  W133 --> T302["T-302 todo: Replace the agenda frame with the overview -> 00-frontmatter/index.md and 02-stacey/index.md"]
  E014 --> W134["W-134 issue todo: 03: the new view after the room"]
  W134 --> T303["T-303 todo: Put the matrix beside the honest count -> 03-chaos/index.md page 25 with stacey-03 right"]
  W134 --> T304["T-304 todo: Tie the board to the explosion -> 03-chaos/index.md page 26 caption"]
  E014 --> W135["W-135 issue todo: 01: how the paths are counted, as a block diagram"]
  W135 --> T305["T-305 todo: Count the paths of a block graph -> scripts/utils/counting.py with paths_of and the figure"]
  W135 --> T306["T-306 todo: Show the diagram on the counting frame -> 01-bits/index.md page 5"]
  E014 --> W136["W-136 issue todo: 01: the storyboard as compact +/- diffs with the length in the tally"]
  W136 --> T307["T-307 todo: Add the compact diff mode -> stagediff.snippet_diff(compact=True) and diffs.lua on ---"]
  W136 --> T308["T-308 todo: Render the steps as compact diffs -> storyboard.step_view and tally_line with the length"]
  W136 --> T309["T-309 todo: Fit the seven frames -> 01-bits/index.md pages 6 to 12 sizes and caps"]
  E014 --> W137["W-137 issue todo: 01: the tests under each request, page 14 in step"]
  W137 --> T310["T-310 todo: Build the tests of each step -> storyboard.step_test(source, n) computed from the step's checkout"]
  W137 --> T311["T-311 todo: Write and show the test diffs -> build/01-bits/test-0..6.diff under each bubble"]
  E014 --> W138["W-138 issue todo: 01: finance finds it, the condition, the test"]
  W138 --> T312["T-312 todo: Relabel the finance chart -> finance.LEGEND expected, received, missing"]
  W138 --> T313["T-313 todo: Foreshadow the conflict on the done frame -> 01-bits/index.md page 13"]
  W138 --> T314["T-314 todo: Run the thread memo, condition, test -> 01-bits/index.md pages 15 and 16"]
  E014 --> W139["W-139 issue todo: 01: the grid that doubles, the badge named"]
  W139 --> T315["T-315 todo: Draw the growing grids -> coverage_view.grid_growth and build/01-bits/grid-growth.png"]
  W139 --> T316["T-316 todo: Reword the frame -> 01-bits/index.md page 17 with the strip and the badge named"]
  E014 --> W140["W-140 issue todo: 02: two readings, two tests that cannot both pass"]
  W140 --> T317["T-317 todo: Write the two readings as tests -> 02-stacey/tests/test_readings.py registered in pyproject.toml"]
  W140 --> T318["T-318 todo: Show each test beside its bubble -> 02-stacey/index.md page 19"]
  E014 --> W141["W-141 issue todo: 03: why the order was replayed, where the room clashed"]
  W141 --> T319["T-319 todo: Scale the certainty axis -> figures.journey with the ticks certain, unsure, lost"]
  W141 --> T320["T-320 todo: Say why the order was replayed -> 03-chaos/index.md page 22 caption and notes"]
  W141 --> T321["T-321 todo: Mark the conflicts in the room -> speakers.lua bold on '! ', room.txt marked, page 23 concluding"]
  E014 --> W142["W-142 issue todo: 04: the fix is v7, the contexts v8, each under its tally"]
  W142 --> T322["T-322 todo: Tally any version -> storyboard.tally_line(version, policies, paths, tests) and scripts.paths tally"]
  W142 --> T323["T-323 todo: Label the fix v6 to v7 with its test -> 04-what/section.mk fix.diff compact, tally-7.txt, page 29"]
  W142 --> T324["T-324 todo: Version the contexts checkout -> tally-8.txt and 04-what/index.md page 31"]
  E014 --> W143["W-143 issue todo: 05: v8 to v9 compact, every snippet with its home and its test"]
  W143 --> T325["T-325 todo: Compact the v5 diff with its tally -> 05-how/section.mk labels checkout v8 to v9, tally-9.txt"]
  W143 --> T326["T-326 todo: Caption where each snippet goes and what tests it -> 05-how/index.md pages 35 to 38"]
  E014 --> W144["W-144 issue todo: 06: v9 to v10 compact, the long snippet cut, every snippet with its home and its test"]
  W144 --> T327["T-327 todo: Compact the seam and seventh diffs with the tally -> 06-simple/section.mk labels checkout v9 to v10, tally-10.txt"]
  W144 --> T328["T-328 todo: Cut the long test snippet -> 06-simple/tests/test_core_paths.py from-bits at 14 lines, no cap"]
  W144 --> T329["T-329 todo: Caption where each snippet goes and what tests it -> 06-simple/index.md pages 41 to 46"]
  W145["W-145 bug todo, standalone: Figure rules miss the palette files, so a colour or label change leaves stale figures"]
  W145 --> T331["T-331 todo: Add the palette prerequisites -> every figure rule in the NN-*/section.mk files"]
  classDef doing fill:#fff3bf,stroke:#b58900,color:#000;
  classDef blocked fill:#ffe3e3,stroke:#c92a2a,color:#000;
  classDef done fill:#e6ffed,stroke:#2b8a3e,color:#000;
  classDef todo fill:#f8f9fa,stroke:#868e96,color:#000;
  classDef pruned fill:#f1f3f5,stroke:#adb5bd,color:#000;
  class E014,W131,T294 doing
  class W130,T291,T292,T293,T330 done
  class T295,T296,W132,T297,T298,T299,W133,T300,T301,T302,W134,T303,T304,W135,T305,T306,W136,T307,T308,T309,W137,T310,T311,W138,T312,T313,T314,W139,T315,T316,W140,T317,T318,W141,T319,T320,T321,W142,T322,T323,T324,W143,T325,T326,W144,T327,T328,T329,W145,T331 todo
```
