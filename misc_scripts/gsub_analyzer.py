#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from fontTools.ttLib import TTFont

class GsubLookupType(object):
    SINGLE = 1
    MULTIPLE = 2
    ALTERNATE = 3
    LIGATURE = 4
    CONTEXT = 5
    CHAINING_CONTEXT = 6
    EXTENSION_SUBSTITUTION = 7
    REVERSE_CHAINING_CONTEXT_SINGLE = 8

class GsubAnalyzer(object):
    def __init__(self, font_path):
        self.font = TTFont(font_path)
        self.gsub = self.font["GSUB"]
        self.lang_system = {}
        self.lookup_indexes = []

    def analyze(self, script, language, feature_tag):
        self._analyze_script()
        feature_indexes = self.lang_system[script][language]

        feature_records = [self.gsub.table.FeatureList.FeatureRecord[idx] for idx in feature_indexes]
        self.lookup_indexes = self._get_lookup_indexes_in_feature(feature_records, feature_tag)

    def show(self):
        for idx in self.lookup_indexes:
            lookup = self.gsub.table.LookupList.Lookup[idx]
            self._analyze_lookup(lookup)

    def _analyze_script(self):
        for record in self.gsub.table.ScriptList.ScriptRecord:
            self.lang_system[record.ScriptTag] = {}
            self.lang_system[record.ScriptTag]["dflt"] = [idx for idx in record.Script.DefaultLangSys.FeatureIndex]
            for lang_record in record.Script.LangSysRecord:
                self.lang_system[record.ScriptTag][lang_record.LangSysTag] = [idx for idx in lang_record.LangSys.FeatureIndex]

    def _get_lookup_indexes_in_feature(self, feature_records, feature_tag):
        for record in feature_records:
            if record.FeatureTag == feature_tag:
                return [idx for idx in record.Feature.LookupListIndex]
        return []

    def _analyze_lookup(self, lookup):
        print "LookupType: {}".format(lookup.LookupType)
        print "LookupFlag: {}".format(lookup.LookupFlag)
        for subtable in lookup.SubTable:
            if subtable.LookupType == GsubLookupType.LIGATURE:
                self._anlyze_lookup_4(subtable)

    def _anlyze_lookup_4(self, subtable):
        print " [subtable]"
        print " Format: {}".format(subtable.Format)
        for left_glyph, ligas in sorted(subtable.ligatures.items(), key=lambda (left_glyph,_): left_glyph):
            for liga in ligas:
                components = " ".join(liga.Component)
                print "  sub {} {} by {};".format(left_glyph, components, liga.LigGlyph)

################################################################################

if __name__ == "__main__":
    analyzer = GsubAnalyzer(sys.argv[1])
    analyzer.analyze("DFLT", "dflt", "liga")
    analyzer.show()
