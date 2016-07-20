#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import sys,re 


with open(sys.argv[1]) as f:
    for line in [l.rstrip() for l in f.readlines()]:
        m = re.search(r"CID\+(\d+)", line)
        if m:
            cid = int(m.group(1))
            if cid <= 9353:
                print(line)
        else:
            print(line)
