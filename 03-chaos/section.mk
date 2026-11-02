# 03-chaos -- the domain story is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/03-chaos/diagrams/journey.png
ARTIFACTS += $(BUILD)/03-chaos/rules.txt

$(BUILD)/03-chaos/rules.txt: data/rules.csv data/cast.csv scripts/paths.py scripts/utils/paths.py
	@$(RUN) python -m scripts.paths rules --rules data/rules.csv --columns bit,who,rule --cast data/cast.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/retro.txt

$(BUILD)/03-chaos/retro.txt: data/questions.csv data/actors.csv scripts/paths.py scripts/utils/retro.py
	@$(RUN) python -m scripts.paths retro --questions data/questions.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/grid-9.png

$(BUILD)/03-chaos/grid-9.png: data/rules.csv 01-bits/data/tested.csv scripts/figures.py scripts/utils/paths.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures grid-panels --rules data/rules.csv --tested 01-bits/data/tested.csv --out $@
	$(call log_done,$@ written)

ARTIFACTS += $(BUILD)/03-chaos/doubling-512.png

$(BUILD)/03-chaos/doubling-512.png: data/cast.csv scripts/figures.py scripts/utils/paths.py \
    scripts/utils/style.py
	@$(RUN) python -m scripts.figures doubling --cast data/cast.csv --room 16 --out $@
	$(call log_done,$@ written)

$(BUILD)/03-chaos/diagrams/journey.png: data/questions.csv data/actors.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures journey --questions data/questions.csv --out $@
	$(call log_done,$@ written)
