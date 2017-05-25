#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from fontTools.ttLib import TTFont

# https://www.microsoft.com/typography/otspec/os2.htm#cpr
def bit2code_page(bit):
    if bit == 0:
        return 1252
    elif bit == 1:
        return 1250
    elif bit == 2:
        return 1251
    elif bit == 3:
        return 1253
    elif bit == 4:
        return 1254
    elif bit == 5:
        return 1255
    elif bit == 6:
        return 1256
    elif bit == 7:
        return 1257
    elif bit == 8:
        return 1258
    elif bit == 16:
        return 874
    elif bit == 17:
        return 932
    elif bit == 18:
        return 936
    elif bit == 19:
        return 949
    elif bit == 20:
        return 950
    elif bit == 21:
        return 1361
    elif bit == 48:
        return 869
    elif bit == 49:
        return 866
    elif bit == 50:
        return 865
    elif bit == 51:
        return 864
    elif bit == 52:
        return 863
    elif bit == 53:
        return 862
    elif bit == 54:
        return 861
    elif bit == 55:
        return 860
    elif bit == 56:
        return 857
    elif bit == 57:
        return 855
    elif bit == 58:
        return 852
    elif bit == 59:
        return 775
    elif bit == 60:
        return 737
    elif bit == 61:
        return 708
    elif bit == 62:
        return 850
    elif bit == 63:
        return 437
    return 0

if __name__ == "__main__":
    font_path = sys.argv[1]
    font = TTFont(font_path)
    OS_2 = font["OS/2"]

    # https://www.microsoft.com/typography/otspec/os2.htm#ur
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
        print("UnicodeRange {}".format(" ".join(map(lambda bit: str(bit), sorted(ulUnicodeRange)))))

    # https://www.microsoft.com/typography/otspec/os2.htm#cpr
    ulCodePageRange = set()
    if hasattr(OS_2, "ulCodePageRange1"):
        for i in range(32):
            if (OS_2.ulCodePageRange1 >> i) & 0x1:
                ulCodePageRange.add(i)
    if hasattr(OS_2, "ulCodePageRange2"):
        for i in range(32):
            if (OS_2.ulCodePageRange2 >> i) & 0x1:
                ulCodePageRange.add(i+32)
    if ulCodePageRange:
        print("CodePageRange {}".format(" ".join(map(lambda bit: str(bit2code_page(bit)), sorted(ulCodePageRange)))))
