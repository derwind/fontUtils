#! /usr/bin/env python
# -*- coding: utf-8 -*-

# http://www.microsoft.com/typography/otspec/otff.htm

import os
import sys
#import struct


################################################################################

## custom exception class
class MyError(Exception) :
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

## utility of values
class ValUtil :
    @staticmethod
    def ushort(data) :
        return data[0] << 8 | data[1]

    @staticmethod
    def ulong(data) :
        return data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3]

## TTCHeader for OTF file
class TTCHeader :
    def __init__(self, data) :
        self.__parse(data)

    @classmethod
    def get_size(self) :
        return 12

    def get_num_tables(self) :
        return self.__num_tables

    def show(self) :
        print("[TTCHeader]")
        print("  num_tables    =%d" % (self.__num_tables))
        print("  search_range  =%d" % (self.__search_range))
        print("  entry_selector=%d" % (self.__entry_selector))
        print("  range_shift   =%d" % (self.__range_shift))

    def __parse(self, data) :
        if data[0] != ord('O') or data[1] != ord('T') or data[2] != ord('T') or data[3] != ord('O') :
            raise MyError("invalid header")

        data = data[4:]
        self.__num_tables     = ValUtil.ushort(data)
        data = data[2:]
        self.__search_range   = ValUtil.ushort(data)
        data = data[2:]
        self.__entry_selector = ValUtil.ushort(data)
        data = data[2:]
        self.__range_shift    = ValUtil.ushort(data)

## TableRecord for each table in OTF file
class TableRecord :
    def __init__(self, data) :
        self.__parse(data)

    @classmethod
    def get_size(self) :
        return 16

    def get_tag(self) :
        return "%c%c%c%c" % (chr(self.__tag >> 24 & 0xff), chr(self.__tag >> 16 & 0xff), chr(self.__tag >> 8 & 0xff),chr(self.__tag & 0xff))

    def get_check_sum(self) :
        return self.__check_sum

    def get_offset(self) :
        return self.__offset

    def get_length(self) :
        return self.__length

    def show(self) :
        print("[TableRecord]")
        print("  tag           =%c%c%c%c" % (chr(self.__tag >> 24 & 0xff), chr(self.__tag >> 16 & 0xff), chr(self.__tag >> 8 & 0xff),chr(self.__tag & 0xff)))
        print("  check_sum     =0x%0x" % (self.__check_sum))
        print("  offset        =%d" % (self.__offset))
        print("  length        =%d" % (self.__length))

    def __parse(self, data) :
        self.__tag       = ValUtil.ulong(data)
        data = data[4:]
        self.__check_sum = ValUtil.ulong(data)
        data = data[4:]
        self.__offset    = ValUtil.ulong(data)
        data = data[4:]
        self.__length    = ValUtil.ulong(data)

## Table in OTF file
class Table :
    def __init__(self, data, tag) :
        self.__tag = tag
        self.__parse(data)

    def show(self) :
        print("[Table(%s)]" % (self.__tag))
        if self.__tag == "name" :
            print("%s" % (self.__data))
        else :
            print("  abbreviated...")

    def __parse(self, data) :
        self.__data = data

## main class of otfparser
class OtfParser :
    def __init__(self) :
        self.__ttc_header = None
        self.__table_record = []
        self.__table        = []

    def parse(self, file) :
        self.__parse(file)

    def show(self) :
        self.__ttc_header.show()
        print("--------------------")
        i = 0
        for tbl_record in self.__table_record :
            tbl_record.show()
            tbl = self.__table[i].show()
            print("--------------------")
            i += 1

    def __parse(self, file) :
#       print("---> " + file)
        with open(file, "rb") as infile :
            bin_data = infile.read(12)
            self.__ttc_header = TTCHeader(bin_data)
            num_tables = self.__ttc_header.get_num_tables()
            for i in range(num_tables) :
               bin_data = infile.read(16)
               self.__table_record.append( TableRecord(bin_data) )

            for table_record in self.__table_record :
               self.__create_table(table_record, infile)

    ## get table corresponding to given TableRecord
    def __create_table(self, table_record, infile) :
        offset = table_record.get_offset()
        length = table_record.get_length()
        infile.seek(offset, os.SEEK_SET)
        data = infile.read(length)
        self.__table.append( Table(data, table_record.get_tag()) )


################################################################################

def help() :
    print( "[usage] %s INPUT_OTF" % (sys.argv[0]) )

if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        help()
        exit(1)

    parser = OtfParser()
    parser.parse(sys.argv[1])
    parser.show()
