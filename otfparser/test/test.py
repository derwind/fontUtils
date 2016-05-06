#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import fontTools.ttLib

font =  fontTools.ttLib.TTFont(sys.argv[1])
cff = font["CFF "]

topDictIndex = cff.cff.topDictIndex
topDict = topDictIndex[0] # XXX

print "[Top DICT]"
for k, v in topDict.rawDict.items():
    print "  {0}: {1}".format(k, v)

print
print "  numGlyphs : {0}".format(topDict.numGlyphs)
print "  charset   : {0}".format(topDict.charset)
print "  GlyphOrder: {0}".format(topDict.getGlyphOrder())

gs = font.getGlyphSet()
for gname in topDict.getGlyphOrder():
    g = gs[gname]

# replace CFF of cid00843 with that of cid00845
# gs["cid00843"]._glyph.setBytecode( gs["cid00845"]._glyph.bytecode )
# font.save("out.otf")
