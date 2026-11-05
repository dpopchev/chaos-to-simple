# 08-backup -- the Stacey overview of the backup is drawn in Python, so the frame shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/08-backup/stacey-overview.png $(BUILD)/08-backup/zones.tex

$(BUILD)/08-backup/stacey-overview.png: $(PALETTE) scripts/figures.py scripts/utils/stacey.py scripts/utils/style.py \
		data/route.csv 02-stacey/data/zones.csv 02-stacey/data/labels.csv
	@$(RUN) python -m scripts.figures stacey --arrows --out $@
	$(call log_done,$@ written)

$(BUILD)/08-backup/zones.tex: $(PALETTE) scripts/zones_tex.py scripts/utils/stacey.py 02-stacey/data/zones.csv
	@$(RUN) python -m scripts.zones_tex --zones 02-stacey/data/zones.csv --out $@
	$(call log_done,$@ written)
