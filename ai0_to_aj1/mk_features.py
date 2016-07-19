#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""a converter from AI0 feature to AJ1 feature"""

# The implementation is very incomplete and very very ugly.

import sys, re
from collections import namedtuple
from enum import Enum


class GsubFragmentType(Enum):
    UNKNOWN = 0
    CID     = 1
    FROMBY  = 2
    OTHER   = 0xbeef

GsubFragment = namedtuple('GsubFragment', ["val", "typ"])


def all_comments(lines):
    for line in lines:
        line = line.strip()
        if line != "" and line[0:1] != "#":
            return False
    return True


def preprocess_class_def(line):
    u"""replace spaces in class definitions with '#'"""

    newline = ""
    iterator = re.finditer(r"\[.*\]?", line)
    if not iterator:
        return line

    e = 0
    for m in iterator:
        new_s = m.start()
        prev_substr = line[e:new_s]
        e = m.end()
        newline += prev_substr + re.sub(r"\s+", "#", m.group())
    newline += line[e:]
    return newline


def preprocess_gsub_line(line, mapf):
    u"""parse GSUB line"""

    # clean up line
    line = re.sub(r"^\s*sub\S*\s+", "", line)
    line = re.sub(r"\s*;.*$", "", line)

    parsed_line = []
    for fragm in re.split(r"\s+", line):
        if fragm == "from" or fragm == "by":
            parsed_line.append( GsubFragment(val=fragm, typ=GsubFragmentType.FROMBY) )
        elif fragm[0:1] == "\\":
            cid = int(fragm[1:])
            if cid not in mapf:
                # this line can't be used because it contains invalid CID for a new font
                return None
            parsed_line.append( GsubFragment(val=mapf[cid], typ=GsubFragmentType.CID) )
        else:
            parsed_line.append( GsubFragment(val=fragm, typ=GsubFragmentType.OTHER) )
    return parsed_line


class LookupProc(object):
    def __init__(self, tag, mapf):
        self.tag = tag
        self.mapf = mapf
        self.lines = []

    def valid(self):
        return True if self.lines else False

    def start(self):
        pass

    def end(self):
        if all_comments(self.lines):
            return
        print("lookup %s {" % (self.tag))
        for line in self.lines:
            print(line)
        print("} %s;" % (self.tag))

    def line(self, line):
        if re.search(r"^\s*sub", line):
            parsed_line = preprocess_gsub_line(line, self.mapf)
            if parsed_line:
                newline = "  substitute"
                for fragm in parsed_line:
                    if fragm.typ == GsubFragmentType.CID:
                        newline += " \\%d" % (fragm.val)
                    elif fragm.typ == GsubFragmentType.FROMBY or fragm.typ == GsubFragmentType.OTHER:
                        newline += " %s" % (fragm.val)
                newline += ";"
                self.lines.append(newline)
        else:
            self.lines.append(line)

##############################


class ClassProc(object):
    def __init__(self, tag, mapf, inside_feature=False):
        self.tag = tag
        self.mapf = mapf
        self.inside_feature = inside_feature
        self.cids = []
        self.cls_def = ""

    def valid(self):
        return True if self.cids else False

    def start(self):
        pass

    def end(self):
        if self.cids:
            self.cls_def = "  {} = [{}];".format(self.tag, " ".join(["\\%d" % (cid) for cid in self.cids]))
            if not self.inside_feature:
                print(self.cls_def)

    def line(self, line):
        for fragm in re.split(r"\s+", line):
            if fragm[0:1] == "\\":
                cid = int(fragm[1:])
                if cid in self.mapf:
                    self.cids.append(self.mapf[cid])

##############################


class TableProc(object):
    def __init__(self, tag, mapf):
        self.tag = tag
        self.mapf = mapf

    def start(self):
        print("table %s {" % (self.tag))

    def end(self):
        print("} %s;" % (self.tag))

    def line(self, line):
        print(line)


class HheaProc(TableProc):
    def __init__(self, mapf):
        super().__init__("hhea", mapf)

    def line(self, line):
        if "Ascender" in line:
            print(re.sub(r"Ascender\s+([-\d]+)", "Ascender 880", line))
        elif "Descender" in line:
            print(re.sub(r"Descender\s+([-\d]+)", "Descender -120", line))
        else:
            print(line)


class VmtxProc(TableProc):
    def __init__(self, mapf):
        super().__init__("vmtx", mapf)

    def line(self, line):
        m = re.search(r"Vert\S+\s+\\(\d+)", line)
        if m:
            cid = int(m.group(1))
            if cid in self.mapf:
                print(re.sub(r"\\\d+", r"\\%d" % (self.mapf[cid]), line))
        else:
            print(line)


class OS2Proc(TableProc):
    def __init__(self, mapf):
        super().__init__("OS/2", mapf)

    def line(self, line):
        if "winAscent" in line:
            print(re.sub(r"winAscent\s+([-\d]+)", "winAscent 880", line))
        elif "winDescent" in line:
            print(re.sub(r"winDescent\s+([-\d]+)", "winDescent 120", line))
        else:
            print(line)

##############################


class FeatureProc(object):
    def __init__(self, tag, mapf, lookups=None):
        self.tag = tag
        self.mapf = mapf
        self.lookups = lookups

    def start(self):
        print("feature %s {" % (self.tag))

    def end(self):
        print("} %s;" % (self.tag))

    def line(self, line):
        print(line)


class GeneralGsubProc(FeatureProc):
    def __init__(self, tag, mapf, lookups):
        super().__init__(tag, mapf, lookups)
        self.lines = []

    def start(self):
        pass

    def end(self):
        if all_comments(self.lines):
            return
        print("feature %s {" % (self.tag))
        for line in self.lines:
            print(line)
        print("} %s;" % (self.tag))

    def line(self, line):
        m = re.search(r"^\s*lookup\s+(\S+)\s*;", line)
        if m:
            lookup = m.group(1)
            if lookup in self.lookups:
                self.lines.append(line)
            return

        if re.search(r"^\s*sub", line):
            parsed_line = preprocess_gsub_line(line, self.mapf)
            if parsed_line:
                newline = "  substitute"
                for fragm in parsed_line:
                    if fragm.typ == GsubFragmentType.CID:
                        newline += " \\%d" % (fragm.val)
                    elif fragm.typ == GsubFragmentType.FROMBY or fragm.typ == GsubFragmentType.OTHER:
                        newline += " %s" % (fragm.val)
                newline += ";"
                self.lines.append(newline)
            return

        self.lines.append(line)


# XXX: very ugly and complicated ...
class LoclProc(FeatureProc):
    def __init__(self, tag, mapf, lookups):
        super().__init__(tag, mapf, lookups)
        self.tmp_script = None
        self.tmp_lang = None
        self.tmp_gsublines = []
        self.lines = []

    def start(self):
        pass

    def end(self):
        if not all_comments(self.tmp_gsublines):
            if self.tmp_script:
                self.lines.append(self.tmp_script)
            if self.tmp_lang:
                self.lines.append(self.tmp_lang)
            self.lines.extend(self.tmp_gsublines)

        if all_comments(self.lines):
            return
        print("feature %s {" % (self.tag))
        for line in self.lines:
            print(line)
        print("} %s;" % (self.tag))

    def line(self, line):
        if re.search(r"^\s*script", line):
            if all_comments(self.tmp_gsublines):
                # first comments
                if not self.tmp_script and not self.tmp_lang:
                    self.lines.extend(self.tmp_gsublines)
            else:
                if self.tmp_script:
                    self.lines.append(self.tmp_script)
                if self.tmp_lang:
                    self.lines.append(self.tmp_lang)
                self.lines.extend(self.tmp_gsublines)
            self.tmp_script = line
            self.tmp_lang   = None
            self.tmp_gsublines = []
            return

        if re.search(r"^\s*language", line):
            if not all_comments(self.tmp_gsublines):
                if self.tmp_script:
                    self.lines.append(self.tmp_script)
                if self.tmp_lang:
                    self.lines.append(self.tmp_lang)
                self.lines.extend(self.tmp_gsublines)
                self.tmp_script = None
            self.tmp_lang = line
            self.tmp_gsublines = []
            return

        m = re.search(r"^\s*lookup\s+(\S+)\s*;", line)
        if m:
            lookup = m.group(1)
            if lookup in self.lookups:
                self.tmp_gsublines.append(line)
            return

        if re.search(r"^\s*sub", line):
            parsed_line = preprocess_gsub_line(line, self.mapf)
            if parsed_line:
                newline = "  substitute"
                for fragm in parsed_line:
                    if fragm.typ == GsubFragmentType.CID:
                        newline += " \\%d" % (fragm.val)
                    elif fragm.typ == GsubFragmentType.FROMBY or fragm.typ == GsubFragmentType.OTHER:
                        newline += " %s" % (fragm.val)
                newline += ";"
                self.tmp_gsublines.append(newline)
            return

        self.tmp_gsublines.append(line)


class PaltVpalHaltVhalProc(FeatureProc):
    def __init__(self, tag, mapf):
        super().__init__(tag, mapf)

    def line(self, line):
        m = re.search(r"pos\S*\s+\\(\d+)", line)
        if m:
            cid = int(m.group(1))
            if cid in self.mapf:
                print(re.sub(r"\\\d+", r"\\%d" % (self.mapf[cid]), line))
        else:
            print(line)


class KernVkrnProc(FeatureProc):
    def __init__(self, tag, mapf, classes):
        super().__init__(tag, mapf)
        self.classes = classes
        self.lines = []

    def start(self):
        pass

    def end(self):
        if all_comments(self.lines):
            return
        print("feature %s {" % (self.tag))
        for line in self.lines:
            print(line)
        print("} %s;" % (self.tag))

    def line(self, line):
        m = re.search(r"^(.*pos\S*)\s+(.*)\s*;", line)
        if m:
            declaration = m.group(1)
            pairs_value = m.group(2).strip()
            latter_half_fragments = []
            for fragm in re.split(r"\s+", pairs_value):
                if fragm[0:1] == "@":
                    if fragm not in self.classes:
                        return
                    latter_half_fragments.append(fragm)
                elif fragm[0:1] == "\\":
                    cid = int(fragm[1:])
                    if cid not in self.mapf:
                        return
                    latter_half_fragments.append("\\%d" % (self.mapf[cid]))
                else:
                    latter_half_fragments.append(fragm)
            self.lines.append("{} {};".format(declaration, " ".join(latter_half_fragments)))
        else:
            self.lines.append(line)

##############################


class Proc(object):
    def __init__(self, mapf):
        self.mapf     = mapf
        self.lookups  = set()
        self.classes  = set()
        self.cur_look = None
        self.cur_cls  = None
        self.cur_tbl  = None
        self.cur_fea  = None

    def line(self, line):
        print(line)

    ###

    def lookup_start(self, tag):
        self.cur_look = Proc.lookup_factory(tag, self.mapf)
        self.cur_look.start()

    def lookup_end(self):
        self.cur_look.end()
        if self.cur_look.valid() and self.cur_look.tag not in self.lookups:
            self.lookups.add(self.cur_look.tag)
        self.cur_look = None

    def lookup_line(self, line):
        self.cur_look.line(line)

    ###

    def class_start(self, tag):
        self.cur_cls = Proc.class_factory(tag, self.mapf, True if self.cur_fea else False)
        self.cur_cls.start()

    def class_end(self):
        self.cur_cls.end()
        if self.cur_cls.valid():
            if self.cur_cls.tag not in self.classes:
                self.classes.add(self.cur_cls.tag)
            # XXX: ugly...
            if self.cur_fea:
                self.cur_fea.line(self.cur_cls.cls_def)
        self.cur_cls = None

    def class_line(self, line):
        self.cur_cls.line(line)

    ###

    def table_start(self, tag):
        self.cur_tbl = Proc.table_factory(tag, self.mapf)
        self.cur_tbl.start()

    def table_end(self):
        self.cur_tbl.end()
        self.cur_tbl = None

    def table_line(self, line):
        self.cur_tbl.line(line)

    ###

    def feature_start(self, tag):
        self.cur_fea = Proc.fearure_factory(tag, self.mapf, self.lookups, self.classes)
        self.cur_fea.start()

    def feature_end(self):
        self.cur_fea.end()
        self.cur_fea = None

    def feature_line(self, line):
        self.cur_fea.line(line)

    #####

    @staticmethod
    def lookup_factory(tag, mapf):
        return LookupProc(tag, mapf)

    @staticmethod
    def class_factory(tag, mapf, inside_feature):
        return ClassProc(tag, mapf, inside_feature)

    @staticmethod
    def table_factory(tag, mapf):
        if tag == "hhea":
            return HheaProc(mapf)
        elif tag == "vmtx":
            return VmtxProc(mapf)
        elif tag == "OS/2":
            return OS2Proc(mapf)
        else:
            return TableProc(tag, mapf)

    @staticmethod
    def fearure_factory(tag, mapf, lookups, classes):
        if tag in ["palt", "vpal", "halt", "vhal"]:
            return PaltVpalHaltVhalProc(tag, mapf)
        elif tag in ["kern", "vkrn"]:
            return KernVkrnProc(tag, mapf, classes)
        elif tag in ["ccmp", "hist", "liga", "dlig", "fwid",
                     "hwid", "pwid", "jp78", "jp83", "jp90",
                     "nlck", "vert", "vrt2"]:
            return GeneralGsubProc(tag, mapf, lookups)
        elif tag == "locl":
            return LoclProc(tag, mapf, lookups)
        else:
            return FeatureProc(tag, mapf, lookups)

##################################################


class FeatureConverter(object):
    def __init__(self):
        self.fea  = sys.argv[1]
        self.mapf = FeatureConverter.readMapFile(sys.argv[2])

        self.cur_tbl  = None
        self.cur_fea  = None
        self.cur_look = None
        self.cur_cls  = None

    def run(self):
        self._walk_through_fea()

    @staticmethod
    def readMapFile(map_f):
        map_ = {}
        with open(map_f) as f:
            for line in f.readlines():
                m = re.search(r"(\d+)\s+(\d+)", line)
                if m:
                    cid_to   = int(m.group(1))
                    cid_from = int(m.group(2))
                    if cid_from not in map_:
                        map_[cid_from] = cid_to
        return map_

    def _walk_through_fea(self):
        proc = Proc(self.mapf)
        with open(self.fea) as f:
            for line in [l.rstrip() for l in f.readlines()]:
                self._line_proc(line, proc)

    def _line_proc(self, line, proc):
        # evaluate lookup case first because it is defined inside feature definition.
        if self._lookup_proc(line, proc):
            pass
        elif self._class_proc(line, proc):
            pass
        elif self._table_proc(line, proc):
            pass
        elif self._feature_proc(line, proc):
            pass
        else:
            proc.line(line)

    def _lookup_proc(self, line, proc):
        m = re.search(r"^\s*lookup\s+(\S+)\s*{", line)
        if m:
            self.cur_look = m.group(1)
            proc.lookup_start(self.cur_look)
            return True
        if self.cur_look:
            if re.search(r"^\s*}\s*%s\s*;" % (self.cur_look), line):
                proc.lookup_end()
                self.cur_look = None
                return True
            proc.lookup_line(line)
            return True
        return False

    def _class_proc(self, line, proc):
        m = re.search(r"^\s*(@[a-zA-Z0-9_]+)\s*=\s*\[(.*)", line)
        if m:
            self.cur_cls = m.group(1)
            latter_half  = m.group(2)
            latter_half = re.sub(r"#.*", "", latter_half).replace(";", "").strip()
            proc.class_start(self.cur_cls)
            if latter_half != "":
                a = latter_half.split("]")
                cls_line = a[0]
                if cls_line != "":
                    proc.class_line(cls_line)
                if len(a) > 1:
                    proc.class_end()
                    self.cur_cls = None
            return True
        if self.cur_look:
            line = re.sub(r"#.*", "", line).replace(";", "").strip()
            a = line.split("]")
            cls_line = a[0]
            if cls_line != "":
                proc.class_line(cls_line)
            if len(a) > 1:
                proc.class_end()
                self.cur_cls = None
            return True
        return False

    def _table_proc(self, line, proc):
        m = re.search(r"^\s*table\s+(\S+)\s*{", line)
        if m:
            self.cur_tbl = m.group(1)
            proc.table_start(self.cur_tbl)
            return True
        if self.cur_tbl:
            if re.search(r"^\s*}\s*%s\s*;" % (self.cur_tbl), line):
                proc.table_end()
                self.cur_tbl = None
                return True
            proc.table_line(line)
            return True
        return False

    def _feature_proc(self, line, proc):
        m = re.search(r"^\s*feature\s+(\S+)\s*{", line)
        if m:
            self.cur_fea = m.group(1)
            proc.feature_start(self.cur_fea)
            return True
        if self.cur_fea:
            if re.search(r"^\s*}\s*%s\s*;" % (self.cur_fea), line):
                proc.feature_end()
                self.cur_fea = None
                return True
            proc.feature_line(line)
            return True
        return False

################################################################################

ver = sys.version_info
if ver.major < 3:
    print("I may not work... :(")

conv = FeatureConverter()
conv.run()
