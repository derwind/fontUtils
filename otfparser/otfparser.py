#! /usr/bin/env python
# -*- coding: utf-8 -*-

# http://www.microsoft.com/typography/otspec/otff.htm

import os
import sys
#import struct
import datetime


################################################################################

py_ver = sys.version_info[0]    # version of python

## custom exception class
class MyError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

## utility of values
class ValUtil(object):
    @staticmethod
    def schar(data):
        global py_ver
        n = ValUtil.uchar(data)

        sign = (n >> 7) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7f) + 1)

    @staticmethod
    def scharpop(data):
        return ValUtil.schar(data), data[1:]

    @staticmethod
    def uchar(data):
        global py_ver
        if py_ver == 2:
            return ord(data[0])
        else:
            return data[0]

    @staticmethod
    def ucharpop(data):
        return ValUtil.uchar(data), data[1:]

    @staticmethod
    def sshort(data):
        global py_ver
        n = ValUtil.ushort(data)

        sign = (n >> 15) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7fff) + 1)

    @staticmethod
    def sshortpop(data):
        return ValUtil.sshort(data), data[2:]

    @staticmethod
    def ushort(data):
        global py_ver
        if py_ver == 2:
            return ord(data[0]) << 8 | ord(data[1])
        else:
            return data[0] << 8 | data[1]

    @staticmethod
    def ushortpop(data):
        return ValUtil.ushort(data), data[2:]

    def sint24(data):
        global py_ver
        n = ValUtil.uint24(data)

        sign = (n >> 23) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7fffff) + 1)

    @staticmethod
    def sint24pop(data):
        return ValUtil.sint24(data), data[3:]

    @staticmethod
    def uint24(data):
        global py_ver
        if py_ver == 2:
            return ord(data[0]) << 16 | ord(data[1]) << 8 | ord(data[2])
        else:
            return data[0] << 16 | data[1] << 8 | data[2]

    @staticmethod
    def uint24pop(data):
        return ValUtil.uint24(data), data[3:]

    def slong(data):
        global py_ver
        n = ValUtil.ulong(data)

        sign = (n >> 31) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7fffffff) + 1)

    @staticmethod
    def slongpop(data):
        return ValUtil.slong(data), data[4:]

    @staticmethod
    def ulong(data):
        global py_ver
        if py_ver == 2:
            return ord(data[0]) << 24 | ord(data[1]) << 16 | ord(data[2]) << 8 | ord(data[3])
        else:
            return data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3]

    @staticmethod
    def ulongpop(data):
        return ValUtil.ulong(data), data[4:]

    @staticmethod
    def ulonglong(data):
        global py_ver
        if py_ver == 2:
            return ord(data[0]) << 56 | ord(data[1]) << 48 | ord(data[2]) << 40 | ord(data[3]) << 32 | ord(data[4]) << 24 | ord(data[5]) << 16 | ord(data[6]) << 8 | ord(data[7])
        else:
            return data[0] << 56 | data[1] << 48 | data[2] << 40 | data[3] << 32 | data[4] << 24 | data[5] << 16 | data[6] << 8 | data[7]

    @staticmethod
    def ulonglongpop(data):
        return ValUtil.ulonglong(data), data[8:]

# https://www.microsoft.com/typography/otspec/otff.htm
class OTData(object):
    @staticmethod
    def Fixed(data):
        return ValUtil.ulongpop(data)

    @staticmethod
    def LONGDATETIME(data):
        return ValUtil.ulonglongpop(data)

    @staticmethod
    def Tag(data):
        return data[:4], data[4:]

    @staticmethod
    def GlyphID(data):
        return ValUtil.ushortpop(data)

    @staticmethod
    def Offset(data):
        return ValUtil.ushortpop(data)

    @staticmethod
    def isNullOffset(offset):
        if isinstance(offset, int):
            return offset == 0
        else:
            return ValUtil.ushort(offset) == 0

# 5176.CFF.pdf  Table 2 CFF Data Types
class CFFData(object):
    @staticmethod
    def Offset(data, n):
        if n == 1:
            return ValUtil.ucharpop(data)
        elif n == 2:
            return ValUtil.ushortpop(data)
        elif n == 3:
            return ValUtil.uint24pop(data)
        elif n == 4:
            return ValUtil.ulongpop(data)
        else:
            raise

    @staticmethod
    def OffSize(data):
        return ValUtil.ucharpop(data)

## utility of LongDateTime
class LongDateTime(object):
    @staticmethod
    def to_date_str(value):
        d = datetime.datetime(1904, 1, 1)
        d += datetime.timedelta(seconds = value) #+ datetime.timedelta(hours = 9)
        return "%u/%02u/%02u %02u:%02u:%02u" % (d.year, d.month, d.day, d.hour, d.minute, d.second)

##################################################

## Header for OTF file
class Header(object):
    def __init__(self, data):
        self.__parse(data)

    @classmethod
    def get_size(cls):
        return 12

    def get_num_tables(self):
        return self.__num_tables

    def show(self):
        print("[Header]")
        print("  num_tables    = %u" % (self.__num_tables))
        print("  search_range  = %u" % (self.__search_range))
        print("  entry_selector= %u" % (self.__entry_selector))
        print("  range_shift   = %u" % (self.__range_shift))

    def __parse(self, data):
        global py_ver
        if py_ver == 2:
            if data[:4] != "OTTO":
                # check whether TTF
                if data[0] != "\x00" or data[1] != "\x01" or data[2] != "\x00" or data[3] != "\x00":
                    raise MyError("invalid header")
        else:
            if data[0] != ord('O') or data[1] != ord('T') or data[2] != ord('T') or data[3] != ord('O'):
                # check whether TTF
                if data[0] != 0 or data[1] != 1 or data[2] != 0 or data[3] != 0:
                    raise MyError("invalid header")

        data = data[4:]
        self.__num_tables, data     = ValUtil.ushortpop(data)
        self.__search_range, data   = ValUtil.ushortpop(data)
        self.__entry_selector, data = ValUtil.ushortpop(data)
        self.__range_shift, data    = ValUtil.ushortpop(data)

## TableRecord for each table in OTF file
class TableRecord(object):
    def __init__(self, data):
        self.__parse(data)

    @classmethod
    def get_size(self):
        return 16

    def get_tag(self):
        return "%c%c%c%c" % (chr(self.__tag >> 24 & 0xff), chr(self.__tag >> 16 & 0xff), chr(self.__tag >> 8 & 0xff),chr(self.__tag & 0xff))

    def get_check_sum(self):
        return self.__check_sum

    def get_offset(self):
        return self.__offset

    def get_length(self):
        return self.__length

    def show(self):
        print("[TableRecord]")
        print("  tag           = %c%c%c%c" % (chr(self.__tag >> 24 & 0xff), chr(self.__tag >> 16 & 0xff), chr(self.__tag >> 8 & 0xff),chr(self.__tag & 0xff)))
        print("  check_sum     = 0x%0x" % (self.__check_sum))
        print("  offset        = %u" % (self.__offset))
        print("  length        = %u" % (self.__length))

    def __parse(self, data):
        self.__tag, data       = ValUtil.ulongpop(data)
        self.__check_sum, data = ValUtil.ulongpop(data)
        self.__offset, data    = ValUtil.ulongpop(data)
        self.__length, data    = ValUtil.ulongpop(data)

## Table in OTF file
class Table(object):
    def __init__(self, data, tag):
        self.tag = tag
        self.parse(data)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, data):
        self.data = data

## http://www.microsoft.com/typography/otspec/head.htm
class HeadTable(Table):
    def __init__(self, data, tag):
        super(HeadTable, self).__init__(data, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  version_number       = 0x%08x" % (self.version_number))
        print("  font_revision        = %u" % (self.font_revision))
        print("  check_sum_adjustment = 0x%08x" % (self.check_sum_adjustment))
        print("  magic_number         = 0x%08x" % (self.magic_number))
        print("  flags                = %s" % (format(self.flags, '016b')))
        print("  units_per_em         = %u" % (self.units_per_em))
        print("  created              = %s" % (LongDateTime.to_date_str(self.created)))
        print("  modified             = %s" % (LongDateTime.to_date_str(self.modified)))
        print("  xmin                 = %d" % (self.xmin))
        print("  ymin                 = %d" % (self.ymin))
        print("  xmax                 = %d" % (self.xmax))
        print("  ymax                 = %d" % (self.ymax))
        print("  mac_style            = %s" % (format(self.mac_style, '016b')))
        print("  lowest_rec_ppem      = %u" % (self.lowest_rec_ppem))
        print("  font_direction_hint  = %d" % (self.font_direction_hint))
        print("  index_to_loc_format  = %d" % (self.index_to_loc_format))
        print("  glyph_data_format    = %d" % (self.glyph_data_format))

    def parse(self, data):
        super(HeadTable, self).parse(data)

        self.version_number, data = ValUtil.ulongpop(data)
        self.font_revision, data = ValUtil.ulongpop(data)
        self.check_sum_adjustment, data = ValUtil.ulongpop(data)
        self.magic_number, data = ValUtil.ulongpop(data)
        self.flags, data = ValUtil.ushortpop(data)
        self.units_per_em, data = ValUtil.ushortpop(data)
        self.created, data = OTData.LONGDATETIME(data)
        self.modified, data = OTData.LONGDATETIME(data)
        self.xmin, data = ValUtil.sshortpop(data)
        self.ymin, data = ValUtil.sshortpop(data)
        self.xmax, data = ValUtil.sshortpop(data)
        self.ymax, data = ValUtil.sshortpop(data)
        self.mac_style, data = ValUtil.ushortpop(data)
        self.lowest_rec_ppem, data = ValUtil.ushortpop(data)
        self.font_direction_hint, data = ValUtil.sshortpop(data)
        self.index_to_loc_format, data = ValUtil.sshortpop(data)
        self.glyph_data_format, data = ValUtil.sshortpop(data)

##################################################
# name table

class NameTable(Table):
    def __init__(self, data, tag):
        super(NameTable, self).__init__(data, tag)

    def parse(self, data):
        super(NameTable, self).parse(data)

        self.format, data        = ValUtil.ushortpop(data)
        self.count, data         = ValUtil.ushortpop(data)
        self.stringOffset, data  = ValUtil.ushortpop(data)
        self.nameRecord = []
        for i in range(self.count):
            name_record = NameRecord(data)
            data = name_record.data
            self.nameRecord.append(name_record)
        if self.format != 0:
            self.langTagCount, data = ValUtil.ushortpop(data)
            for i in range(self.langTagCount):
                lang_tag_record = LangTagRecord(data)
                data = lang_tag_record.data
                self.langTagRecord.append(lang_tag_record)
        self.storage = data

    def show(self):
        print("[Table(%s)]" % (self.tag))
        #print("%s" % (self.data))
        print("  format       = %d" % (self.format))
        print("  count        = %d" % (self.count))
        print("  stringOffset = %d" % (self.stringOffset))
        for name_record in self.nameRecord:
            name_record.show(self.storage)
        if self.format != 0:
            for lang_tag_record in self.langTagRecord:
                lang_tag_record.show(self.storage)

class NameRecord(object):
    def __init__(self, data):
        self.data = self.parse(data)

    def parse(self, data):
        self.platformID, data = ValUtil.ushortpop(data)
        self.encodingID, data = ValUtil.ushortpop(data)
        self.languageID, data = ValUtil.ushortpop(data)
        self.nameID, data     = ValUtil.ushortpop(data)
        self.length, data     = ValUtil.ushortpop(data)
        self.offset, data     = ValUtil.ushortpop(data)
        return data

    def show(self, storage = None):
        print("  [NameRecord]")
        print("    platformID = %d" % (self.platformID))
        print("    encodingID = %d" % (self.encodingID))
        print("    languageID = %d" % (self.languageID))
        print("    nameID     = %d" % (self.nameID))
        print("    length     = %d" % (self.length))
        print("    offset     = %d" % (self.offset))
        if storage:
            s = storage[self.offset:self.offset+self.length]
            print("    string     = %s" % (s))

class LangTagRecord(object):
    def __init__(self, data):
        self.data = self.parse(data)

    def parse(self, data):
        self.length, data     = ValUtil.ushortpop(data)
        self.offset, data     = ValUtil.ushortpop(data)
        return data

    def show(self, storage = None):
        print("  [LangTagRecord]")
        print("    length   = %d" % (self.length))
        print("    offset   = %d" % (self.offset))
        if storage:
            s = storage[self.offset:self.offset+self.length]
            print("    Lang-tag = %s" % (s))

# name table
##################################################
# CFF

## http://www.microsoft.com/typography/otspec/cff.htm
## http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5176.CFF.pdf
## http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5177.Type2.pdf
## OOps...
class CffTable(Table):
    def __init__(self, data, tag):
        super(CffTable, self).__init__(data, tag)

    def parse(self, data):
        super(CffTable, self).parse(data)

        # 5176.CFF.pdf  Table 1 CFF Data Layout
        self.data_head        = data
        self.header           = CffHeader(data)
        self.nameIndex        = NameIndex(self.header.data)
        self.topDictIndex     = TopDictIndex(self.nameIndex.data)
        self.stringIndex      = CffIndexData(self.topDictIndex.data, "String")
        self.globalSubrIndex  = CffIndexData(self.stringIndex.data, "Global Subr")
        self.encodings        = None
        self.charsets         = None
        self.FDSelect         = None

    def show(self):
        print("[Table(%s)]" % (self.tag))
        self.header.show()
        self.nameIndex.show()
        self.topDictIndex.show()
        self.stringIndex.show()
        self.globalSubrIndex.show()

# 5176.CFF.pdf  6 Header
class CffHeader(object):
    def __init__(self, data):
        self.data = self.parse(data)

    def parse(self, data):
        self.major, data   = ValUtil.ucharpop(data)
        self.minor, data   = ValUtil.ucharpop(data)
        self.hdrSize, data = ValUtil.ucharpop(data)
        self.offSize, data = CFFData.OffSize(data)
        return data

    def show(self, storage = None):
        print("  [CffHeader]")
        print("    major   = %d" % (self.major))
        print("    minor   = %d" % (self.minor))
        print("    hdrSize = %d" % (self.hdrSize))
        print("    offSize = %d" % (self.offSize))

# 5176.CFF.pdf  4 DICT Data
# dictionary: [value][key][value][key]...
#
# [------------------- value -----------------------][-------- key ---------]
# [operand(s); variable-size; integer or real values][operator; 1- or 2-byte]
class CffDictData(object):
    pass

# 5176.CFF.pdf  5 INDEX Data
class CffIndexData(object):
    def __init__(self, data, name):
        self.name = name
        self.data = self.parse(data)

    def parse(self, data):
        self.count, data   = ValUtil.ushortpop(data)
        if self.count != 0:
            self.offSize, data = CFFData.OffSize(data)
            self.offset = []
            for i in range(self.count + 1):
                val, data = CFFData.Offset(data, self.offSize)
                self.offset.append(val)
            self.objData = []
            for i in range(1, self.count + 1):
                length = self.offset[i]-self.offset[i-1]
                objData, data = data[:length], data[length:]
                self.objData.append(objData)
        return data

    def show(self):
        print("  [CffIndexData(%s)]" % (self.name))
        print("    count   = %d" % (self.count))
        if self.count != 0:
            print("    offSize = %d" % (self.offSize))
            print("    offset  = {0}".format(", ".join([str(val) for val in self.offset])))

class NameIndex(CffIndexData):
    def __init__(self, data):
        super(NameIndex, self).__init__(data, "Name")

    def parse(self, data):
        return super(NameIndex, self).parse(data)

    def show(self):
        super(NameIndex, self).show()

        if self.count != 0:
            print("    data    = {0}".format(", ".join(self.objData)))

class TopDictIndex(CffIndexData):
    def __init__(self, data):
        super(TopDictIndex, self).__init__(data, "Top DICT")

    def parse(self, data):
        data = super(TopDictIndex, self).parse(data)
        return data

    def show(self):
        super(TopDictIndex, self).show()

        if self.count != 0:
            print("    data    = {0}".format(", ".join(self.objData)))

# CFF
##################################################
# GPOS

# https://www.microsoft.com/typography/otspec/gpos.htm
# http://partners.adobe.com/public/developer/opentype/index_table_formats2.html
class GposTable(Table):
    def __init__(self, data, tag):
        super(GposTable, self).__init__(data, tag)

    def parse(self, data):
        super(GposTable, self).parse(data)

        self.header     = GposHeader(data)
        self.scriptList = ScriptList(data[self.header.ScriptList:])

    def show(self):
        print("[Table(%s)]" % (self.tag))
        self.header.show()
        self.scriptList.show()

class GposHeader(object):
    def __init__(self, data):
        self.data = self.parse(data)

    def parse(self, data):
        self.Version, data     = OTData.Fixed(data)
        self.ScriptList, data  = OTData.Offset(data)
        self.FeatureList, data = OTData.Offset(data)
        self.LookupList, data  = OTData.Offset(data)
        return data

    def show(self):
        print("  [GposHeader]")
        print("    Version     = 0x%08x" % (self.Version))
        print("    ScriptList  = %d" % (self.ScriptList))
        print("    FeatureList = %d" % (self.FeatureList))
        print("    LookupList  = %d" % (self.LookupList))

# https://www.microsoft.com/typography/otspec/chapter2.htm
# http://partners.adobe.com/public/developer/opentype/index_table_formats.html
class ScriptList(object):
    def __init__(self, data):
        self.data_head = data
        self.parse(data)

    def parse(self, data):
        self.ScriptCount, data = ValUtil.ushortpop(data)
        self.ScriptRecord = []
        for i in range(self.ScriptCount):
            record = ScriptRecord(data, self.data_head)
            data = record.data
            self.ScriptRecord.append(record)

    def show(self):
        print("  [ScriptList]")
        print("    ScriptCount = %d" % (self.ScriptCount))
        for record in self.ScriptRecord:
            record.show()

class ScriptRecord(object):
    def __init__(self, data, scriptListHead = None):
        self.data = self.parse(data, scriptListHead)

    def parse(self, data, scriptListHead = None):
        self.ScriptTag, data = OTData.Tag(data)
        self.Script, data    = OTData.Offset(data)
        self.ScriptTable     = None
        if scriptListHead:
            self.ScriptTable = ScriptTable(scriptListHead[self.Script:])
        return data

    def show(self):
        print("    [ScriptRecord]")
        print("      ScriptTag = %s" % (self.ScriptTag))
        print("      Script    = %d" % (self.Script))
        if self.ScriptTable:
            self.ScriptTable.show()

class ScriptTable(object):
    def __init__(self, data):
        self.data_head = data
        self.parse(data)

    def parse(self, data):
        self.DefaultLangSys, data = OTData.Offset(data)
        self.LangSysCount, data   = ValUtil.ushortpop(data)
        self.DefaultLangSysTable  = None
        if not OTData.isNullOffset(self.DefaultLangSys):
            self.DefaultLangSysTable = LangSysTable(self.data_head[self.DefaultLangSys:])
        self.LangSysTable = []
        for i in range(self.LangSysCount):
            langSysTable = LangSysRecord(data, self.data_head)
            data = langSysTable.data
            self.LangSysTable.append(langSysTable)
        return data

    def show(self):
        print("      [ScriptTable]")
        print("        DefaultLangSys = %s" % (self.DefaultLangSys))
        print("        LangSysCount   = %d" % (self.LangSysCount))
        if self.DefaultLangSysTable:
            print("        [DefaultLangSysTable]")
            self.DefaultLangSysTable.show()
        for langSysTable in self.LangSysTable:
            langSysTable.show()

class LangSysRecord(object):
    def __init__(self, data, scriptTableHead = None):
        self.data = self.parse(data, scriptTableHead)

    def parse(self, data, scriptTableHead):
        self.LangSysTag, data = OTData.Tag(data)
        self.LangSys, data    = OTData.Offset(data)
        self.LangSysTable = None
        if scriptTableHead:
            self.LangSysTable = LangSysTable(scriptTableHead[self.LangSys:])
        return data

    def show(self):
        print("        [LangSysRecord]")
        print("          LangSysTag = %s" % (self.LangSysTag))
        print("          LangSys    = %d" % (self.LangSys))
        if self.LangSysTable:
            self.LangSysTable.show()

class LangSysTable(object):
    def __init__(self, data):
        self.data = self.parse(data)

    def parse(self, data):
        self.LookupOrder, data     = OTData.Offset(data)
        self.ReqFeatureIndex, data = ValUtil.ushortpop(data)
        self.FeatureCount, data    = ValUtil.ushortpop(data)
        self.FeatureIndex = []
        for i in range(self.FeatureCount):
            index, data = ValUtil.ushortpop(data)
            self.FeatureIndex.append(index)
        return data

    def show(self):
        print("          [LangSysTable]")
        print("            LookupOrder     = %d" % (self.LookupOrder))
        print("            ReqFeatureIndex = 0x%04x" % (self.ReqFeatureIndex))
        print("            FeatureCount    = %d" % (self.FeatureCount))
        if self.FeatureIndex:
            print("            FeatureIndex    = {0}".format(", ".join([str(index) for index in self.FeatureIndex])))

# GPOS
##################################################
# GSUB

class GsubTable(Table):
    def __init__(self, data, tag):
        super(GsubTable, self).__init__(data, tag)

    def parse(self, data):
        super(GsubTable, self).parse(data)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("%s" % (self.data))

# GSUB
##################################################

## TTF has a loca table
class LocaTable(Table):
    def __init__(self, data, tag):
        super(LocaTable, self).__init__(data, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, data):
        super(LocaTable, self).parse(data)

##################################################

## TTF has a glyp table
class GlypTable(Table):
    def __init__(self, data, tag):
        super(GlypTable, self).__init__(data, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, data):
        super(GlypTable, self).parse(data)

##################################################

## main class of otfparser
class OtfParser(object):
    def __init__(self):
        self.__header = None
        self.__table_record = []
        self.__table        = []

    def parse(self, file):
        self.__parse(file)

    def show(self):
        self.__header.show()
        print("--------------------")
        i = 0
        for tbl_record in self.__table_record:
            tbl_record.show()
            tbl = self.__table[i].show()
            print("--------------------")
            i += 1

    def __parse(self, file):
#       print("---> " + file)
        with open(file, "rb") as infile:
            bin_data = infile.read(12)
            self.__header = Header(bin_data)
            num_tables = self.__header.get_num_tables()
            for i in range(num_tables):
                bin_data = infile.read(16)
                self.__table_record.append( TableRecord(bin_data) )

            for table_record in self.__table_record:
                self.__create_table(table_record, infile)

    ## get table corresponding to given TableRecord
    def __create_table(self, table_record, infile):
        offset = table_record.get_offset()
        length = table_record.get_length()
        infile.seek(offset, os.SEEK_SET)
        data = infile.read(length)
        tag = table_record.get_tag()

        if tag.lower() == "cff ":
            self.__table.append( CffTable(data, tag) )
        elif tag.lower() == "loca":
            self.__table.append( LocaTable(data, tag) )
        elif tag.lower() == "glyp":
            self.__table.append( GlypTable(data, tag) )
        elif tag.lower() == "gpos":
            self.__table.append( GposTable(data, tag) )
        elif tag.lower() == "gsub":
            self.__table.append( GsubTable(data, tag) )
        elif tag.lower() == "head":
            self.__table.append( HeadTable(data, tag) )
        elif tag.lower() == "name":
            self.__table.append( NameTable(data, tag) )
        else:
            self.__table.append( Table(data, tag) )


################################################################################

def help():
    print( "[usage] %s INPUT_OTF" % (sys.argv[0]) )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
        exit(1)

    parser = OtfParser()
    parser.parse(sys.argv[1])
    parser.show()
