# data: facts shared by more than one section

Only data that two or more sections read lives here. Data one section reads lives in
that section (`03-chaos/data/` holds the red cards, nobody else needs them).

| File | Columns | Read by |
|---|---|---|
| `rules.csv` | `bit, scope, context, name, rule, code` | 03 (example map, counts), 04 (glossary), 06 (chart), `scripts/paths.py` |
| `seventh.csv` | `bit, scope, context, name, rule, code` | 06 (epilogue: the seventh core if, counted beside `rules.csv`), `scripts/paths.py` |
| `cast.csv` | `bit, week, requested_by, words, fragment` | 01 (the cast table beside the checkout, the doubling by week), 04 (who asked for each bit), `scripts/paths.py` |
| `incidents.csv` | `id, week, told_in, closed_in, closed_by, kind, cost` | 06 (the wounds close by name: `closed_by` tests are run), `scripts/paths.py` |
| `examples.csv` | `scope, bit, name, given, then` | 03 (green cards), 06 (every `name` must have a `test_<name>`) |
| `route.csv` | `section, zone, counter, move` | 00 (agenda) and 02 (the route slide): `scripts/utils/figures.py` lays each section in its Stacey zone; `zone` and `move` are empty for a section off the map |
| `lines.csv` | `section, believed, learned` | `make lines` (each learned line must stand in its section's `index.md` and in `07-close/index.md`; believed is the claim the talk flips) |

## Conventions

- `bit`: `b0..b5` are core decisions (the What), `s0..s2` are shell effects (the How).
- `scope`: `core` or `shell`. `context`: the bounded context that owns the bit.
- `name` is an identifier: snake_case, used verbatim as a test name in `06-simple/tests`.
- The numbers on the slides come from these files through `make artifacts`
  (`build/data/rules.txt`, `build/data/counts.txt`, `build/06-simple/paths.png`);
  nothing on a slide is typed by hand twice.
- Changing a row here changes the talk: 9 bits give 512 tangled paths and 64 + 8 = 72 split.
  `scripts/tests/test_paths.py` pins those three numbers.
