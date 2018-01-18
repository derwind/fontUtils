#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
dump Type 2 Charstring
"""

import os, sys, re
import argparse
from fontTools.ttLib import TTFont

class ProgramDumper(object):
    def __init__(self, in_font):
        self.in_font = in_font

    # https://github.com/googlei18n/compreffor/blob/master/src/python/compreffor/test/util.py#L26-L43
    def run(self):
        font = TTFont(self.in_font)
        gs = font.getGlyphSet()
        for gname in font.getGlyphOrder():
            g = gs[gname]._glyph
            g.decompile()
            print("[{}]".format(gname))
            operands = []
            for b in g.program:
                if isinstance(b, int):
                    operands.append(b)
                else:
                    print("  [{}] << {} >>".format(", ".join(map(lambda v: str(v), operands)), b))
                    operands = []
            print("  -----")

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_font", metavar="FONT", type=str,
                        help="input font")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    tool = ProgramDumper(args.in_font)
    sys.exit(tool.run())

if __name__ == "__main__":
    main()
