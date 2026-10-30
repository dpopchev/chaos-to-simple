# Storyline principles, data, exhibits and ranked visuals

From: the developer, 2026-10-30, mid-burn of E-002 (T-033 doing). A suggestion list for
the inbox: filed `todo` after the doing Task closes, ordered by the developer.

## The item it would become

A root (Epic, standalone of E-002 so the burn does not start it) that puts the talk on
one loop and one palette, with the must and should visuals below drawn in Python.

- Hypothesis: does every incident section (01, 03, 05, 06 and the epilogue) run the same
  loop -- exhibit, instinct, count, move, proof -- with each exhibit a found document from
  a text file, each count from a csv through make artifacts, each move a figure drawn
  by scripts.figures in one palette where a bit keeps its colour from 01 to 06?
- Criterion sketch: Given the repository, When make talk runs, Then each must visual in
  the table below is in the deck, built from its source, and make lines checks a
  believed / learned pair per section.
- Overlaps with E-002 to decide at its close: data/cast.csv (adds week; words differ),
  data/lines.csv of T-024 (believed, learned columns), 01-bits/data/incident.txt and
  05-how/data/incident.txt (the exhibit texts below differ: 41 refunds, six working days),
  the message of T-015, the route of T-014 (route.csv labels).
- Developer note on renderers: even where the table says Mermaid, draw it in Python
  (W-016's one deck style); focus on must and should, the rest are suggestions.

## Principles (verbatim)

Evidence before explanation. Every resolution starts with something the world sent (a
report, a log, a chat line), shown as a found document before past me says a word. The
audience should spot the problem a beat before he does.

One loop, five times. Exhibit, instinct, count, move, proof. Same order in 01, 03, 05, 06
and the epilogue; the repetition is what makes it feel like a journey instead of six
topics.

Counts by the build, shapes by hand. Numbers come from *.csv through make artifacts;
diagrams are Mermaid in diagrams/; a diagram never carries a number a test does not pin.
(Superseded on the renderer by the developer's Decision on E-002: figures in Python.)

One palette. Pricing, shipping, tax, shell, tangled: five colours defined once and used in
every chart, Mermaid classDef and table, so a bit keeps its colour from the cast table in
01 to the epilogue bar in 06.

```text
flowchart LR
  X[Exhibit<br/>what the world sent] --> I[Instinct<br/>what past me did first]
  I --> C[Count<br/>what the number says]
  C --> M[Move<br/>the pattern: x becomes +]
  M --> P[Proof<br/>a run, by name]
  P -. next incident .-> X
```

## Slide kinds

| Slide kind | Looks like | Example |
|---|---|---|
| Exhibit | monospace text block, header line From/To/Subject or a chat timestamp | finance report, support summary, the message |
| Instinct | code past me wrote, numbered | the two tests, class Checkout |
| Count | a generated table or the footer counter moving | doubling.txt, counts.txt, 45 vs 44 |
| Move | a Mermaid diagram | the seam, bits moving to homes |
| Proof | real pytest output, names visible | wounds.txt, pytest.txt |

## Data

cast.csv

```text
bit,week,requested_by,words,fragment
b0,3,Marketing,"10 BGN off with the autumn code",order.coupon_valid_until
b1,5,Loyalty,"members get 10%, obviously after the coupon",order.member
b2,6,Logistics,"free shipping from 50",subtotal >= Decimal(50)
b3,6,Logistics,"abroad is 20, not 5",order.international
b4,9,Marketing,"gift wrap for the campaign, just one more if",order.gift_wrap
b5,10,Accounting,"a VAT ID means no VAT",order.vat_id is None
s0,,nobody,"the provider answers",charge(total)
s1,,nobody,"the warehouse answers",reserve(order.lines)
s2,,nobody,"the mailer answers",send(order.email, total)
```

incidents.csv

```text
id,week,told_in,closed_in,closed_by,kind,cost
I1,14,01,06,test_free_shipping_after_discount,rule,"1,214 orders, 6,070 BGN"
I2,15,02,04,rules.csv b2,decision,one meeting nobody had called
I3,18,05,06,test_out_of_stock_rejects_before_payment,effect,41 refunds in six working days
```

lines.csv

```text
section,believed,learned
01,A green badge means tested,Coverage counts edges; bugs live in combinations. Count the paths before you trust the badge.
02,A bug is fixed with a test,Before fixing the How check whether the What is agreed.
03,Counting makes it worse,You cannot shrink a count you have not made. The bigger number is the first good news.
04,Naming is cosmetics,Every if was somebody's sentence. Write it down give it a home pass values between homes.
05,A class will keep it tidy,A method that does and tells hides a bit. Separate asking from doing; make every answer a value.
06,One more if is cheap,Decisions in the core effects in the shell. The next if costs 8 not 512.
```

Note: the learned lines above drop commas the sections now carry (02, 04, 06); one
spelling must win before make lines compares them.

route.csv: section, zone, counter, move -- 01 chaos 64 count; 03 complex 512 agree;
04 what 512 name; 05 how 512 separate; 06 simple 72 split. Feeds the route diagram labels
and the closing chart.

## The exhibits (fictional, verbatim)

- 00, the message: #dev, Thursday 21:40. past me: Checkout is done. Six rules, all tested,
  coverage 100%. Shipping tonight so the campaign starts Monday. marketing: you are the
  best. one more thing next week, small, just one if.
- 01, finance: Subject: shipping cost, October. Shipping charged to customers: 0 BGN on
  1,214 domestic orders with under 50 BGN of goods. Our cost 5 BGN each, 6,070 BGN. All
  1,214 used the autumn coupon. No customer has complained. Was this intended?
- 05, support: Subject: charged, no parcel. 41 customers paid for books the warehouse did
  not have. The warehouse answered "out of stock"; it is in the log; nobody reads the log.
  Refunds take six working days.
- 01 teaser and 06 epilogue, marketing: digital books launch in two weeks. no shipping for
  those, obviously. just one more if?

## Ranked visuals (draw in Python; must and should first)

| Rank | Visual | What it shows | Source | Renderer | Where |
|---|---|---|---|---|---|
| must | Doubling with faces: week, who, asked for, bits, paths | the human story and the arithmetic on one slide | cast.csv | scripts.paths doubling | 01 count along |
| must | Two-if tree in the rule's bits, tested leaves green, I1 leaf red | edges covered, paths not | hand | Mermaid | 01 zoom-in |
| must | Exhibits as found documents | evidence first | text files per section | include | 00, 01, 05, 06 |
| must | Believed / learned pair | the inner flip | lines.csv | last slide of each section; six rows in 07 | all |
| must | Wounds proof run: pytest -v -k over closed_by names | closure by name, in real output | incidents.csv | section.mk | 06 |
| should | Bits move, none deleted: 9 bits from checkout() to pricing 2, shipping 3, tax 1, shell 3 | the contract made visible | rules.csv | Mermaid sankey-beta (fallback: flowchart) | 04 or 06 |
| should | Route on the map: quadrants as subgraphs, edges labelled with the incident and the move | how each discovery moves him | route.csv labels | Mermaid flowchart | 00 agenda, 02 |
| should | What it felt like vs what it was: bits (1..6) and paths (2..64) over weeks, counts annotated | the antagonist's curve | cast.csv | matplotlib line chart | 01 or 03 |
| should | Example map before and after the room: cards coloured yellow, blue, green, red; 6 blue and 0 red, then 9 blue and 6 red | the bits nobody wrote down appearing | rules, examples, questions | matplotlib | 03 |
| should | Core and shell with three ports, arrows labelled with the sum types | the seam | hand | Mermaid | 05 or 06 |
| should | Epilogue stacked bars, before and after the seventh if; only the shipping segment grows | +8, visibly local | rules + seventh.csv | existing stacked_bar | 06 |
| nice | 60 -> 50 -> 45 against 60 -> 54 -> 44 | the hidden bit | hand | Mermaid stateDiagram | 05 |
| nice | Counter over the talk: 64, 512, 72 | it got worse before it got better | route.csv | matplotlib | 07 |
| nice | Commit log generated from the cast: six commits, six faces, two tests at the end | just one more if, in git | cast.csv | scripts.paths log | 01 |

## The two-if tree, the one piece worth getting exactly right

```text
flowchart TD
  A{coupon valid?} -->|no| B0{free shipping earned?}
  A -->|yes| B1{free shipping earned?}
  B0 -->|no| L00["00  tested: 40, no coupon -> fee 5"]
  B0 -->|yes| L01["01  never ran: 60, no coupon -> fee 0, happens to be right"]
  B1 -->|no| L10["10  never ran: 55 + coupon -> fee 0, should be 5 (I1)"]
  B1 -->|yes| L11["11  tested: 100 + coupon -> fee 0"]
  classDef tested fill:#cfe8cf,stroke:#2e7d32
  classDef bug fill:#f8d0cc,stroke:#c62828
  classDef never fill:#eeeeee,stroke:#757575
  class L00,L11 tested
  class L10 bug
  class L01 never
```

## Conflicts with E-002

Each place the note above differs from the repository at main commit 6469c17 (E-002
closed and tagged v0.2.0), with the file and the two versions. The note's version is
the suggestion; the repository's version is what the deck builds today. Each one needs
the developer's pick before the root is filed (T-036).

### C1. data/cast.csv: the week column

- Note: header `bit,week,requested_by,words,fragment`; weeks b0 3, b1 5, b2 6, b3 6,
  b4 9, b5 10; s0, s1, s2 empty.
- Repository: header `bit,requested_by,words,fragment`; no week column.

### C2. data/cast.csv: the requested_by, words and fragment cells

| Bit | Field | Note | Repository |
|---|---|---|---|
| b0 | fragment | `order.coupon_valid_until` | `coupon_valid_until >= today` |
| b1 | requested_by | `Loyalty` | `Loyalty program` |
| b1 | words | `members get 10%, obviously after the coupon` | `members get 10%; obviously after the coupon` |
| b1 | fragment | `order.member` | `if order.member` |
| b2 | words | `free shipping from 50` | `free shipping from 50 (from what? nobody asked)` |
| b2 | fragment | `subtotal >= Decimal(50)` | `if subtotal >=` |
| b3 | fragment | `order.international` | `if order.international` |
| b4 | requested_by | `Marketing` | `Marketing, two weeks before launch` |
| b4 | words | `gift wrap for the campaign, just one more if` | `just one more if` |
| b4 | fragment | `order.gift_wrap` | `if order.gift_wrap` |
| b5 | words | `a VAT ID means no VAT` | `companies with a VAT ID pay no VAT` |
| b5 | fragment | `order.vat_id is None` | `if order.vat_id is None` |
| s0 | requested_by | `nobody` | `Nobody` |
| s0 | words | `the provider answers` | `the provider answers; nobody wrote the answer down` |
| s1 | requested_by | `nobody` | `Nobody` |
| s1 | words | `the warehouse answers` | `the warehouse answers; nobody wrote the answer down` |
| s2 | requested_by | `nobody` | `Nobody` |
| s2 | words | `the mailer answers` | `the mailer answers; nobody wrote the answer down` |
| s2 | fragment | `send(order.email, total)` | `send(order.email` |

The b0 words (`10 BGN off with the autumn code`), the b3 words (`abroad is 20, not 5`),
the b5 requested_by (`Accounting`) and the s0, s1 fragments agree.

### C3. data/lines.csv (T-024): the columns and the section keys

- Note: header `section,believed,learned`; section keys `01` .. `06`; a believed line per
  section (`A green badge means tested` .. `One more if is cheap`).
- Repository: header `section,line`; section keys `01-bits`, `02-stacey`, `03-chaos`,
  `04-what`, `05-how`, `06-simple`; no believed line.

### C4. data/lines.csv (T-024): the commas of the learned lines

| Section | Note (learned) | Repository (line) |
|---|---|---|
| 02 | `Before fixing the How check whether the What is agreed.` | `Before fixing the How, check whether the What is agreed.` |
| 04 | `Write it down give it a home pass values between homes.` | `Write it down, give it a home, pass values between homes.` |
| 06 | `Decisions in the core effects in the shell. The next if costs 8 not 512.` | `Decisions in the core, effects in the shell. The next if costs 8, not 512.` |

Sections 01, 03 and 05 carry the same text in both.

### C5. 01-bits/data/incident.txt: the finance exhibit (I1)

- Note: an email, `Subject: shipping cost, October.`; "Shipping charged to customers:
  0 BGN on 1,214 domestic orders with under 50 BGN of goods. Our cost 5 BGN each, 6,070
  BGN. All 1,214 used the autumn coupon. No customer has complained. Was this
  intended?"
- Repository: a report headed `FINANCE REPORT -- incident I1, free shipping under the
  threshold`, field lines Period ("the month closed on the last audit"), Orders ("1,214
  shipped free with a goods value under 50 BGN"), Shipping due ("5 BGN each, 1,214 x 5 =
  6,070 BGN not charged"), Common factor ("every one of the 1,214 orders used a
  coupon"), Complaints ("none; no customer wrote in, the loss was found in the books"),
  Test status ("the checkout had 100% test coverage"), Cause ("under investigation by
  engineering"), Action ("finance asks for the shipping rule to be explained in
  writing").
- Differ: the form (email vs report), the period (October vs the last audit), domestic
  (note only), the autumn coupon vs a coupon, the closing question (note) vs the test
  status, cause and action lines (repository). The numbers 1,214, 5 BGN and 6,070 BGN
  agree.

### C6. 05-how/data/incident.txt: the support exhibit (I3)

- Note: `Subject: charged, no parcel.`; "41 customers paid for books the warehouse did
  not have. The warehouse answered "out of stock"; it is in the log; nobody reads the
  log. Refunds take six working days." incidents.csv repeats it: I3 cost `41 refunds in
  six working days`, week 18.
- Repository: headed `Incident I3: cards charged for parcels we did not have`, "Support
  summary, week of 2026-10-23, shop orders"; "Impact: 37 support tickets opened this
  week"; "A refund took about a week to reach the customer's card, so most people wrote
  in twice"; "out of stock" written to "a log line that nobody read. No alert, no
  dashboard"; "Next step: the order must be refused before the card is charged."
- Differ: 41 customers vs 37 support tickets; six working days vs about a week; the
  subject line; books (note) vs parcels (repository); the next-step line (repository
  only).

### C7. 00-frontmatter/index.md: the message of T-015

- Note: "#dev, Thursday 21:40. past me: Checkout is done. Six rules, all tested,
  coverage 100%. Shipping tonight so the campaign starts Monday. marketing: you are the
  best. one more thing next week, small, just one if."
- Repository: `#dev, Thursday 21:40 -- past me: Checkout done. 100% coverage. Shipping
  tonight.`
- Differ: the note adds six rules, all tested, the campaign on Monday and the marketing
  reply that plants "just one if"; the repository has past me's line alone.

### C8. scripts/utils/figures.py: the route of T-014

- Note: a route.csv (section, zone, counter, move) over five sections: 01 chaos 64
  count; 03 complex 512 agree; 04 what 512 name; 05 how 512 separate; 06 simple 72
  split; the edges labelled with the incident and the move, quadrants as subgraphs.
  incidents.csv tells I2 in 02 (told_in 02).
- Repository: no route.csv; `SECTIONS` in scripts/utils/figures.py holds eight boxes
  with a counter and no zone or move: 00 pride ?, 01 bits 64, 02 which problem 64, 03
  the room 512, 04 homes 512, 05 the seam 512, 06 simple 72, 07 six lines 72;
  `INCIDENTS` puts I1 on the arrow into 01, I2 into 03, I3 into 05.
- Differ: five sections vs eight; zone and move labels (note only); I2 told in 02 vs
  drawn into 03. The counters of 01, 03, 04, 05 and 06 agree.

## Plan

The root W-017 proposes, drafted at main 6469c17 for the developer to agree before
anything is filed. Ids are the next free ones (`board next-id`: E-003, W-018); Task ids
are given at filing. Every Task brief below assumes the leading option of each conflict
(C1..C8, end of this section); a different pick rewrites the named Task's Action before
it is filed. A Task that changes a closed E-002 Task's output names that Task (scope
rule 4). Lookups: `board knowledge --search` for palette found no match; exhibit, lines,
route, cast and incident found only E-001's exhibit-code Decision, E-002's Deviation
that filed W-017, and E-002's closed Tasks named below.

### Epic E-003: The talk runs one loop

- Title: `The talk runs one loop: found documents, built counts, figures in one style,
  the believed line flipped`
- Hypothesis: Does `make talk` build a deck in which 01, 05, 06 and the epilogue each
  run the loop exhibit, instinct, count, move, proof -- the exhibit a found document
  from a text file, the count from a csv through `make artifacts`, the move a figure
  drawn in Python in the one deck style -- and every section closes on a believed /
  learned pair that `make lines` checks?
- Outcome: `make talk` builds the deck with the five must and six should visuals of
  this note, each built from its source by `make artifacts`, and `make lines` checks a
  believed / learned pair per section.
- Acceptance criteria:
  - AC1 Given data/incidents.csv, When make talk runs, Then the 06 slide "The wounds
    close by name" shows build/06-simple/wounds.txt with each closed_by test PASSED by
    name -> W-018
  - AC2 Given the text files under NN-*/data/, When make talk runs, Then 00, 01, 05 and
    06 each show their found document included from its text file -> W-019
  - AC3 Given data/cast.csv with its week column, When make talk runs, Then the 01 slide
    "Count along" shows build/01-bits/doubling.txt, six rows from week 3 to week 10
    ending at 6 bits and 64 paths -> W-020
  - AC4 Given data/lines.csv with believed and learned, When make lines runs, Then it
    passes only when each section's index.md and 07-close/index.md carry both lines of
    that section -> W-021
  - AC5 Given 01-bits/s01_bits/two_ifs.py, When make talk runs, Then the 01 slide "Four
    paths, the same two tests" shows build/01-bits/tree.png with leaves 00 and 11
    green, 10 red as I1 and 01 grey -> W-022
  - AC6 Given data/route.csv, When make talk runs, Then the 00 agenda and the 02 route
    slide show build/00-frontmatter/route.png with each section in its zone and each
    arrow labelled with its move -> W-023
  - AC7 Given data/cast.csv with its week column, When make talk runs, Then 03 shows
    build/03-chaos/growth.png, bits 1..6 and paths 2..64 over the weeks -> W-024
  - AC8 Given data/rules.csv, When make talk runs, Then the 04 slide "Bounded contexts"
    shows build/04-what/moves.png, nine bits leaving checkout() into pricing 2,
    shipping 3, tax 1 and shell 3 -> W-025
  - AC9 Given data/rules.csv, data/examples.csv and 03-chaos/data/questions.md, When
    make talk runs, Then 03 shows build/03-chaos/example_map.png, 6 blue and 0 red
    cards before the room, 9 blue and 6 red after -> W-026
  - AC10 Given data/rules.csv, When make talk runs, Then the 05 slide "The ports" shows
    build/05-how/ports.png, the core and three ports, each arrow labelled with its sum
    type -> W-027
  - AC11 Given data/rules.csv and data/seventh.csv, When make talk runs, Then the 06
    epilogue shows build/06-simple/epilogue.png, only the shipping segment growing from
    8 to 16 and the totals 22 and 30 -> W-028

### Order

1. W-018 the wounds run: the thin skeleton, csv to `make artifacts` to pytest to a
   slide, the loop's Proof step, on tests that exist today.
2. W-019 the exhibits: the loop's first step, text files only, and the conflicts C5,
   C6, C7 it settles.
3. W-020 the doubling: adds the week column every time visual reads (C1, C2).
4. W-021 the believed / learned pair: the last must; touches every section's last
   slide, so it lands after the exhibits and the doubling settle 01.
5. W-022 the two-if tree: the last must, a figure from the exhibit code alone.
6. W-023 the route on the map: the first should; reads data/incidents.csv of W-018.
7. W-024 what it felt like: reads the week column of W-020.
8. W-025 the bits move: adds the context palette W-028 reuses.
9. W-026 the example map: 03's figure, from three files that exist today.
10. W-027 the ports: 05's figure, from rules.csv's shell rows.
11. W-028 the epilogue bars: reuses stacked_bar and W-025's palette.

The must visuals come first (W-018..W-022), then the should ones (W-023..W-028). Each
work item lands a slide `make talk` shows; none lands only internals.

### Work items

#### W-018 06-simple: the wounds close by name in a run built from incidents.csv

- Kind: issue. Reasoning: deductive -- the two test closed_by names exist on main
  (06-simple/tests/test_examples.py: test_free_shipping_after_discount;
  06-simple/tests/test_shell.py: test_out_of_stock_rejects_before_payment).
- Hypothesis: Does `make artifacts` write build/06-simple/wounds.txt as `pytest -v`
  output selected by the closed_by names of data/incidents.csv, every one PASSED?
- Criterion: Given data/incidents.csv, When make talk runs, Then the 06 slide "The
  wounds close by name" shows build/06-simple/wounds.txt with
  test_free_shipping_after_discount and test_out_of_stock_rejects_before_payment
  PASSED by name.
- Files: data/incidents.csv (new), data/README.md, scripts/utils/paths.py,
  scripts/utils/test_paths.py, scripts/paths.py, 06-simple/section.mk,
  06-simple/index.md
- Tasks:
  1. `Add the incidents -> data/incidents.csv and load_incidents`
     - Action: write data/incidents.csv as in the note's Data section (C6 leading:
       I3's cost as the note gives it); in scripts/utils/paths.py a frozen dataclass
       Incident (id, week, told_in, closed_in, closed_by, kind, cost) and
       load_incidents(path); test RED first in scripts/utils/test_paths.py on a
       fixture file; a data/README.md row.
     - Output: test_load_incidents_reads_every_column passing.
     - Check: `make test K=test_load_incidents -> [DONE] tests passed`
  2. `Select the wounds by name -> wounds_selector and scripts.paths wounds`
     - Action: wounds_selector(incidents) joins with " or " the closed_by values that
       start with `test_` (I2's `rules.csv b2` is no test and is left out);
       `python -m scripts.paths wounds --incidents data/incidents.csv` prints it.
     - Output: test_wounds_selector_skips_a_closed_by_that_is_no_test passing.
     - Check: `make test K=test_wounds_selector -> [DONE] tests passed`
  3. `Run the wounds -> build/06-simple/wounds.txt`
     - Action: in 06-simple/section.mk a rule running `pytest 06-simple/tests -v -k`
       with the selector of Task 2, depending on data/incidents.csv and the 06 tests;
       append it to ARTIFACTS.
     - Output: build/06-simple/wounds.txt.
     - Check: `make build/06-simple/wounds.txt && grep -q 'test_out_of_stock_rejects_before_payment PASSED' build/06-simple/wounds.txt -> exit 0`
  4. `Show the wounds -> 06-simple/index.md includes build/06-simple/wounds.txt`
     - Action: the slide "The wounds close by name" includes the run under the two
       snippets (amends T-029's slide).
     - Output: the include line in 06-simple/index.md.
     - Check: `grep -q 'include=build/06-simple/wounds.txt' 06-simple/index.md -> exit 0`

#### W-019 00-frontmatter, 01-bits, 05-how, 06-simple: the exhibits as found documents

- Kind: issue. Reasoning: abductive -- the likeliest reason the incidents read as
  topics is that past me explains before the audience sees the evidence; the smallest
  test is the deck with each incident opening on the document alone.
- Hypothesis: Does each of 00, 01, 05 and 06 open its incident on a found document
  included from a text file, with every number in it equal to data/incidents.csv?
- Criterion: Given the text files under NN-*/data/, When make talk runs, Then 00, 01,
  05 and 06 each show their found document included from its text file.
- Files: 00-frontmatter/data/message.txt (new), 00-frontmatter/index.md,
  01-bits/data/incident.txt, 01-bits/index.md, 05-how/data/incident.txt,
  06-simple/data/teaser.txt (new), 06-simple/index.md, scripts/utils/test_paths.py
- Tasks:
  1. `Rewrite the I1 and I3 exhibits -> 01-bits/data/incident.txt, 05-how/data/incident.txt`
     - Action: C5 and C6 leading: the note's finance and support exhibits verbatim
       (amends T-011's and T-021's outputs); a test RED first in
       scripts/utils/test_paths.py reading data/incidents.csv (W-018) and both
       exhibits: every number of I1's and I3's cost stands in its exhibit (1,214 and
       6,070 in 01; 41 in 05).
     - Output: test_exhibits_carry_the_incident_costs passing.
     - Check: `make test K=test_exhibits_carry_the_incident_costs -> [DONE] tests passed`
  2. `Write the message and the teaser -> 00-frontmatter/data/message.txt, 06-simple/data/teaser.txt`
     - Action: C7 leading: the note's 00 message verbatim; the note's "01 teaser and 06
       epilogue" marketing line verbatim.
     - Output: the two text files.
     - Check: `grep -q 'just one if' 00-frontmatter/data/message.txt && grep -q 'digital books' 06-simple/data/teaser.txt -> exit 0`
  3. `Show the found documents -> 00-frontmatter/index.md, 01-bits/index.md, 06-simple/index.md`
     - Action: "Checkout done" includes message.txt in place of its one-line block
       (amends T-015's slide; still four slides); "Parked for section 03" in 01 and
       "Epilogue: marketing's seventh if" in 06 include teaser.txt.
     - Output: the three include lines.
     - Check: `test "$(grep -l 'include=06-simple/data/teaser.txt' 01-bits/index.md 06-simple/index.md | wc -l)" -eq 2 && grep -q 'include=00-frontmatter/data/message.txt' 00-frontmatter/index.md -> exit 0`

#### W-020 01-bits: the doubling with faces

- Kind: issue. Reasoning: deductive -- paths are 2^bits (scripts/utils/paths.py
  tangled), and the cast rows carry who and what was asked.
- Hypothesis: Does `make artifacts` write build/01-bits/doubling.txt from
  data/cast.csv, one row per core bit with week, who, asked for, bits and paths, ending
  at 6 bits and 64 paths?
- Criterion: Given data/cast.csv with its week column, When make talk runs, Then the
  01 slide "Count along" shows build/01-bits/doubling.txt, six rows from week 3 to
  week 10 ending at 6 bits and 64 paths.
- Files: data/cast.csv, data/README.md, scripts/utils/paths.py,
  scripts/utils/test_paths.py, scripts/paths.py, 01-bits/section.mk, 01-bits/index.md
- Tasks:
  1. `Add the week -> data/cast.csv week column and CastRow.week`
     - Action: C1 leading: the note's week values, the repository's other cells (C2
       leading); CastRow gains week (empty for s0..s2); the fixture of
       test_cast_row_reads_every_column gains the column first (RED); data/README.md
       row updated.
     - Output: test_cast_row_reads_every_column passing with the week.
     - Check: `make test K=test_cast_row_reads_every_column -> [DONE] tests passed`
  2. `Render the doubling -> doubling_table and scripts.paths doubling`
     - Action: doubling_table(cast) in scripts/utils/paths.py: the b-rows in order,
       columns week, who, asked for, bits, paths; `python -m scripts.paths doubling
       --cast data/cast.csv --out <file>`; tests RED first, one assert each.
     - Output: test_doubling_last_row_is_six_bits_64_paths passing.
     - Check: `make test K=test_doubling -> [DONE] tests passed`
  3. `Show the doubling -> build/01-bits/doubling.txt on "Count along"`
     - Action: a rule in 01-bits/section.mk, appended to ARTIFACTS; "Count along"
       includes it after the six clicks (the nine-slide format of T-013 stays).
     - Output: build/01-bits/doubling.txt and its include line.
     - Check: `make build/01-bits/doubling.txt && grep -q 'include=build/01-bits/doubling.txt' 01-bits/index.md -> exit 0`

#### W-021 lines: the believed / learned pair

- Kind: issue. Reasoning: deductive -- scripts/check_lines.py already checks a line in
  its section and in 07; the pair adds one column to the same check.
- Hypothesis: Does `make lines` fail when a section or 07 lacks that section's
  believed line, as it fails today for the learned one?
- Criterion: Given data/lines.csv with believed and learned, When make lines runs, Then
  it passes only when each section's index.md and 07-close/index.md carry both lines
  of that section.
- Files: data/lines.csv, data/README.md, scripts/utils/lines.py,
  scripts/utils/test_lines.py, 01-bits/index.md, 02-stacey/index.md,
  03-chaos/index.md, 04-what/index.md, 05-how/index.md, 06-simple/index.md,
  07-close/index.md
- Tasks:
  1. `Read the pair -> Line(section, believed, learned) and data/lines.csv`
     - Action: C3 and C4 leading: header `section,believed,learned`, the repository's
       keys and commas, the note's believed lines; load_lines reads both; missing()
       still compares learned, so `make lines` stays green; test RED first.
     - Output: test_load_lines_reads_believed_and_learned passing.
     - Check: `make test K=test_load_lines_reads_believed_and_learned -> [DONE] tests passed`
  2. `Put the believed lines on the slides -> NN-*/index.md and 07-close/index.md`
     - Action: each section's line slide (01: "Parked for section 03") gets its
       believed line above the learned one; 07's first slide lists six rows
       `believed -> learned` (amends T-024's slide).
     - Output: the believed lines in the seven index.md files.
     - Check: `grep -q 'A green badge means tested' 07-close/index.md -> exit 0`
  3. `Check the pair -> missing() names an absent believed line`
     - Action: missing() checks believed and learned in the section and in 07; test
       RED first in scripts/utils/test_lines.py; data/README.md row.
     - Output: test_missing_names_an_absent_believed_line passing.
     - Check: `make test K=test_missing_names_an_absent_believed_line -> [DONE] tests passed`

#### W-022 01-bits: the two-if tree

- Kind: issue. Reasoning: deductive -- 01-bits/s01_bits/two_ifs.py ship() computes
  each leaf; the two tests of test_two_ifs.py cover 00 and 11.
- Hypothesis: Does a figure drawn from leaves pinned against ship() show the four
  paths, two tested, one I1 and one never ran?
- Criterion: Given 01-bits/s01_bits/two_ifs.py, When make talk runs, Then the 01 slide
  "Four paths, the same two tests" shows build/01-bits/tree.png with leaves 00 and 11
  green, 10 red as I1 and 01 grey.
- Files: scripts/utils/figures.py, scripts/utils/test_figures.py, scripts/figures.py,
  01-bits/section.mk, 01-bits/index.md
- Tasks:
  1. `Pin the leaves -> TREE_LEAVES in scripts/utils/figures.py`
     - Action: the four leaves of the note's tree (subtotal, coupon, fee shown, state
       tested / bug / never); a test RED first: each fee equals ship(subtotal, coupon)
       minus the goods.
     - Output: test_tree_leaves_match_ship passing.
     - Check: `make test K=test_tree_leaves_match_ship -> [DONE] tests passed`
  2. `Draw the tree -> tree(out) and scripts.figures tree`
     - Action: tree(out) in the deck style, green / red / grey by state, the note's
       labels; `python -m scripts.figures tree --out <png>`.
     - Output: test_tree_writes_a_png passing.
     - Check: `make test K=test_tree_writes_a_png -> [DONE] tests passed`
  3. `Show the tree -> build/01-bits/tree.png on "Four paths"`
     - Action: a rule in 01-bits/section.mk, appended to ARTIFACTS; the slide shows
       the figure beside two_ifs.txt.
     - Output: build/01-bits/tree.png and its image line.
     - Check: `make build/01-bits/tree.png && grep -q 'build/01-bits/tree.png' 01-bits/index.md -> exit 0`

#### W-023 00-frontmatter: the route on the map

- Kind: issue. Reasoning: deductive -- the zones of scripts/utils/figures.py ZONES and
  the counters of SECTIONS exist; route.csv makes them data.
- Hypothesis: Does a route drawn from data/route.csv place each section in its Stacey
  zone and label each arrow with its move and, from data/incidents.csv, its incident?
- Criterion: Given data/route.csv, When make talk runs, Then the 00 agenda and the 02
  route slide show build/00-frontmatter/route.png with each section in its zone and
  each arrow labelled with its move.
- Files: data/route.csv (new), data/README.md, scripts/utils/figures.py,
  scripts/utils/test_figures.py, scripts/figures.py, 00-frontmatter/section.mk,
  02-stacey/index.md
- Tasks:
  1. `Add the route -> data/route.csv and load_route`
     - Action: C8 leading: eight rows section, zone, counter, move; load_route in
       scripts/utils/figures.py; test RED first; data/README.md row.
     - Output: test_load_route_reads_eight_sections passing.
     - Check: `make test K=test_load_route -> [DONE] tests passed`
  2. `Place the route on the map -> route_layout(stops)`
     - Action: route_layout maps each stop to a point inside its zone (00, 02, 07,
       with no zone, beside the square); route(out) draws from it and from
       load_incidents (W-018), replacing SECTIONS and INCIDENTS (amends T-014).
     - Output: test_route_layout_puts_06_in_simple passing.
     - Check: `make test K=test_route_layout -> [DONE] tests passed`
  3. `Show the map -> 00-frontmatter/section.mk and 02-stacey/index.md`
     - Action: the route.png rule depends on data/route.csv and data/incidents.csv;
       "The route of this talk" in 02 shows the figure in place of its list.
     - Output: the image line in 02-stacey/index.md.
     - Check: `make build/00-frontmatter/route.png && grep -q 'build/00-frontmatter/route.png' 02-stacey/index.md -> exit 0`

#### W-024 03-chaos: what it felt like vs what it was

- Kind: issue. Reasoning: deductive -- the week column (W-020) and 2^bits give each
  point; depends on W-020.
- Hypothesis: Does a line chart of bits and paths over the weeks of data/cast.csv show
  the paths doubling while each request felt like one more if?
- Criterion: Given data/cast.csv with its week column, When make talk runs, Then 03
  shows build/03-chaos/growth.png, bits 1..6 and paths 2..64 over the weeks.
- Files: scripts/utils/paths.py, scripts/utils/test_paths.py, scripts/paths.py,
  03-chaos/section.mk, 03-chaos/index.md
- Tasks:
  1. `Count the growth -> growth(cast)`
     - Action: growth(cast) returns (week, bits, paths) per core bit in week order;
       tests RED first.
     - Output: test_growth_ends_at_week_10_with_64_paths passing.
     - Check: `make test K=test_growth -> [DONE] tests passed`
  2. `Draw the growth -> growth_chart(out, points) and scripts.paths growth`
     - Action: two lines in the deck style, each point annotated with its count.
     - Output: test_growth_chart_writes_a_png passing.
     - Check: `make test K=test_growth_chart_writes_a_png -> [DONE] tests passed`
  3. `Show the growth -> build/03-chaos/growth.png before "The honest count"`
     - Action: a rule in 03-chaos/section.mk; a slide before "The honest count".
     - Output: build/03-chaos/growth.png and its image line.
     - Check: `make build/03-chaos/growth.png && grep -q 'build/03-chaos/growth.png' 03-chaos/index.md -> exit 0`

#### W-025 04-what: the bits move, none deleted

- Kind: issue. Reasoning: deductive -- data/rules.csv holds pricing b0 b1, shipping b2
  b3 b4, tax b5 and the shell s0 s1 s2: 2 + 3 + 1 + 3 = 9.
- Hypothesis: Does a flow figure from data/rules.csv move all nine bits out of
  checkout() into their homes, in one palette per context?
- Criterion: Given data/rules.csv, When make talk runs, Then the 04 slide "Bounded
  contexts" shows build/04-what/moves.png, nine bits leaving checkout() into pricing
  2, shipping 3, tax 1 and shell 3.
- Files: scripts/utils/style.py, scripts/utils/test_style.py, scripts/utils/figures.py,
  scripts/utils/test_figures.py, scripts/figures.py, 04-what/section.mk,
  04-what/index.md
- Tasks:
  1. `Add the context palette -> context_colour(name) in scripts/utils/style.py`
     - Action: the note's One palette: pricing, shipping, tax, shell, tangled, five
       colours from palette(), defined once; test RED first.
     - Output: test_context_colour_gives_five_distinct_colours passing.
     - Check: `make test K=test_context_colour -> [DONE] tests passed`
  2. `Count the moves -> moves(rules)`
     - Action: moves(rules) returns (home, bits) with the shell rows grouped as shell;
       tests RED first.
     - Output: test_moves_sum_to_nine passing.
     - Check: `make test K=test_moves -> [DONE] tests passed`
  3. `Draw the moves -> moves_figure(out, moves) and scripts.figures moves`
     - Action: checkout() on the left, the four homes on the right, band widths by
       bits, coloured by context_colour; `--rules` read by scripts/figures.py.
     - Output: test_moves_figure_writes_a_png passing.
     - Check: `make test K=test_moves_figure_writes_a_png -> [DONE] tests passed`
  4. `Show the moves -> build/04-what/moves.png on "Bounded contexts"`
     - Action: a rule in 04-what/section.mk; the slide shows it beside contexts.txt.
     - Output: build/04-what/moves.png and its image line.
     - Check: `make build/04-what/moves.png && grep -q 'build/04-what/moves.png' 04-what/index.md -> exit 0`

#### W-026 03-chaos: the example map before and after the room

- Kind: issue. Reasoning: deductive -- blue cards are the rows of data/rules.csv (9),
  red the numbered questions of 03-chaos/data/questions.md (6), green the rows of
  data/examples.csv (14); before the room, the six core ifs and no question.
- Hypothesis: Does a two-panel card figure, every count measured from its file, show
  the bits nobody wrote down appearing in the room?
- Criterion: Given data/rules.csv, data/examples.csv and 03-chaos/data/questions.md,
  When make talk runs, Then 03 shows build/03-chaos/example_map.png, 6 blue and 0 red
  cards before the room, 9 blue and 6 red after.
- Files: scripts/utils/examples.py, scripts/utils/test_examples.py,
  scripts/utils/figures.py, scripts/utils/test_figures.py, scripts/figures.py,
  03-chaos/section.mk, 03-chaos/index.md
- Open: the note gives no green count before the room; INFERRED proposal 2 (the two
  tests of 01-bits/tests/test_chaos.py), to confirm with the plan.
- Tasks:
  1. `Count the cards -> card_counts in scripts/utils/examples.py`
     - Action: card_counts(rules, examples, questions_md) returns the after counts by
       colour; the before counts from the core rows; tests RED first.
     - Output: test_card_counts_after_the_room_are_9_blue_6_red passing.
     - Check: `make test K=test_card_counts -> [DONE] tests passed`
  2. `Draw the map -> example_map(out, before, after) and scripts.figures example-map`
     - Action: two panels of coloured cards, yellow story card on top, in the deck
       style.
     - Output: test_example_map_writes_a_png passing.
     - Check: `make test K=test_example_map_writes_a_png -> [DONE] tests passed`
  3. `Show the map -> build/03-chaos/example_map.png on "The six questions"`
     - Action: a rule in 03-chaos/section.mk depending on the three files.
     - Output: build/03-chaos/example_map.png and its image line.
     - Check: `make build/03-chaos/example_map.png && grep -q 'build/03-chaos/example_map.png' 03-chaos/index.md -> exit 0`

#### W-027 05-how: the core and the shell with three ports

- Kind: issue. Reasoning: deductive -- the shell rows of data/rules.csv carry the sum
  types in their code column (Charged | Declined, Reserved | OutOfStock, Sent |
  Bounced), so no label is typed by hand.
- Hypothesis: Does a seam figure read from the shell rows of data/rules.csv name each
  port and its sum type?
- Criterion: Given data/rules.csv, When make talk runs, Then the 05 slide "The ports"
  shows build/05-how/ports.png, the core and three ports, each arrow labelled with its
  sum type.
- Files: scripts/utils/figures.py, scripts/utils/test_figures.py, scripts/figures.py,
  05-how/section.mk (new), 05-how/index.md
- Tasks:
  1. `Read the ports -> ports_of(rules)`
     - Action: ports_of(rules) returns (context, code) of the shell rows; test RED
       first.
     - Output: test_ports_of_reads_three_sum_types passing.
     - Check: `make test K=test_ports_of -> [DONE] tests passed`
  2. `Draw the seam -> seam(out, ports) and scripts.figures seam`
     - Action: the core box, three port boxes, the labelled arrows, in the deck style.
     - Output: test_seam_writes_a_png passing.
     - Check: `make test K=test_seam_writes_a_png -> [DONE] tests passed`
  3. `Show the seam -> 05-how/section.mk and "The ports"`
     - Action: a new 05-how/section.mk declaring build/05-how/ports.png; the slide
       shows it beside the ports snippet.
     - Output: build/05-how/ports.png and its image line.
     - Check: `make build/05-how/ports.png && grep -q 'build/05-how/ports.png' 05-how/index.md -> exit 0`

#### W-028 06-simple: the epilogue as stacked bars

- Kind: issue. Reasoning: deductive -- build/06-simple/epilogue.txt reads 22 -> 30
  +8 today; the contexts + shell bar of bars_from_rules gives pricing 4, shipping 8,
  tax 2, shell 8, and b6 of data/seventh.csv makes shipping 16.
- Hypothesis: Does the epilogue chart show the seventh if growing one segment only?
- Criterion: Given data/rules.csv and data/seventh.csv, When make talk runs, Then the
  06 epilogue shows build/06-simple/epilogue.png, only the shipping segment growing
  from 8 to 16 and the totals 22 and 30.
- Files: scripts/utils/paths.py, scripts/utils/test_paths.py, scripts/paths.py,
  06-simple/section.mk, 06-simple/index.md
- Tasks:
  1. `Build the two bars -> epilogue_bars(before, after)`
     - Action: the contexts + shell bar before and after the seventh if, segments
       coloured by context_colour (W-025); tests RED first.
     - Output: test_epilogue_bars_grow_shipping_only passing.
     - Check: `make test K=test_epilogue_bars -> [DONE] tests passed`
  2. `Show the bars -> build/06-simple/epilogue.png on the epilogue`
     - Action: `scripts.paths epilogue-chart` through stacked_bar; a rule in
       06-simple/section.mk; the slide shows it beside epilogue.txt.
     - Output: build/06-simple/epilogue.png and its image line.
     - Check: `make build/06-simple/epilogue.png && grep -q 'build/06-simple/epilogue.png' 06-simple/index.md -> exit 0`

### Deferred (nice, not planned)

- 60 -> 50 -> 45 against 60 -> 54 -> 44, the hidden bit (05).
- The counter over the talk: 64, 512, 72 (07), from data/route.csv once W-023 lands.
- The commit log from the cast: six commits, six faces (01).
- Open: the note names no exhibit for 03 (I2, "one meeting nobody had called"); the
  Epic covers 01, 05, 06 and the epilogue, and 03 opens on the story figure as today.
  It would join if the developer writes an I2 exhibit.

### Conflicts to decide

Each pick becomes the spike's decision (`board note W-017 --event decision`, then
`spike.decision`).

C1. data/cast.csv: the week column

- Leading: [Data] Adopt the note's week column: one more column in cast.csv, read by
  W-020 Task 1 (CastRow.week); cast.txt and contexts.txt do not change. The answer if
  W-020 and W-024 stay planned.
- [Data] Weeks in their own data/weeks.csv (bit, week): cast.csv stays as T-010 closed
  it; a per-bit fact in a second file joined by bit. The answer if cast.csv must stay
  frozen.
- [Scope] No weeks: W-020 shows bits and paths only, W-024 is pruned; the time story is
  told by voice. The answer if the developer cuts the curve.

C2. data/cast.csv: the requested_by, words and fragment cells

- Leading: [Data] Keep the repository's cells: they carry the beats the slides use
  ("two weeks before launch", "from what? nobody asked", "nobody wrote the answer
  down") and are what build/01-bits/cast.txt and build/04-what/contexts.txt show; the
  note's cast.csv drops its words, requested_by and fragments and keeps its week. The
  answer if the doubling table of W-020 fits one slide with the long words.
- [Data] The note's words and requested_by: shorter cells fit the doubling; cast.txt,
  contexts.txt and the 01 and 04 speaker notes change, carried by W-020 Task 1. The
  answer if the doubling overflows at the deck's smallest font.
- [Data] The repository's words with the note's fragments: each note fragment matches
  exactly one line of 01-bits/s01_bits/chaos.py (checked at 6469c17), and s2's
  `send(order.email, total)` is the whole call where the repository's is cut; no slide
  shows the change. The answer if the fragment cells must read as code.

C3. data/lines.csv: the columns and the section keys

- Leading: [Data] `section,believed,learned` with the repository's keys `01-bits` ..
  `06-simple`: scripts/check_lines.py keys each index.md by its directory name, so `01`
  matches none; carried by W-021 Task 1, `line` renamed `learned`. The note drops its
  `01` .. `06` keys. The answer if the keys never show on a slide.
- [Data] The note's `01` .. `06` keys with a prefix match in scripts/utils/lines.py:
  shorter keys, one mapping rule more. The answer if the keys appear on 07's table.
- [Data] Keep `section,line` and put believed in data/believed.csv: lines.csv stays as
  T-024 closed it; one section's pair in two files. The answer if lines.csv must stay
  frozen.

C4. data/lines.csv: the commas

- Leading: [Spelling] The repository's commas: 02, 04, 06 and 07 carry them and `make
  lines` passes on main; no learned line changes on a slide. The note's lines.csv
  drops its comma-less spelling. The answer unless the developer reads the lines
  without pauses on purpose.
- [Spelling] The note's spelling: W-021 Task 1 rewrites data/lines.csv and the four
  index.md files (02, 04, 06, 07) in one commit so `make lines` stays green. The answer
  if the comma-less rhythm is the spoken one.

C5. 01-bits/data/incident.txt: the finance exhibit

- Leading: [Content] The note's email verbatim: its `Subject:` header is the Exhibit
  slide kind, and it ends on a question to the room; the 100% coverage stays in the
  speaker notes of 01-bits/index.md, which already say it; carried by W-019 Task 1
  (amends T-011). The repository's report drops.
- [Content] The email plus the repository's `Test status` line: the badge stays on the
  slide; a found email that reads partly like a report. The answer if the badge must be
  seen, not said.
- [Content] Keep the repository's report: the note's exhibit drops; the Exhibit kind's
  header form is not followed in 01. The answer if finance writes reports, not emails,
  in the story.

C6. 05-how/data/incident.txt: the support exhibit

- Leading: [Content] The note's numbers and text: 41 customers, six working days, the
  same as I3's cost in data/incidents.csv, pinned by W-019 Task 1's test (amends
  T-021). The repository's 37 tickets, about a week and its next-step line drop; the
  next step is the test 06 shows anyway.
- [Content] Keep the repository's 37 tickets and about a week; I3's cost in
  data/incidents.csv becomes `37 tickets, refunds in about a week` and the note's
  exhibit drops. The answer if tickets and customers were meant to differ.
- [Content] The note's numbers in the repository's report form (header, week of
  2026-10-23, next step). The answer if the date and the next step must stay.

C7. 00-frontmatter/index.md: the message of T-015

- Leading: [Content] The note's message in 00-frontmatter/data/message.txt, included by
  "Checkout done": it plants "just one if" for the epilogue; carried by W-019 Tasks 2
  and 3 (amends T-015; still four slides). The one-line message drops.
- [Content] Keep the one-liner; the marketing reply lives in the teaser of 01 and 06
  only. The answer if the opening must stay one breath.

C8. scripts/utils/figures.py: the route of T-014

- Leading: [Data] data/route.csv with eight rows, section, zone, counter, move: the
  note's five rows plus 00 pride ?, 02 which problem 64 and 07 six lines 72 with no
  zone or move; the incident on an arrow comes from data/incidents.csv told_in, its one
  home, so I2 moves to the arrow into 02, where E-002's spine has the dispute surface;
  carried by W-023 (amends T-014). SECTIONS and INCIDENTS leave the code.
- [Data] The note's five rows only: the map shows the five moves; 00 keeps today's
  eight-box figure, so two route figures. The answer if the agenda must name every
  section.
- [Data] Eight rows, I2 kept on the arrow into 03 where question 3 is decided, and
  data/incidents.csv told_in 03. The answer if "told" means where the room decides it.
