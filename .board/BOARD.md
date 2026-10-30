# Board -- chaos-to-simple
record: local
open path: E-001 > W-002   | blocked: 0 | todo roots: 2 | done: 6 | pruned: 0

## Tree

```text
E-001         [doing]    Deck infrastructure: the drafts become one beamer PDF through make
  W-001  issue  [done]     The front door: base Makefile, python layer and the 3.14 toolchain -- T-001 [done], T-002 [done]
  W-002  issue  [doing]    The deck builds: mk/deck.mk, lualatex and the installed fonts -- T-003 [done], T-004 [done], T-005 [done]
W-003  bug    [todo]     (standalone) Slide artifacts carry a PytestConfigWarning about stats_file   (filed during T-004) -- T-006 [todo]
W-004  bug    [todo]     (standalone) 00-frontmatter/README.md still names xelatex and the DejaVu fonts   (filed during T-004) -- T-007 [todo]
```

## Diagram
```mermaid
flowchart TD
  E001["E-001 doing: Deck infrastructure: the drafts become one beamer PDF through make"]
  E001 --> W001["W-001 issue done: The front door: base Makefile, python layer and the 3.14 toolchain"]
  W001 --> T001["T-001 done: Write the base Makefile, the python layer and the 3.14 toolchain files -> make check prints [DONE] all checks passed"]
  W001 --> T002["T-002 done: Move the helper tests beside their modules under the one-assert conftest -> make test M=model K=test_bars_follow_the_inventory passes"]
  E001 --> W002["W-002 issue doing: The deck builds: mk/deck.mk, lualatex and the installed fonts"]
  W002 --> T003["T-003 done: Add the diagram fallback helper scripts/utils/diagram.py with its edge test -> make test M=edge K=test_write_placeholder passes"]
  W002 --> T004["T-004 done: Add mk/deck.mk with the deck targets, lualatex and the installed fonts -> make deliverable prints [DONE] deliverables built: deliverable-talk"]
  W002 --> T005["T-005 done: Rewrite the README build section and add CLAUDE.md with the gate deviations -> grep finds ## Gate deviations in CLAUDE.md"]
  W003["W-003 bug todo, standalone: Slide artifacts carry a PytestConfigWarning about stats_file"]
  W003 --> T006["T-006 todo: Register the pytest stats ini options for every run -> grep counts 0 PytestConfigWarning in build/06-simple/pytest.txt"]
  W004["W-004 bug todo, standalone: 00-frontmatter/README.md still names xelatex and the DejaVu fonts"]
  W004 --> T007["T-007 todo: Update 00-frontmatter/README.md to lualatex and the Adwaita fonts -> grep counts 0 lines naming xelatex or DejaVu"]
  classDef doing fill:#fff3bf,stroke:#b58900,color:#000;
  classDef blocked fill:#ffe3e3,stroke:#c92a2a,color:#000;
  classDef done fill:#e6ffed,stroke:#2b8a3e,color:#000;
  classDef todo fill:#f8f9fa,stroke:#868e96,color:#000;
  classDef pruned fill:#f1f3f5,stroke:#adb5bd,color:#000;
  class E001,W002 doing
  class W001,T001,T002,T003,T004,T005 done
  class W003,T006,W004,T007 todo
```
