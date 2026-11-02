# data: facts shared by more than one section

Only data that two or more sections read lives here. Data one section reads lives in
that section (`03-chaos/data/` holds the room log, nobody else needs it).

| File | Columns | Read by |
|---|---|---|
| `rules.csv` | `bit, scope, context, name, rule, code` | 03 (counts), 04 (glossary), 06 (chart), `scripts/paths.py` |
| `seventh.csv` | `bit, scope, context, name, rule, code` | 06 (epilogue: the seventh core if, counted beside `rules.csv`), `scripts/paths.py` |
| `actors.csv` | `actor, kind, label, color, icon, context` | the one home of every actor's colour (hex, no `#`), label and icon name; `scripts/utils/palette.py` |
| `contexts.csv` | `context, kind, label, color` | the one home of every context's colour and label; `scripts/utils/palette.py`, `scripts/utils/style.py` |
| `cast.csv` | `bit, step, week, requested_by, words, aside, fragment` | 01 (the cast table by source line, the doubling by week), 04 (who asked for each bit), `scripts/paths.py`; `requested_by` is an `actors.csv` key, tables print its label |
| `incidents.csv` | `id, week, date, told_in, decided_in, closed_in, closed_by, kind, cost, decision, principle` | 00 (the incident marks of the agenda by `told_in`), 06 (the wounds close by name: `closed_by` tests are run; `decision` and `principle` fill the post-mortem table), `scripts/paths.py` |
| `examples.csv` | `scope, bit, name, given, then` | 06 (every `name` must have a `test_<name>`), `scripts/utils/examples.py` |
| `questions.csv` | `id, question, raised_by, bit, status, decision, subdomain` | 03 (the retro table: the six questions the room raised, each with the decision that closed it; `subdomain` is core for q1-q3 and generic for q4-q6; `raised_by` is an `actors.csv` key: accounting, loyalty, logistics or dev) |
| `route.csv` | `section, label, icon, counter, incident, x, y` | 00 (the agenda strip): `scripts/utils/stage.py` draws one box per section with its `icon` pictogram (a name `scripts/utils/icons.py` maps), `label` and `counter` under it; `incident` is the incident id told in that section (`incidents.csv` `told_in` decides the mark drawn); `x, y` place the section on the Stacey square (certainty on the How, agreement on the What, empty for 00 and 07) |
| `artifacts.csv` | `path, kind, producer` | `make stubs`: every build path the slides include, its kind (png, txt, diff, tex) and what builds it; a path no make rule builds gets a placeholder, `STRICT=1` fails on it |
| `budget.csv` | `section, frames, minutes` | `make budget`: the frames each section's `index.md` holds (its `## ` lines) and the minutes it gets; frames sum 43, minutes 45 (the title frames of 00 and 07 are not counted) |
| `lines.csv` | `section, believed, learned` | `make lines` (each learned line must stand in its section's `index.md` and in `07-close/index.md`; believed is the claim the talk flips) |

## Conventions

- `bit`: `b0..b5` are core decisions (the What), `s0..s2` are shell effects (the How).
- `cast.csv` `aside`: the speaker's remark about a request ("from what? nobody asked"), kept out
  of `words` and `requested_by` so no table shows it; empty for most rows.
- `scope`: `core` or `shell`. `context`: the bounded context that owns the bit; every shell
  row has context `shell` (the provider that answers is the cast's `requested_by`).
- `cast.csv` `step`: the order the bits join the story, 0 for a shell effect nobody asked for.
- `name` is an identifier: snake_case, used verbatim as a test name in `06-simple/tests`.
- The numbers on the slides come from these files through `make artifacts`
  (`build/data/rules.txt`, `build/data/counts.txt`, `build/06-simple/paths.png`);
  nothing on a slide is typed by hand twice.
- Changing a row here changes the talk: 9 bits give 512 tangled paths and 64 + 8 = 72 split.
  `scripts/tests/test_paths.py` pins those three numbers.
