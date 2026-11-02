# 05-how -- the seam is drawn in Python from the shell rows, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/05-how/ports.png $(BUILD)/05-how/effects.txt

$(BUILD)/05-how/effects.txt: data/cast.csv 01-bits/s01_bits/chaos.py scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths effects --cast data/cast.csv --source 01-bits/s01_bits/chaos.py --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/05-how/board.png

$(BUILD)/05-how/board.png: data/rules.csv data/questions.csv data/examples.csv $(wildcard 06-simple/tests/*.py) scripts/figures.py scripts/utils/board.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures board --stage 5 --out $@
	$(call log_done,$@ written)

$(BUILD)/05-how/ports.png: data/rules.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures seam --rules data/rules.csv --out $@
	$(call log_done,$@ written)
