# 07-close -- the rules board at stage 06, every row green with its test name.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/07-close/board.png

$(BUILD)/07-close/board.png: data/rules.csv data/questions.csv data/examples.csv $(wildcard 06-simple/tests/*.py) scripts/figures.py scripts/utils/board.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures board --stage 6 --out $@
	$(call log_done,$@ written)
