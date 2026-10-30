# Board -- chaos-to-simple
record: local
open path: W-017   | blocked: 0 | todo roots: 0 | done: 53 | pruned: 1

## Tree

```text
W-017  spike  [doing]    (standalone) storyline: which of the developer's principles, data and ranked visuals the talk adopts   (filed during T-033) -- T-035 [done], T-036 [done]
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

## Diagram
```mermaid
flowchart TD
  W017["W-017 spike doing, standalone: storyline: which of the developer's principles, data and ranked visuals the talk adopts"]
  W017 --> T035["T-035 done: Write the suggestions into the repository -> docs/storyline.md"]
  W017 --> T036["T-036 done: Draft the root from the suggestions -> docs/storyline.md Plan section"]
  classDef doing fill:#fff3bf,stroke:#b58900,color:#000;
  classDef blocked fill:#ffe3e3,stroke:#c92a2a,color:#000;
  classDef done fill:#e6ffed,stroke:#2b8a3e,color:#000;
  classDef todo fill:#f8f9fa,stroke:#868e96,color:#000;
  classDef pruned fill:#f1f3f5,stroke:#adb5bd,color:#000;
  class W017 doing
  class T035,T036 done
```
