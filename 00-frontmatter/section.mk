# 00-frontmatter -- the agenda of the talk is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/00-frontmatter/agenda.png $(BUILD)/00-frontmatter/actors.tex $(BUILD)/00-frontmatter/business-map.png
ARTIFACTS += $(foreach n,00 01 02 03 04 05 06,$(BUILD)/00-frontmatter/agenda-$(n).png)
ARTIFACTS += $(BUILD)/00-frontmatter/beats.tex $(BUILD)/00-frontmatter/stacey-overview.png

$(BUILD)/00-frontmatter/stacey-overview.png: $(PALETTE) scripts/figures.py scripts/utils/stacey.py scripts/utils/style.py \
		data/route.csv 02-stacey/data/zones.csv 02-stacey/data/labels.csv
	@$(RUN) python -m scripts.figures stacey --arrows --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/beats.tex: $(PALETTE) scripts/beats_tex.py scripts/utils/beats.py scripts/utils/lines.py data/lines.csv
	@$(RUN) python -m scripts.beats_tex --lines data/lines.csv --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/business-map.png: $(PALETTE) scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/style.py data/actors.csv data/cast.csv data/rules.csv
	@$(RUN) python -m scripts.figures business-map --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/actors.tex: $(PALETTE) scripts/actors_tex.py scripts/utils/icons.py
	@$(RUN) python -m scripts.actors_tex --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/agenda.png: $(PALETTE) scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/icons.py scripts/utils/style.py data/route.csv data/incidents.csv 02-stacey/data/zones.csv scripts/utils/stacey.py
	@$(RUN) python -m scripts.figures agenda --out $@
	$(call log_done,$@ written)

$(BUILD)/00-frontmatter/agenda-%.png: $(PALETTE) scripts/figures.py scripts/utils/stage.py scripts/utils/figures.py scripts/utils/icons.py scripts/utils/style.py data/route.csv data/incidents.csv 02-stacey/data/zones.csv scripts/utils/stacey.py
	@$(RUN) python -m scripts.figures agenda --highlight $* --out $@
	$(call log_done,$@ written)
