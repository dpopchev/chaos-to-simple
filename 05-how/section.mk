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
		--name checkout --version 9 --policies 9 --paths 512 --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/tests-order.txt

$(BUILD)/05-how/tests-order.txt: 05-how/section.mk scripts/paths.py scripts/utils/storyboard.py \
    $(wildcard 05-how/tests/*.py)
	@$(RUN) python -m scripts.paths tally --version 8 --tests-dir 05-how/tests \
		--only test_oo_order --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/oo.txt

$(BUILD)/05-how/oo.txt: 05-how/section.mk scripts/paths.py scripts/utils/storyboard.py \
    05-how/s05_how/oo_checkout.py
	@$(RUN) python -m scripts.paths tally-code --name Checkout --version 8 --policies 2 --paths 4 \
		--source 05-how/s05_how/oo_checkout.py --snippet oo --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/ports-code.txt

$(BUILD)/05-how/ports-code.txt: 05-how/section.mk scripts/paths.py scripts/utils/storyboard.py \
    05-how/s05_how/ports.py
	@$(RUN) python -m scripts.paths tally-code --name ports --version 9 --policies 3 --paths 8 \
		--source 05-how/s05_how/ports.py --snippet ports --out $@
	$(call log_done,$@ written)

# The fakes' acceptance: pyright must exit 0 over the fakes and their test; only its summary is kept.
ARTIFACTS += $(BUILD)/05-how/pyright.txt

$(BUILD)/05-how/pyright.txt: 05-how/section.mk 05-how/s05_how/fakes.py 05-how/s05_how/ports.py \
    05-how/tests/test_ports.py
	@mkdir -p $(@D)
	@tmp=$$(mktemp); \
	if ! $(RUN) pyright 05-how/s05_how/fakes.py 05-how/tests/test_ports.py > $$tmp 2>&1; then \
	  cat $$tmp; rm -f $$tmp; echo "pyright: the fakes are not accepted" >&2; exit 1; \
	fi; \
	grep -E '^[0-9]+ errors?, ' $$tmp | sed -E 's/ +$$//' > $@; \
	rm -f $$tmp
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/imports.txt

$(BUILD)/05-how/imports.txt: 05-how/section.mk scripts/paths.py scripts/utils/imports.py \
    04-what/s04_what/pricing.py 04-what/s04_what/shipping.py 04-what/s04_what/tax.py \
    05-how/s05_how/ports.py 05-how/s05_how/checkout_v5.py
	@$(RUN) python -m scripts.paths imports --source 04-what/s04_what/pricing.py \
		--source 04-what/s04_what/shipping.py --source 04-what/s04_what/tax.py \
		--source 05-how/s05_how/ports.py --source 05-how/s05_how/checkout_v5.py --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/imports.png

$(BUILD)/05-how/imports.png: 05-how/section.mk scripts/paths.py scripts/utils/imports.py \
    scripts/utils/style.py scripts/utils/palette.py data/contexts.csv \
    04-what/s04_what/pricing.py 04-what/s04_what/shipping.py 04-what/s04_what/tax.py \
    05-how/s05_how/ports.py 05-how/s05_how/checkout_v5.py
	@$(RUN) python -m scripts.paths imports-figure --source 04-what/s04_what/pricing.py \
		--source 04-what/s04_what/shipping.py --source 04-what/s04_what/tax.py \
		--source 05-how/s05_how/ports.py --source 05-how/s05_how/checkout_v5.py --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/fakes-code.txt

$(BUILD)/05-how/fakes-code.txt: 05-how/section.mk scripts/paths.py scripts/utils/storyboard.py \
    05-how/s05_how/fakes.py
	@$(RUN) python -m scripts.paths tally-code --name fakes --version 9 --policies 2 --paths 4 \
		--source 05-how/s05_how/fakes.py --snippet fakes --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/promise.png

$(BUILD)/05-how/promise.png: $(PALETTE) 05-how/data/promise.csv scripts/figures.py scripts/utils/promise.py
	@$(RUN) python -m scripts.figures promise --out $@
	$(call log_done,$@ written)

$(BUILD)/05-how/ports.png: $(PALETTE) data/rules.csv data/cast.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures seam --rules data/rules.csv --cast data/cast.csv --out $@
	$(call log_done,$@ written)
