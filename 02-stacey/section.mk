# 02-stacey -- the Stacey matrix is drawn in Python, so the slide shows a built figure.
# A plain `#` keeps it out of make help.
ARTIFACTS += $(BUILD)/02-stacey/stacey.png \
	$(foreach n,01 02 03 04 05 06,$(BUILD)/02-stacey/stacey-$(n).png) \
	$(foreach k,0 1 2,$(BUILD)/02-stacey/bubble-$(k).txt)

$(foreach k,0 1 2,$(BUILD)/02-stacey/bubble-$(k).txt) &: 02-stacey/data/bubbles.csv \
		data/actors.csv scripts/paths.py scripts/utils/storyboard.py
	@$(RUN) python -m scripts.paths bubbles --bubbles 02-stacey/data/bubbles.csv \
	  --actors data/actors.csv --out $(BUILD)/02-stacey
	$(call log_done,$(BUILD)/02-stacey bubbles written)

$(BUILD)/02-stacey/stacey.png: scripts/figures.py scripts/utils/stacey.py scripts/utils/style.py \
		data/route.csv 02-stacey/data/zones.csv 02-stacey/data/labels.csv
	@$(RUN) python -m scripts.figures stacey --out $@
	$(call log_done,$@ written)

$(BUILD)/02-stacey/stacey-%.png: scripts/figures.py scripts/utils/stacey.py scripts/utils/style.py \
		data/route.csv 02-stacey/data/zones.csv 02-stacey/data/labels.csv
	@$(RUN) python -m scripts.figures stacey --plain --arrows --highlight $* --out $@
	$(call log_done,$@ written)
