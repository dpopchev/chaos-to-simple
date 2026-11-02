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

ARTIFACTS += $(BUILD)/04-what/fix.diff $(BUILD)/04-what/v4.diff

$(BUILD)/04-what/fix.diff: 01-bits/s01_bits/chaos.py 04-what/s04_what/checkout_fixed.py scripts/paths.py scripts/utils/stagediff.py
	@$(RUN) python -m scripts.paths diff --from 01-bits/s01_bits/chaos.py \
		--to 04-what/s04_what/checkout_fixed.py --snippet checkout --out $@
	$(call log_done,$@ written)

$(BUILD)/04-what/v4.diff: 04-what/s04_what/checkout_fixed.py 04-what/s04_what/checkout_v4.py 04-what/section.mk scripts/paths.py scripts/utils/stagediff.py
	@$(RUN) python -m scripts.paths diff --from 04-what/s04_what/checkout_fixed.py \
		--to 04-what/s04_what/checkout_v4.py --snippet checkout --added-only --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/dispute.txt

$(BUILD)/04-what/dispute.txt: data/questions.csv scripts/paths.py scripts/utils/retro.py
	@$(RUN) python -m scripts.paths retro --only q3 --questions data/questions.csv --out $@
	$(call log_done,$@ written)
