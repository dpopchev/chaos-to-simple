### chaos-to-simple: one deck, built by pandoc from one index.md per section.
### Run every target from the repo root; all paths inside the sections are root-relative.
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --no-builtin-rules --no-print-directory
.DEFAULT_GOAL := all

### Toolchain (override on the command line: make PANDOC=/opt/pandoc/bin/pandoc)
UV     ?= uv
PANDOC ?= pandoc
MMDC   ?= mmdc
PY     := $(UV) run python

### Layout: the frontmatter owns the configuration, every other NN-* directory is one section
FRONT    := 00-frontmatter
DEFAULTS := $(FRONT)/defaults.yaml
META     := $(FRONT)/meta.yaml
PREAMBLE := $(FRONT)/preamble.tex
FILTERS  := $(sort $(wildcard $(FRONT)/filters/*.lua))
SECTIONS := $(sort $(wildcard [0-9][0-9]-*))
INDEXES  := $(sort $(wildcard [0-9][0-9]-*/index.md))
MMD      := $(sort $(wildcard [0-9][0-9]-*/diagrams/*.mmd))
DIAGRAMS := $(patsubst %.mmd,build/%.png,$(MMD))
RULES    := data/rules.csv
SHARED   := build/data/rules.txt build/data/counts.txt
ARTIFACTS := $(SHARED)
PDF      := build/talk.pdf
NOTES    := build/talk-notes.pdf

### Logging: log_ok closes every target, log_warn only when the reader must act
log_ok   = printf 'ok    %s\n' '$(1)'
log_warn = printf 'warn  %s\n' '$(1)'

### Section rules: a section that generates artifacts declares them in its own section.mk
### (it appends to ARTIFACTS and writes only under build/<section>/). Included before the
### deck rule so the deck depends on every artifact.
-include $(wildcard [0-9][0-9]-*/section.mk)

.PHONY: all slides draft notes check lint type test ascii artifacts diagrams sync doctor clean new help

all: check slides ## check the snippets, then build the deck (default)

slides: $(PDF) ## build build/talk.pdf

$(PDF): $(INDEXES) $(META) $(DEFAULTS) $(PREAMBLE) $(FILTERS) $(DIAGRAMS) $(ARTIFACTS) | build
	$(PANDOC) --defaults $(DEFAULTS) $(INDEXES) -o $@
	@$(call log_ok,$@ from $(words $(INDEXES)) index files)

draft: $(DIAGRAMS) $(ARTIFACTS) | build ## build the deck without make check
	$(PANDOC) --defaults $(DEFAULTS) $(INDEXES) -o $(PDF)
	@$(call log_warn,draft deck: snippets were not checked; run make check before presenting)
	@$(call log_ok,$(PDF))

notes: $(DIAGRAMS) $(ARTIFACTS) | build ## build build/talk-notes.pdf with the speaker notes shown
	$(PANDOC) --defaults $(DEFAULTS) --variable 'beameroption=show notes on second screen=right' $(INDEXES) -o $(NOTES)
	@$(call log_ok,$(NOTES))

### Shared data renders once into build/data/; any section may include those files
build/data/rules.txt: $(RULES) scripts/paths.py scripts/utils/paths.py | build
	@mkdir -p $(@D)
	$(PY) -m scripts.paths rules --rules $(RULES) --out $@
	@$(call log_ok,$@)

build/data/counts.txt: $(RULES) scripts/paths.py scripts/utils/paths.py | build
	@mkdir -p $(@D)
	$(PY) -m scripts.paths counts --rules $(RULES) --out $@
	@$(call log_ok,$@)

### Diagrams: Mermaid sources next to the slides, rendered by mermaid-cli into build/
build/%.png: %.mmd | build
	@mkdir -p $(@D)
	$(MMDC) -i $< -o $@ -b white -s 2 >/dev/null
	@$(call log_ok,$@)

diagrams: $(DIAGRAMS) ## render every diagrams/*.mmd
	@$(call log_ok,diagrams)

artifacts: $(ARTIFACTS) ## generate every included artifact (coverage demo, counts, chart)
	@$(call log_ok,artifacts)

### Checks: ruff + pyright + pytest + ascii. No board in this repo, so no board-check.
check: lint type test ascii ## run every check
	@$(call log_ok,check)

lint: ## ruff check and ruff format --check
	$(UV) run ruff check .
	$(UV) run ruff format --check .
	@$(call log_ok,lint)

type: ## pyright over scripts and every section with code
	$(UV) run pyright
	@$(call log_ok,type)

test: ## pytest over scripts/tests and every section's tests
	$(UV) run pytest
	@$(call log_ok,test)

ascii: ## no byte above 127 in code, config, data and prose (add --skip-slides once the slides are in Bulgarian)
	$(PY) -m scripts.check_ascii --root .
	@$(call log_ok,ascii)

### Housekeeping
sync: ## create or update the environment
	$(UV) sync
	@$(call log_ok,sync)

doctor: ## report which tools are present
	@for tool in $(UV) $(PANDOC) xelatex $(MMDC); do \
	  if command -v $$tool >/dev/null 2>&1; then printf 'ok    %s\n' "$$tool"; \
	  else printf 'warn  %s missing, see README toolchain\n' "$$tool"; fi; \
	done
	@if fc-list 2>/dev/null | grep -qi 'DejaVu Sans'; then printf 'ok    font DejaVu Sans\n'; \
	  else printf 'warn  font DejaVu Sans missing, needed for Cyrillic\n'; fi
	@$(call log_ok,doctor)

clean: ## remove build/
	rm -rf build
	@$(call log_ok,clean)

new: ## scaffold a section: make new SECTION=08-name TITLE="Section title"
	@test -n "$(SECTION)" || { printf 'usage: make new SECTION=NN-name TITLE="Section title"\n'; exit 1; }
	@test ! -e "$(SECTION)" || { printf '%s exists\n' "$(SECTION)"; exit 1; }
	@mkdir -p $(SECTION)
	@cp templates/section/README.md templates/section/index.md $(SECTION)/
	@sed -i.bak 's/{{SECTION}}/$(SECTION)/g; s/{{TITLE}}/$(TITLE)/g' $(SECTION)/README.md $(SECTION)/index.md
	@rm -f $(SECTION)/*.bak
	@$(call log_ok,$(SECTION) scaffolded; register its tests dir in pyproject when it gets code)

help: ## list targets
	@grep -hE '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | sort | awk -F ':.*## ' '{ printf "  %-10s %s\n", $$1, $$2 }'

build:
	@mkdir -p build
