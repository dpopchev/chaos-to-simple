# chaos-to-simple

Slides and tested code for the DEV.BG Python user group talk on 2026-11-05:
"Python: From chaos to simple, one bit at a time, or what I should have known from
the start". One checkout example goes from six tangled ifs (64 paths, 100% branch
coverage, one planted bug) to a functional core and an imperative shell
(64 + 8 = 72 paths instead of 512). `make` builds a single PDF with pandoc; every
code snippet on a slide is included from a file that the tests run.

## Layout

```
Makefile                 top-level build: check, artifacts, slides
pyproject.toml           uv environment, pytest/ruff/pyright config, section paths
00-frontmatter/          deck configuration (meta, defaults, preamble, filters) and the agenda
01-bits/ .. 07-close/    one directory per section, numbered in talk order
data/                    data read by two or more sections (rules.csv, cast.csv, examples.csv)
scripts/                 tested helpers the build calls (paths, ascii check, examples)
templates/section/       stubs for make new
build/                   artifacts; make clean removes it; never tracked
local/                   scratch, env, secrets; never tracked
```

The built deck, `build/talk.pdf`, is 50 pages: 43 content frames, counted by
`data/budget.csv`, and the title and other pages the build adds.

Each section directory holds:

| File | Role |
|---|---|
| `README.md` | directions for the author: beat, minutes, what it owns, uses and produces, slide checklist, live steps, done-when, open decisions |
| `index.md` | the slides of the section; the only file the build picks up |
| `section.mk` | optional; artifact rules for this section, included by the top-level Makefile |
| `sNN_name/` | optional; the code shown on the slides, a real package with a unique name |
| `tests/` | optional; the tests that keep the snippets honest |
| `data/` | optional; data only this section reads |

## Rules that keep the sections cohesive and decoupled

1. A section owns everything it shows: its code, its tests, its diagrams, its own data.
2. Data read by two or more sections lives in `data/` and renders once into `build/data/`.
3. Code dependencies point backwards in the story only: 05 imports 04, 06 imports 04 and 05,
   nothing imports a later section. The build order equals the story order.
4. A slide includes code by snippet name from a tested file, never by paste; a line range
   is allowed only for generated text. All include paths are repo-root relative.
5. A section that generates an artifact declares it in its own `section.mk` and writes only
   under `build/NN-name/`. The deck depends on every artifact, so `make slides` runs them.
6. Nothing on a slide is a number typed by hand if the build can measure it: coverage,
   test counts, path counts and the chart are artifacts.
7. The frontmatter is the one place allowed to know all sections (the agenda).

## Why `index.md`

The build globs `[0-9][0-9]-*/index.md`, sorted, so the directory name gives the order and
the file name gives the entry point; any other Markdown in a section (README, notes, data)
is invisible to pandoc by construction. `index.md` opens with a level-1 heading, which
beamer turns into the section's title slide, so the file is also the section's index in
the deck; the close is the one section that opens on its first frame, with no title slide. Speaker notes live in `::: notes` blocks next to the slide they belong to.

Alternatives considered: one big `slides.md` (merge conflicts, no ownership), a hand-kept
list of files in the Makefile (a second place to keep in order), `slides.md` per section
(works the same; `index` was chosen because the name already means "entry point").

## Build

```
make help                 every target with its description (the default goal)
make doctor               which tools are present and the fonts found
make sync                 uv environment with pytest, ruff, pyright, matplotlib
make check                every check: board, ruff, pyright, pytest, ascii, lines, lengths, budget, titles, widths, overflow
make talk                 check, then build build/talk.pdf
make test K=<expression>  pytest -k: only the tests matching the expression
make lines                fail on a slide line over the limit
make budget               fail on a section whose frame count differs from data/budget.csv
make titles               fail on a content frame title under eight words
make lengths              fail on an included block over its line cap
make deliverable          every deliverable: build/talk.pdf, not empty
make draft                the PDF without the checks, for layout work
make notes                build/talk-notes.pdf with speaker notes on a second screen
make artifacts            coverage report, counts, grid, chart
make stubs                placeholder for each data/artifacts.csv path no rule builds yet
make talk STRICT=1        fail (stubs and missing includes) while a manifest path has no rule
make new SECTION=08-name TITLE="Section title"
```

Toolchain: `uv`, `pandoc` (3.x), `lualatex`, and the Adwaita Sans and Adwaita Mono fonts,
which cover Latin and Cyrillic. `make doctor` reports what is missing.

Per-chapter loop: one board item per section, its brief the section's `README.md`. Scaffold
the section with `make new`, write its `index.md` slides and code, run `make check`, then
`make deliverable` before the item closes.

Overrides go on the command line, for example `make PANDOC=/opt/pandoc/bin/pandoc`.

## Conventions

- ASCII only in code, config, data and READMEs; `make ascii` enforces it. Slides are
  included in the check until they go Bulgarian, then the target gets `--skip-slides`.
- Figures and diagrams are drawn by `scripts/figures.py` and `scripts/paths.py` with
  matplotlib and seaborn in the one deck style of `scripts/utils/style.py`. Charts are
  stacked bars with exact counts on the segments, drawn from `data/rules.csv`; never
  plain, grouped or pie.
- One assert per test, exhibit tests included; only the category-marker gate exempts the
  exhibit tests under `NN-*/tests/` (Decision on E-007).
- Snippet markers in Python: `# [snippet: name]` and `# [/snippet]`, no nesting.
- A new section with code is registered in `pyproject.toml` (`testpaths`, `pythonpath`,
  ruff `src`, pyright `include`/`extraPaths`): the one place that lists sections with code.

## The numbers, pinned by `scripts/tests/test_paths.py`

| count | value |
|---|---|
| one function, 9 bits | 2^9 = 512 |
| core 6 bits + shell 3 bits | 64 + 8 = 72 |
| pricing 2 + shipping 3 + tax 1 + shell 3 | 4 + 8 + 2 + 8 = 22 |
| epilogue, one function, 10 bits | 512 -> 1024 (+512) |
| epilogue, core 7 bits + shell 3 bits | 72 -> 136 (+64) |
| epilogue, shipping 4 bits joins the contexts | 22 -> 30 (+8) |

The footer counter plan, pinned by `scripts/utils/test_counter_plan.py`: 01 opens
1, 2, 4, 8, 16, 32, 64; each section ends at its `data/route.csv` counter and never
falls inside it (06 aside); 03's room frames carry 64 until The honest count reveals
512; 06's frames carry 512 until The number reveals 72.
