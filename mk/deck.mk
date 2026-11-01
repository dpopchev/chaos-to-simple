# mk/deck.mk -- the deck layer: one beamer PDF built by pandoc from one index.md
# per NN-* section. Uses the base's UV, BUILD, log_done / log_warn / _log_line
# and the python layer's RUN (read at recipe time, so the include order of
# mk/*.mk does not matter); appends ascii to CHECKS and deliverable-talk to
# DELIVERABLES. The slides name build/ paths literally, so BUILD stays build.

# ------------------------------------------------------------------------------
### Deck
# ------------------------------------------------------------------------------

# Toolchain -- override on the command line: make PANDOC=/opt/pandoc/bin/pandoc
PANDOC ?= pandoc

# Layout: the frontmatter owns the configuration, every other NN-* directory is
# one section.
FRONT     := 00-frontmatter
DEFAULTS  := $(FRONT)/defaults.yaml
META      := $(FRONT)/meta.yaml
PREAMBLE  := $(FRONT)/preamble.tex
FILTERS   := $(sort $(wildcard $(FRONT)/filters/*.lua))
INDEXES   := $(sort $(wildcard [0-9][0-9]-*/index.md))
RULES     := data/rules.csv
SHARED    := $(BUILD)/data/rules.txt $(BUILD)/data/counts.txt $(BUILD)/data/splits.txt
ARTIFACTS := $(SHARED)
PDF       := $(BUILD)/talk.pdf
NOTES     := $(BUILD)/talk-notes.pdf

# make new SECTION=08-name TITLE="Section title"
SECTION ?=
TITLE   ?=

CHECKS       += ascii lines lengths budget
DELIVERABLES += deliverable-talk

# A section that generates artifacts declares them in its own section.mk: it
# appends to ARTIFACTS and writes only under build/<section>/. Included before
# the deck rule, because make expands prerequisites when it reads a rule.
include $(wildcard [0-9][0-9]-*/section.mk)

DECK_INPUTS := $(INDEXES) $(META) $(DEFAULTS) $(PREAMBLE) $(FILTERS) $(ARTIFACTS)

$(PDF): $(DECK_INPUTS) | stubs
	@mkdir -p $(@D)
	@$(PANDOC) --defaults $(DEFAULTS) $(INDEXES) -o $@
	$(call log_done,$@ built from $(words $(INDEXES)) index files)

$(NOTES): $(DECK_INPUTS) | stubs
	@mkdir -p $(@D)
	@$(PANDOC) --defaults $(DEFAULTS) \
	  --variable 'beameroption=show notes on second screen=right' $(INDEXES) -o $@
	$(call log_done,$@ built with the speaker notes)

.PHONY: slides
slides: $(PDF) | stubs ## Build build/talk.pdf
	$(call log_done,$(PDF) current)

.PHONY: draft
draft: $(ARTIFACTS) ## Rebuild the deck now, snippets unchecked
	@mkdir -p $(dir $(PDF))
	@$(PANDOC) --defaults $(DEFAULTS) $(INDEXES) -o $(PDF)
	$(call log_warn,draft deck -- the snippets were not checked; run make talk before presenting)
	$(call log_done,$(PDF) built as a draft)

.PHONY: notes
notes: $(NOTES) ## Build build/talk-notes.pdf with the speaker notes
	$(call log_done,$(NOTES) current)

.PHONY: talk
talk: check slides | stubs ## Run every check, then build the deck
	$(call log_done,checked and built $(PDF))

# The manifest names every artifact the new frame plan includes; a path that no
# rule builds yet gets a placeholder. STRICT=1 writes nothing and fails on each.
STRICT ?=

.PHONY: stubs
stubs: ## Write a placeholder for each manifest path no rule builds; STRICT=1 fails instead
	@$(RUN) python -m scripts.stubs --manifest data/artifacts.csv \
	  --built $(sort $(ARTIFACTS)) $(if $(STRICT),--strict)
	$(call log_done,manifest paths without a rule stubbed)

# Shared data renders once into build/data/; any section may include those files.
$(BUILD)/data/rules.txt: $(RULES) scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths rules --rules $(RULES) --out $@
	$(call log_done,$@ written)

$(BUILD)/data/counts.txt: $(RULES) scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths counts --rules $(RULES) --out $@
	$(call log_done,$@ written)

$(BUILD)/data/splits.txt: $(RULES) scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths splits --rules $(RULES) --out $@
	$(call log_done,$@ written)

.PHONY: artifacts
artifacts: $(ARTIFACTS) ## Generate every artifact the slides include
	$(call log_done,$(words $(ARTIFACTS)) artifacts current)

# Add --skip-slides once the slides are in Bulgarian.
.PHONY: ascii
ascii: ## Fail on a byte above 127 in code, config, data, prose
	@$(RUN) python -m scripts.check_ascii --root .
	$(call log_done,no byte above 127)

.PHONY: lines
lines: ## Check the six should-have-known lines in their sections and in 07
	@$(RUN) python -m scripts.check_lines --root .
	$(call log_done,the six lines are in their sections and in 07)

.PHONY: budget
budget: ## Fail naming each section whose frame count differs from data/budget.csv
	@$(RUN) python -m scripts.check_budget --root .
	$(call log_done,every section holds its budgeted frames)

.PHONY: widths
widths: $(ARTIFACTS) ## Fail naming each included line wider than its column
	@$(RUN) python -m scripts.check_widths --root . --full 104
	$(call log_done,every included line fits its column)

.PHONY: lengths
lengths: $(ARTIFACTS) ## Fail naming each included block over its line cap
	@$(RUN) python -m scripts.check_lengths --root . --cap 14
	$(call log_done,every included block is within its line cap)

OVERFLOW := local/state/overflow

.PHONY: overflow
overflow: $(DECK_INPUTS) ## Fail naming each beamer frame that runs past the frame bottom
	@mkdir -p $(OVERFLOW)
	@$(PANDOC) --defaults $(DEFAULTS) -t beamer -s $(INDEXES) -o $(OVERFLOW)/talk.tex
	@lualatex -interaction=nonstopmode -output-directory $(OVERFLOW) $(OVERFLOW)/talk.tex >/dev/null
	@$(RUN) python -m scripts.overflow --tex $(OVERFLOW)/talk.tex --log $(OVERFLOW)/talk.log
	$(call log_done,no overfull frame)

.PHONY: doctor
doctor: ## Report the deck toolchain and the fonts
	@for tool in $(UV) $(PANDOC) lualatex; do \
	  if command -v $$tool >/dev/null; then \
	    $(call _log_line,$(CYAN),INFO,found $$tool) \
	  else \
	    $(call _log_line,$(YELLOW),WARN,$$tool missing -- see the README toolchain) \
	  fi; \
	done
	@for font in "Adwaita Sans" "Adwaita Mono"; do \
	  if fc-list "$$font" family | grep -q .; then \
	    $(call _log_line,$(CYAN),INFO,found font $$font) \
	  else \
	    $(call _log_line,$(YELLOW),WARN,font $$font missing -- the deck needs it for Latin and Cyrillic) \
	  fi; \
	done
	$(call log_done,toolchain reported)

.PHONY: new
new: ## Scaffold a section, SECTION=NN-name TITLE="Section title"
	@if [ -z "$(SECTION)" ]; then \
	  $(call _log_line,$(RED),FAIL,usage -- make new SECTION=NN-name TITLE=<title>) exit 1; \
	fi
	@if [ -e "$(SECTION)" ]; then \
	  $(call _log_line,$(RED),FAIL,$(SECTION) exists) exit 1; \
	fi
	@mkdir -p $(SECTION)
	@cp templates/section/README.md templates/section/index.md $(SECTION)/
	@sed -i.bak 's/{{SECTION}}/$(SECTION)/g; s/{{TITLE}}/$(TITLE)/g' $(SECTION)/README.md $(SECTION)/index.md
	@rm -f $(SECTION)/*.bak
	$(call log_done,$(SECTION) scaffolded; register its tests dir in pyproject when it gets code)

.PHONY: deliverable-talk
deliverable-talk: $(PDF) ## Build the deck PDF and check it is not empty
	@test -s $(PDF)
	$(call log_done,$(PDF) built)
