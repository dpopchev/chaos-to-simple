# 04-what -- the slide figures and diffs are build artifacts. A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/04-what/moves.png

$(BUILD)/04-what/moves.png: data/rules.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py scripts/utils/paths.py
	@$(RUN) python -m scripts.figures moves --rules data/rules.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/board.png

$(BUILD)/04-what/board.png: data/rules.csv data/questions.csv data/examples.csv $(wildcard 06-simple/tests/*.py) scripts/figures.py scripts/utils/board.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures board --stage 4 --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/colorcode.png

$(BUILD)/04-what/colorcode.png: 01-bits/s01_bits/chaos.py data/cast.csv data/rules.csv data/actors.csv data/contexts.csv scripts/figures.py scripts/utils/colorcode.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures colorcode --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/fix.diff

$(BUILD)/04-what/fix.diff: 01-bits/s01_bits/chaos.py 04-what/s04_what/checkout_fixed.py 04-what/section.mk scripts/paths.py scripts/utils/stagediff.py
	@$(RUN) python -m scripts.paths diff --from 01-bits/s01_bits/chaos.py \
		--to 04-what/s04_what/checkout_fixed.py --snippet checkout --compact \
		--label-from 'checkout v6' --label-to 'v7' --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/tally-7.txt

$(BUILD)/04-what/tally-7.txt: 04-what/section.mk scripts/paths.py scripts/utils/storyboard.py \
    $(wildcard 01-bits/tests/*.py)
	@$(RUN) python -m scripts.paths tally --version 7 --policies 6 --paths 64 \
		--tests-dir 01-bits/tests --only 'test_chaos|test_planted_bug' --out $@
	$(call log_done,$@ written)

# The fix run: the I1 example against checkout_fixed must pass (status 0); the passed line
# stays, without the timing.
ARTIFACTS += $(BUILD)/04-what/fix-run.txt

$(BUILD)/04-what/fix-run.txt: 04-what/section.mk 04-what/s04_what/checkout_fixed.py \
    04-what/tests/test_checkout_stages.py
	@mkdir -p $(@D)
	@log=$$(mktemp); status=0; \
	$(RUN) pytest 04-what/tests/test_checkout_stages.py -q --no-header -p no:cacheprovider \
	  -k 'test_i1_example_pays_shipping and fixed' > $$log 2>&1 || status=$$?; \
	if [ $$status -ne 0 ]; then cat $$log; rm -f $$log; \
	  echo "fix-run: pytest exited $$status, expected 0 (the fix passes)" >&2; exit 1; fi; \
	grep -E '^[0-9]+ passed' $$log | sed -E 's/, [0-9]+ (deselected|warnings?)//g; s/ in [0-9.]+s$$//' > $@; \
	rm -f $$log
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/dispute.txt

$(BUILD)/04-what/dispute.txt: data/questions.csv scripts/paths.py scripts/utils/retro.py
	@$(RUN) python -m scripts.paths retro --only q3 --questions data/questions.csv --out $@
	$(call log_done,$@ written)
