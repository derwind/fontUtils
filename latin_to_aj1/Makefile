SRC_DIR      = ../../source-sans-pro/Roman/Regular
SRC_FONT     = $(SRC_DIR)/font.ufo

TARGET   = source-cid-test.otf
FEATURES = features
CID_FONT = source-cid-test.cid
SYMBOL_T1_FONT     = source-SYMBOL.pfa
FIGURES_T1_FONT    = source-FIGURES.pfa
LOWERCASE_T1_FONT  = source-LOWERCASE.pfa
UPPERCASE_T1_FONT  = source-UPPERCASE.pfa

TX_DIR    = $(shell which tx)
FDK_DIR   = $(dir $(TX_DIR))/../..
CMAP      = "$(FDK_DIR)/Tools/SharedData/Adobe Cmaps/Adobe-Japan1/UniJIS-UTF32-H"
SEQUENCES = sequences.txt

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(CID_FONT)
	makeotf -r -f $< -o $@ -ff $(FEATURES) -ch $(CMAP) -ci $(SEQUENCES) 2>&1 | tee build.txt
	autohint $(TARGET)

$(CID_FONT): $(SYMBOL_T1_FONT) $(FIGURES_T1_FONT) $(LOWERCASE_T1_FONT) $(UPPERCASE_T1_FONT)
	mergeFonts -cid cidfontinfo $@ map_SYMBOL.txt $(SYMBOL_T1_FONT) map_FIGURES.txt $(FIGURES_T1_FONT) map_LOWERCASE.txt $(LOWERCASE_T1_FONT) map_UPPERCASE.txt $(UPPERCASE_T1_FONT)

$(SYMBOL_T1_FONT):
	tx -t1 -o $@ $(SRC_FONT)
#	tx -t1 -g 1,1146,1151 -o $@ $(SRC_FONT)

$(FIGURES_T1_FONT):
	tx -t1 -g 1087-1096 -o $@ $(SRC_FONT)

$(LOWERCASE_T1_FONT):
	tx -t1 -g 28-53 -o $@ $(SRC_FONT)

$(UPPERCASE_T1_FONT):
	tx -t1 -g 2-27 -o $@ $(SRC_FONT)

.PHONY: clean
clean:
	rm -rf $(TARGET) $(CID_FONT) $(SYMBOL_T1_FONT) $(FIGURES_T1_FONT) $(LOWERCASE_T1_FONT) $(UPPERCASE_T1_FONT) current.fpr build.txt

.PHONY: features_clean
features_clean:
	rm -rf $(TARGET_FEATURES)
