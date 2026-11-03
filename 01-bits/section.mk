# 01-bits -- the coverage report, the 64-path grid and the storyboard are build artifacts, so
# the numbers on the slides are measured, not typed. A plain `#` keeps it out of make help.
STORY_FILES := $(foreach k,0 1 2 3 4 5 6,$(BUILD)/01-bits/step-$(k).diff) \
  $(foreach k,0 1 2 3 4 5 6,$(BUILD)/01-bits/test-$(k).diff) \
  $(foreach k,0 1 2 3 4 5 6,$(BUILD)/01-bits/tally-$(k).txt) \
  $(foreach k,0 1 2 3 4 5 6 7 8,$(BUILD)/01-bits/bubble-$(k).txt)

ARTIFACTS += $(BUILD)/01-bits/coverage.txt $(BUILD)/01-bits/grid.txt $(BUILD)/01-bits/doubling.txt
ARTIFACTS += $(BUILD)/01-bits/coverage-summary.txt $(STORY_FILES) $(BUILD)/01-bits/next.txt
ARTIFACTS += $(BUILD)/01-bits/grid.png $(BUILD)/01-bits/doubling.png
ARTIFACTS += $(BUILD)/01-bits/coverage-view.png $(BUILD)/01-bits/finance.png
ARTIFACTS += $(BUILD)/01-bits/counting.png
ARTIFACTS += $(BUILD)/01-bits/bug-run.txt

# The xfail is lifted (--runxfail) so the slide shows the failure the suite hides; the exit
# status must be 1 (one test failed) or the recipe fails; only the assert lines and the
# summary stay, without the timing.
$(BUILD)/01-bits/bug-run.txt: 01-bits/section.mk 01-bits/s01_bits/chaos.py \
    01-bits/tests/test_planted_bug.py
	@mkdir -p $(@D)
	@log=$$(mktemp); status=0; \
	$(RUN) pytest 01-bits/tests/test_planted_bug.py --runxfail -q --no-header \
	  -p no:cacheprovider > $$log || status=$$?; \
	if [ $$status -ne 1 ]; then rm -f $$log; \
	  echo "bug-run: pytest exited $$status, expected 1 (one failed test)" >&2; exit 1; fi; \
	grep -E '^E +Assertion|^[0-9]+ failed' $$log \
	  | sed -E 's/ in [0-9.]+s$$//' > $@; rm -f $$log
	$(call log_done,$@ written)

$(BUILD)/01-bits/finance.png: 01-bits/data/october.csv \
    scripts/figures.py scripts/utils/finance.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures finance --october 01-bits/data/october.csv \
	  --out $(BUILD)/01-bits/finance.png
	$(call log_done,$(BUILD)/01-bits/finance.png written)

$(BUILD)/01-bits/counting.png: scripts/figures.py scripts/utils/counting.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures counting --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/grid.png: 01-bits/data/tested.csv scripts/figures.py scripts/utils/paths.py \
    scripts/utils/coverage_view.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures grid-image --tested 01-bits/data/tested.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/doubling.png: data/cast.csv scripts/figures.py scripts/utils/paths.py \
    scripts/utils/style.py
	@$(RUN) python -m scripts.figures doubling --cast data/cast.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/coverage-view.png: 01-bits/data/tested.csv scripts/figures.py \
    scripts/utils/coverage_view.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures coverage-view --tested 01-bits/data/tested.csv --out $@
	$(call log_done,$@ written)

$(STORY_FILES) &: 01-bits/s01_bits/chaos.py 01-bits/data/bubbles.csv data/actors.csv \
    scripts/paths.py scripts/utils/storyboard.py
	@PYTHONPATH=01-bits $(RUN) python -m scripts.paths storyboard --source 01-bits/s01_bits/chaos.py \
	  --bubbles 01-bits/data/bubbles.csv --actors data/actors.csv --out $(BUILD)/01-bits
	$(call log_done,$(BUILD)/01-bits storyboard written)

$(BUILD)/01-bits/coverage-summary.txt: $(BUILD)/01-bits/coverage.txt
	@grep -E 'chaos\.py|^TOTAL|^2 passed' $< > $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/doubling.txt: data/cast.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths doubling --cast data/cast.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/next.txt: scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths next --bits 6 --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/coverage.txt: 01-bits/s01_bits/chaos.py 01-bits/tests/test_chaos.py
	@mkdir -p $(@D)
	@$(RUN) pytest 01-bits/tests/test_chaos.py -q --no-header \
	  --cov=s01_bits.chaos --cov-branch \
	  --cov-report=term-missing > $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/grid.txt: scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths grid --bits 6 --out $@
	$(call log_done,$@ written)
