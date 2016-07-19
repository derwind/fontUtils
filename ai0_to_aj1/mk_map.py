#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""make a map file for mergeFonts"""

import sys, os
from fontTools.ttLib import TTFont
from cmap_reader import readCMap

font = TTFont(sys.argv[1])
aj1_cmap = readCMap(sys.argv[2])
cmap = font["cmap"].getcmap(platformID=0, platEncID=3).cmap
geta_uni = 0x3013
geta_ai0_cid = int(cmap[geta_uni].replace("cid", ""))
std_last_cid = 9353
# reverseMap: name(cidXXXXX)-->GID
#reverseMap = font.getReverseGlyphMap()

# fill with GETA in case
aj1_cid2ai0_cid = {}
for cid in range(1, std_last_cid+1):
    aj1_cid2ai0_cid[cid] = geta_ai0_cid

# map AJ1 CID to AI0 CID
for uni, name in cmap.items():
    if name == ".notdef":
        continue
    if not uni in aj1_cmap.keys():
        continue
    aj1_cid = aj1_cmap[uni]
    if aj1_cid > std_last_cid: # not Std
        continue

    ai0_cid = int(name.replace("cid", ""))
    #gid = reverseMap[name]
    aj1_cid2ai0_cid[aj1_cid] = ai0_cid
    #cid2name[cid] = name

print("mergeFonts")
print("00000 00000")
for aj1_cid, ai0_cid in sorted(aj1_cid2ai0_cid.items(), key=lambda x:x[0]):
    print("%05d %05d" % (aj1_cid, ai0_cid))
