# 03-chaos -- the domain story is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/03-chaos/story.png

$(BUILD)/03-chaos/story.png: scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures story --out $@
	$(call log_done,$@ written)
