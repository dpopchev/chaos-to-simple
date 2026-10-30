### 06-simple: the test run and the closing chart are build artifacts.
ARTIFACTS += build/06-simple/pytest.txt build/06-simple/paths.png

build/06-simple/pytest.txt: $(wildcard 06-simple/s06_simple/*.py) $(wildcard 06-simple/tests/*.py) \
    $(wildcard 04-what/s04_what/*.py) $(wildcard 05-how/s05_how/*.py)
	@mkdir -p $(@D)
	$(UV) run pytest 06-simple/tests -q -p no:cacheprovider > $@
	@$(call log_ok,$@)

build/06-simple/paths.png: $(RULES) scripts/paths.py scripts/utils/paths.py
	@mkdir -p $(@D)
	$(PY) -m scripts.paths chart --rules $(RULES) --out $@
	@$(call log_ok,$@)
