#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from fontTools.ttLib import TTFont

if __name__ == "__main__":
    font_path = sys.argv[1]
    font = TTFont(font_path)
    OS_2 = font["OS/2"]

    ulUnicodeRange = set()
    if hasattr(OS_2, "ulUnicodeRange1"):
        for i in range(32):
            if (OS_2.ulUnicodeRange1 >> i) & 0x1:
                ulUnicodeRange.add(i)
    if hasattr(OS_2, "ulUnicodeRange2"):
        for i in range(32):
            if (OS_2.ulUnicodeRange2 >> i) & 0x1:
                ulUnicodeRange.add(i+32)
    if hasattr(OS_2, "ulUnicodeRange3"):
        for i in range(32):
            if (OS_2.ulUnicodeRange3>> i) & 0x1:
                ulUnicodeRange.add(i+64)
    if hasattr(OS_2, "ulUnicodeRange4"):
        for i in range(32):
            if (OS_2.ulUnicodeRange4 >> i) & 0x1:
                ulUnicodeRange.add(i+96)
    if ulUnicodeRange:
        print("UnicodeRange {}".format(" ".join(map(lambda x: str(x), sorted(ulUnicodeRange)))))

    ulCodePageRange = set()
    if hasattr(OS_2, "ulCodePageRange1"):
        for i in range(32):
            if (OS_2.ulUnicodeRange1 >> i) & 0x1:
                ulCodePageRange.add(i)
    if hasattr(OS_2, "ulCodePageRange2"):
        for i in range(32):
            if (OS_2.ulUnicodeRange2 >> i) & 0x1:
                ulCodePageRange.add(i+32)
    if ulCodePageRange:
        print("CodePageRange {}".format(" ".join(map(lambda x: str(x), sorted(ulCodePageRange)))))
