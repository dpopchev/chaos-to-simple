# 06-simple -- the test run and the closing chart are build artifacts.
ARTIFACTS += $(BUILD)/06-simple/pytest.txt $(BUILD)/06-simple/paths.png \
    $(BUILD)/06-simple/epilogue.txt $(BUILD)/06-simple/epilogue.png \
    $(BUILD)/06-simple/wounds.txt $(BUILD)/06-simple/pytest-core.txt \
    $(BUILD)/06-simple/postmortem.txt $(BUILD)/06-simple/cards.txt

$(BUILD)/06-simple/cards.txt: $(PALETTE) data/incidents.csv data/examples.csv data/rules.csv $(BUILD)/06-simple/wounds.txt scripts/paths.py scripts/utils/cards.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths cards --incidents data/incidents.csv --examples data/examples.csv --wounds $(BUILD)/06-simple/wounds.txt --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/postmortem.txt: $(PALETTE) data/incidents.csv data/rules.csv data/contexts.csv scripts/paths.py scripts/utils/paths.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths postmortem --incidents data/incidents.csv --rules data/rules.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/pytest-core.txt: $(wildcard 06-simple/s06_simple/*.py) $(wildcard 06-simple/tests/*.py) \
    $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py)
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests/test_core_paths.py -q > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/wounds.txt: $(PALETTE) data/incidents.csv $(wildcard 06-simple/tests/*.py) \
    scripts/paths.py scripts/utils/paths.py
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests -q -rp --no-header -k "$$($(RUN) python -m scripts.paths wounds --incidents data/incidents.csv)" > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/pytest.txt: $(wildcard 06-simple/s06_simple/*.py) $(wildcard 06-simple/tests/*.py) \
    $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py)
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests -q > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/paths.png: $(PALETTE) $(RULES) scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths chart --rules $(RULES) --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/seventh.diff $(BUILD)/06-simple/worlds.txt

$(BUILD)/06-simple/worlds.txt: $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py) \
    $(wildcard 06-simple/s06_simple/*.py)
	@mkdir -p $(@D)
	@PYTHONPATH=01-bits:04-what:05-how:06-simple $(RUN) python -m s06_simple.worlds --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/seventh.diff: $(PALETTE) 04-what/s04_what/shipping.py 06-simple/s06_simple/seventh.py scripts/paths.py scripts/utils/stagediff.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths diff --from 04-what/s04_what/shipping.py --to 06-simple/s06_simple/seventh.py \
		--snippet fee --to-snippet fee-digital \
		--name shipping_fee --version 11 --policies 4 --paths 16 --compact --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/member15.diff

$(BUILD)/06-simple/member15.diff: $(PALETTE) 04-what/s04_what/pricing.py 06-simple/s06_simple/member15.py scripts/paths.py scripts/utils/stagediff.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths diff --from 04-what/s04_what/pricing.py --to 06-simple/s06_simple/member15.py \
		--snippet discounted --to-snippet member15 --compact \
		--label-from 'discount 10%' --label-to 'discount 15%' --out $@
	$(call log_done,$@ written)

# The gateway swap's acceptance: pyright must exit 0 over the other gateway and its test.
ARTIFACTS += $(BUILD)/06-simple/pyright.txt

$(BUILD)/06-simple/pyright.txt: 06-simple/section.mk 06-simple/s06_simple/other_gateway.py \
    05-how/s05_how/ports.py 06-simple/tests/test_other_gateway.py
	@mkdir -p $(@D)
	@tmp=$$(mktemp); \
	if ! $(RUN) pyright 06-simple/s06_simple/other_gateway.py \
	    06-simple/tests/test_other_gateway.py > $$tmp 2>&1; then \
	  cat $$tmp; rm -f $$tmp; echo "pyright: the other gateway is not accepted" >&2; exit 1; \
	fi; \
	grep -E '^[0-9]+ errors?, ' $$tmp | sed -E 's/ +$$//' > $@; \
	rm -f $$tmp
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/responsibilities.png \
    $(foreach n,pricing payment shipping,$(BUILD)/06-simple/responsibilities-$(n).png)

$(BUILD)/06-simple/responsibilities.png: $(PALETTE) $(RULES) scripts/figures.py \
    scripts/utils/responsibilities.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures responsibilities --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/responsibilities-%.png: $(PALETTE) $(RULES) scripts/figures.py \
    scripts/utils/responsibilities.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures responsibilities --highlight $* --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/seam.diff $(BUILD)/06-simple/pytest-core-summary.txt

$(BUILD)/06-simple/seam.diff: $(PALETTE) 05-how/s05_how/checkout_v5.py 06-simple/s06_simple/shell.py scripts/paths.py scripts/utils/stagediff.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths diff --from 05-how/s05_how/checkout_v5.py --to 06-simple/s06_simple/shell.py \
		--snippet checkout --hide 'assert_never|case _ as unreachable' --compact \
		--label-from 'checkout v9' --label-to 'v10' --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/price.txt $(BUILD)/06-simple/shell.txt \
    $(BUILD)/06-simple/tests-core.txt $(BUILD)/06-simple/worlds-code.txt

$(BUILD)/06-simple/price.txt: 06-simple/section.mk scripts/paths.py scripts/utils/storyboard.py \
    06-simple/s06_simple/core.py
	@$(RUN) python -m scripts.paths tally-code --name price --version 10 --policies 6 --paths 64 \
		--source 06-simple/s06_simple/core.py --snippet price --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/shell.txt: 06-simple/section.mk scripts/paths.py scripts/utils/storyboard.py \
    06-simple/s06_simple/shell.py
	@$(RUN) python -m scripts.paths tally-code --name checkout --version 10 --policies 3 --paths 8 \
		--source 06-simple/s06_simple/shell.py --snippet checkout --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/tests-core.txt: 06-simple/section.mk scripts/paths.py scripts/utils/storyboard.py \
    $(wildcard 06-simple/tests/*.py)
	@$(RUN) python -m scripts.paths tally --version 10 --tests-dir 06-simple/tests \
		--only test_core_paths --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/worlds-code.txt: 06-simple/section.mk scripts/paths.py scripts/utils/storyboard.py \
    06-simple/s06_simple/worlds.py
	@$(RUN) python -m scripts.paths tally-code --name world --version 10 --policies 3 --paths 8 \
		--source 06-simple/s06_simple/worlds.py --snippet eight --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/request.txt $(BUILD)/06-simple/outcome.txt

$(BUILD)/06-simple/request.txt: 06-simple/section.mk scripts/paths.py scripts/utils/storyboard.py \
    06-simple/s06_simple/core.py
	@$(RUN) python -m scripts.paths tally-code --name Request --version 10 --policies 6 --paths 64 \
		--source 06-simple/s06_simple/core.py --snippet request --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/outcome.txt: 06-simple/section.mk scripts/paths.py scripts/utils/storyboard.py \
    06-simple/s06_simple/shell.py
	@$(RUN) python -m scripts.paths tally-code --name Outcome --version 10 --policies 3 --paths 8 \
		--source 06-simple/s06_simple/shell.py --snippet outcome --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/ifs.txt $(BUILD)/06-simple/imports.txt $(BUILD)/06-simple/ifs.png \
    $(BUILD)/06-simple/imports.png

$(BUILD)/06-simple/imports.png: $(PALETTE) 06-simple/section.mk scripts/paths.py scripts/utils/imports.py \
    06-simple/s06_simple/core.py 06-simple/s06_simple/shell.py
	@$(RUN) python -m scripts.paths imports-figure --source 06-simple/s06_simple/core.py \
		--source 06-simple/s06_simple/shell.py --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/ifs.png: $(PALETTE) 06-simple/section.mk scripts/paths.py scripts/utils/imports.py \
    04-what/s04_what/pricing.py 04-what/s04_what/shipping.py 04-what/s04_what/tax.py \
    06-simple/s06_simple/core.py 06-simple/s06_simple/shell.py
	@$(RUN) python -m scripts.paths ifs-chart --source 04-what/s04_what/pricing.py \
		--source 04-what/s04_what/shipping.py --source 04-what/s04_what/tax.py \
		--source 06-simple/s06_simple/core.py --source 06-simple/s06_simple/shell.py --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/ifs.txt: 06-simple/section.mk scripts/paths.py scripts/utils/imports.py \
    04-what/s04_what/pricing.py 04-what/s04_what/shipping.py 04-what/s04_what/tax.py \
    06-simple/s06_simple/core.py 06-simple/s06_simple/shell.py
	@$(RUN) python -m scripts.paths ifs --source 04-what/s04_what/pricing.py \
		--source 04-what/s04_what/shipping.py --source 04-what/s04_what/tax.py \
		--source 06-simple/s06_simple/core.py --source 06-simple/s06_simple/shell.py --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/imports.txt: 06-simple/section.mk scripts/paths.py scripts/utils/imports.py \
    06-simple/s06_simple/core.py 06-simple/s06_simple/shell.py
	@$(RUN) python -m scripts.paths imports --source 06-simple/s06_simple/core.py \
		--source 06-simple/s06_simple/shell.py --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/pytest-core-summary.txt: $(BUILD)/06-simple/pytest-core.txt 06-simple/section.mk
	@tail -n 4 $< > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/epilogue.txt: $(PALETTE) $(RULES) data/seventh.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths epilogue --rules $(RULES) --seventh data/seventh.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/epilogue.png: $(PALETTE) $(RULES) data/seventh.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths epilogue-chart --rules $(RULES) --seventh data/seventh.csv --out $@
	$(call log_done,$@ written)
