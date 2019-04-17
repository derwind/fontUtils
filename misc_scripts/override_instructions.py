#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
override TT instructions
"""

import os, sys, re
import argparse
import array
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._f_p_g_m import table__f_p_g_m
from fontTools.ttLib.tables._c_v_t import table__c_v_t
from fontTools.ttLib.tables._p_r_e_p import table__p_r_e_p
from fontTools.ttLib.tables.ttProgram import Program

class OverrideInstructions(object):
    def __init__(self, in_font, out_font, gname_instruction=None, fpgm=None, clear_cvt=False, clear_prep=False):
        self.in_font = in_font
        self.out_font = out_font
        self.gname_instruction = gname_instruction
        self.fpgm = fpgm
        self.clear_cvt = clear_cvt
        self.clear_prep = clear_prep

    def run(self):
        ttFont = TTFont(self.in_font)

        if self.gname_instruction is not None:
            self.override_glyph_instruction(ttFont, self.gname_instruction)
        if self.fpgm is not None:
            self.override_fpgm(ttFont, self.fpgm)

        if self.clear_cvt and "cvt " in ttFont:
            ttFont["cvt "] = cvt = table__c_v_t()
            cvt.values = array.array("h")
        if self.clear_prep and "prep" in ttFont:
            ttFont["prep"] = prep = table__p_r_e_p()
            prep.program = Program()

        ttFont.save(self.out_font)

        return 0

    def override_glyph_instruction(self, ttFont, gname_instruction):
        glyf = ttFont["glyf"]
        glyph2instruction = {}
        for g_i in gname_instruction.split(","):
            gname, instruction = g_i.split("=")
            glyph2instruction[gname] = instruction
        for gname in ttFont.getGlyphOrder():
            g = glyf[gname]
            if gname in glyph2instruction:
                with open(instruction) as f:
                    content = [line.strip() for line in f.readlines()]
                    g.fromXML("instructions", None, [("assembly", None, content)], ttFont)
            else:
                g.program = Program()

    def override_fpgm(self, ttFont, fpgm):
        ttFont["fpgm"] = table__f_p_g_m()
        with open(fpgm) as f:
            content = [line.strip() for line in f.readlines()]
            ttFont["fpgm"].fromXML("assembly", None, content, ttFont)

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_font", metavar="FONT", type=str, help="input font")
    parser.add_argument("-o", "--output", metavar="OUT_FONT", dest="out_font", default=None, help="output font")
    parser.add_argument("-g", "--glyph-instruction", metavar="GLYPH_NAME=INSTRUCTION[,GLYPH_NAME=INSTRUCTION,...]", dest="gname_instruction", default=None, help="glyph name=instruction")
    parser.add_argument("--fpgm", metavar="FPGM", dest="fpgm", default=None, help="font program")
    parser.add_argument("--clear-cvt", dest="clear_cvt", action="store_true", help="clear 'cvt' table")
    parser.add_argument("--clear-prep", dest="clear_prep", action="store_true", help="clear 'prep' table")

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

    tool = OverrideInstructions(args.in_font, args.out_font, args.gname_instruction, args.fpgm, args.clear_cvt, args.clear_prep)
    sys.exit(tool.run())

if __name__ == "__main__":
    main()
