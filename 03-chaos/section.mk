# 03-chaos -- the domain story is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/03-chaos/story.png $(BUILD)/03-chaos/growth.png
ARTIFACTS += $(BUILD)/03-chaos/example_map.png

$(BUILD)/03-chaos/example_map.png: data/rules.csv data/examples.csv 03-chaos/data/questions.md scripts/figures.py scripts/utils/figures.py scripts/utils/examples.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures example-map --rules data/rules.csv --examples data/examples.csv --questions 03-chaos/data/questions.md --out $@
	$(call log_done,$@ written)

$(BUILD)/03-chaos/growth.png: data/cast.csv scripts/paths.py scripts/utils/paths.py scripts/utils/style.py
	@$(RUN) python -m scripts.paths growth --cast data/cast.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/03-chaos/story.png: scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures story --out $@
	$(call log_done,$@ written)
