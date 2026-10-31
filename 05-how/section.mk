# 05-how -- the seam is drawn in Python from the shell rows, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/05-how/ports.png

$(BUILD)/05-how/ports.png: data/rules.csv scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures seam --rules data/rules.csv --out $@
	$(call log_done,$@ written)
