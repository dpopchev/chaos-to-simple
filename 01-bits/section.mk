# 01-bits -- the coverage report and the 64-path grid are build artifacts, so the
# numbers on the slides are measured, not typed. A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/01-bits/coverage.txt $(BUILD)/01-bits/grid.txt

$(BUILD)/01-bits/coverage.txt: 01-bits/s01_bits/chaos.py 01-bits/tests/test_chaos.py
	@mkdir -p $(@D)
	@$(RUN) pytest 01-bits/tests -q -k all_flags \
	  --cov=s01_bits --cov-branch \
	  --cov-report=term-missing > $@
	$(call log_done,$@ written)

$(BUILD)/01-bits/grid.txt: scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths grid --bits 6 --out $@
	$(call log_done,$@ written)
