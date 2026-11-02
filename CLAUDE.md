# CLAUDE.md

Slides and tested code for the DEV.BG Python user group talk. The front door is `make help`;
the layout and the build are in README.md.

## Gate deviations

- Exhibit code and tests under `NN-*/sNN_*/` and `NN-*/tests/` are talk content: linted,
  type-checked and run, but exempt from the category-marker gate only; the one-assert gate
  covers them too (`conftest.py` filters the markers by path; `scripts/` meets every gate).
  Decisions on E-001 (the exemption) and E-007 (the one-assert lift).
- The deck draws its figures in Python with matplotlib and seaborn, not Mermaid, by the
  developer's Decision on E-002.
- `scripts/paths.py`, `scripts/figures.py` and `scripts/check_ascii.py` are entry points run as `python -m scripts.<name>`
  from the Makefile, not as bare scripts. Decision context: `rules/python-project.md`, Gate deviations.
