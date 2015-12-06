#! /usr/bin/env python
# -*- coding: utf-8 -*-

from outlineCheckCore import Glyph, Contour

g   = Glyph()
cons = [Contour(), Contour()]

for con in cons:
    g.addContour(con)

print "test finished"
