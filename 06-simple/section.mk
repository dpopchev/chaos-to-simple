# 06-simple -- the test run and the closing chart are build artifacts.
ARTIFACTS += $(BUILD)/06-simple/pytest.txt $(BUILD)/06-simple/paths.png \
    $(BUILD)/06-simple/epilogue.txt $(BUILD)/06-simple/wounds.txt

$(BUILD)/06-simple/wounds.txt: data/incidents.csv $(wildcard 06-simple/tests/*.py) \
    scripts/paths.py scripts/utils/paths.py
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests -v -k "$$($(RUN) python -m scripts.paths wounds --incidents data/incidents.csv)" > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/pytest.txt: $(wildcard 06-simple/s06_simple/*.py) $(wildcard 06-simple/tests/*.py) \
    $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py)
	@mkdir -p $(@D)
	@$(RUN) pytest 06-simple/tests -q > $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/paths.png: $(RULES) scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths chart --rules $(RULES) --out $@
	$(call log_done,$@ written)

$(BUILD)/06-simple/epilogue.txt: $(RULES) data/seventh.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths epilogue --rules $(RULES) --seventh data/seventh.csv --out $@
	$(call log_done,$@ written)
