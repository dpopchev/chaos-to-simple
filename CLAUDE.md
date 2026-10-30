# CLAUDE.md

Slides and tested code for the DEV.BG Python user group talk. The front door is `make help`;
the layout and the build are in README.md.

## Gate deviations

- Exhibit code and tests under `NN-*/sNN_*/` and `NN-*/tests/` are talk content: linted,
  type-checked and run, but exempt from the one-assert and category-marker gates
  (`scripts/conftest.py` filters by path; `scripts/` meets every gate). Decision on E-001.
- The deck draws its figures in Python with matplotlib and seaborn, not Mermaid, by the
  developer's Decision on E-002.
- `scripts/paths.py`, `scripts/figures.py` and `scripts/check_ascii.py` are entry points run as `python -m scripts.<name>`
  from the Makefile, not as bare scripts. Decision context: `rules/python-project.md`, Gate deviations.
