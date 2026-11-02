# 06-simple -- the test run and the closing chart are build artifacts.
ARTIFACTS += $(BUILD)/06-simple/pytest.txt $(BUILD)/06-simple/paths.png \
    $(BUILD)/06-simple/epilogue.txt $(BUILD)/06-simple/epilogue.png \
    $(BUILD)/06-simple/wounds.txt $(BUILD)/06-simple/pytest-core.txt

$(BUILD)/06-simple/pytest-core.txt: $(wildcard 06-simple/s06_simple/*.py) $(wildcard 06-simple/tests/*.py) \
    $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py)
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests/test_core_paths.py -q > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/wounds.txt: data/incidents.csv $(wildcard 06-simple/tests/*.py) \
    scripts/paths.py scripts/utils/paths.py
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests -q -rp --no-header -k "$$($(RUN) python -m scripts.paths wounds --incidents data/incidents.csv)" > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/pytest.txt: $(wildcard 06-simple/s06_simple/*.py) $(wildcard 06-simple/tests/*.py) \
    $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py)
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests -q > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/paths.png: $(RULES) scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths chart --rules $(RULES) --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/seventh.diff $(BUILD)/06-simple/worlds.txt

$(BUILD)/06-simple/worlds.txt: $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py) \
    $(wildcard 06-simple/s06_simple/*.py)
	@mkdir -p $(@D)
	@PYTHONPATH=01-bits:04-what:05-how:06-simple $(RUN) python -m s06_simple.worlds --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/seventh.diff: 04-what/s04_what/shipping.py 06-simple/s06_simple/seventh.py scripts/paths.py scripts/utils/stagediff.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths diff --from 04-what/s04_what/shipping.py --to 06-simple/s06_simple/seventh.py \
		--snippet fee --to-snippet fee-digital \
		--label-from shipping_fee --label-to '+ digital' --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/06-simple/seam.diff $(BUILD)/06-simple/pytest-core-summary.txt

$(BUILD)/06-simple/seam.diff: 05-how/s05_how/checkout_v5.py 06-simple/s06_simple/shell.py scripts/paths.py scripts/utils/stagediff.py 06-simple/section.mk
	@$(RUN) python -m scripts.paths diff --from 05-how/s05_how/checkout_v5.py --to 06-simple/s06_simple/shell.py \
		--snippet checkout --start 'match inventory' --hide 'assert_never|case _ as unreachable' \
		--label-from 'checkout v5' --label-to shell --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/pytest-core-summary.txt: $(BUILD)/06-simple/pytest-core.txt 06-simple/section.mk
	@tail -n 4 $< > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/epilogue.txt: $(RULES) data/seventh.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths epilogue --rules $(RULES) --seventh data/seventh.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/epilogue.png: $(RULES) data/seventh.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths epilogue-chart --rules $(RULES) --seventh data/seventh.csv --out $@
	$(call log_done,$@ written)
