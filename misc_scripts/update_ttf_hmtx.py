#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import argparse
from fontTools.ttLib import TTFont

class HtmxUpdater(object):
    def __init__(self, in_font, out_font, update_vmtx=False):
        self.in_font = in_font
        self.out_font = out_font
        self.update_vmtx = update_vmtx

    def run(self):
        font = TTFont(self.in_font)
        gs = font.getGlyphSet()
        glyf = font["glyf"]
        hmtx = font["hmtx"]
        for gname, (adw, lsb) in hmtx.metrics.items():
            g = glyf[gname]
            # obtain xMin
            g.recalcBounds(glyf)
            hmtx.metrics[gname] = (adw, g.xMin)
        if self.update_vmtx:
            from fontTools.pens.boundsPen import BoundsPen
            vmtx = font["vmtx"]
            for gname, (adh, tsb) in vmtx.metrics.items():
                g = glyf[gname]
                # obtain yMax
                g.recalcBounds(glyf)
                pen = BoundsPen(gs)
                g.draw(pen, glyf)
                if pen.bounds is None:
                    continue
                left, bottom, right, top = pen.bounds
                vmtx.metrics[gname] = (adh, top + tsb - g.yMax)

        font.save(self.out_font)

        return 0

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_font", metavar="FONT", type=str,
                        help="input font")
    parser.add_argument("-o", "--output", dest="out_font", default=None,
                        help="output font")
    parser.add_argument("-v", "--vmtx", dest="update_vmtx", action="store_true",
                        help="also update vmtx")

    args = parser.parse_args()

    if args.out_font is None:
        args.out_font = args.in_font

    return args

def main():
    args = get_args()
    _, ext = os.path.splitext(os.path.basename(args.in_font))
    if ext != ".ttf":
        print>>sys.stderr, "only TTF is supported"
        sys.exit(1)

    tool = HtmxUpdater(args.in_font, args.out_font, args.update_vmtx)
    sys.exit(tool.run())

if __name__ == "__main__":
    main()
