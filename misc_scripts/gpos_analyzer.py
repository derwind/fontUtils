#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from abc import ABCMeta, abstractmethod
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otBase import ValueRecord

class Renderer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self, lookup):
        pass

# https://www.microsoft.com/typography/otspec/gpos.htm
# LookupType Enumeration table for glyph positioning
class GposLookupType(object):
    SINGLE = 1
    PAIR = 2
    CURSIVE_ATT = 3
    MARK2BASE_ATT = 4
    MARK2LIGA_ATT = 5
    MARK2MARK_ATT = 6
    CONTEXT_POSITIONING = 7
    CHAINED_CONTEXT_POSITIONING = 8
    EXTENSION_POSITIONING = 9

class GposAnalyzer(object):
    def __init__(self, font_path):
        self.font = TTFont(font_path)
        self.gpos = self.font["GPOS"]
        self.lang_system = {}
        self.lookup_indexes = []

    def analyze(self, script, language, feature_tag):
        self._analyze_script()
        feature_indexes = self.lang_system[script][language]

        feature_records = [self.gpos.table.FeatureList.FeatureRecord[idx] for idx in feature_indexes]
        self.lookup_indexes = self._get_lookup_indexes_in_feature(feature_records, feature_tag)

    def show(self, renderer):
        for idx in self.lookup_indexes:
            lookup = self.gpos.table.LookupList.Lookup[idx]
            renderer.render(lookup)

    def _analyze_script(self):
        for record in self.gpos.table.ScriptList.ScriptRecord:
            self.lang_system[record.ScriptTag] = {}
            self.lang_system[record.ScriptTag]["dflt"] = [idx for idx in record.Script.DefaultLangSys.FeatureIndex]
            for lang_record in record.Script.LangSysRecord:
                self.lang_system[record.ScriptTag][lang_record.LangSysTag] = [idx for idx in lang_record.LangSys.FeatureIndex]

    def _get_lookup_indexes_in_feature(self, feature_records, feature_tag):
        for record in feature_records:
            if record.FeatureTag == feature_tag:
                return [idx for idx in record.Feature.LookupListIndex]
        return []

class GposRenderer(Renderer):
    def render(self, lookup):
        self._render_lookup(lookup)

    def _render_lookup(self, lookup):
        print("LookupType: {}, LookupFlag: {}".format(lookup.LookupType, lookup.LookupFlag))
        for subtable in lookup.SubTable:
            if subtable.LookupType == GposLookupType.SINGLE:
                self._render_single(subtable)
            elif subtable.LookupType == GposLookupType.PAIR:
                self._render_pair(subtable)
            elif subtable.LookupType == GposLookupType.EXTENSION_POSITIONING:
                extSubTable = subtable.ExtSubTable
                if extSubTable.LookupType == GposLookupType.SINGLE:
                    self._render_single(extSubTable)
                elif extSubTable.LookupType == GposLookupType.PAIR:
                    self._render_pair(extSubTable)
                else:
                    pass

    def _render_single(self, subtable):
        coverage = subtable.Coverage
        # SinglePosFormat1 subtable: Single positioning value
        if subtable.Format == 1:
            for gname in coverage.glyphs:
                # some fonts have odd data
                if subtable.Value is None:
                    if 0:
                        print("[WARN] {} has an invalid metrics".format(gname))
                self._render_ValueRecord(gname, subtable.Value)
        # SinglePosFormat2 subtable: Array of positioning values
        elif subtable.Format == 2:
            for gname, val in zip(coverage.glyphs, subtable.Value):
                self._render_ValueRecord(gname, val)
        else:
            raise "not implemented yet"

    def _render_pair(self, subtable):
        coverage = subtable.Coverage
        # PairPosFormat1 subtable: Adjustments for glyph pairs
        if subtable.Format == 1:
            for FirstGlyph, pair in zip(coverage.glyphs, subtable.PairSet):
                for record in pair.PairValueRecord:
                    SecondGlyph = record.SecondGlyph
                    Value1 = record.Value1
                    Value2 = record.Value2
                    self._render_ValueRecord2(FirstGlyph, SecondGlyph, Value1)
        # PairPosFormat2 subtable: Class pair adjustment
        elif subtable.Format == 2:
            ordered_classes1 = self._order_classes(subtable.ClassDef1.classDefs)
            ordered_classes2 = self._order_classes(subtable.ClassDef2.classDefs)

            for classValue1, gnames1 in ordered_classes1:
                class1Record = subtable.Class1Record[classValue1]
                class2Record = class1Record.Class2Record
                for classValue2, gnames2 in ordered_classes2:
                    record = class2Record[classValue2]
                    if self._has_no_adjustments(record.Value1):
                        continue
                    self._render_PairAdjustment(gnames1, gnames2, record.Value1)
        else:
            raise "not implemented yet"

    def _render_ValueRecord(self, glyph_name, record):
        xplc, yplc, xadv, yadv = self._get_adjustment(record)
        print("  pos {} <{} {} {} {}>;".format(glyph_name, xplc, yplc, xadv, yadv))

    def _render_ValueRecord2(self, glyph_name1, glyph_name2, record):
        xplc, yplc, xadv, yadv = self._get_adjustment(record)
        print("  pos {} {} <{} {} {} {}>;".format(glyph_name1, glyph_name2, xplc, yplc, xadv, yadv))

    def _render_PairAdjustment(self, gnames1, gnames2, record):
        xplc, yplc, xadv, yadv = self._get_adjustment(record)
        print("  pos [{}] [{}] <{} {} {} {}>;".format(",".join(gnames1), ",".join(gnames2), xplc, yplc, xadv, yadv))

    def _has_no_adjustments(self, record):
        xplc, yplc, xadv, yadv = self._get_adjustment(record)
        return xplc == 0 and yplc == 0 and xadv == 0 and yadv == 0

    def _get_adjustment(self, record):
        xplc = 0
        yplc = 0
        xadv = 0
        yadv = 0
        if hasattr(record, "XPlacement"):
            xplc = record.XPlacement
        if hasattr(record, "YPlacement"):
            yplc = record.YPlacement
        if hasattr(record, "XAdvance"):
            xadv = record.XAdvance
        if hasattr(record, "YAdvance"):
            yadv = record.YAdvance
        return xplc, yplc, xadv, yadv

    def _order_classes(self, classDefs):
        d = {}
        for gname, classValue in classDefs.items():
            if not classValue in d:
                d[classValue] = []
            d[classValue].append(gname)
        for classValue, gnames in d.items():
            d[classValue] = sorted(gnames)
        # for python 2, 'lambda (classValue,gnames): gnames[0]' is also valid
        return sorted(d.items(), key=lambda classValue_gnames: classValue_gnames[1][0])

################################################################################

if __name__ == "__main__":
    font_path = sys.argv[1]
    fea = "palt"
    if len(sys.argv) > 2:
        fea = sys.argv[2]
    analyzer = GposAnalyzer(font_path)
    analyzer.analyze("DFLT", "dflt", fea)
    analyzer.show(GposRenderer())
