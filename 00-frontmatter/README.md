# 00-frontmatter: configuration and the opening slides

This directory owns everything that is about the deck as a whole and nothing that
belongs to one section. It is the only directory allowed to know the list of sections
(the agenda slide).

## Files

| File | What it does | Touch it when |
|---|---|---|
| `meta.yaml` | title, author, date, language, theme, fonts | the title or the language changes |
| `defaults.yaml` | pandoc options: beamer, lualatex, slide level 2, filters, resource path | a filter or an engine option changes |
| `preamble.tex` | footer path counter, smaller code font, no navigation symbols | the footer or the look changes |
| `build/00-frontmatter/beats.tex` | generated from `data/lines.csv`: the believed line and the strip name of each section, read by the section page in `preamble.tex` | the lines change |
| `build/00-frontmatter/agenda-NN.png` | the agenda strip with stop NN highlighted, one per section, shown on its section page | the route changes |
| `filters/include-code-files.lua` | fills fenced code blocks from source files, by snippet marker or line range; an optional `heading="..."` attribute, or `heading-file=PATH` (the first line of a built file), renders as a shaded `\snippethead` label above the block | never, unless the marker syntax changes |
| `filters/diffs.lua` | turns a `.diff` block into a Verbatim: the first line (the caption) the grey heading, lines starting `-`, `+`, `~`, `...` in red, green, dark yellow, grey (macros in `preamble.tex`); sized `\snippetsize` (`\tiny`, set once in `preamble.tex` with highlighted code and the storyboard) | the colouring or the size changes |
| `filters/story.lua` | renders the request box only (a `.request` Div); a storyboard `.diff .python` block goes through `diffs.lua` like every diff | the request box changes |
| `filters/speakers.lua` | turns a `.speakers` block into a Verbatim with each actor label (full or first word) in its colour from `data/actors.csv`; `highlight=q3` sets that row bold; sized `\exhibitsize` (`\scriptsize`, text exhibits) | the colouring or the size changes |
| `filters/paths-footer.lua` | turns `## Title {paths=64}` into the footer counter | never |
| `index.md` | the opening: the business map and the agenda strip, each with its speaker notes; the title slide comes from `meta.yaml` | the opening changes |

## How a slide pulls code

    ```{.python include=01-bits/s01_bits/chaos.py snippet=checkout}
    ```

The path is relative to the repo root. The snippet is delimited in the source by the
comment lines `# [snippet: checkout]` and `# [/snippet]`. Prefer snippet names over
line ranges: a line range rots on the first edit above it, a name does not.
Add `.numberLines` (`{.python .numberLines include=... snippet=checkout}`) and the
numbers are the file's own line numbers, starting at the first line shown.

A heading over the block is `heading="text"`, or `heading-file=build/01-bits/tests-6.txt`, which
reads the first line of a built file, so a measured tally is never typed. Write it before
`include=` in the fence, so `make widths` and `make lengths` keep matching the include.

A source line may end with a step marker, `# [step: N]` (N from 0 to 6). The filter strips
it on include, so no slide shows it; the step diffs read it to know which request added the
line. `make widths` and `make lengths` measure the stripped line.

## How a slide moves the footer counter

    ## Three numbers {paths=64}

The value stays until another slide sets it. Use `?` while the count is unknown.

## Language switch

The talk is in Bulgarian; the skeleton text is English and ASCII so the ascii check
covers it. When the slides go Bulgarian: set `lang: bg-BG` in `meta.yaml`, keep the
Adwaita Sans and Adwaita Mono fonts (both carry Cyrillic), and pass `--skip-slides` to
the ascii target in the Makefile so only code, config, data and READMEs stay ASCII-only.
The engine is lualatex with these fonts, the only pair the build machine has.

## Pictograms

Each actor and each route stop is drawn as an icon, in the deck by lualatex and in the
figures by matplotlib. The W-053 spike (`make spike-fa`, `build/spike/fa-probe.pdf` and
`build/spike/fa-probe.png`) drew the nine actor icons with no missing glyph from:

| Font | lualatex | matplotlib |
|---|---|---|
| Font Awesome 7 Free Solid (otf-font-awesome, `/usr/share/fonts/OTF`) | fontspec | by the fc-list path |
| the fontawesome5 package (its own Font Awesome 5 Free OTF) | `\faIcon{name}` | no |
| Hack Nerd Font (`~/.local/share/fonts`) | fontspec | by the fc-list path |

An icon name maps to its glyph through `ICONS` in `scripts/utils/icons.py`: one codepoint
per font, read from the font's cmap with fontTools, since Nerd Fonts moves warehouse,
store and layer-group out of their Font Awesome codepoints. `make doctor` reports
fontawesome5.sty and the icon fonts.

Decision: Font Awesome 7 Free Solid serves both renderers: fontspec in lualatex, its fc-list path in matplotlib; ICONS in scripts/utils/icons.py maps a name to its codepoint; fontawesome5 is the second choice, Hack Nerd Font the third, a labelled box the fallback if fc-list finds none.

## Done when

- Given `make slides`, when the deck opens, then the title slide shows title, subtitle,
  author, institute and date, and the footer reads `paths to reason about: ?`.
- Given `make talk`, when frame 00 opens, then the business map shows the nine named
  parts and the agenda strip shows eight stops with I1, I2 and I3 marked, and each
  frame carries its speaker notes.
