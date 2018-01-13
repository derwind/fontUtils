# fontUtils
utilities related to fonts

## otfparser
parser for OTF

## otfanalyzer
analyzer for OTF

## outlineCheckerMini
check outlines of glyphs in a font (inactive project)

## outlineChecker
detect intersections of outlines

## adobe
scripts related to Adobe tools

### adobe/mkicf.py
python version of mkicf.pl

## ai0\_to\_aj1
test project which converts Adobe-Identity-0 CID-keyed fonts to Adobe-Japan1-3 CID-keyed fonts

## latin\_to\_aj1
test project which converts Latin Name-keyed fonts to Adobe-Japan1-3 CID-keyed fonts

## misc_scripts
miscellaneous scripts such as an analyzer of OTF

### misc\_scripts/aalt\_analyzer.py
an analyzer for features aalt.

### misc\_scripts/gpos\_analyzer.py
an analyzer for features in GPOS.

### misc\_scripts/gsub\_analyzer.py
an analyzer for features in GSUB.

### misc\_scripts/compare\_bounds.py
compare bbox of one font with that of another font

### misc\_scripts/compare\_lsb\_with\_bbox.py
compare bbox with hmtx.lsb and show concordance rate

### misc\_scripts/investigateUnicodeRange.py
analyze unicode range and code page range

### misc\_scripts/show\_glyf\_info.py
compare actual bbox with naive bbox and show info when they are different

### misc\_scripts/update\_ttf\_hmtx.py
set hmtx.lsb to glyf.xMin