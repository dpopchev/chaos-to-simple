# 01-bits -- the coverage report, the 64-path grid and the storyboard are build artifacts, so
# the numbers on the slides are measured, not typed. A plain `#` keeps it out of make help.
STORY_FILES := $(foreach k,0 1 2 3 4 5 6,$(BUILD)/01-bits/step-$(k).diff) \
  $(foreach k,0 1 2 3 4 5 6 7 8,$(BUILD)/01-bits/bubble-$(k).txt)

ARTIFACTS += $(BUILD)/01-bits/coverage.txt $(BUILD)/01-bits/grid.txt $(BUILD)/01-bits/doubling.txt
ARTIFACTS += $(BUILD)/01-bits/coverage-summary.txt $(STORY_FILES)
ARTIFACTS += $(BUILD)/01-bits/grid.png
ARTIFACTS += $(BUILD)/01-bits/coverage-view.png $(BUILD)/01-bits/finance.png \
  $(BUILD)/01-bits/finance.txt

$(BUILD)/01-bits/finance.png $(BUILD)/01-bits/finance.txt &: 01-bits/data/october.csv \
    scripts/figures.py scripts/utils/finance.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures finance --october 01-bits/data/october.csv \
	  --out $(BUILD)/01-bits/finance.png
	$(call log_done,$(BUILD)/01-bits/finance.png written)

$(BUILD)/01-bits/grid.png: 01-bits/data/tested.csv scripts/figures.py scripts/utils/paths.py \
    scripts/utils/coverage_view.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures grid-image --tested 01-bits/data/tested.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/coverage-view.png: 01-bits/data/tested.csv scripts/figures.py \
    scripts/utils/coverage_view.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures coverage-view --tested 01-bits/data/tested.csv --out $@
	$(call log_done,$@ written)

$(STORY_FILES) &: 01-bits/s01_bits/chaos.py 01-bits/data/bubbles.csv data/actors.csv \
    scripts/paths.py scripts/utils/storyboard.py
	@$(RUN) python -m scripts.paths storyboard --source 01-bits/s01_bits/chaos.py \
	  --bubbles 01-bits/data/bubbles.csv --actors data/actors.csv --out $(BUILD)/01-bits
	$(call log_done,$(BUILD)/01-bits storyboard written)

$(BUILD)/01-bits/coverage-summary.txt: $(BUILD)/01-bits/coverage.txt
	@grep -E 'chaos\.py|^TOTAL|^2 passed' $< > $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/doubling.txt: data/cast.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths doubling --cast data/cast.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/coverage.txt: 01-bits/s01_bits/chaos.py 01-bits/tests/test_chaos.py
	@mkdir -p $(@D)
	@$(RUN) pytest 01-bits/tests -q --no-header -k 'test_regular_order or test_order_with_everything' \
	  --cov=s01_bits.chaos --cov-branch \
	  --cov-report=term-missing > $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/grid.txt: scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths grid --bits 6 --out $@
	$(call log_done,$@ written)
