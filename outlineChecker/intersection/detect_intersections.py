#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
detect intersections
"""

import os, sys, re
import argparse
import numpy as np
import bezier
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import AbstractPen, decomposeQuadraticSegment

class ConvPen(AbstractPen):
    def __init__(self, degree):
        self.contours = []
        self.current_contour = None
        self.degree = degree
        self.__currentPoint = None

    def moveTo(self, pt):
        self.current_contour = []
        self.__currentPoint = pt

    def lineTo(self, pt):
        pts = [self.double(self.__currentPoint)]
        if self.degree == 2:
            # dummy off-curve
            mid_p = ((self.__currentPoint[0] + pt[0]) * .5, (self.__currentPoint[1] + pt[1]) * .5)
            pts.append(mid_p)
        else:
            # dummy off-curves
            pts.append(self.double(self.__currentPoint))
            pts.append(self.double(pt))
        pts.append(pt)
        nodes = np.asfortranarray(pts)
        curve = bezier.Curve(nodes, degree=self.degree)
        self.current_contour.append(curve)
        self.__currentPoint = pt

    def curveTo(self, *points):
        pts = [self.double(self.__currentPoint)]
        pts.extend([self.double(pt) for pt in points])
        nodes = np.asfortranarray(pts)
        curve = bezier.Curve(nodes, degree=self.degree)
        self.current_contour.append(curve)
        self.__currentPoint = points[-1]

    def qCurveTo(self, *points):
        _qCurveToOne = self._qCurveToOne
        for pt1, pt2 in decomposeQuadraticSegment(points):
            _qCurveToOne(pt1, pt2)
            self.__currentPoint = pt2

    def closePath(self):
        self._closePath()
        self.__currentPoint = None

    def endPath(self):
        self._endPath(self.current_contour)
        self.__currentPoint = None

    def _closePath(self):
        self.contours.append(self.current_contour)
        self.current_contour = None

    def _endPath(self):
        pass

    def _qCurveToOne(self, pt1, pt2):
        pts = [self.double(self.__currentPoint)]
        pts.append(self.double(pt1))
        pts.append(self.double(pt2))
        nodes = np.asfortranarray(pts)
        curve = bezier.Curve(nodes, degree=self.degree)
        self.current_contour.append(curve)

    def _getCurrentPoint(self):
        return self.__currentPoint

    def double(self, pt):
        return (float(pt[0]), float(pt[1]))

    #def addComponent(self, glyphName, transformation):
    #    pass

class DetectIntersections(object):
    def __init__(self, in_font):
        self.in_font = in_font
        basename, ext = os.path.splitext(os.path.basename(in_font))
        self.degree = 2 if ext.lower() == ".ttf" else 3

    def run(self):
        font = TTFont(self.in_font)

        gs = font.getGlyphSet()
        for gname in font.getGlyphOrder():
            g = gs[gname]
            intersections = self.detect(g, gname, gs)
            if intersections:
                print "{}:".format(gname), ", ".join(["({}, {})".format(pt[0], pt[1]) for pt in intersections])

    def detect(self, glyph, name, glyphSet):
        pen = ConvPen(self.degree)
        glyph.draw(pen)
        contours = pen.contours

        intersections = set()
        for contour in contours:
            intersections = intersections | self.detect_in_contour(contour)

        if len(contours) <= 1:
            return

        for i in range(len(contours) - 1):
            for j in range(i+1, len(contours)):
                intersections = intersections | self.detect_between_contours(contours[i], contours[j])

        return intersections

    def detect_in_contour(self, contour):
        intersections = set()
        for i in range(len(contour) - 1):
            for j in range(i+1, len(contour)):
                adjacent = j==i+1 or (i==0 and j >= len(contour) - 1)
                intersections = intersections | self.detect_between_curves(contour[i], contour[j], adjacent=adjacent)
        return intersections

    def detect_between_contours(self, contour1, contour2):
        intersections = set()
        for curve1 in contour1:
            for curve2 in contour2:
                intersections = intersections | self.detect_between_curves(curve1, curve2)
        return intersections

    def detect_between_curves(self, curve1, curve2, adjacent=False):
        try:
            intersections = curve1.intersect(curve2)
            if len(intersections) > 0 and not adjacent:
                intersections_ = set()
                for pt in intersections:
                    intersections_.add((pt[0], pt[1]))
                return intersections_
        except NotImplementedError:
            pass
        return set()

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("in_font", metavar="FONT", type=str,
                        help="input font")
    #parser.add_argument("-o", "--output", dest="out_font", default=None,
    #                    help="output font")

    args = parser.parse_args()

    #if args.out_font is None:
    #    args.out_font = args.in_font

    return args

def main():
     args = get_args()
     tool = DetectIntersections(args.in_font)
     sys.exit(tool.run())

if __name__ == "__main__":
    main()
