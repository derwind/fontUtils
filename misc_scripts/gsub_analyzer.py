#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
from abc import ABCMeta, abstractmethod
from fontTools.ttLib import TTFont

class Renderer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self, lookup, all_lookups = None):
        u"""
        render the given lookup

        :param Lookup lookup: the target lookup which is rendered
        :param Lookup[] all_lookups: all lookups belonging to GSUB
        """

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
            renderer.render(lookup, self.gsub.table.LookupList.Lookup)

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
    def render(self, lookup, all_lookups):
        self._render_lookup(lookup, all_lookups)

    def _render_lookup(self, lookup, all_lookups):
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
            elif subtable.LookupType == GsubLookupType.CONTEXT:
                self._render_lookup_5(subtable)
            elif subtable.LookupType == GsubLookupType.CHAINING_CONTEXT:
                self._render_lookup_6(subtable, all_lookups)
            elif subtable.LookupType == GsubLookupType.EXTENSION_SUBSTITUTION:
                self._render_lookup_7(subtable)

    def _render_lookup_1(self, subtable):
        print(" [subtable] Format: {}".format(subtable.Format))
        for from_, to_ in self._render_lookup_1_2_impl(subtable):
            print("  sub {} by {};".format(from_, to_))

    def _render_lookup_1_2_impl(self, subtable):
        fromtos = []
        for from_, to_ in sorted(subtable.mapping.items(), key=lambda from_to: from_to[0]):
            fromtos.append((from_, to_))
        return fromtos

    def _render_lookup_2(self, subtable):
        print(" [subtable] Format: {}".format(subtable.Format))
        for from_, tos_ in self._render_lookup_1_2_impl(subtable):
            print("  sub {} by {};".format(from_, " ".join(tos_)))

    def _render_lookup_3(self, subtable):
        print(" [subtable] Format: {}".format(subtable.Format))
        for from_, tos in sorted(subtable.alternates.items(), key=lambda from_to: from_to[0]):
            for to_ in tos:
                print("  sub {} by {};".format(from_, to_))

    def _render_lookup_4(self, subtable):
        print(" [subtable] Format: {}".format(subtable.Format))
        for left_glyph, component, ligGlyph in self._render_lookup_4_impl(subtable):
            print("  sub {} {} by {};".format(left_glyph, " ".join(component), ligGlyph))

    def _render_lookup_4_impl(self, subtable):
        left_comp_ligs = []
        # for python 2, 'lambda (left_glyph,_): left_glyph' is also valid
        for left_glyph, ligas in sorted(subtable.ligatures.items(), key=lambda leftGlyph_ligas: leftGlyph_ligas[0]):
            for liga in ligas:
                left_comp_ligs.append((left_glyph, liga.Component, liga.LigGlyph))
        return left_comp_ligs

    def _render_lookup_5(self, subtable):
        print(" [subtable] Format: {}".format(subtable.Format))

    def _render_lookup_6(self, subtable, all_lookups):
        print(" [subtable] Format: {}".format(subtable.Format))
        if subtable.Format == 1:
            pass
        elif subtable.Format == 2:
            pass
        elif subtable.Format == 3:
            def glyphs2str(glyphs):
                return glyphs[0] if len(glyphs) <= 1 else "[{}]".format(" ".join(glyphs))

            Backtrack = [glyphs2str(coverage.glyphs) for coverage in subtable.BacktrackCoverage]
            Input = [coverage.glyphs for coverage in subtable.InputCoverage]
            Input_formatted = map(lambda glyphs: glyphs2str(glyphs), Input)
            Input_prime = map(lambda gname: "{}'".format(gname), Input_formatted)
            LookAhead = [glyphs2str(coverage.glyphs) for coverage in subtable.LookAheadCoverage]

            if subtable.SubstCount <= 0:
                s = "ignore sub {} {} {}".format(" ".join(reversed(Backtrack)), " ".join(Input_prime), " ".join(LookAhead))
            else:
                by_glyphs_str = self._render_lookup_6_SubstLookupRecord(subtable, Input, all_lookups)

                s = "sub {} {} {} by {}".format(" ".join(reversed(Backtrack)), " ".join(Input_prime), " ".join(LookAhead), by_glyphs_str)
            print("  {};".format(re.sub(r"\s+", " ", s).strip()))

    def _render_lookup_6_SubstLookupRecord(self, subtable, Input, all_lookups):
        # XXX: lazy and ugly implementation...

        # e.g. [a,d,e] is a representative if Input is [[a,b,c], [d], [e,f]]
        representative = [glyphs[0] for glyphs in Input]

        for record in subtable.SubstLookupRecord:
            #print "  SequenceIndex:{} LookupListIndex:{}".format(record.SequenceIndex, record.LookupListIndex)
            lookup = all_lookups[record.LookupListIndex]
            for subtable in lookup.SubTable:
                if subtable.LookupType == GsubLookupType.SINGLE:
                    for from_, to_ in self._render_lookup_1_impl(subtable):
                        if [from_] == representative:
                            return to_
                elif subtable.LookupType == GsubLookupType.LIGATURE:
                    for left_glyph, component, ligGlyph in self._render_lookup_4_impl(subtable):
                        sequence = [left_glyph]
                        sequence.extend(component)
                        if sequence == representative:
                            return ligGlyph
                else:
                    raise NotImplementedError()
        return "???"

    def _render_lookup_7(self, subtable):
        extSubTable = subtable.ExtSubTable
        print(" LookupType(ext): {}".format(extSubTable.LookupType))
        if extSubTable.LookupType == GsubLookupType.SINGLE:
            self._render_lookup_1(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.MULTIPLE:
            self._render_lookup_2(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.ALTERNATE:
            self._render_lookup_3(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.LIGATURE:
            self._render_lookup_4(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.CONTEXT:
            self._render_lookup_5(extSubTable)
        elif extSubTable.LookupType == GsubLookupType.CHAINING_CONTEXT:
            self._render_lookup_6(extSubTable)
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
