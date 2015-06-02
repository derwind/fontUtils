#! /usr/bin/env python
# -*- coding: utf-8 -*-

# http://www.microsoft.com/typography/otspec/otff.htm

import sys
#import struct

class MyError(Exception) :
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return repr(self.__value)

def ushort(data) :
    return data[0] << 8 | data[1]

def ulong(data) :
    return data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3]

class TTCHeader :
    def __init__(self, data) :
        self.__parse(data)

    def show(self) :
        print("[TTCHeader]")
        print("  num_tables   =%d" % (self.__num_tables))
        print("  search_range =%d" % (self.__search_range))
        print("  entry_selecto=%d" % (self.__entry_selector))
        print("  range_shift  =%d" % (self.__range_shift))

    def __parse(self, data) :
        if data[0] != ord('O') or data[1] != ord('T') or data[2] != ord('T') or data[3] != ord('O') :
            raise MyError("invalid header")

        data = data[4:]
        self.__num_tables     = ushort(data)
        data = data[2:]
        self.__search_range   = ushort(data)
        data = data[2:]
        self.__entry_selector = ushort(data)
        data = data[2:]
        self.__range_shift    = ushort(data)

class TableRecord :
    def __init__(self, data) :
        self.__parse(data)

    def show(self) :
        print("[TableRecord]")
        print("  tag       =%c%c%c%c" % (chr(self.__tag >> 24 & 0xff), chr(self.__tag >> 16 & 0xff), chr(self.__tag >> 8 & 0xff),chr(self.__tag & 0xff)))
        print("  check_sum =0x%0x" % (self.__check_sum))
        print("  offset    =%d" % (self.__offset))
        print("  length    =%d" % (self.__length))

    def __parse(self, data) :
        self.__tag       = ulong(data)
        data = data[4:]
        self.__check_sum = ulong(data)
        data = data[4:]
        self.__offset    = ulong(data)
        data = data[4:]
        self.__length    = ulong(data)

class OtfParser :
    def __init__(self) :
        self.__ttc_header = None
        self.__table_record = None

    def parse(self, file) :
        self.__parse(file)

    def show(self) :
        self.__ttc_header.show()
        self.__table_record.show()

    def __parse(self, file) :
        print("---> " + file)
        with open(file, "rb") as infile :
            bin_data = infile.read(12)
            self.__ttc_header = TTCHeader(bin_data)
            bin_data = infile.read(16)
            self.__table_record = TableRecord(bin_data)


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
