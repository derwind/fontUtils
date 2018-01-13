#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import argparse
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

class GlyfInfo(object):
    def __init__(self, in_font):
        self.in_font = in_font

    def run(self):
        font = TTFont(self.in_font)
        glyf = font["glyf"]
        hmtx = font["hmtx"]
        for gname, (adw, lsb) in hmtx.metrics.items():
            bounds1 = calc_boundsFromGlyph(font, gname, BoundsPen)
            bounds2 = calc_boundsFrom_TTGlyphGlyf(font, gname, BoundsPen)
            g = glyf[gname]
            g.recalcBounds(glyf)
            if bounds1 is None or bounds2 is None:
                if bounds1 is not None or bounds2 is not None:
                    print "[{}] bbox(Glyph)={} bbox(_TTGlyphGlyf)={} LSB={} xMin={}".format(gname, bounds1, bounds2, lsb, g.xMin)
            elif bounds_differ(bounds1, bounds2):
                print "[{}] bbox(Glyph)={} bbox(_TTGlyphGlyf)={} LSB={} xMin={}".format(gname, bounds1, bounds2, lsb, g.xMin)
                pen = DecomposingRecordingPen(font.getGlyphSet())
                glyf[gname].draw(pen, glyf)
                for operator, operands in pen.value:
                    print "  {} {}".format(operator, operands)

def calc_boundsFromGlyph(font, gname, penclass):
    gs = font.getGlyphSet()
    g = gs[gname]
    pen = penclass(gs)
    g.draw(pen)
    return [round(v, 2) for v in pen.bounds] if pen.bounds is not None else None

def calc_boundsFrom_TTGlyphGlyf(font, gname, penclass):
    gs = font.getGlyphSet()
    glyf = font["glyf"]
    g = glyf[gname]
    pen = penclass(gs)
    g.draw(pen, glyf)
    return [round(v, 2) for v in pen.bounds] if pen.bounds is not None else None

def bounds_differ(bounds1, bounds2):
    for v1, v2 in zip(bounds1, bounds2):
        if abs(v1 - v2) >= 1:
            return True
    return False

def compare_bounds():
    font_path = sys.argv[1]
    font1 = TTFont(font1_path, fontNumber=0)
    for gname in font1.getGlyphOrder():
        bound1 = calc_bounds(font1, gname, BoundsPen)
        bound2 = calc_bounds(font2, gname, BoundsPen)
        if bound1 is None or bound2 is None:
            if bound1 is not None or bound2 is not None:
                print "[{}] {} {}".format(gname, bound1, bound2)
        elif bounds_differ(bound1, bound2):
            print "[{}] {} {}".format(gname, bound1, bound2)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_font", metavar="FONT", type=str,
                        help="input font")

    args = parser.parse_args()

    return args

def main():
    args = get_args()
    _, ext = os.path.splitext(os.path.basename(args.in_font))
    if ext != ".ttf":
        print>>sys.stderr, "only TTF is supported"
        sys.exit(1)

    tool = GlyfInfo(args.in_font)
    sys.exit(tool.run())

if __name__ == "__main__":
    main()
