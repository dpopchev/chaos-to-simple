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
