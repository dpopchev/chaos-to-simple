# 00-frontmatter -- the route of the talk is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/00-frontmatter/route.png

$(BUILD)/00-frontmatter/route.png: scripts/figures.py scripts/utils/figures.py scripts/utils/style.py
	@$(RUN) python -m scripts.figures route --out $@
	$(call log_done,$@ written)
