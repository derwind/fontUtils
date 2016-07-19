SRC_DIR      = .
SRC_FONT     = $(SRC_DIR)/SourceHanSansJP-Regular.otf
SRC_FEATURES = $(SRC_DIR)/features.JP

TARGET   = SourceHanSansJP-Regular_AJ1.otf
TARGET_FEATURES = features
CID_FONT = SourceHanSansJP.cid
MAP_FILE = map.txt

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(CID_FONT) $(TARGET_FEATURES)
	makeotf -f $< -o $@ -ff $(TARGET_FEATURES) -ch UniJIS-UTF32-H

$(CID_FONT): $(MAP_FILE)
	mergeFonts -cid cidfontinfo $@ $< $(SRC_FONT)

$(MAP_FILE): $(SRC_FONT)
	python -B mk_map.py $< UniJIS-UTF32-H > $@

$(TARGET_FEATURES): $(SRC_FEATURES) $(MAP_FILE)
	python -B mk_features.py $^ > $@


.PHONY: clean
clean:
	rm -rf $(TARGET) $(TARGET_FEATURES) $(CID_FONT) $(MAP_FILE) current.fpr

.PHONY: map_clean
map_clean:
	rm -rf $(MAP_FILE)

.PHONY: features_clean
features_clean:
	rm -rf $(TARGET_FEATURES)
