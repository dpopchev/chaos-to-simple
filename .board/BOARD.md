# Board -- chaos-to-simple
record: local
open path: E-003 > W-024   | blocked: 0 | todo roots: 2 | done: 82 | pruned: 1

## Tree

```text
E-003         [doing]    The talk runs one loop: found documents, built counts, figures in one style, the believed line flipped
  W-018  issue  [done]     06-simple: the wounds close by name in a run built from incidents.csv -- T-037 [done], T-038 [done], T-039 [done], T-040 [done]
  W-019  issue  [done]     00-frontmatter, 01-bits, 05-how, 06-simple: the exhibits as found documents -- T-041 [done], T-042 [done], T-043 [done]
  W-020  issue  [done]     01-bits: the doubling with faces -- T-044 [done], T-045 [done], T-046 [done]
  W-021  issue  [done]     lines: the believed / learned pair -- T-047 [done], T-048 [done], T-049 [done]
  W-022  issue  [done]     01-bits: the two-if tree -- T-050 [done], T-051 [done], T-052 [done]
  W-023  issue  [done]     00-frontmatter: the route on the map -- T-053 [done], T-054 [done], T-055 [done]
  W-024  issue  [doing]    03-chaos: what it felt like vs what it was -- T-056 [done], T-057 [done], T-058 [done]
  W-025  issue  [todo]     04-what: the bits move, none deleted -- T-059 [todo], T-060 [todo], T-061 [todo], T-062 [todo]
  W-026  issue  [todo]     03-chaos: the example map before and after the room -- T-063 [todo], T-064 [todo], T-065 [todo]
  W-027  issue  [todo]     05-how: the core and the shell with three ports -- T-066 [todo], T-067 [todo], T-068 [todo]
  W-028  issue  [todo]     06-simple: the epilogue as stacked bars -- T-069 [todo], T-070 [todo]
W-029  bug    [todo]     (standalone) deck: four slides run past the frame bottom   (filed during T-040) -- T-071 [todo], T-072 [todo], T-073 [todo]
W-030  issue  [todo]     (standalone) 00-frontmatter: the route boxes name their sections   (filed during T-055) -- T-074 [todo], T-075 [todo]
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

## Diagram
```mermaid
flowchart TD
  E003["E-003 doing: The talk runs one loop: found documents, built counts, figures in one style, the believed line flipped"]
  E003 --> W018["W-018 issue done: 06-simple: the wounds close by name in a run built from incidents.csv"]
  W018 --> T037["T-037 done: Add the incidents -> data/incidents.csv and load_incidents"]
  W018 --> T038["T-038 done: Select the wounds by name -> wounds_selector and scripts.paths wounds"]
  W018 --> T039["T-039 done: Run the wounds -> build/06-simple/wounds.txt"]
  W018 --> T040["T-040 done: Show the wounds -> 06-simple/index.md includes build/06-simple/wounds.txt"]
  E003 --> W019["W-019 issue done: 00-frontmatter, 01-bits, 05-how, 06-simple: the exhibits as found documents"]
  W019 --> T041["T-041 done: Rewrite the I1 and I3 exhibits -> 01-bits/data/incident.txt, 05-how/data/incident.txt"]
  W019 --> T042["T-042 done: Write the message and the teaser -> 00-frontmatter/data/message.txt, 06-simple/data/teaser.txt"]
  W019 --> T043["T-043 done: Show the found documents -> 00-frontmatter/index.md, 01-bits/index.md, 06-simple/index.md"]
  E003 --> W020["W-020 issue done: 01-bits: the doubling with faces"]
  W020 --> T044["T-044 done: Add the week -> data/cast.csv week column and CastRow.week"]
  W020 --> T045["T-045 done: Render the doubling -> doubling_table and scripts.paths doubling"]
  W020 --> T046["T-046 done: Show the doubling -> build/01-bits/doubling.txt on Count along"]
  E003 --> W021["W-021 issue done: lines: the believed / learned pair"]
  W021 --> T047["T-047 done: Read the pair -> Line(section, believed, learned) and data/lines.csv"]
  W021 --> T048["T-048 done: Put the believed lines on the slides -> NN-*/index.md and 07-close/index.md"]
  W021 --> T049["T-049 done: Check the pair -> missing() names an absent believed line"]
  E003 --> W022["W-022 issue done: 01-bits: the two-if tree"]
  W022 --> T050["T-050 done: Pin the leaves -> TREE_LEAVES in scripts/utils/figures.py"]
  W022 --> T051["T-051 done: Draw the tree -> tree(out) and scripts.figures tree"]
  W022 --> T052["T-052 done: Show the tree -> build/01-bits/tree.png on Four paths"]
  E003 --> W023["W-023 issue done: 00-frontmatter: the route on the map"]
  W023 --> T053["T-053 done: Add the route -> data/route.csv and load_route"]
  W023 --> T054["T-054 done: Place the route on the map -> route_layout(stops)"]
  W023 --> T055["T-055 done: Show the map -> 00-frontmatter/section.mk and 02-stacey/index.md"]
  E003 --> W024["W-024 issue doing: 03-chaos: what it felt like vs what it was"]
  W024 --> T056["T-056 done: Count the growth -> growth(cast)"]
  W024 --> T057["T-057 done: Draw the growth -> growth_chart(out, points) and scripts.paths growth"]
  W024 --> T058["T-058 done: Show the growth -> build/03-chaos/growth.png before The honest count"]
  E003 --> W025["W-025 issue todo: 04-what: the bits move, none deleted"]
  W025 --> T059["T-059 todo: Add the context palette -> context_colour(name) in scripts/utils/style.py"]
  W025 --> T060["T-060 todo: Count the moves -> moves(rules)"]
  W025 --> T061["T-061 todo: Draw the moves -> moves_figure(out, moves) and scripts.figures moves"]
  W025 --> T062["T-062 todo: Show the moves -> build/04-what/moves.png on Bounded contexts"]
  E003 --> W026["W-026 issue todo: 03-chaos: the example map before and after the room"]
  W026 --> T063["T-063 todo: Count the cards -> card_counts in scripts/utils/examples.py"]
  W026 --> T064["T-064 todo: Draw the map -> example_map(out, before, after) and scripts.figures example-map"]
  W026 --> T065["T-065 todo: Show the map -> build/03-chaos/example_map.png on The six questions"]
  E003 --> W027["W-027 issue todo: 05-how: the core and the shell with three ports"]
  W027 --> T066["T-066 todo: Read the ports -> ports_of(rules)"]
  W027 --> T067["T-067 todo: Draw the seam -> seam(out, ports) and scripts.figures seam"]
  W027 --> T068["T-068 todo: Show the seam -> 05-how/section.mk and The ports"]
  E003 --> W028["W-028 issue todo: 06-simple: the epilogue as stacked bars"]
  W028 --> T069["T-069 todo: Build the two bars -> epilogue_bars(rules, seventh)"]
  W028 --> T070["T-070 todo: Show the bars -> build/06-simple/epilogue.png on the epilogue"]
  W029["W-029 bug todo, standalone: deck: four slides run past the frame bottom"]
  W029 --> T071["T-071 todo: Name the overfull frames -> scripts/utils/overflow.py and make overflow"]
  W029 --> T072["T-072 todo: Fit the 01-bits frames -> 01-bits/index.md"]
  W029 --> T073["T-073 todo: Fit the 05-how frames -> 05-how/index.md"]
  W030["W-030 issue todo, standalone: 00-frontmatter: the route boxes name their sections"]
  W030 --> T074["T-074 todo: Add the names -> data/route.csv name column and Stop.name"]
  W030 --> T075["T-075 todo: Label the boxes -> stop_label(stop) used by route(out)"]
  classDef doing fill:#fff3bf,stroke:#b58900,color:#000;
  classDef blocked fill:#ffe3e3,stroke:#c92a2a,color:#000;
  classDef done fill:#e6ffed,stroke:#2b8a3e,color:#000;
  classDef todo fill:#f8f9fa,stroke:#868e96,color:#000;
  classDef pruned fill:#f1f3f5,stroke:#adb5bd,color:#000;
  class E003,W024 doing
  class W018,T037,T038,T039,T040,W019,T041,T042,T043,W020,T044,T045,T046,W021,T047,T048,T049,W022,T050,T051,T052,W023,T053,T054,T055,T056,T057,T058 done
  class W025,T059,T060,T061,T062,W026,T063,T064,T065,W027,T066,T067,T068,W028,T069,T070,W029,T071,T072,T073,W030,T074,T075 todo
```
