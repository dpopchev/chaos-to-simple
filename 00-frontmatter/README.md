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
| `filters/include-code-files.lua` | fills fenced code blocks from source files, by snippet marker or line range | never, unless the marker syntax changes |
| `filters/paths-footer.lua` | turns `## Title {paths=64}` into the footer counter | never |
| `index.md` | the opening question and the agenda; the title slide comes from `meta.yaml` | the agenda changes |

## How a slide pulls code

    ```{.python include=01-bits/s01_bits/chaos.py snippet=checkout}
    ```

The path is relative to the repo root. The snippet is delimited in the source by the
comment lines `# [snippet: checkout]` and `# [/snippet]`. Prefer snippet names over
line ranges: a line range rots on the first edit above it, a name does not.
Add `.numberLines` (`{.python .numberLines include=... snippet=checkout}`) and the
numbers are the file's own line numbers, starting at the first line shown.

## How a slide moves the footer counter

    ## Three numbers {paths=64}

The value stays until another slide sets it. Use `?` while the count is unknown.

## Language switch

The talk is in Bulgarian; the skeleton text is English and ASCII so the ascii check
covers it. When the slides go Bulgarian: set `lang: bg-BG` in `meta.yaml`, keep the
Adwaita Sans and Adwaita Mono fonts (both carry Cyrillic), and pass `--skip-slides` to
the ascii target in the Makefile so only code, config, data and READMEs stay ASCII-only.
The engine is lualatex with these fonts, the only pair the build machine has.

## Done when

- Given `make slides`, when the deck opens, then the title slide shows title, subtitle,
  author, institute and date, and the footer reads `paths to reason about: ?`.
