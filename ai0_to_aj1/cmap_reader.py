#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""a simple CMap reader"""

import re

def readCMap(cmap_f):
    pat_cidchar  = re.compile(r"^\s*<([0-9a-f]+)>\s+(\d+)")
    pat_cidrange = re.compile(r"^\s*<([0-9a-f]+)>\s+<([0-9a-f]+)>\s+(\d+)")
    uni_cid_h = {}
    with open(cmap_f) as f:
        in_def = False
        for line in f.readlines():
            if "begincidchar" in line or "begincidrange" in line:
                in_def = True
                continue
            elif "endcidchar" in line or "endcidrange" in line:
                in_def = False
                continue

            if not in_def:
                continue

            m = pat_cidchar.search(line)
            if m:
                uni = int(m.group(1), 16)
                cid = int(m.group(2))
                uni_cid_h[uni] = cid
                continue
            m = pat_cidrange.search(line)
            if m:
                uni1 = int(m.group(1), 16)
                uni2 = int(m.group(2), 16)
                cid  = int(m.group(3))

                for cid_ in range(cid, cid + uni2 - uni1 + 1):
                    uni = uni1 + (cid_ - cid)
                    uni_cid_h[uni] = cid_
    return uni_cid_h
