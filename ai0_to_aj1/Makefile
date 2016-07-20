SRC_DIR      = ../../source-han-sans/Regular
SRC_FONT     = $(SRC_DIR)/SourceHanSansJP-Regular.otf
SRC_FEATURES = $(SRC_DIR)/features.JP

TARGET   = SourceHanSansJP-Regular_AJ1.otf
TARGET_FEATURES  = features
TARGET_SEQUENCES = sequences.txt
CID_FONT = SourceHanSansJP.cid
MAP_FILE = map.txt

TX_DIR    = $(shell which tx)
FDK_DIR   = $(dir $(TX_DIR))/../..
CMAP      = "$(FDK_DIR)/Tools/SharedData/Adobe Cmaps/Adobe-Japan1/UniJIS-UTF32-H"
SEQUENCES = "$(FDK_DIR)/Tools/SharedData/Adobe Cmaps/Adobe-Japan1/Adobe-Japan1_sequences.txt"

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(CID_FONT) $(TARGET_FEATURES) $(TARGET_SEQUENCES)
	makeotf -f $< -o $@ -ff $(TARGET_FEATURES) -ch $(CMAP) -ci $(TARGET_SEQUENCES) 2>&1 | tee build.txt

$(CID_FONT): $(MAP_FILE)
	mergeFonts -cid cidfontinfo $@ $< $(SRC_FONT)

$(MAP_FILE): $(SRC_FONT)
	python -B mk_map.py $< $(CMAP) > $@

$(TARGET_FEATURES): $(SRC_FEATURES) $(MAP_FILE)
	python -B mk_features.py $^ > $@

$(TARGET_SEQUENCES):
	python -B mk_sequences.py $(SEQUENCES) > $@


.PHONY: clean
clean:
	rm -rf $(TARGET) $(TARGET_FEATURES) $(TARGET_SEQUENCES) $(CID_FONT) $(MAP_FILE) current.fpr build.txt

.PHONY: map_clean
map_clean:
	rm -rf $(MAP_FILE)

.PHONY: features_clean
features_clean:
	rm -rf $(TARGET_FEATURES)
