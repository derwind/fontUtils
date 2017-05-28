#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from abc import ABCMeta, abstractmethod
from fontTools.ttLib import TTFont

class Renderer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self, lookup):
        pass

# https://www.microsoft.com/typography/otspec/gsub.htm
# LookupType Enumeration table for glyph substitution
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

    def show(self, renderer):
        for idx in self.lookup_indexes:
            lookup = self.gsub.table.LookupList.Lookup[idx]
            renderer.render(lookup)

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

class GsubRenderer(Renderer):
    def render(self, lookup):
        self._render_lookup(lookup)

    def _render_lookup(self, lookup):
        print("LookupType: {}, LookupFlag: {}".format(lookup.LookupType, lookup.LookupFlag))
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
        print(" [subtable]")
        print(" Format: {}".format(subtable.Format))
        for from_, to_ in sorted(subtable.mapping.items(), key=lambda from_to: from_to[0]):
            print("  sub {} by {};".format(from_, to_))

    def _render_lookup_2(self, subtable):
        print(" [subtable]")
        print(" Format: {}".format(subtable.Format))

    def _render_lookup_3(self, subtable):
        print(" [subtable]")
        print(" Format: {}".format(subtable.Format))
        for to_, from_ in sorted(subtable.alternates.items(), key=lambda to_from: to_from[0]):
            print("  sub {} from {};".format(to_, " ".join(sorted(from_))))

    def _render_lookup_4(self, subtable):
        print(" [subtable]")
        print(" Format: {}".format(subtable.Format))
        # for python 2, 'lambda (left_glyph,_): left_glyph' is also valid
        for left_glyph, ligas in sorted(subtable.ligatures.items(), key=lambda leftGlyph_ligas: leftGlyph_ligas[0]):
            for liga in ligas:
                components = " ".join(liga.Component)
                print("  sub {} {} by {};".format(left_glyph, components, liga.LigGlyph))

    def _render_lookup_7(self, subtable):
        extSubTable = subtable.ExtSubTable
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
    fea = "liga"
    if len(sys.argv) > 2:
        fea = sys.argv[2]
    analyzer = GsubAnalyzer(font_path)
    analyzer.analyze("DFLT", "dflt", fea)
    analyzer.show(GsubRenderer())
