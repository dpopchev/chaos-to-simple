### 01-bits: the coverage report and the 64-path grid are build artifacts, so the numbers
### on the slides are measured, not typed.
ARTIFACTS += build/01-bits/coverage.txt build/01-bits/grid.txt

build/01-bits/coverage.txt: 01-bits/s01_bits/chaos.py 01-bits/tests/test_chaos.py
	@mkdir -p $(@D)
	$(UV) run pytest 01-bits/tests -q -k all_flags --cov=s01_bits --cov-branch \
	  --cov-report=term-missing -p no:cacheprovider > $@
	@$(call log_ok,$@)

build/01-bits/grid.txt: scripts/paths.py scripts/utils/paths.py
	@mkdir -p $(@D)
	$(PY) -m scripts.paths grid --bits 6 --out $@
	@$(call log_ok,$@)
