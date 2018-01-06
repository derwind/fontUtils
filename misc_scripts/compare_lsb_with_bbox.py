#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen

def calc_concordance_and_maxdiff(font, penclass):
    hmtx = font["hmtx"]
    gs = font.getGlyphSet()

    cnt = concordance_cnt = 0
    maxdiff = 0
    for gname in font.getGlyphOrder():
        g = gs[gname]

        pen = penclass(gs)
        g.draw(pen)
        if pen.bounds is None:
            continue

        left, _, _, _ = pen.bounds
        lsb = hmtx.metrics[gname][1]

        cnt += 1
        diff = abs(left - lsb)
        if diff <= 1:
            concordance_cnt += 1
        elif diff > maxdiff:
            maxdiff = diff
    return cnt, concordance_cnt, round(maxdiff, 2)

def lsb_means_left_of_control_bbox_or_strict_bbox():
    font_path = sys.argv[1]
    basename = os.path.basename(font_path)
    font = TTFont(font_path, fontNumber=0)
    flag_1 = (font["head"].flags >> 1 & 0x1)

    cnt, cb_cnt, cb_maxdiff = calc_concordance_and_maxdiff(font, ControlBoundsPen)
    cnt, b_cnt, b_maxdiff = calc_concordance_and_maxdiff(font, BoundsPen)

    print "[{}]".format(basename)
    print "  head.flags[1]: {}".format(flag_1)
    print "  ControlBounds: {}/{} ({}%); maxdiff={}".format(cb_cnt, cnt, round(100.*cb_cnt/cnt, 2), cb_maxdiff)
    print "  Bounds       : {}/{} ({}%); maxdiff={}".format(b_cnt, cnt, round(100.*b_cnt/cnt, 2), b_maxdiff)

def main():
    lsb_means_left_of_control_bbox_or_strict_bbox()

if __name__ == "__main__":
    main()
