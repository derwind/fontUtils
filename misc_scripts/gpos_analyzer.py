#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from abc import ABCMeta, abstractmethod
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otBase import ValueRecord

class Renderer(object):
    __metaclass__=ABCMeta

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
        print "LookupType: {}".format(lookup.LookupType)
        print "LookupFlag: {}".format(lookup.LookupFlag)
        for subtable in lookup.SubTable:
            if subtable.LookupType == GposLookupType.SINGLE:
                self._render_single(subtable)
            elif subtable.LookupType == GposLookupType.EXTENSION_POSITIONING:
                extSubTable = subtable.ExtSubTable
                if extSubTable.LookupType == GposLookupType.SINGLE:
                    self._render_single(ExtSubTable)
                else:
                    pass

    def _render_single(self, subtable):
        coverage = subtable.Coverage
        if type(subtable.Value) == list:
            for gname, val in zip(coverage.glyphs, subtable.Value):
                self._render_ValueRecord(gname, val) 
        elif type(subtable.Value) == ValueRecord:
            for gname in coverage.glyphs:
                self._render_ValueRecord(gname, subtable.Value)
        else:
            #print "???", type(subtable.Value)
            pass

    def _render_ValueRecord(self, glyph_name, record):
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
        print "  pos {} <{} {} {} {}>;".format(glyph_name, xplc, yplc, xadv, yadv)

################################################################################

if __name__ == "__main__":
    font_path = sys.argv[1]
    fea = "palt"
    if len(sys.argv) > 2:
        fea = sys.argv[2]
    analyzer = GposAnalyzer(font_path)
    analyzer.analyze("DFLT", "dflt", fea)
    analyzer.show(GposRenderer())
