# 02-stacey -- the Stacey matrix is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/02-stacey/stacey.png

$(BUILD)/02-stacey/stacey.png: scripts/figures.py scripts/utils/stacey.py scripts/utils/style.py \
		data/route.csv 02-stacey/data/zones.csv 02-stacey/data/labels.csv
	@$(RUN) python -m scripts.figures stacey --out $@
	$(call log_done,$@ written)
