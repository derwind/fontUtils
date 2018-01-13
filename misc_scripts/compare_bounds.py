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

def calc_bounds(font, gname, penclass):
    gs = font.getGlyphSet()
    g = gs[gname]
    pen = penclass(gs)
    g.draw(pen)
    return [round(v, 2) for v in pen.bounds] if pen.bounds is not None else None

def bounds_differ(bounds1, bounds2):
    for v1, v2 in zip(bounds1, bounds2):
        if abs(v1 - v2) >= 1:
            return True
    return False

def compare_bounds():
    font1_path = sys.argv[1]
    font2_path = sys.argv[2]
    font1 = TTFont(font1_path, fontNumber=0)
    font2 = TTFont(font2_path, fontNumber=0)
    for gname in font1.getGlyphOrder():
        bounds1 = calc_bounds(font1, gname, BoundsPen)
        bounds2 = calc_bounds(font2, gname, BoundsPen)
        if bounds1 is None or bounds2 is None:
            if bounds1 is not None or bounds2 is not None:
                print "[{}] {} {}".format(gname, bounds1, bounds2)
        elif bounds_differ(bounds1, bounds2):
            print "[{}] {} {}".format(gname, bounds1, bounds2)

def main():
    compare_bounds()

if __name__ == "__main__":
    main()
