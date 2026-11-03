# 05-how -- the seam is drawn in Python from the shell rows, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/05-how/ports.png

# The I3 run: pytest must fail exactly once (status 1); the assert line and the summary are kept.
ARTIFACTS += $(BUILD)/05-how/i3-run.txt

$(BUILD)/05-how/i3-run.txt: 05-how/tests/test_i3.py 04-what/s04_what/checkout_v4.py 05-how/section.mk
	@mkdir -p $(@D)
	@tmp=$$(mktemp); \
	status=0; \
	$(RUN) pytest 05-how/tests/test_i3.py --runxfail -q --no-header -p no:cacheprovider \
	  > $$tmp 2>&1 || status=$$?; \
	if [ "$$status" -ne 1 ]; then \
	  cat $$tmp; rm -f $$tmp; \
	  echo "i3-run: expected pytest status 1 (one failed test), got $$status" >&2; exit 1; \
	fi; \
	grep -E '^E +(Assertion|assert)|^[0-9]+ failed' $$tmp | sed -E 's/ in [0-9.]+s.*$$//; s/, [0-9]+ warnings?$$//' > $@; \
	rm -f $$tmp
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/board.png

$(BUILD)/05-how/board.png: $(PALETTE) data/rules.csv data/questions.csv data/examples.csv $(wildcard 06-simple/tests/*.py) scripts/figures.py scripts/utils/board.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures board --stage 5 --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/v5.diff

$(BUILD)/05-how/v5.diff: $(PALETTE) 04-what/s04_what/checkout_v4.py 05-how/s05_how/checkout_v5.py scripts/paths.py scripts/utils/stagediff.py 05-how/section.mk
	@$(RUN) python -m scripts.paths diff --from 04-what/s04_what/checkout_v4.py \
		--to 05-how/s05_how/checkout_v5.py --snippet checkout --start 'total = total_with_vat' \
		--hide 'assert_never|case _ as unreachable' --compact \
		--label-from 'checkout v8' --label-to 'v9' --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/tally-9.txt

$(BUILD)/05-how/tally-9.txt: $(PALETTE) 05-how/section.mk scripts/paths.py scripts/utils/storyboard.py \
    $(wildcard 05-how/tests/*.py)
	@$(RUN) python -m scripts.paths tally --version 9 --policies 9 --paths 512 \
		--tests-dir 05-how/tests --out $@
	$(call log_done,$@ written)

$(BUILD)/05-how/ports.png: $(PALETTE) data/rules.csv data/cast.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures seam --rules data/rules.csv --cast data/cast.csv --out $@
	$(call log_done,$@ written)
