#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen

class ConcordanceInfo(object):
    def __init__(self):
        self.glyphs = 0
        self.concordant_glyphs = 0
        self.maxdiff = 0
        self.maxdiff_gname = None

    def update(self, diff, gname):
        self.glyphs += 1
        if diff <= 1:
            self.concordant_glyphs += 1
        elif diff > self.maxdiff:
            self.maxdiff = round(diff, 2)
            self.maxdiff_gname = gname

def calc_concordance_and_maxdiff(font, penclass):
    hmtx = font["hmtx"]
    gs = font.getGlyphSet()

    info = ConcordanceInfo()
    for gname in font.getGlyphOrder():
        pen = penclass(gs)
        if "glyf" in font:
            glyf = font["glyf"]
            g = glyf[gname]
            g.draw(pen, glyf)
        else:
            g = gs[gname]
            g.draw(pen)
        if pen.bounds is None:
            continue

        left, _, _, _ = pen.bounds
        lsb = hmtx.metrics[gname][1]

        diff = abs(left - lsb)
        info.update(diff, gname)
    return info

def calc_concordance_of_xMin_yMax_and_control_bbox(font):
    gs = font.getGlyphSet()

    info = ConcordanceInfo()
    for gname in font.getGlyphOrder():
        pen = ControlBoundsPen(gs)
        glyf = font["glyf"]
        g = glyf[gname]
        g.draw(pen, glyf)
        if pen.bounds is None:
            continue

        left, _, _, top = pen.bounds
        g.recalcBounds(glyf)

        diff = abs(left - g.xMin) + abs(top - g.yMax)
        info.update(diff, gname)
    return info

def lsb_means_left_of_control_bbox_or_strict_bbox():
    font_path = sys.argv[1]
    basename = os.path.basename(font_path)
    font = TTFont(font_path, fontNumber=0)
    flag_1 = (font["head"].flags >> 1 & 0x1)

    cb_info = calc_concordance_and_maxdiff(font, ControlBoundsPen)
    b_info = calc_concordance_and_maxdiff(font, BoundsPen)

    print "[{}]".format(basename)
    print " LSB vs bbox.left"
    print "  head.flags[1]: {}".format(flag_1)
    print "  ControlBounds: {}/{} ({}%); maxdiff={} ({})".format(cb_info.concordant_glyphs, cb_info.glyphs, round(100.*cb_info.concordant_glyphs/cb_info.glyphs, 2), cb_info.maxdiff, cb_info.maxdiff_gname)
    print "  Bounds       : {}/{} ({}%); maxdiff={} ({})".format(b_info.concordant_glyphs, b_info.glyphs, round(100.*b_info.concordant_glyphs/b_info.glyphs, 2), b_info.maxdiff, b_info.maxdiff_gname)
    if "glyf" not in font:
        return

    info = calc_concordance_of_xMin_yMax_and_control_bbox(font)
    print " xMin/yMax vs control bbox"
    print "  ControlBounds vs xMin/yMax: {}/{} ({}%); maxdiff={} ({})".format(info.concordant_glyphs, info.glyphs, round(100.*info.concordant_glyphs/info.glyphs, 2), info.maxdiff, info.maxdiff_gname)

def main():
    lsb_means_left_of_control_bbox_or_strict_bbox()

if __name__ == "__main__":
    main()
