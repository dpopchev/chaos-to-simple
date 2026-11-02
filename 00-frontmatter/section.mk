# 00-frontmatter -- the agenda of the talk is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/00-frontmatter/agenda.png $(BUILD)/00-frontmatter/actors.tex $(BUILD)/00-frontmatter/business-map.png
ARTIFACTS += $(foreach n,01 02 03 04 05 06,$(BUILD)/00-frontmatter/agenda-$(n).png)

$(BUILD)/00-frontmatter/business-map.png: scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/style.py data/actors.csv data/cast.csv data/rules.csv
	@$(RUN) python -m scripts.figures business-map --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/actors.tex: scripts/actors_tex.py scripts/utils/palette.py scripts/utils/icons.py data/actors.csv data/contexts.csv
	@$(RUN) python -m scripts.actors_tex --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/agenda.png: scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/icons.py scripts/utils/style.py data/route.csv data/incidents.csv
	@$(RUN) python -m scripts.figures agenda --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/agenda-%.png: scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/icons.py scripts/utils/style.py data/route.csv data/incidents.csv
	@$(RUN) python -m scripts.figures agenda --highlight $* --out $@
	$(call log_done,$@ written)
