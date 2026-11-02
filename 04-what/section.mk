# 04-what -- the contexts table is a build artifact, joined from the rules and the cast, so the
# numbers on the slides are measured, not typed. A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/04-what/contexts.txt $(BUILD)/04-what/moves.png

$(BUILD)/04-what/moves.png: data/rules.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py scripts/utils/paths.py
	@$(RUN) python -m scripts.figures moves --rules data/rules.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/04-what/board.png

$(BUILD)/04-what/board.png: data/rules.csv data/questions.csv data/examples.csv $(wildcard 06-simple/tests/*.py) scripts/figures.py scripts/utils/board.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures board --stage 4 --out $@
	$(call log_done,$@ written)

$(BUILD)/04-what/contexts.txt: data/rules.csv data/cast.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths contexts --rules data/rules.csv --cast data/cast.csv --out $@
	$(call log_done,$@ written)
