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
    def schar(buf):
        global py_ver
        n = ValUtil.uchar(buf)

        sign = (n >> 7) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7f) + 1)

    @staticmethod
    def scharpop(buf):
        return ValUtil.schar(buf), buf[1:]

    @staticmethod
    def uchar(buf):
        global py_ver
        if py_ver == 2:
            return ord(buf[0])
        else:
            return buf[0]

    @staticmethod
    def ucharpop(buf):
        return ValUtil.uchar(buf), buf[1:]

    @staticmethod
    def sshort(buf):
        global py_ver
        n = ValUtil.ushort(buf)

        sign = (n >> 15) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7fff) + 1)

    @staticmethod
    def sshortpop(buf):
        return ValUtil.sshort(buf), buf[2:]

    @staticmethod
    def ushort(buf):
        global py_ver
        if py_ver == 2:
            return ord(buf[0]) << 8 | ord(buf[1])
        else:
            return buf[0] << 8 | buf[1]

    @staticmethod
    def ushortpop(buf):
        return ValUtil.ushort(buf), buf[2:]

    def sint24(buf):
        global py_ver
        n = ValUtil.uint24(buf)

        sign = (n >> 23) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7fffff) + 1)

    @staticmethod
    def sint24pop(buf):
        return ValUtil.sint24(buf), buf[3:]

    @staticmethod
    def uint24(buf):
        global py_ver
        if py_ver == 2:
            return ord(buf[0]) << 16 | ord(buf[1]) << 8 | ord(buf[2])
        else:
            return buf[0] << 16 | buf[1] << 8 | buf[2]

    @staticmethod
    def uint24pop(buf):
        return ValUtil.uint24(buf), buf[3:]

    def slong(buf):
        global py_ver
        n = ValUtil.ulong(buf)

        sign = (n >> 31) & 0x1
        if sign == 0:
            return n
        else:
            return -((~n & 0x7fffffff) + 1)

    @staticmethod
    def slongpop(buf):
        return ValUtil.slong(buf), buf[4:]

    @staticmethod
    def ulong(buf):
        global py_ver
        if py_ver == 2:
            return ord(buf[0]) << 24 | ord(buf[1]) << 16 | ord(buf[2]) << 8 | ord(buf[3])
        else:
            return buf[0] << 24 | buf[1] << 16 | buf[2] << 8 | buf[3]

    @staticmethod
    def ulongpop(buf):
        return ValUtil.ulong(buf), buf[4:]

    @staticmethod
    def ulonglong(buf):
        global py_ver
        if py_ver == 2:
            return ord(buf[0]) << 56 | ord(buf[1]) << 48 | ord(buf[2]) << 40 | ord(buf[3]) << 32 | ord(buf[4]) << 24 | ord(buf[5]) << 16 | ord(buf[6]) << 8 | ord(buf[7])
        else:
            return buf[0] << 56 | buf[1] << 48 | buf[2] << 40 | buf[3] << 32 | buf[4] << 24 | buf[5] << 16 | buf[6] << 8 | buf[7]

    @staticmethod
    def ulonglongpop(buf):
        return ValUtil.ulonglong(buf), buf[8:]

# https://www.microsoft.com/typography/otspec/otff.htm
class OTData(object):
    @staticmethod
    def Fixed(buf):
        return ValUtil.ulongpop(buf)

    @staticmethod
    def LONGDATETIME(buf):
        return ValUtil.ulonglongpop(buf)

    @staticmethod
    def Tag(buf):
        return buf[:4], buf[4:]

    @staticmethod
    def GlyphID(buf):
        return ValUtil.ushortpop(buf)

    @staticmethod
    def Offset(buf):
        return ValUtil.ushortpop(buf)

    @staticmethod
    def isNullOffset(offset):
        if isinstance(offset, int):
            return offset == 0
        else:
            return ValUtil.ushort(offset) == 0

# 5176.CFF.pdf  Table 2 CFF Data Types
class CFFData(object):
    @staticmethod
    def Offset(buf, n):
        if n == 1:
            return ValUtil.ucharpop(buf)
        elif n == 2:
            return ValUtil.ushortpop(buf)
        elif n == 3:
            return ValUtil.uint24pop(buf)
        elif n == 4:
            return ValUtil.ulongpop(buf)
        else:
            raise

    @staticmethod
    def OffSize(buf):
        return ValUtil.ucharpop(buf)

# 5176.CFF.pdf  Appendix A Standard Strings
class SID(object):
    nStdStrings = 391

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
    def __init__(self, buf):
        self.__parse(buf)

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

    def __parse(self, buf):
        global py_ver
        if py_ver == 2:
            if buf[:4] != "OTTO":
                # check whether TTF
                if buf[0] != "\x00" or buf[1] != "\x01" or buf[2] != "\x00" or buf[3] != "\x00":
                    raise MyError("invalid header")
        else:
            if buf[0] != ord('O') or buf[1] != ord('T') or buf[2] != ord('T') or buf[3] != ord('O'):
                # check whether TTF
                if buf[0] != 0 or buf[1] != 1 or buf[2] != 0 or buf[3] != 0:
                    raise MyError("invalid header")

        buf = buf[4:]
        self.__num_tables, buf     = ValUtil.ushortpop(buf)
        self.__search_range, buf   = ValUtil.ushortpop(buf)
        self.__entry_selector, buf = ValUtil.ushortpop(buf)
        self.__range_shift, buf    = ValUtil.ushortpop(buf)

## TableRecord for each table in OTF file
class TableRecord(object):
    def __init__(self, buf):
        self.__parse(buf)

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

    def __parse(self, buf):
        self.__tag, buf       = ValUtil.ulongpop(buf)
        self.__check_sum, buf = ValUtil.ulongpop(buf)
        self.__offset, buf    = ValUtil.ulongpop(buf)
        self.__length, buf    = ValUtil.ulongpop(buf)

## Table in OTF file
class Table(object):
    def __init__(self, buf, tag):
        self.tag = tag
        self.parse(buf)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, buf):
        self.buf = buf

## http://www.microsoft.com/typography/otspec/head.htm
class HeadTable(Table):
    def __init__(self, buf, tag):
        super(HeadTable, self).__init__(buf, tag)

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
        print("  glyph_buf_format    = %d" % (self.glyph_buf_format))

    def parse(self, buf):
        super(HeadTable, self).parse(buf)

        self.version_number, buf = ValUtil.ulongpop(buf)
        self.font_revision, buf = ValUtil.ulongpop(buf)
        self.check_sum_adjustment, buf = ValUtil.ulongpop(buf)
        self.magic_number, buf = ValUtil.ulongpop(buf)
        self.flags, buf = ValUtil.ushortpop(buf)
        self.units_per_em, buf = ValUtil.ushortpop(buf)
        self.created, buf = OTData.LONGDATETIME(buf)
        self.modified, buf = OTData.LONGDATETIME(buf)
        self.xmin, buf = ValUtil.sshortpop(buf)
        self.ymin, buf = ValUtil.sshortpop(buf)
        self.xmax, buf = ValUtil.sshortpop(buf)
        self.ymax, buf = ValUtil.sshortpop(buf)
        self.mac_style, buf = ValUtil.ushortpop(buf)
        self.lowest_rec_ppem, buf = ValUtil.ushortpop(buf)
        self.font_direction_hint, buf = ValUtil.sshortpop(buf)
        self.index_to_loc_format, buf = ValUtil.sshortpop(buf)
        self.glyph_buf_format, buf = ValUtil.sshortpop(buf)

##################################################
# name table

class NameTable(Table):
    def __init__(self, buf, tag):
        super(NameTable, self).__init__(buf, tag)

    def parse(self, buf):
        super(NameTable, self).parse(buf)

        self.format, buf        = ValUtil.ushortpop(buf)
        self.count, buf         = ValUtil.ushortpop(buf)
        self.stringOffset, buf  = ValUtil.ushortpop(buf)
        self.nameRecord = []
        for i in range(self.count):
            name_record = NameRecord(buf)
            buf = name_record.buf
            self.nameRecord.append(name_record)
        if self.format != 0:
            self.langTagCount, buf = ValUtil.ushortpop(buf)
            for i in range(self.langTagCount):
                lang_tag_record = LangTagRecord(buf)
                buf = lang_tag_record.buf
                self.langTagRecord.append(lang_tag_record)
        self.storage = buf

    def show(self):
        print("[Table(%s)]" % (self.tag))
        #print("%s" % (self.buf))
        print("  format       = %d" % (self.format))
        print("  count        = %d" % (self.count))
        print("  stringOffset = %d" % (self.stringOffset))
        for name_record in self.nameRecord:
            name_record.show(self.storage)
        if self.format != 0:
            for lang_tag_record in self.langTagRecord:
                lang_tag_record.show(self.storage)

class NameRecord(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.platformID, buf = ValUtil.ushortpop(buf)
        self.encodingID, buf = ValUtil.ushortpop(buf)
        self.languageID, buf = ValUtil.ushortpop(buf)
        self.nameID, buf     = ValUtil.ushortpop(buf)
        self.length, buf     = ValUtil.ushortpop(buf)
        self.offset, buf     = ValUtil.ushortpop(buf)
        return buf

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
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.length, buf     = ValUtil.ushortpop(buf)
        self.offset, buf     = ValUtil.ushortpop(buf)
        return buf

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
    def __init__(self, buf, tag):
        super(CffTable, self).__init__(buf, tag)

    def parse(self, buf):
        super(CffTable, self).parse(buf)

        # 5176.CFF.pdf  Table 1 CFF Data Layout (p.8)
        self.buf_head        = buf
        self.header           = CffHeader(buf)
        buf = self.header.buf
        self.nameIndex        = NameIndex(buf)
        buf = self.nameIndex.buf
        self.topDictIndex     = TopDictIndex(buf)
        buf = self.topDictIndex.buf
        self.stringIndex      = CffINDEXData(buf, "String")
        buf = self.stringIndex.buf
        self.globalSubrIndex  = CffINDEXData(buf, "Global Subr")
        self.encodings        = None
        self.charsets         = None
        self.FDSelect         = None

    def show(self):
        print("[Table(%s)]" % (self.tag))
        self.header.show()
        self.nameIndex.show()
        self.topDictIndex.show(self.stringIndex)
        self.stringIndex.show()
        self.globalSubrIndex.show()

# 5176.CFF.pdf  6 Header (p.13)
class CffHeader(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.major, buf   = ValUtil.ucharpop(buf)
        self.minor, buf   = ValUtil.ucharpop(buf)
        self.hdrSize, buf = ValUtil.ucharpop(buf)
        self.offSize, buf = CFFData.OffSize(buf)
        return buf

    def show(self, storage = None):
        print("  [CffHeader]")
        print("    major   = %d" % (self.major))
        print("    minor   = %d" % (self.minor))
        print("    hdrSize = %d" % (self.hdrSize))
        print("    offSize = %d" % (self.offSize))

# 5176.CFF.pdf  4 DICT Data (p.9)
# dictionary: [value][key][value][key]...
#
# [------------------- value -----------------------][-------- key ---------]
# [operand(s); variable-size; integer or real values][operator; 1- or 2-byte]
class CffDictData(object):
    def __init__(self, buf):
        self.dict = []
        self.buf  = self.parse(buf)

    def items(self):
        return self.dict

    def parse(self, buf):
        operands = []
        while len(buf) > 0:
            b = ValUtil.uchar(buf)
            if CffDictData._is_operator(b):
                operator, buf = CffDictData._operator(buf)
                self.dict.append( (operator, operands) )
                operands = []
            else:
                operand, buf = CffDictData._operand(buf)
                operands.append(operand)

    @staticmethod
    def _is_operator(b):
        if 0 <= b <= 21:
            return True
        elif 28 <= b <= 30 or 32 <= b <= 254:
            return False
        else:
            raise

    @staticmethod
    def _operator(buf):
        b0, buf = ValUtil.ucharpop(buf)
        if b0 != 12:
            return b0, buf
        else:
            b1, buf = ValUtil.ucharpop(buf)
            return b0<<8|b1, buf

    @staticmethod
    def _operand(buf):
        b0, buf = ValUtil.ucharpop(buf)
        if b0 == 30: # real number
            s = ""
            def nibble_proc(s, nibble):
                if 0 <= nibble <= 9:
                    return s + str(nibble), 0
                elif nibble == 0xa:
                    return s + ".", 0
                elif nibble == 0xb:
                    return s + "E", 0
                elif nibble == 0xc:
                    return s + "E-", 0
                elif nibble == 0xe:
                    return "-" + s, 0
                elif nibble2 == 0xf:
                    return s, 1
                else:
                    raise

            while True:
                b, buf = ValUtil.ucharpop(buf)
                nibble1, nibble2 = b>>4, b&0xf
                s, end = nibble_proc(s, nibble1)
                s, end = nibble_proc(s, nibble2)
                if end:
                    return float(s), buf
        else: # integer
            if 32 <= b0 <= 246:
                return b0-139, buf
            else:
                b1, buf   = ValUtil.ucharpop(buf)
                if 247 <= b0 <= 250:
                    return  (b0-247)*256+b1+108, buf
                elif 251 <= b0 <= 254:
                    return -(b0-251)*256-b1-108, buf
                else:
                    b2, buf   = ValUtil.ucharpop(buf)
                    if b0 == 28:
                        return b1<<8|b2, buf
                    elif b0 == 29:
                        b3, buf   = ValUtil.ucharpop(buf)
                        b4, buf   = ValUtil.ucharpop(buf)
                        return b1<<24|b2<<16|b3<<8|b4, buf
                    else:
                        raise


# 5176.CFF.pdf  5 INDEX Data (p.12)
class CffINDEXData(object):
    def __init__(self, buf, name):
        self.name  = name
        self.count = 0
        self.data  = None
        self.buf   = self.parse(buf)

    def parse(self, buf):
        self.count, buf   = ValUtil.ushortpop(buf)
        if self.count != 0:
            self.offSize, buf = CFFData.OffSize(buf)
            self.offset = []
            for i in range(self.count + 1):
                val, buf = CFFData.Offset(buf, self.offSize)
                self.offset.append(val)
            self.data = []
            for i in range(1, self.count + 1):
                length = self.offset[i]-self.offset[i-1]
                data, buf = buf[:length], buf[length:]
                self.data.append(data)
        return buf

    def show(self):
        print("  [CffINDEXData(%s)]" % (self.name))
        print("    count   = %d" % (self.count))
        if self.count != 0:
            print("    offSize = %d" % (self.offSize))
            print("    offset  = {0}".format(", ".join([str(val) for val in self.offset])))

class NameIndex(CffINDEXData):
    def __init__(self, buf):
        super(NameIndex, self).__init__(buf, "Name")

    def parse(self, buf):
        return super(NameIndex, self).parse(buf)

    def show(self):
        super(NameIndex, self).show()

        if self.count != 0:
            print("    data    = {0}".format(", ".join(self.data)))

class TopDictIndex(CffINDEXData):
    def __init__(self, buf):
        self.cffDict = []
        super(TopDictIndex, self).__init__(buf, "Top DICT")

    def parse(self, buf):
        buf = super(TopDictIndex, self).parse(buf)
        self.cffDict = [CffDictData(data) for data in self.data]
        return buf

    def show(self, stringIndex = None):
        super(TopDictIndex, self).show()

        if self.count != 0:
            for cffDict in self.cffDict:
                print("    -----")
                for k,v in cffDict.items():
                    if stringIndex is None:
                        print("    {0} = {1}".format(TopDictOp.to_s(k), v))
                    else:
                        if k == TopDictOp.version or k == TopDictOp.Notice or k == TopDictOp.Copyright \
                           or k == TopDictOp.FullName or k == TopDictOp.FamilyName or k == TopDictOp.Weight \
                           or k == TopDictOp.PostScript or k == TopDictOp.BaseFontName or k == TopDictOp.FontName:
                            print("    {0} = {1} << {2} >>".format(TopDictOp.to_s(k), v, stringIndex.data[v[0] - SID.nStdStrings]))
                        elif k == TopDictOp.ROS:
                            print("    {0} = {1} << {2}-{3}-{4} >>".format(TopDictOp.to_s(k), v,
                                stringIndex.data[v[0] - SID.nStdStrings], stringIndex.data[v[1] - SID.nStdStrings], v[2]))
                        else:
                            print("    {0} = {1}".format(TopDictOp.to_s(k), v))

class TopDictOp(object):
    version            = 0
    Notice             = 1
    Copyright          = 12<<8|0
    FullName           = 2
    FamilyName         = 3
    Weight             = 4
    isFixedPitch       = 12<<8|1
    ItalicAngle        = 12<<8|2
    UnderlinePosition  = 12<<8|3
    UnderlineThickness = 12<<8|4
    PaintType          = 12<<8|5
    CharstringType     = 12<<8|6
    FontMatrix         = 12<<8|7
    UniqueID           = 13
    FontBBox           = 5
    StrokeWidth        = 12<<8|8
    XUID               = 14
    charset            = 15
    Encoding           = 16
    CharStrings        = 17
    Private            = 18
    SyntheticBase      = 12<<8|20
    PostScript         = 12<<8|21
    BaseFontName       = 12<<8|22
    BaseFontBlend      = 12<<8|23
    ROS                = 12<<8|30
    CIDFontVersion     = 12<<8|31
    CIDFontRevision    = 12<<8|32
    CIDFontType        = 12<<8|33
    CIDCount           = 12<<8|34
    UIDBase            = 12<<8|35
    FDArray            = 12<<8|36
    FDSelect           = 12<<8|37
    FontName           = 12<<8|38

    @classmethod
    def to_s(cls, op):
        if op == cls.version:
            return "version"
        elif op == cls.Notice:
            return "Notice"
        elif op == cls.Copyright:
            return "Copyright"
        elif op == cls.FullName:
            return "FullName"
        elif op == cls.FamilyName:
            return "FamilyName"
        elif op == cls.Weight:
            return "Weight"
        elif op == cls.isFixedPitch:
            return "isFixedPitch"
        elif op == cls.ItalicAngle:
            return "ItalicAngle"
        elif op == cls.UnderlinePosition:
            return "UnderlinePosition"
        elif op == cls.UnderlineThickness:
            return "UnderlineThickness"
        elif op == cls.PaintType:
            return "PaintType"
        elif op == cls.CharstringType:
            return "CharstringType"
        elif op == cls.FontMatrix:
            return "FontMatrix"
        elif op == cls.UniqueID:
            return "UniqueID"
        elif op == cls.FontBBox:
            return "FontBBox"
        elif op == cls.StrokeWidth:
            return "StrokeWidth"
        elif op == cls.XUID:
            return "XUID"
        elif op == cls.charset:
            return "charset"
        elif op == cls.Encoding:
            return "Encoding"
        elif op == cls.CharStrings:
            return "CharStrings"
        elif op == cls.Private:
            return "Private"
        elif op == cls.SyntheticBase:
            return "SyntheticBase"
        elif op == cls.PostScript:
            return "PostScript"
        elif op == cls.BaseFontName:
            return "BaseFontName"
        elif op == cls.BaseFontBlend:
            return "BaseFontBlend"
        elif op == cls.ROS:
            return "ROS"
        elif op == cls.CIDFontVersion:
            return "CIDFontVersion"
        elif op == cls.CIDFontRevision:
            return "CIDFontRevision"
        elif op == cls.CIDFontType:
            return "CIDFontType"
        elif op == cls.CIDCount:
            return "CIDCount"
        elif op == cls.UIDBase:
            return "UIDBase"
        elif op == cls.FDArray:
            return "FDArray"
        elif op == cls.FDSelect:
            return "FDSelect"
        elif op == cls.FontName:
            return "FontName"
        else:
            return "unknown"

# CFF
##################################################
# GPOS

# https://www.microsoft.com/typography/otspec/gpos.htm
# http://partners.adobe.com/public/developer/opentype/index_table_formats2.html
class GposTable(Table):
    def __init__(self, buf, tag):
        super(GposTable, self).__init__(buf, tag)

    def parse(self, buf):
        super(GposTable, self).parse(buf)

        self.header     = GposHeader(buf)
        self.scriptList = ScriptList(buf[self.header.ScriptList:])

    def show(self):
        print("[Table(%s)]" % (self.tag))
        self.header.show()
        self.scriptList.show()

class GposHeader(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.Version, buf     = OTData.Fixed(buf)
        self.ScriptList, buf  = OTData.Offset(buf)
        self.FeatureList, buf = OTData.Offset(buf)
        self.LookupList, buf  = OTData.Offset(buf)
        return buf

    def show(self):
        print("  [GposHeader]")
        print("    Version     = 0x%08x" % (self.Version))
        print("    ScriptList  = %d" % (self.ScriptList))
        print("    FeatureList = %d" % (self.FeatureList))
        print("    LookupList  = %d" % (self.LookupList))

# https://www.microsoft.com/typography/otspec/chapter2.htm
# http://partners.adobe.com/public/developer/opentype/index_table_formats.html
class ScriptList(object):
    def __init__(self, buf):
        self.buf_head = buf
        self.parse(buf)

    def parse(self, buf):
        self.ScriptCount, buf = ValUtil.ushortpop(buf)
        self.ScriptRecord = []
        for i in range(self.ScriptCount):
            record = ScriptRecord(buf, self.buf_head)
            buf = record.buf
            self.ScriptRecord.append(record)

    def show(self):
        print("  [ScriptList]")
        print("    ScriptCount = %d" % (self.ScriptCount))
        for record in self.ScriptRecord:
            record.show()

class ScriptRecord(object):
    def __init__(self, buf, scriptListHead = None):
        self.buf = self.parse(buf, scriptListHead)

    def parse(self, buf, scriptListHead = None):
        self.ScriptTag, buf = OTData.Tag(buf)
        self.Script, buf    = OTData.Offset(buf)
        self.ScriptTable     = None
        if scriptListHead:
            self.ScriptTable = ScriptTable(scriptListHead[self.Script:])
        return buf

    def show(self):
        print("    [ScriptRecord]")
        print("      ScriptTag = %s" % (self.ScriptTag))
        print("      Script    = %d" % (self.Script))
        if self.ScriptTable:
            self.ScriptTable.show()

class ScriptTable(object):
    def __init__(self, buf):
        self.buf_head = buf
        self.parse(buf)

    def parse(self, buf):
        self.DefaultLangSys, buf = OTData.Offset(buf)
        self.LangSysCount, buf   = ValUtil.ushortpop(buf)
        self.DefaultLangSysTable  = None
        if not OTData.isNullOffset(self.DefaultLangSys):
            self.DefaultLangSysTable = LangSysTable(self.buf_head[self.DefaultLangSys:])
        self.LangSysTable = []
        for i in range(self.LangSysCount):
            langSysTable = LangSysRecord(buf, self.buf_head)
            buf = langSysTable.buf
            self.LangSysTable.append(langSysTable)
        return buf

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
    def __init__(self, buf, scriptTableHead = None):
        self.buf = self.parse(buf, scriptTableHead)

    def parse(self, buf, scriptTableHead):
        self.LangSysTag, buf = OTData.Tag(buf)
        self.LangSys, buf    = OTData.Offset(buf)
        self.LangSysTable = None
        if scriptTableHead:
            self.LangSysTable = LangSysTable(scriptTableHead[self.LangSys:])
        return buf

    def show(self):
        print("        [LangSysRecord]")
        print("          LangSysTag = %s" % (self.LangSysTag))
        print("          LangSys    = %d" % (self.LangSys))
        if self.LangSysTable:
            self.LangSysTable.show()

class LangSysTable(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.LookupOrder, buf     = OTData.Offset(buf)
        self.ReqFeatureIndex, buf = ValUtil.ushortpop(buf)
        self.FeatureCount, buf    = ValUtil.ushortpop(buf)
        self.FeatureIndex = []
        for i in range(self.FeatureCount):
            index, buf = ValUtil.ushortpop(buf)
            self.FeatureIndex.append(index)
        return buf

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
    def __init__(self, buf, tag):
        super(GsubTable, self).__init__(buf, tag)

    def parse(self, buf):
        super(GsubTable, self).parse(buf)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("%s" % (self.buf))

# GSUB
##################################################

## TTF has a loca table
class LocaTable(Table):
    def __init__(self, buf, tag):
        super(LocaTable, self).__init__(buf, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, buf):
        super(LocaTable, self).parse(buf)

##################################################

## TTF has a glyp table
class GlypTable(Table):
    def __init__(self, buf, tag):
        super(GlypTable, self).__init__(buf, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, buf):
        super(GlypTable, self).parse(buf)

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
            bin_buf = infile.read(12)
            self.__header = Header(bin_buf)
            num_tables = self.__header.get_num_tables()
            for i in range(num_tables):
                bin_buf = infile.read(16)
                self.__table_record.append( TableRecord(bin_buf) )

            for table_record in self.__table_record:
                self.__create_table(table_record, infile)

    ## get table corresponding to given TableRecord
    def __create_table(self, table_record, infile):
        offset = table_record.get_offset()
        length = table_record.get_length()
        infile.seek(offset, os.SEEK_SET)
        buf = infile.read(length)
        tag = table_record.get_tag()

        if tag.lower() == "cff ":
            self.__table.append( CffTable(buf, tag) )
        elif tag.lower() == "loca":
            self.__table.append( LocaTable(buf, tag) )
        elif tag.lower() == "glyp":
            self.__table.append( GlypTable(buf, tag) )
        elif tag.lower() == "gpos":
            self.__table.append( GposTable(buf, tag) )
        elif tag.lower() == "gsub":
            self.__table.append( GsubTable(buf, tag) )
        elif tag.lower() == "head":
            self.__table.append( HeadTable(buf, tag) )
        elif tag.lower() == "name":
            self.__table.append( NameTable(buf, tag) )
        else:
            self.__table.append( Table(buf, tag) )


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
