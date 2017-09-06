#! /usr/bin/env python
# -*- coding -*-

import sys, re

if __name__ == "__main__":
    num = 0

    if len(sys.argv) < 3:
        raise Exception("You need to specify both the CMAP file and the AFM file")
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    count = llx = urx = lly = ury = 0
    code2cid = {}
    cid2code = {}

    with open("features.BASE", "w") as fout:
        with open(file1) as cmap:
            target_lines = False
            for line in cmap.readlines():
                line = line.rstrip()
                if re.search(r"begincidrange$", line):
                    target_lines = True
                    continue
                elif re.search(r"^endcidrange", line):
                    target_lines = False
                    continue
                if target_lines:
                    m = re.search(r"^<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>\s+(\d+)$", line)
                    if m:
                        begin = int(m.group(1), 16)
                        end = int(m.group(2), 16)
                        cid = int(m.group(3))
                        for char in range(begin, end+1):
                            if int("4E00", 16) <= char <= int("9FA5", 16) or \
                               int("F900", 16) <= char <= int("FA2D", 16) or \
                               int("3041", 16) <= char <= int("3094", 16) or \
                               int("30A1", 16) <= char <= int("30FA", 16) or \
                               int("AC00", 16) <= char <= int("D7A3", 16):
                                   code = "{0:02X}".format(char)
                                   code2cid[code] = cid
                                   cid2code[cid] = code
                                   count += 1
                                   cid += 1
        print "Done."

        fontname = ""
        version = ""
        notice = ""
        data = {}
        with open(file2) as afm:
            target_lines = False
            for line in afm.readlines():
                line = line.rstrip()
                m = re.search(r"^FontName\s+(.*)$", line)
                if m:
                    fontname = m.group(1)
                    print>>sys.stderr, "\"{}\" CIDFont into lookup structure...".format(fontname)
                    continue
                m = re.search(r"^Version\s+(.*)$", line)
                if m:
                    version = m.group(1)
                    continue
                m = re.search(r"^Notice\s+(.*)$", line)
                if m:
                    notice = m.group(1)
                    notice = re.sub(r"\([Cc]\)\s+", "", notice)
                    continue
                m = re.search(r"^StartCharMetrics", line)
                if m:
                    target_lines = True
                    continue
                elif re.search(r"^EndCharMetrics", line):
                    target_lines = False
                    continue
                if target_lines:
                    m = re.search(r"^\s*C\s+-1\s+;\s+W0X\s+(\d+)\s+;\s+N\s+(\d+)\s+;\s+B\s+((-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+))\s+;\s*$", line)
                    if m:
                        width = int(m.group(1))
                        cid = int(m.group(2))
                        bbox = m.group(3)
                        a = int(m.group(4))
                        b = int(m.group(5))
                        c = int(m.group(6))
                        d = int(m.group(7))
                        if cid in cid2code:
                            num += 1
                            data[cid] = "W0X {} ; B {} ;".format(width, bbox)
                            if bbox != "0 0 0 0":
                                llx += a
                                lly += b
                                urx += c
                                ury += d
        print "Done."

        left = llx / num
        right = 1000 - (urx / num)
        bottom = 120 + (lly / num)
        top = 880 - (ury / num)

        result = (left + right + bottom + top) / 4

        left = result
        right = 1000 - result
        bottom = -120 + result
        top = 880 - result

        print>>fout, """
table BASE {
"""[1:-1]
        print>>fout, """
  HorizAxis.BaseTagList                 icfb  icft  ideo  romn;
  HorizAxis.BaseScriptList  hani  ideo   {0}  {1}   -120  0,
                            kana  ideo   {0}  {1}   -120  0,
                            latn  romn   {0}  {1}   -120  0,
                            cyrl  romn   {0}  {1}   -120  0,
                            grek  romn   {0}  {1}   -120  0;

  VertAxis.BaseTagList                  icfb  icft  ideo  romn;
  VertAxis.BaseScriptList   hani  ideo  {2}    {3}   0     120,
                            kana  ideo  {2}    {3}   0     120,
                            latn  romn  {2}    {3}   0     120,
                            cyrl  romn  {2}    {3}   0     120,
                            grek  romn  {2}    {3}   0     120;
"""[1:-1].format(bottom, top, left, right)
        print>>fout, """
} BASE;
"""[1:-1]
