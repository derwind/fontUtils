#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen

def lsb_means_left_of_control_bbox_or_strict_bbox():
    font_path = sys.argv[1]
    font = TTFont(font_path, fontNumber=0)

    hmtx = font["hmtx"]

    gs = font.getGlyphSet()

    cnt = 0
    cb_cnt = 0
    b_cnt = 0

    for gname in font.getGlyphOrder():
        g = gs[gname]

        cb_pen = ControlBoundsPen(gs)
        b_pen = BoundsPen(gs)
        g.draw(cb_pen)
        g.draw(b_pen)
        if b_pen.bounds is None:
            continue

        cb_left, _, _, _ = cb_pen.bounds
        b_left, _, _, _ = b_pen.bounds
        lsb = hmtx.metrics[gname][1]

        cnt += 1
        if abs(cb_left - lsb) <= 1:
            cb_cnt += 1
        if abs(b_left - lsb) <= 1:
            b_cnt += 1

    print "ControlBounds: {}/{} ({}%)".format(cb_cnt, cnt, round(100.*cb_cnt/cnt, 2))
    print "Bounds       : {}/{} ({}%)".format(b_cnt, cnt, round(100.*b_cnt/cnt, 2))

def main():
    lsb_means_left_of_control_bbox_or_strict_bbox()

if __name__ == "__main__":
    main()
