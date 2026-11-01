# 00-frontmatter -- the route of the talk is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/00-frontmatter/route.png $(BUILD)/00-frontmatter/actors.tex $(BUILD)/00-frontmatter/business-map.png

$(BUILD)/00-frontmatter/business-map.png: scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/style.py data/actors.csv data/cast.csv data/rules.csv
	@$(RUN) python -m scripts.figures business-map --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/actors.tex: scripts/actors_tex.py scripts/utils/palette.py scripts/utils/icons.py data/actors.csv data/contexts.csv
	@$(RUN) python -m scripts.actors_tex --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/route.png: scripts/figures.py scripts/utils/figures.py scripts/utils/style.py data/route.csv data/incidents.csv
	@$(RUN) python -m scripts.figures route --out $@
	$(call log_done,$@ written)
