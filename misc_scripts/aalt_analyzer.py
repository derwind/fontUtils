#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from fontTools.ttLib import TTFont

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
from gsub_analyzer import *

class SubstitutionMap(Renderer):
    def __init__(self):
        super(SubstitutionMap, self).__init__()
        self.map = {}

    def render(self, lookup, all_lookups):
        self._render_lookup(lookup)

    def _render_lookup(self, lookup):
        #print("LookupType: {}, LookupFlag: {}".format(lookup.LookupType, lookup.LookupFlag))
        for subtable in lookup.SubTable:
            if subtable.LookupType == GsubLookupType.SINGLE:
                self._render_lookup_1(subtable)
            elif subtable.LookupType == GsubLookupType.MULTIPLE:
                self._render_lookup_2(subtable)
            elif subtable.LookupType == GsubLookupType.ALTERNATE:
                self._render_lookup_3(subtable)
            elif subtable.LookupType == GsubLookupType.LIGATURE:
                self._render_lookup_4(subtable)
            elif subtable.LookupType == GsubLookupType.EXTENSION_SUBSTITUTION:
                self._render_lookup_7(subtable)

    def _render_lookup_1(self, subtable):
        #print(" [subtable]")
        #print(" Format: {}".format(subtable.Format))
        for from_, to_ in sorted(subtable.mapping.items(), key=lambda from_to: from_to[0]):
            #print("  sub {} by {};".format(from_, to_))
            if from_ not in self.map:
                self.map[from_] = set()
            self.map[from_].add(to_)

    def _render_lookup_2(self, subtable):
        #print(" [subtable]")
        #print(" Format: {}".format(subtable.Format))
        raise

    def _render_lookup_3(self, subtable):
        #print(" [subtable]")
        #print(" Format: {}".format(subtable.Format))
        for from_, tos in sorted(subtable.alternates.items(), key=lambda from_to: from_to[0]):
            for to_ in tos:
                #print("  sub {} by {};".format(from_, to_))
                if from_ not in self.map:
                    self.map[from_] = set()
                self.map[from_].add(to_)


        #print(" [subtable]")
        #print(" Format: {}".format(subtable.Format))
        for to_, from_ in sorted(subtable.alternates.items(), key=lambda to_from: to_from[0]):
            #print("  sub {} from {};".format(to_, " ".join(sorted(from_))))
            for frm in from_:
                if frm not in self.map:
                    self.map[frm] = set()
                self.map[frm].add(to_)

    def _render_lookup_4(self, subtable):
        #print(" [subtable]")
        #print(" Format: {}".format(subtable.Format))
        # for python 2, 'lambda (left_glyph,_): left_glyph' is also valid
        for left_glyph, ligas in sorted(subtable.ligatures.items(), key=lambda leftGlyph_ligas: leftGlyph_ligas[0]):
            for liga in ligas:
                components = " ".join(liga.Component)
                #print("  sub {} {} by {};".format(left_glyph, components, liga.LigGlyph))
                raise

    def _render_lookup_7(self, subtable):
        extSubTable = subtable.ExtSubTable
        #print(" LookupType(ext): {}".format(extSubTable.LookupType))
        if extSubTable.LookupType == GsubLookupType.SINGLE:
            self._render_lookup_1(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.MULTIPLE:
            self._render_lookup_2(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.ALTERNATE:
            self._render_lookup_3(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.LIGATURE:
            self._render_lookup_4(extSubTable)
        else:
            pass

################################################################################

if __name__ == "__main__":
    font_path = sys.argv[1]
    fea_type = "liga"
    if len(sys.argv) > 2:
        fea_type = sys.argv[2]
    analyzer = GsubAnalyzer(font_path)
    analyzer.analyze("DFLT", "dflt", "aalt")
    aalt = SubstitutionMap()
    analyzer.show(aalt)
    analyzer = GsubAnalyzer(font_path)
    analyzer.analyze("DFLT", "dflt", fea_type)
    fea = SubstitutionMap()
    analyzer.show(fea)

    ok = True
    total_cnt = 0
    ng_cnt = 0
    for from_cid, to_cids in fea.map.items():
        for to_cid in to_cids:
            total_cnt += 1
            if from_cid not in aalt.map:
                print "{} is not in aalt".format(from_cid)
                ng_cnt += 1
                ok = False
            elif to_cid not in aalt.map[from_cid]:
                print "'{}->{}' is not in aalt".format(from_cid, to_cid)
                ng_cnt += 1
                ok = False
    if ok:
        print "OK"
    else:
        print "-"*50
        print "{}%({}/{}) substitutions are included in aalt".format(round(1.*(total_cnt-ng_cnt)/total_cnt, 2), total_cnt-ng_cnt, total_cnt)
