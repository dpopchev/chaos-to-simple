# 03-chaos -- the domain story is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/03-chaos/diagrams/journey.png
ARTIFACTS += $(BUILD)/03-chaos/rules.txt

$(BUILD)/03-chaos/rules.txt: $(PALETTE) data/rules.csv data/cast.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths rules --rules data/rules.csv --columns bit,who,rule --cast data/cast.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/retro.txt

$(BUILD)/03-chaos/retro.txt: $(PALETTE) data/questions.csv data/actors.csv scripts/paths.py scripts/utils/retro.py
	@$(RUN) python -m scripts.paths retro --questions data/questions.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/grid-9.png

$(BUILD)/03-chaos/grid-9.png: $(PALETTE) data/rules.csv 01-bits/data/tested.csv scripts/figures.py scripts/utils/paths.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures grid-panels --rules data/rules.csv --tested 01-bits/data/tested.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/doubling-512.png

$(BUILD)/03-chaos/doubling-512.png: $(PALETTE) data/cast.csv scripts/figures.py scripts/utils/paths.py \
    scripts/utils/style.py
	@$(RUN) python -m scripts.figures doubling --cast data/cast.csv --room 16 --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/board.png

$(BUILD)/03-chaos/board.png: $(PALETTE) data/rules.csv data/questions.csv data/examples.csv $(wildcard 06-simple/tests/*.py) scripts/figures.py scripts/utils/board.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures board --stage 3 --out $@
	$(call log_done,$@ written)

$(BUILD)/03-chaos/diagrams/journey.png: $(PALETTE) data/questions.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures journey --questions data/questions.csv --out $@
	$(call log_done,$@ written)
