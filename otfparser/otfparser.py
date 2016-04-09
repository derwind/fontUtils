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


## utility of LongDateTime
class LongDateTime(object):
    @staticmethod
    def to_date_str(value):
        d = datetime.datetime(1904, 1, 1)
        d += datetime.timedelta(seconds = value) #+ datetime.timedelta(hours = 9)
        return "%u/%02u/%02u %02u:%02u:%02u" % (d.year, d.month, d.day, d.hour, d.minute, d.second)

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
        print("  num_tables    =%u" % (self.__num_tables))
        print("  search_range  =%u" % (self.__search_range))
        print("  entry_selector=%u" % (self.__entry_selector))
        print("  range_shift   =%u" % (self.__range_shift))

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
        print("  tag           =%c%c%c%c" % (chr(self.__tag >> 24 & 0xff), chr(self.__tag >> 16 & 0xff), chr(self.__tag >> 8 & 0xff),chr(self.__tag & 0xff)))
        print("  check_sum     =0x%0x" % (self.__check_sum))
        print("  offset        =%u" % (self.__offset))
        print("  length        =%u" % (self.__length))

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

## http://www.microsoft.com/typography/otspec/cff.htm
## http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5177.Type2.pdf
## OOps...
class CffTable(Table):
    def __init__(self, data, tag):
        super(CffTable, self).__init__(data, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("%s" % (self.data))

    def parse(self, data):
        super(CffTable, self).parse(data)

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
        self.created, data = ValUtil.ulonglongpop(data)
        self.modified, data = ValUtil.ulonglongpop(data)
        self.xmin, data = ValUtil.sshortpop(data)
        self.ymin, data = ValUtil.sshortpop(data)
        self.xmax, data = ValUtil.sshortpop(data)
        self.ymax, data = ValUtil.sshortpop(data)
        self.mac_style, data = ValUtil.ushortpop(data)
        self.lowest_rec_ppem, data = ValUtil.ushortpop(data)
        self.font_direction_hint, data = ValUtil.sshortpop(data)
        self.index_to_loc_format, data = ValUtil.sshortpop(data)
        self.glyph_data_format, data = ValUtil.sshortpop(data)


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
        if storage is not None:
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
        if storage is not None:
            s = storage[self.offset:self.offset+self.length]
            print("    Lang-tag = %s" % (s))

class NameTable(Table):
    def __init__(self, data, tag):
        super(NameTable, self).__init__(data, tag)

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

## TTF has a loca table
class LocaTable(Table):
    def __init__(self, data, tag):
        super(LocaTable, self).__init__(data, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, data):
        super(LocaTable, self).parse(data)

## TTF has a glyp table
class GlypTable(Table):
    def __init__(self, data, tag):
        super(GlypTable, self).__init__(data, tag)

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  abbreviated...")

    def parse(self, data):
        super(GlypTable, self).parse(data)

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
        if tag.lower() == "head":
            self.__table.append( HeadTable(data, tag) )
        elif tag.lower() == "cff":
            self.__table.append( CffTable(data, tag) )
        elif tag.lower() == "name":
            self.__table.append( NameTable(data, tag) )
        elif tag.lower() == "loca":
            self.__table.append( LocaTable(data, tag) )
        elif tag.lower() == "glyp":
            self.__table.append( GlypTable(data, tag) )
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
