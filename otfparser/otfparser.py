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
        return ValUtil.signed(n)

    @staticmethod
    def scharpop(buf):
        return ValUtil.schar(buf), buf[1:]

    @staticmethod
    def signed(n, bit = 8):
        if 7 <= bit <= 8:
            sign = (n >> 7) & 0x1
            if sign == 0:
                return n
            else:
                return -((~n & 0x7f) + 1)
        elif 15 <= bit <= 16:
            sign = (n >> 15) & 0x1
            if sign == 0:
                return n
            else:
                return -((~n & 0x7fff) + 1)
        elif 23 <= bit <= 24:
            sign = (n >> 23) & 0x1
            if sign == 0:
                return n
            else:
                return -((~n & 0x7fffff) + 1)
        elif 31 <= bit <= 32:
            sign = (n >> 31) & 0x1
            if sign == 0:
                return n
            else:
                return -((~n & 0x7fffffff) + 1)
        else:
            raise

    @staticmethod
    def chars(buf, n):
        global py_ver
        if py_ver == 2:
            return [ ValUtil.signed(ord(buf[i])) for i in range(n) ]
        else:
            return [ ValUtil.signed(buf[i]) for i in range(n) ]

    @staticmethod
    def charspop(buf, n):
        return ValUtil.chars(buf, n), buf[n:]

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
    def bytes(buf, n):
        global py_ver
        if py_ver == 2:
            return [ ord(buf[i]) for i in range(n) ]
        else:
            return [ buf[i] for i in range(n) ]

    @staticmethod
    def bytespop(buf, n):
        return ValUtil.bytes(buf, n), buf[n:]

    @staticmethod
    def sshort(buf):
        global py_ver
        n = ValUtil.ushort(buf)
        return ValUtil.signed(n, 16)

    @staticmethod
    def sshortpop(buf):
        return ValUtil.sshort(buf), buf[2:]

    @staticmethod
    def sshorts(buf, n):
        global py_ver
        if py_ver == 2:
            return [ ValUtil.signed(ord(buf[i*2]) << 8 | ord(buf[i*2+1]), 16) for i in range(n) ]
        else:
            return [ ValUtil.signed(buf[i*2] << 8 | buf[i*2+1], 16) for i in range(n) ]

    @staticmethod
    def sshortspop(buf, n):
        return ValUtil.sshorts(buf, n), buf[2*n:]

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

    @staticmethod
    def ushorts(buf, n):
        global py_ver
        if py_ver == 2:
            return [ ord(buf[i*2]) << 8 | ord(buf[i*2+1]) for i in range(n) ]
        else:
            return [ buf[i*2] << 8 | buf[i*2+1] for i in range(n) ]

    @staticmethod
    def ushortspop(buf, n):
        return ValUtil.ushorts(buf, n), buf[2*n:]

    def sint24(buf):
        global py_ver
        n = ValUtil.uint24(buf)
        return ValUtil.signed(n, 24)

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
        return ValUtil.signed(n, 32)

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

## utility of LongDateTime
class LongDateTime(object):
    @staticmethod
    def to_date_str(value):
        d = datetime.datetime(1904, 1, 1)
        d += datetime.timedelta(seconds = value) #+ datetime.timedelta(hours = 9)
        return "%u/%02u/%02u %02u:%02u:%02u" % (d.year, d.month, d.day, d.hour, d.minute, d.second)

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

# 5176.CFF.pdf  Appendix A Standard Strings
class StdStr(object):
    _notdef             = 0
    space               = 1
    exclam              = 2
    quotedbl            = 3
    numbersign          = 4
    dollar              = 5
    percent             = 6
    ampersand           = 7
    quoteright          = 8
    parenleft           = 9
    parenright          = 10
    asterisk            = 11
    plus                = 12
    comma               = 13
    hyphen              = 14
    period              = 15
    slash               = 16
    zero                = 17
    one                 = 18
    two                 = 19
    three               = 20
    four                = 21
    five                = 22
    six                 = 23
    seven               = 24
    eight               = 25
    nine                = 26
    colon               = 27
    semicolon           = 28
    less                = 29
    equal               = 30
    greater             = 31
    question            = 32
    at                  = 33
    A                   = 34
    B                   = 35
    C                   = 36
    D                   = 37
    E                   = 38
    F                   = 39
    G                   = 40
    H                   = 41
    I                   = 42
    J                   = 43
    K                   = 44
    L                   = 45
    M                   = 46
    N                   = 47
    O                   = 48
    P                   = 49
    Q                   = 50
    R                   = 51
    S                   = 52
    T                   = 53
    U                   = 54
    V                   = 55
    W                   = 56
    X                   = 57
    Y                   = 58
    Z                   = 59
    bracketleft         = 60
    backslash           = 61
    bracketright        = 62
    asciicircum         = 63
    underscore          = 64
    quoteleft           = 65
    a                   = 66
    b                   = 67
    c                   = 68
    d                   = 69
    e                   = 70
    f                   = 71
    g                   = 72
    h                   = 73
    i                   = 74
    j                   = 75
    k                   = 76
    l                   = 77
    m                   = 78
    n                   = 79
    o                   = 80
    p                   = 81
    q                   = 82
    r                   = 83
    s                   = 84
    t                   = 85
    u                   = 86
    v                   = 87
    w                   = 88
    x                   = 89
    y                   = 90
    z                   = 91
    braceleft           = 92
    bar                 = 93
    braceright          = 94
    asciitilde          = 95
    exclamdown          = 96
    cent                = 97
    sterling            = 98
    fraction            = 99
    yen                 = 100
    florin              = 101
    section             = 102
    currency            = 103
    quotesingle         = 104
    quotedblleft        = 105
    guillemotleft       = 106
    guilsinglleft       = 107
    guilsinglright      = 108
    fi                  = 109
    fl                  = 110
    endash              = 111
    dagger              = 112
    daggerdbl           = 113
    periodcentered      = 114
    paragraph           = 115
    bullet              = 116
    quotesinglbase      = 117
    quotedblbase        = 118
    quotedblright       = 119
    guillemotright      = 120
    ellipsis            = 121
    perthousand         = 122
    questiondown        = 123
    grave               = 124
    acute               = 125
    circumflex          = 126
    tilde               = 127
    macron              = 128
    breve               = 129
    dotaccent           = 130
    dieresis            = 131
    ring                = 132
    cedilla             = 133
    hungarumlaut        = 134
    ogonek              = 135
    caron               = 136
    emdash              = 137
    AE                  = 138
    ordfeminine         = 139
    Lslash              = 140
    Oslash              = 141
    OE                  = 142
    ordmasculine        = 143
    ae                  = 144
    dotlessi            = 145
    lslash              = 146
    oslash              = 147
    oe                  = 148
    germandbls          = 149
    onesuperior         = 150
    logicalnot          = 151
    mu                  = 152
    trademark           = 153
    Eth                 = 154
    onehalf             = 155
    plusminus           = 156
    Thorn               = 157
    onequarter          = 158
    divide              = 159
    brokenbar           = 160
    degree              = 161
    thorn               = 162
    threequarters       = 163
    twosuperior         = 164
    registered          = 165
    minus               = 166
    eth                 = 167
    multiply            = 168
    threesuperior       = 169
    copyright           = 170
    Aacute              = 171
    Acircumflex         = 172
    Adieresis           = 173
    Agrave              = 174
    Aring               = 175
    Atilde              = 176
    Ccedilla            = 177
    Eacute              = 178
    Ecircumflex         = 179
    Edieresis           = 180
    Egrave              = 181
    Iacute              = 182
    Icircumflex         = 183
    Idieresis           = 184
    Igrave              = 185
    Ntilde              = 186
    Oacute              = 187
    Ocircumflex         = 188
    Odieresis           = 189
    Ograve              = 190
    Otilde              = 191
    Scaron              = 192
    Uacute              = 193
    Ucircumflex         = 194
    Udieresis           = 195
    Ugrave              = 196
    Yacute              = 197
    Ydieresis           = 198
    Zcaron              = 199
    aacute              = 200
    acircumflex         = 201
    adieresis           = 202
    agrave              = 203
    aring               = 204
    atilde              = 205
    ccedilla            = 206
    eacute              = 207
    ecircumflex         = 208
    edieresis           = 209
    egrave              = 210
    iacute              = 211
    icircumflex         = 212
    idieresis           = 213
    igrave              = 214
    ntilde              = 215
    oacute              = 216
    ocircumflex         = 217
    odieresis           = 218
    ograve              = 219
    otilde              = 220
    scaron              = 221
    uacute              = 222
    ucircumflex         = 223
    udieresis           = 224
    ugrave              = 225
    yacute              = 226
    ydieresis           = 227
    zcaron              = 228
    exclamsmall         = 229
    Hungarumlautsmall   = 230
    dollaroldstyle      = 231
    dollarsuperior      = 232
    ampersandsmall      = 233
    Acutesmall          = 234
    parenleftsuperior   = 235
    parenrightsuperior  = 236
    twodotenleader      = 237
    onedotenleader      = 238
    zerooldstyle        = 239
    oneoldstyle         = 240
    twooldstyle         = 241
    threeoldstyle       = 242
    fouroldstyle        = 243
    fiveoldstyle        = 244
    sixoldstyle         = 245
    sevenoldstyle       = 246
    eightoldstyle       = 247
    nineoldstyle        = 248
    commasuperior       = 249
    threequartersemdash = 250
    periodsuperior      = 251
    questionsmall       = 252
    asuperior           = 253
    bsuperior           = 254
    centsuperior        = 255
    dsuperior           = 256
    esuperior           = 257
    isuperior           = 258
    lsuperior           = 259
    msuperior           = 260
    nsuperior           = 261
    osuperior           = 262
    rsuperior           = 263
    ssuperior           = 264
    tsuperior           = 265
    ff                  = 266
    ffi                 = 267
    ffl                 = 268
    parenleftinferior   = 269
    parenrightinferior  = 270
    Circumflexsmall     = 271
    hyphensuperior      = 272
    Gravesmall          = 273
    Asmall              = 274
    Bsmall              = 275
    Csmall              = 276
    Dsmall              = 277
    Esmall              = 278
    Fsmall              = 279
    Gsmall              = 280
    Hsmall              = 281
    Ismall              = 282
    Jsmall              = 283
    Ksmall              = 284
    Lsmall              = 285
    Msmall              = 286
    Nsmall              = 287
    Osmall              = 288
    Psmall              = 289
    Qsmall              = 290
    Rsmall              = 291
    Ssmall              = 292
    Tsmall              = 293
    Usmall              = 294
    Vsmall              = 295
    Wsmall              = 296
    Xsmall              = 297
    Ysmall              = 298
    Zsmall              = 299
    colonmonetary       = 300
    onefitted           = 301
    rupiah              = 302
    Tildesmall          = 303
    exclamdownsmall     = 304
    centoldstyle        = 305
    Lslashsmall         = 306
    Scaronsmall         = 307
    Zcaronsmall         = 308
    Dieresissmall       = 309
    Brevesmall          = 310
    Caronsmall          = 311
    Dotaccentsmall      = 312
    Macronsmall         = 313
    figuredash          = 314
    hypheninferior      = 315
    Ogoneksmall         = 316
    Ringsmall           = 317
    Cedillasmall        = 318
    questiondownsmall   = 319
    oneeighth           = 320
    threeeighths        = 321
    fiveeighths         = 322
    seveneighths        = 323
    onethird            = 324
    twothirds           = 325
    zerosuperior        = 326
    foursuperior        = 327
    fivesuperior        = 328
    sixsuperior         = 329
    sevensuperior       = 330
    eightsuperior       = 331
    ninesuperior        = 332
    zeroinferior        = 333
    oneinferior         = 334
    twoinferior         = 335
    threeinferior       = 336
    fourinferior        = 337
    fiveinferior        = 338
    sixinferior         = 339
    seveninferior       = 340
    eightinferior       = 341
    nineinferior        = 342
    centinferior        = 343
    dollarinferior      = 344
    periodinferior      = 345
    commainferior       = 346
    Agravesmall         = 347
    Aacutesmall         = 348
    Acircumflexsmall    = 349
    Atildesmall         = 350
    Adieresissmall      = 351
    Aringsmall          = 352
    AEsmall             = 353
    Ccedillasmall       = 354
    Egravesmall         = 355
    Eacutesmall         = 356
    Ecircumflexsmall    = 357
    Edieresissmall      = 358
    Igravesmall         = 359
    Iacutesmall         = 360
    Icircumflexsmall    = 361
    Idieresissmall      = 362
    Ethsmall            = 363
    Ntildesmall         = 364
    Ogravesmall         = 365
    Oacutesmall         = 366
    Ocircumflexsmall    = 367
    Otildesmall         = 368
    Odieresissmall      = 369
    OEsmall             = 370
    Oslashsmall         = 371
    Ugravesmall         = 372
    Uacutesmall         = 373
    Ucircumflexsmall    = 374
    Udieresissmall      = 375
    Yacutesmall         = 376
    Thornsmall          = 377
    Ydieresissmall      = 378
    Black               = 383
    Bold                = 384
    Book                = 385
    Light               = 386
    Medium              = 387
    Regular             = 388
    Roman               = 389
    Semibold            = 390
    nStdStr             = 391

    @classmethod
    def to_s(cls, sid):
        if sid == cls._notdef:
            return ".notdef"
        elif sid == cls.space:
            return "space"
        elif sid == cls.exclam:
            return "exclam"
        elif sid == cls.quotedbl:
            return "quotedbl"
        elif sid == cls.numbersign:
            return "numbersign"
        elif sid == cls.dollar:
            return "dollar"
        elif sid == cls.percent:
            return "percent"
        elif sid == cls.ampersand:
            return "ampersand"
        elif sid == cls.quoteright:
            return "quoteright"
        elif sid == cls.parenleft:
            return "parenleft"
        elif sid == cls.parenright:
            return "parenright"
        elif sid == cls.asterisk:
            return "asterisk"
        elif sid == cls.plus:
            return "plus"
        elif sid == cls.comma:
            return "comma"
        elif sid == cls.hyphen:
            return "hyphen"
        elif sid == cls.period:
            return "period"
        elif sid == cls.slash:
            return "slash"
        elif sid == cls.zero:
            return "zero"
        elif sid == cls.one:
            return "one"
        elif sid == cls.two:
            return "two"
        elif sid == cls.three:
            return "three"
        elif sid == cls.four:
            return "four"
        elif sid == cls.five:
            return "five"
        elif sid == cls.six:
            return "six"
        elif sid == cls.seven:
            return "seven"
        elif sid == cls.eight:
            return "eight"
        elif sid == cls.nine:
            return "nine"
        elif sid == cls.colon:
            return "colon"
        elif sid == cls.semicolon:
            return "semicolon"
        elif sid == cls.less:
            return "less"
        elif sid == cls.equal:
            return "equal"
        elif sid == cls.greater:
            return "greater"
        elif sid == cls.question:
            return "question"
        elif sid == cls.at:
            return "at"
        elif sid == cls.A:
            return "A"
        elif sid == cls.B:
            return "B"
        elif sid == cls.C:
            return "C"
        elif sid == cls.D:
            return "D"
        elif sid == cls.E:
            return "E"
        elif sid == cls.F:
            return "F"
        elif sid == cls.G:
            return "G"
        elif sid == cls.H:
            return "H"
        elif sid == cls.I:
            return "I"
        elif sid == cls.J:
            return "J"
        elif sid == cls.K:
            return "K"
        elif sid == cls.L:
            return "L"
        elif sid == cls.M:
            return "M"
        elif sid == cls.N:
            return "N"
        elif sid == cls.O:
            return "O"
        elif sid == cls.P:
            return "P"
        elif sid == cls.Q:
            return "Q"
        elif sid == cls.R:
            return "R"
        elif sid == cls.S:
            return "S"
        elif sid == cls.T:
            return "T"
        elif sid == cls.U:
            return "U"
        elif sid == cls.V:
            return "V"
        elif sid == cls.W:
            return "W"
        elif sid == cls.X:
            return "X"
        elif sid == cls.Y:
            return "Y"
        elif sid == cls.Z:
            return "Z"
        elif sid == cls.bracketleft:
            return "bracketleft"
        elif sid == cls.backslash:
            return "backslash"
        elif sid == cls.bracketright:
            return "bracketright"
        elif sid == cls.asciicircum:
            return "asciicircum"
        elif sid == cls.underscore:
            return "underscore"
        elif sid == cls.quoteleft:
            return "quoteleft"
        elif sid == cls.a:
            return "a"
        elif sid == cls.b:
            return "b"
        elif sid == cls.c:
            return "c"
        elif sid == cls.d:
            return "d"
        elif sid == cls.e:
            return "e"
        elif sid == cls.f:
            return "f"
        elif sid == cls.g:
            return "g"
        elif sid == cls.h:
            return "h"
        elif sid == cls.i:
            return "i"
        elif sid == cls.j:
            return "j"
        elif sid == cls.k:
            return "k"
        elif sid == cls.l:
            return "l"
        elif sid == cls.m:
            return "m"
        elif sid == cls.n:
            return "n"
        elif sid == cls.o:
            return "o"
        elif sid == cls.p:
            return "p"
        elif sid == cls.q:
            return "q"
        elif sid == cls.r:
            return "r"
        elif sid == cls.s:
            return "s"
        elif sid == cls.t:
            return "t"
        elif sid == cls.u:
            return "u"
        elif sid == cls.v:
            return "v"
        elif sid == cls.w:
            return "w"
        elif sid == cls.x:
            return "x"
        elif sid == cls.y:
            return "y"
        elif sid == cls.z:
            return "z"
        elif sid == cls.braceleft:
            return "braceleft"
        elif sid == cls.bar:
            return "bar"
        elif sid == cls.braceright:
            return "braceright"
        elif sid == cls.asciitilde:
            return "asciitilde"
        elif sid == cls.exclamdown:
            return "exclamdown"
        elif sid == cls.cent:
            return "cent"
        elif sid == cls.sterling:
            return "sterling"
        elif sid == cls.fraction:
            return "fraction"
        elif sid == cls.yen:
            return "yen"
        elif sid == cls.florin:
            return "florin"
        elif sid == cls.section:
            return "section"
        elif sid == cls.currency:
            return "currency"
        elif sid == cls.quotesingle:
            return "quotesingle"
        elif sid == cls.quotedblleft:
            return "quotedblleft"
        elif sid == cls.guillemotleft:
            return "guillemotleft"
        elif sid == cls.guilsinglleft:
            return "guilsinglleft"
        elif sid == cls.guilsinglright:
            return "guilsinglright"
        elif sid == cls.fi:
            return "fi"
        elif sid == cls.fl:
            return "fl"
        elif sid == cls.endash:
            return "endash"
        elif sid == cls.dagger:
            return "dagger"
        elif sid == cls.daggerdbl:
            return "daggerdbl"
        elif sid == cls.periodcentered:
            return "periodcentered"
        elif sid == cls.paragraph:
            return "paragraph"
        elif sid == cls.bullet:
            return "bullet"
        elif sid == cls.quotesinglbase:
            return "quotesinglbase"
        elif sid == cls.quotedblbase:
            return "quotedblbase"
        elif sid == cls.quotedblright:
            return "quotedblright"
        elif sid == cls.guillemotright:
            return "guillemotright"
        elif sid == cls.ellipsis:
            return "ellipsis"
        elif sid == cls.perthousand:
            return "perthousand"
        elif sid == cls.questiondown:
            return "questiondown"
        elif sid == cls.grave:
            return "grave"
        elif sid == cls.acute:
            return "acute"
        elif sid == cls.circumflex:
            return "circumflex"
        elif sid == cls.tilde:
            return "tilde"
        elif sid == cls.macron:
            return "macron"
        elif sid == cls.breve:
            return "breve"
        elif sid == cls.dotaccent:
            return "dotaccent"
        elif sid == cls.dieresis:
            return "dieresis"
        elif sid == cls.ring:
            return "ring"
        elif sid == cls.cedilla:
            return "cedilla"
        elif sid == cls.hungarumlaut:
            return "hungarumlaut"
        elif sid == cls.ogonek:
            return "ogonek"
        elif sid == cls.caron:
            return "caron"
        elif sid == cls.emdash:
            return "emdash"
        elif sid == cls.AE:
            return "AE"
        elif sid == cls.ordfeminine:
            return "ordfeminine"
        elif sid == cls.Lslash:
            return "Lslash"
        elif sid == cls.Oslash:
            return "Oslash"
        elif sid == cls.OE:
            return "OE"
        elif sid == cls.ordmasculine:
            return "ordmasculine"
        elif sid == cls.ae:
            return "ae"
        elif sid == cls.dotlessi:
            return "dotlessi"
        elif sid == cls.lslash:
            return "lslash"
        elif sid == cls.oslash:
            return "oslash"
        elif sid == cls.oe:
            return "oe"
        elif sid == cls.germandbls:
            return "germandbls"
        elif sid == cls.onesuperior:
            return "onesuperior"
        elif sid == cls.logicalnot:
            return "logicalnot"
        elif sid == cls.mu:
            return "mu"
        elif sid == cls.trademark:
            return "trademark"
        elif sid == cls.Eth:
            return "Eth"
        elif sid == cls.onehalf:
            return "onehalf"
        elif sid == cls.plusminus:
            return "plusminus"
        elif sid == cls.Thorn:
            return "Thorn"
        elif sid == cls.onequarter:
            return "onequarter"
        elif sid == cls.divide:
            return "divide"
        elif sid == cls.brokenbar:
            return "brokenbar"
        elif sid == cls.degree:
            return "degree"
        elif sid == cls.thorn:
            return "thorn"
        elif sid == cls.threequarters:
            return "threequarters"
        elif sid == cls.twosuperior:
            return "twosuperior"
        elif sid == cls.registered:
            return "registered"
        elif sid == cls.minus:
            return "minus"
        elif sid == cls.eth:
            return "eth"
        elif sid == cls.multiply:
            return "multiply"
        elif sid == cls.threesuperior:
            return "threesuperior"
        elif sid == cls.copyright:
            return "copyright"
        elif sid == cls.Aacute:
            return "Aacute"
        elif sid == cls.Acircumflex:
            return "Acircumflex"
        elif sid == cls.Adieresis:
            return "Adieresis"
        elif sid == cls.Agrave:
            return "Agrave"
        elif sid == cls.Aring:
            return "Aring"
        elif sid == cls.Atilde:
            return "Atilde"
        elif sid == cls.Ccedilla:
            return "Ccedilla"
        elif sid == cls.Eacute:
            return "Eacute"
        elif sid == cls.Ecircumflex:
            return "Ecircumflex"
        elif sid == cls.Edieresis:
            return "Edieresis"
        elif sid == cls.Egrave:
            return "Egrave"
        elif sid == cls.Iacute:
            return "Iacute"
        elif sid == cls.Icircumflex:
            return "Icircumflex"
        elif sid == cls.Idieresis:
            return "Idieresis"
        elif sid == cls.Igrave:
            return "Igrave"
        elif sid == cls.Ntilde:
            return "Ntilde"
        elif sid == cls.Oacute:
            return "Oacute"
        elif sid == cls.Ocircumflex:
            return "Ocircumflex"
        elif sid == cls.Odieresis:
            return "Odieresis"
        elif sid == cls.Ograve:
            return "Ograve"
        elif sid == cls.Otilde:
            return "Otilde"
        elif sid == cls.Scaron:
            return "Scaron"
        elif sid == cls.Uacute:
            return "Uacute"
        elif sid == cls.Ucircumflex:
            return "Ucircumflex"
        elif sid == cls.Udieresis:
            return "Udieresis"
        elif sid == cls.Ugrave:
            return "Ugrave"
        elif sid == cls.Yacute:
            return "Yacute"
        elif sid == cls.Ydieresis:
            return "Ydieresis"
        elif sid == cls.Zcaron:
            return "Zcaron"
        elif sid == cls.aacute:
            return "aacute"
        elif sid == cls.acircumflex:
            return "acircumflex"
        elif sid == cls.adieresis:
            return "adieresis"
        elif sid == cls.agrave:
            return "agrave"
        elif sid == cls.aring:
            return "aring"
        elif sid == cls.atilde:
            return "atilde"
        elif sid == cls.ccedilla:
            return "ccedilla"
        elif sid == cls.eacute:
            return "eacute"
        elif sid == cls.ecircumflex:
            return "ecircumflex"
        elif sid == cls.edieresis:
            return "edieresis"
        elif sid == cls.egrave:
            return "egrave"
        elif sid == cls.iacute:
            return "iacute"
        elif sid == cls.icircumflex:
            return "icircumflex"
        elif sid == cls.idieresis:
            return "idieresis"
        elif sid == cls.igrave:
            return "igrave"
        elif sid == cls.ntilde:
            return "ntilde"
        elif sid == cls.oacute:
            return "oacute"
        elif sid == cls.ocircumflex:
            return "ocircumflex"
        elif sid == cls.odieresis:
            return "odieresis"
        elif sid == cls.ograve:
            return "ograve"
        elif sid == cls.otilde:
            return "otilde"
        elif sid == cls.scaron:
            return "scaron"
        elif sid == cls.uacute:
            return "uacute"
        elif sid == cls.ucircumflex:
            return "ucircumflex"
        elif sid == cls.udieresis:
            return "udieresis"
        elif sid == cls.ugrave:
            return "ugrave"
        elif sid == cls.yacute:
            return "yacute"
        elif sid == cls.ydieresis:
            return "ydieresis"
        elif sid == cls.zcaron:
            return "zcaron"
        elif sid == cls.exclamsmall:
            return "exclamsmall"
        elif sid == cls.Hungarumlautsmall:
            return "Hungarumlautsmall"
        elif sid == cls.dollaroldstyle:
            return "dollaroldstyle"
        elif sid == cls.dollarsuperior:
            return "dollarsuperior"
        elif sid == cls.ampersandsmall:
            return "ampersandsmall"
        elif sid == cls.Acutesmall:
            return "Acutesmall"
        elif sid == cls.parenleftsuperior:
            return "parenleftsuperior"
        elif sid == cls.parenrightsuperior:
            return "parenrightsuperior"
        elif sid == cls.twodotenleader:
            return "twodotenleader"
        elif sid == cls.onedotenleader:
            return "onedotenleader"
        elif sid == cls.zerooldstyle:
            return "zerooldstyle"
        elif sid == cls.oneoldstyle:
            return "oneoldstyle"
        elif sid == cls.twooldstyle:
            return "twooldstyle"
        elif sid == cls.threeoldstyle:
            return "threeoldstyle"
        elif sid == cls.fouroldstyle:
            return "fouroldstyle"
        elif sid == cls.fiveoldstyle:
            return "fiveoldstyle"
        elif sid == cls.sixoldstyle:
            return "sixoldstyle"
        elif sid == cls.sevenoldstyle:
            return "sevenoldstyle"
        elif sid == cls.eightoldstyle:
            return "eightoldstyle"
        elif sid == cls.nineoldstyle:
            return "nineoldstyle"
        elif sid == cls.commasuperior:
            return "commasuperior"
        elif sid == cls.threequartersemdash:
            return "threequartersemdash"
        elif sid == cls.periodsuperior:
            return "periodsuperior"
        elif sid == cls.questionsmall:
            return "questionsmall"
        elif sid == cls.asuperior:
            return "asuperior"
        elif sid == cls.bsuperior:
            return "bsuperior"
        elif sid == cls.centsuperior:
            return "centsuperior"
        elif sid == cls.dsuperior:
            return "dsuperior"
        elif sid == cls.esuperior:
            return "esuperior"
        elif sid == cls.isuperior:
            return "isuperior"
        elif sid == cls.lsuperior:
            return "lsuperior"
        elif sid == cls.msuperior:
            return "msuperior"
        elif sid == cls.nsuperior:
            return "nsuperior"
        elif sid == cls.osuperior:
            return "osuperior"
        elif sid == cls.rsuperior:
            return "rsuperior"
        elif sid == cls.ssuperior:
            return "ssuperior"
        elif sid == cls.tsuperior:
            return "tsuperior"
        elif sid == cls.ff:
            return "ff"
        elif sid == cls.ffi:
            return "ffi"
        elif sid == cls.ffl:
            return "ffl"
        elif sid == cls.parenleftinferior:
            return "parenleftinferior"
        elif sid == cls.parenrightinferior:
            return "parenrightinferior"
        elif sid == cls.Circumflexsmall:
            return "Circumflexsmall"
        elif sid == cls.hyphensuperior:
            return "hyphensuperior"
        elif sid == cls.Gravesmall:
            return "Gravesmall"
        elif sid == cls.Asmall:
            return "Asmall"
        elif sid == cls.Bsmall:
            return "Bsmall"
        elif sid == cls.Csmall:
            return "Csmall"
        elif sid == cls.Dsmall:
            return "Dsmall"
        elif sid == cls.Esmall:
            return "Esmall"
        elif sid == cls.Fsmall:
            return "Fsmall"
        elif sid == cls.Gsmall:
            return "Gsmall"
        elif sid == cls.Hsmall:
            return "Hsmall"
        elif sid == cls.Ismall:
            return "Ismall"
        elif sid == cls.Jsmall:
            return "Jsmall"
        elif sid == cls.Ksmall:
            return "Ksmall"
        elif sid == cls.Lsmall:
            return "Lsmall"
        elif sid == cls.Msmall:
            return "Msmall"
        elif sid == cls.Nsmall:
            return "Nsmall"
        elif sid == cls.Osmall:
            return "Osmall"
        elif sid == cls.Psmall:
            return "Psmall"
        elif sid == cls.Qsmall:
            return "Qsmall"
        elif sid == cls.Rsmall:
            return "Rsmall"
        elif sid == cls.Ssmall:
            return "Ssmall"
        elif sid == cls.Tsmall:
            return "Tsmall"
        elif sid == cls.Usmall:
            return "Usmall"
        elif sid == cls.Vsmall:
            return "Vsmall"
        elif sid == cls.Wsmall:
            return "Wsmall"
        elif sid == cls.Xsmall:
            return "Xsmall"
        elif sid == cls.Ysmall:
            return "Ysmall"
        elif sid == cls.Zsmall:
            return "Zsmall"
        elif sid == cls.colonmonetary:
            return "colonmonetary"
        elif sid == cls.onefitted:
            return "onefitted"
        elif sid == cls.rupiah:
            return "rupiah"
        elif sid == cls.Tildesmall:
            return "Tildesmall"
        elif sid == cls.exclamdownsmall:
            return "exclamdownsmall"
        elif sid == cls.centoldstyle:
            return "centoldstyle"
        elif sid == cls.Lslashsmall:
            return "Lslashsmall"
        elif sid == cls.Scaronsmall:
            return "Scaronsmall"
        elif sid == cls.Zcaronsmall:
            return "Zcaronsmall"
        elif sid == cls.Dieresissmall:
            return "Dieresissmall"
        elif sid == cls.Brevesmall:
            return "Brevesmall"
        elif sid == cls.Caronsmall:
            return "Caronsmall"
        elif sid == cls.Dotaccentsmall:
            return "Dotaccentsmall"
        elif sid == cls.Macronsmall:
            return "Macronsmall"
        elif sid == cls.figuredash:
            return "figuredash"
        elif sid == cls.hypheninferior:
            return "hypheninferior"
        elif sid == cls.Ogoneksmall:
            return "Ogoneksmall"
        elif sid == cls.Ringsmall:
            return "Ringsmall"
        elif sid == cls.Cedillasmall:
            return "Cedillasmall"
        elif sid == cls.questiondownsmall:
            return "questiondownsmall"
        elif sid == cls.oneeighth:
            return "oneeighth"
        elif sid == cls.threeeighths:
            return "threeeighths"
        elif sid == cls.fiveeighths:
            return "fiveeighths"
        elif sid == cls.seveneighths:
            return "seveneighths"
        elif sid == cls.onethird:
            return "onethird"
        elif sid == cls.twothirds:
            return "twothirds"
        elif sid == cls.zerosuperior:
            return "zerosuperior"
        elif sid == cls.foursuperior:
            return "foursuperior"
        elif sid == cls.fivesuperior:
            return "fivesuperior"
        elif sid == cls.sixsuperior:
            return "sixsuperior"
        elif sid == cls.sevensuperior:
            return "sevensuperior"
        elif sid == cls.eightsuperior:
            return "eightsuperior"
        elif sid == cls.ninesuperior:
            return "ninesuperior"
        elif sid == cls.zeroinferior:
            return "zeroinferior"
        elif sid == cls.oneinferior:
            return "oneinferior"
        elif sid == cls.twoinferior:
            return "twoinferior"
        elif sid == cls.threeinferior:
            return "threeinferior"
        elif sid == cls.fourinferior:
            return "fourinferior"
        elif sid == cls.fiveinferior:
            return "fiveinferior"
        elif sid == cls.sixinferior:
            return "sixinferior"
        elif sid == cls.seveninferior:
            return "seveninferior"
        elif sid == cls.eightinferior:
            return "eightinferior"
        elif sid == cls.nineinferior:
            return "nineinferior"
        elif sid == cls.centinferior:
            return "centinferior"
        elif sid == cls.dollarinferior:
            return "dollarinferior"
        elif sid == cls.periodinferior:
            return "periodinferior"
        elif sid == cls.commainferior:
            return "commainferior"
        elif sid == cls.Agravesmall:
            return "Agravesmall"
        elif sid == cls.Aacutesmall:
            return "Aacutesmall"
        elif sid == cls.Acircumflexsmall:
            return "Acircumflexsmall"
        elif sid == cls.Atildesmall:
            return "Atildesmall"
        elif sid == cls.Adieresissmall:
            return "Adieresissmall"
        elif sid == cls.Aringsmall:
            return "Aringsmall"
        elif sid == cls.AEsmall:
            return "AEsmall"
        elif sid == cls.Ccedillasmall:
            return "Ccedillasmall"
        elif sid == cls.Egravesmall:
            return "Egravesmall"
        elif sid == cls.Eacutesmall:
            return "Eacutesmall"
        elif sid == cls.Ecircumflexsmall:
            return "Ecircumflexsmall"
        elif sid == cls.Edieresissmall:
            return "Edieresissmall"
        elif sid == cls.Igravesmall:
            return "Igravesmall"
        elif sid == cls.Iacutesmall:
            return "Iacutesmall"
        elif sid == cls.Icircumflexsmall:
            return "Icircumflexsmall"
        elif sid == cls.Idieresissmall:
            return "Idieresissmall"
        elif sid == cls.Ethsmall:
            return "Ethsmall"
        elif sid == cls.Ntildesmall:
            return "Ntildesmall"
        elif sid == cls.Ogravesmall:
            return "Ogravesmall"
        elif sid == cls.Oacutesmall:
            return "Oacutesmall"
        elif sid == cls.Ocircumflexsmall:
            return "Ocircumflexsmall"
        elif sid == cls.Otildesmall:
            return "Otildesmall"
        elif sid == cls.Odieresissmall:
            return "Odieresissmall"
        elif sid == cls.OEsmall:
            return "OEsmall"
        elif sid == cls.Oslashsmall:
            return "Oslashsmall"
        elif sid == cls.Ugravesmall:
            return "Ugravesmall"
        elif sid == cls.Uacutesmall:
            return "Uacutesmall"
        elif sid == cls.Ucircumflexsmall:
            return "Ucircumflexsmall"
        elif sid == cls.Udieresissmall:
            return "Udieresissmall"
        elif sid == cls.Yacutesmall:
            return "Yacutesmall"
        elif sid == cls.Thornsmall:
            return "Thornsmall"
        elif sid == cls.Ydieresissmall:
            return "Ydieresissmall"
        elif sid == cls.Black:
            return "Black"
        elif sid == cls.Bold:
            return "Bold"
        elif sid == cls.Book:
            return "Book"
        elif sid == cls.Light:
            return "Light"
        elif sid == cls.Medium:
            return "Medium"
        elif sid == cls.Regular:
            return "Regular"
        elif sid == cls.Roman:
            return "Roman"
        elif sid == cls.Semibold:
            return "Semibold"
        else:
            return "unknown"

# 5177.Type2.pdf  Appendix A Type 2 Charstring Command Codes (p.31)
class Type2Op(object):
    hstem      = 1
    vstem      = 3
    vmoveto    = 4
    rlineto    = 5
    hlineto    = 6
    vlineto    = 7
    rrcurveto  = 8
    callsubr   = 10
    _return    = 11
    escape     = 12
    endchar    = 14
    hstemhm    = 18
    hintmask   = 19
    cntrmask   = 20
    rmoveto    = 21
    hmoveto    = 22
    vstemhm    = 23
    rcurveline = 24
    rlinecurve = 25
    vvcurveto  = 26
    hhcurveto  = 27
    shortint   = 28
    callgsubr  = 29
    vhcurveto  = 30
    hvcurveto  = 31
    _and       = 12<<8|3
    _or        = 12<<8|4
    _not       = 12<<8|5
    abs        = 12<<8|9
    add        = 12<<8|10
    sub        = 12<<8|11
    div        = 12<<8|12
    neg        = 12<<8|14
    eq         = 12<<8|15
    put        = 12<<8|20
    get        = 12<<8|21
    ifelse     = 12<<8|22
    random     = 12<<8|23
    mul        = 12<<8|24
    sqrt       = 12<<8|26
    dup        = 12<<8|27
    exch       = 12<<8|28
    index      = 12<<8|29
    roll       = 12<<8|30
    hflex      = 12<<8|34
    flex       = 12<<8|35
    hflex1     = 12<<8|36
    flex1      = 12<<8|37

    @classmethod
    def to_s(cls, op):
        if op == cls.hstem:
            return "hstem"
        elif op == cls.vstem:
            return "vstem"
        elif op == cls.vmoveto:
            return "vmoveto"
        elif op == cls.rlineto:
            return "rlineto"
        elif op == cls.hlineto:
            return "hlineto"
        elif op == cls.vlineto:
            return "vlineto"
        elif op == cls.rrcurveto:
            return "rrcurveto"
        elif op == cls.callsubr:
            return "callsubr"
        elif op == cls._return:
            return "return"
        elif op == cls.escape:
            return "escape"
        elif op == cls.endchar:
            return "endchar"
        elif op == cls.hstemhm:
            return "hstemhm"
        elif op == cls.hintmask:
            return "hintmask"
        elif op == cls.cntrmask:
            return "cntrmask"
        elif op == cls.rmoveto:
            return "rmoveto"
        elif op == cls.hmoveto:
            return "hmoveto"
        elif op == cls.vstemhm:
            return "vstemhm"
        elif op == cls.rcurveline:
            return "rcurveline"
        elif op == cls.rlinecurve:
            return "rlinecurve"
        elif op == cls.vvcurveto:
            return "vvcurveto"
        elif op == cls.hhcurveto:
            return "hhcurveto"
        elif op == cls.shortint:
            return "shortint"
        elif op == cls.callgsubr:
            return "callgsubr"
        elif op == cls.vhcurveto:
            return "vhcurveto"
        elif op == cls.hvcurveto:
            return "hvcurveto"
        elif op == cls._and:
            return "and"
        elif op == cls._or:
            return "or"
        elif op == cls._not:
            return "not"
        elif op == cls.abs:
            return "abs"
        elif op == cls.add:
            return "add"
        elif op == cls.sub:
            return "sub"
        elif op == cls.div:
            return "div"
        elif op == cls.neg:
            return "neg"
        elif op == cls.eq:
            return "eq"
        elif op == cls.put:
            return "put"
        elif op == cls.get:
            return "get"
        elif op == cls.ifelse:
            return "ifelse"
        elif op == cls.random:
            return "random"
        elif op == cls.mul:
            return "mul"
        elif op == cls.sqrt:
            return "sqrt"
        elif op == cls.dup:
            return "dup"
        elif op == cls.exch:
            return "exch"
        elif op == cls.index:
            return "index"
        elif op == cls.roll:
            return "roll"
        elif op == cls.hflex:
            return "hflex"
        elif op == cls.flex:
            return "flex"
        elif op == cls.hflex1:
            return "hflex1"
        elif op == cls.flex1:
            return "flex1"
        else:
            return "unknown"

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

##################################################
# cmap table

## https://www.microsoft.com/typography/otspec/cmap.htm
class CmapTable(Table):
    def __init__(self, buf, tag):
        super(CmapTable, self).__init__(buf, tag)

    def parse(self, buf, scriptListHead = None):
        self.buf_head       = buf # the top of the cmap table buffer
        self.version, buf   = ValUtil.ushortpop(buf)
        self.numTables, buf = ValUtil.ushortpop(buf)
        self.encodingTables = []
        for i in range(self.numTables):
            encodingTbl = CmapEncodingTable(buf)
            self.encodingTables.append(encodingTbl)
            buf = encodingTbl.buf
        self.subTables = []
        for i in range(self.numTables):
            subTbl = CmapSubTable(self.buf_head[self.encodingTables[i].offset:])
            self.subTables.append(subTbl)

        return buf

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  version       = %d" % (self.version))
        print("  numTables     = %d" % (self.numTables))
        for encodingTbl in self.encodingTables:
            encodingTbl.show()
        for subTbl in self.subTables:
            subTbl.show()

class CmapEncodingTable(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.platformID, buf = ValUtil.ushortpop(buf)
        self.encodingID, buf = ValUtil.ushortpop(buf)
        self.offset, buf     = ValUtil.ulongpop(buf)
        return buf

    def show(self):
        print("  [EncodingTable]")
        print("    platformID = %d" % (self.platformID))
        print("    encodingID = %d" % (self.encodingID))
        print("    offset     = %d" % (self.offset))

class CmapSubTable(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        format = ValUtil.ushort(buf)
        if format == 0:
            self.subtable = CmapSubTable0(buf)
        elif format == 2:
            self.subtable = CmapSubTable2(buf)
        elif format == 4:
            self.subtable = CmapSubTable4(buf)
        elif format == 14:
            self.subtable = CmapSubTable14(buf)
        else:
            raise MyError("currently not support")

        return self.subtable.buf

    def show(self):
        self.subtable.show()

class CmapSubTable0(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.format, buf       = ValUtil.ushortpop(buf)
        self.length, buf       = ValUtil.ushortpop(buf)
        self.language, buf     = ValUtil.ushortpop(buf)
        self.glyphIdArray, buf = ValUtil.bytespop(buf, 256)

        return buf

    def show(self):
        print("  [CmapSubTable0]")
        print("    format       = %d" % (self.format))
        print("    length       = %d" % (self.length))
        print("    language     = %d" % (self.language))
        print("    glyphIdArray = %d" % (self.glyphIdArray))

class CmapSubTable2(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.format, buf       = ValUtil.ushortpop(buf)
        self.length, buf       = ValUtil.ushortpop(buf)
        self.language, buf     = ValUtil.ushortpop(buf)

        return buf

    def show(self):
        print("  [CmapSubTable2]")
        print("    format       = %d" % (self.format))
        print("    length       = %d" % (self.length))
        print("    language     = %d" % (self.language))

class CmapSubTable4(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.format, buf        = ValUtil.ushortpop(buf)
        self.length, buf        = ValUtil.ushortpop(buf)
        self.language, buf      = ValUtil.ushortpop(buf)
        self.segCountX2, buf    = ValUtil.ushortpop(buf)
        self.searchRange, buf   = ValUtil.ushortpop(buf)
        self.entrySelector, buf = ValUtil.ushortpop(buf)
        self.rangeShift, buf    = ValUtil.ushortpop(buf)

        segCount = self.segCountX2 / 2

        self.endCount, buf      = ValUtil.ushortspop(buf, segCount)
        self.reservedPad, buf   = ValUtil.ushortpop(buf)
        self.startCount, buf    = ValUtil.ushortspop(buf, segCount)
        self.idDelta, buf       = ValUtil.sshortspop(buf, segCount)
        self.idRangeOffset, buf = ValUtil.ushortspop(buf, segCount)

        ramaining = self.length - 2*7 - self.segCountX2 - 2 - self.segCountX2*3

        self.glyphIdArray = []
        while ramaining > 0:
            gid, buf = ValUtil.ushortpop(buf)
            self.glyphIdArray.append(gid)
            ramaining -= 2

        return buf

    def show(self):
        print("  [CmapSubTable4]")
        print("    format        = %d" % (self.format))
        print("    length        = %d" % (self.length))
        print("    language      = %d" % (self.language))
        print("    segCountX2    = %d" % (self.segCountX2))
        print("    searchRange   = %d" % (self.searchRange))
        print("    entrySelector = %d" % (self.entrySelector))
        print("    rangeShift    = %d" % (self.rangeShift))
        print("    endCount      = {0}".format(self.endCount))
        print("    reservedPad   = %d" % (self.reservedPad))
        print("    startCount    = {0}".format(self.startCount))
        print("    idDelta       = {0}".format(self.idDelta))
        print("    idRangeOffset = {0}".format(self.idRangeOffset))
        print("    glyphIdArray  = {0}".format(self.glyphIdArray))

class CmapSubTable14(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.format, buf                = ValUtil.ushortpop(buf)
        self.length, buf                = ValUtil.ulongpop(buf)
        self.numVarSelectorRecords, buf = ValUtil.ulongpop(buf)

        return buf

    def show(self):
        print("  [CmapSubTable14]")
        print("    format                = %d" % (self.format))
        print("    length                = %d" % (self.length))
        print("    numVarSelectorRecords = %d" % (self.numVarSelectorRecords))

# cmap table
##################################################
# head table

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
        print("  glyph_buf_format     = %d" % (self.glyph_buf_format))

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

# head table
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
# OS/2 table

# https://www.microsoft.com/typography/otspec/os2.htm
class OS_2Table(Table):
    def __init__(self, buf, tag):
        super(OS_2Table, self).__init__(buf, tag)

    def parse(self, buf):
        super(OS_2Table, self).parse(buf)

        self.version, buf              = ValUtil.ushortpop(buf)
        self.xAvgCharWidth, buf        = ValUtil.sshortpop(buf)
        self.usWeightClass, buf        = ValUtil.ushortpop(buf)
        self.usWidthClass, buf         = ValUtil.ushortpop(buf)
        self.fsType, buf               = ValUtil.ushortpop(buf)
        self.ySubscriptXSize, buf      = ValUtil.sshortpop(buf)
        self.ySubscriptYSize, buf      = ValUtil.sshortpop(buf)
        self.ySubscriptXOffset, buf    = ValUtil.sshortpop(buf)
        self.ySubscriptYOffset, buf    = ValUtil.sshortpop(buf)
        self.ySuperscriptXSize, buf    = ValUtil.sshortpop(buf)
        self.ySuperscriptYSize, buf    = ValUtil.sshortpop(buf)
        self.ySuperscriptXOffset, buf  = ValUtil.sshortpop(buf)
        self.ySuperscriptYOffset, buf  = ValUtil.sshortpop(buf)
        self.yStrikeoutSize, buf       = ValUtil.sshortpop(buf)
        self.yStrikeoutPosition, buf   = ValUtil.sshortpop(buf)
        self.sFamilyClass, buf         = ValUtil.sshortpop(buf)
        self.panose, buf               = ValUtil.bytespop(buf, 10)
        self.ulUnicodeRange1, buf      = ValUtil.ulongpop(buf)
        self.ulUnicodeRange2, buf      = ValUtil.ulongpop(buf)
        self.ulUnicodeRange3, buf      = ValUtil.ulongpop(buf)
        self.ulUnicodeRange4, buf      = ValUtil.ulongpop(buf)
        self.achVendID, buf            = ValUtil.charspop(buf, 4)
        self.fsSelection, buf          = ValUtil.ushortpop(buf)
        self.usFirstCharIndex, buf     = ValUtil.ushortpop(buf)
        self.usLastCharIndex, buf      = ValUtil.ushortpop(buf)
        self.sTypoAscender, buf        = ValUtil.sshortpop(buf)
        self.sTypoDescender, buf       = ValUtil.sshortpop(buf)
        self.sTypoLineGap, buf         = ValUtil.sshortpop(buf)
        self.usWinAscent, buf          = ValUtil.ushortpop(buf)
        self.usWinDescent, buf         = ValUtil.ushortpop(buf)
        self.ulCodePageRange1, buf     = ValUtil.ulongpop(buf)
        self.ulCodePageRange2, buf     = ValUtil.ulongpop(buf)
        self.sxHeight, buf             = ValUtil.sshortpop(buf)
        self.sCapHeight, buf           = ValUtil.sshortpop(buf)
        self.usDefaultChar, buf        = ValUtil.ushortpop(buf)
        self.usBreakChar, buf          = ValUtil.ushortpop(buf)
        self.usMaxContext, buf         = ValUtil.ushortpop(buf)
        if self.version >= 5:
            self.usLowerOpticalPointSize, buf  = ValUtil.ushortpop(buf)
            self.usUpperOpticalPointSize, buf  = ValUtil.ushortpop(buf)

        return buf

    def show(self):
        print("[Table(%s)]" % (self.tag))
        print("  version             = %d" % (self.version))
        print("  xAvgCharWidth       = %d" % (self.xAvgCharWidth))
        print("  usWeightClass       = %d" % (self.usWeightClass))

        print("  usWidthClass        = %d" % (self.usWidthClass))
        print("  fsType              = %d" % (self.fsType))
        print("  ySubscriptXSize     = %d" % (self.ySubscriptXSize))
        print("  ySubscriptYSize     = %d" % (self.ySubscriptYSize))
        print("  ySubscriptXOffset   = %d" % (self.ySubscriptXOffset))
        print("  ySubscriptYOffset   = %d" % (self.ySubscriptYOffset))
        print("  ySuperscriptXSize   = %d" % (self.ySuperscriptXSize))
        print("  ySuperscriptYSize   = %d" % (self.ySuperscriptYSize))
        print("  ySuperscriptXOffset = %d" % (self.ySuperscriptXOffset))
        print("  ySuperscriptYOffset = %d" % (self.ySuperscriptYOffset))
        print("  yStrikeoutSize      = %d" % (self.yStrikeoutSize))
        print("  yStrikeoutPosition  = %d" % (self.yStrikeoutPosition))
        print("  panose              = {0}".format(self.panose))
        print("  ulUnicodeRange1     = 0x%08x" % (self.ulUnicodeRange1))
        print("  ulUnicodeRange2     = 0x%08x" % (self.ulUnicodeRange2))
        print("  ulUnicodeRange3     = 0x%08x" % (self.ulUnicodeRange3))
        print("  ulUnicodeRange4     = 0x%08x" % (self.ulUnicodeRange4))
        print("  achVendID           = %c%c%c%c" % (self.achVendID[0], self.achVendID[1], self.achVendID[2], self.achVendID[3]))
        print("  fsSelection         = %d" % (self.fsSelection))
        print("  usFirstCharIndex    = %d" % (self.usFirstCharIndex))
        print("  usLastCharIndex     = %d" % (self.usLastCharIndex))
        print("  sTypoAscender       = %d" % (self.sTypoAscender))
        print("  sTypoDescender      = %d" % (self.sTypoDescender))
        print("  sTypoLineGap        = %d" % (self.sTypoLineGap))
        print("  usWinAscent         = %d" % (self.usWinAscent))
        print("  usWinDescent        = %d" % (self.usWinDescent))
        print("  ulCodePageRange1    = 0x%08x" % (self.ulCodePageRange1))
        print("  ulCodePageRange2    = 0x%08x" % (self.ulCodePageRange2))
        print("  sxHeight            = %d" % (self.sxHeight))
        print("  sCapHeight          = %d" % (self.sCapHeight))
        print("  usDefaultChar       = %d" % (self.usDefaultChar))
        print("  usBreakChar         = %d" % (self.usBreakChar))
        print("  usMaxContext        = %d" % (self.usMaxContext))
        if self.version >= 5:
            print("  usLowerOpticalPointSize = %d" % (self.usLowerOpticalPointSize))
            print("  usUpperOpticalPointSize = %d" % (self.usUpperOpticalPointSize))

# OS/2 table
##################################################
# CFF

## http://www.microsoft.com/typography/otspec/cff.htm
## http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5176.CFF.pdf
## http://wwwimages.adobe.com/content/dam/Adobe/en/devnet/font/pdfs/5177.Type2.pdf
class CffTable(Table):
    def __init__(self, buf, tag):
        super(CffTable, self).__init__(buf, tag)

    def parse(self, buf):
        super(CffTable, self).parse(buf)

        # 5176.CFF.pdf  Table 1 CFF Data Layout (p.8)
        self.buf_head         = buf # the top of the CFF buffer
        self.header           = CffHeader(buf)
        buf = self.header.buf
        self.nameIndex        = NameIndex(buf)
        buf = self.nameIndex.buf
        self.topDictIndex     = TopDictIndex(buf)
        buf = self.topDictIndex.buf
        self.stringIndex      = CffINDEXData(buf, "String")
        buf = self.stringIndex.buf
        self.globalSubrIndex  = CffINDEXData(buf, "Global Subr")
        buf = self.globalSubrIndex.buf
        # XXX: currently support only one font, so directly use cffDict[0]
        cffDict = self.topDictIndex.cffDict[0]
        self.encodings        = None
        if TopDictOp.Encoding in cffDict:
            offset = cffDict[TopDictOp.Encoding][0]
            self.encodings    = CffEncodings(self.buf_head[offset:])
        self.charStringsIndex = None
        if TopDictOp.CharStrings in cffDict:
            offset = cffDict[TopDictOp.CharStrings][0]
            charstringType = cffDict[TopDictOp.CharstringType][0]
            self.charStringsIndex = CharStringsIndex(self.buf_head[offset:], charstringType)
        self.charsets         = None
        if TopDictOp.charset in cffDict:
            offset = cffDict[TopDictOp.charset][0]
            self.charsets     = CffCharsets(self.buf_head[offset:], self.charStringsIndex.count)
        self.FDSelect         = None

    def show(self):
        print("[Table(%s)]" % (self.tag))
        self.header.show()
        self.nameIndex.show()
        self.topDictIndex.show(self.stringIndex)
        self.stringIndex.show()
        self.globalSubrIndex.show()
        if self.encodings:
            self.encodings.show()
        if self.charStringsIndex:
            self.charStringsIndex.show()
        if self.charsets:
            self.charsets.show()

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
    def __init__(self, buf, defaultDict = {}):
        self._dict = defaultDict
        self.buf  = self.parse(buf)

    # like a dict
    def __setitem__(self, key, value):
        self._dict[key] = value
    def __getitem__(self, key):
        return self._dict[key]
    def __delitem__(self, key):
        del self._dict[key]
    def __iter__(self):
        return iter(self._dict)
    def __len__(self):
        return len(self._dict)
    def __contains__(self, item):
        return item in self._dict
    def __str__(self):
        return str(self._dict)
    def has_key(self, key):
        return self._dict.has_key(key)
    def items(self):
        return self._dict.items()

    def parse(self, buf):
        operands = []
        while len(buf) > 0:
            b = ValUtil.uchar(buf)
            if CffDictData._is_operator(b):
                operator, buf = CffDictData._operator(buf)
                # self.dict.append( (operator, operands) )
                self._dict[operator] = operands
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
            return CffDecorder.decodeInteger(buf, b0)

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
        self.cffDict = [CffDictData(data, TopDictIndex.gen_defaultDict()) for data in self.data]
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
                            s = stringIndex.data[v[0] - StdStr.nStdStr] if v[0] >= StdStr.nStdStr else StdStr.to_s(v[0])
                            print("    {0} = {1} << {2} >>".format(TopDictOp.to_s(k), v, s))
                        elif k == TopDictOp.ROS:
                            s0 = stringIndex.data[v[0] - StdStr.nStdStr] if v[0] >= StdStr.nStdStr else StdStr.to_s(v[0])
                            s1 = stringIndex.data[v[1] - StdStr.nStdStr] if v[1] >= StdStr.nStdStr else StdStr.to_s(v[1])
                            print("    {0} = {1} << {2}-{3}-{4} >>".format(TopDictOp.to_s(k), v, s0, s1, v[2]))
                        else:
                            print("    {0} = {1}".format(TopDictOp.to_s(k), v))

    @staticmethod
    def gen_defaultDict():
        return {
            TopDictOp.isFixedPitch:       [0],
            TopDictOp.ItalicAngle:        [0],
            TopDictOp.UnderlinePosition:  [-100],
            TopDictOp.UnderlineThickness: [50],
            TopDictOp.PaintType:          [0],
            TopDictOp.CharstringType:     [2],
            TopDictOp.FontMatrix:         [0.001, 0, 0, 0001, 0, 0],
            TopDictOp.FontBBox:           [0, 0, 0, 0],
            TopDictOp.StrokeWidth:        [0],
            TopDictOp.charset:            [0],
            TopDictOp.Encoding:           [0]
        }

class CffEncodings(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.format, buf = ValUtil.ucharpop(buf)
        if self.format == 0:
            self.nCodes, buf = ValUtil.ucharpop(buf)
            self.code = []
            for i in range(self.nCodes):
                code, buf = ValUtil.ucharpop(buf)
                self.code.append(code)
        elif self.format == 1:
            self.nRanges, buf = ValUtil.ucharpop(buf)
            self.Range1 = []
            for i in range(self.nRanges):
                ran1 = CffEncodingsRange1(buf)
                self.Range1.append(ran1)
                buf = ran1.buf
        else:
            #raise MyError("not supported format: {0}".format(self.format))
            self.nSups = self.format
            self.Supplement = []
            for i in range(self.nSups):
                sup = CffEncodingsSupplement(buf)
                self.Supplement.append(sup)
                buf = sup.buf

        return buf

    def show(self):
        print("  [Encodings]")
        if self.format == 0:
            print("    format  = %d" % (self.format))
            print("    nCodes  = %d" % (self.nCodes))
            print("    code    = {0}".format(self.code))
        elif self.format == 1:
            print("    format  = %d" % (self.format))
            print("    nRanges = %d" % (self.nRanges))
            print("    Range1  = {0}".format([(r.first, r.nLeft) for r in self.Range1]))
        else:
            print("    nSups      = %d" % (self.nSups))
            print("    Supplement = {0}".format([(s.code, s.glyph) for s in self.Supplement]))

class CffEncodingsRange1(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.first, buf = ValUtil.ucharpop(buf)
        self.nLeft, buf = ValUtil.ucharpop(buf)
        return buf

class CffEncodingsSupplement(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.code, buf  = ValUtil.ucharpop(buf)
        self.glyph, buf = ValUtil.ushortpop(buf)
        return buf

# 5176.CFF.pdf  14 CharStrings INDEX (p.23)
class CharStringsIndex(CffINDEXData):
    def __init__(self, buf, charstringType):
        self.charstringType = charstringType
        if self.charstringType != 2:
            raise MyError("currently not support CharstringType which is not 2")
        super(CharStringsIndex, self).__init__(buf, "CharStrings")

    def parse(self, buf):
        buf = super(CharStringsIndex, self).parse(buf)
        self.glyphs = [ Type2Charstring(d) for d in self.data ]
        return buf

    def show(self, stringIndex = None):
        super(CharStringsIndex, self).show()

        for g in self.glyphs:
            print("    -----")
            g.show()

# 5177.Type2.pdf  3.1 Type 2 Charstring Organization (p.10)
class Type2Charstring(object):
    def __init__(self, buf):
        self.cmds = []
        self.buf  = self.parse(buf)

    # w? {hs* vs* cm* hm* mt subpath}? {mt subpath}* endchar
    def parse(self, buf):
        args = []
        while len(buf) > 0:
            b, buf = ValUtil.ucharpop(buf)
            # Table 1 Type 2 Charstring Encoding Values (p.13)
            if 0<= b <= 11: # operators
                self.cmds.append( (b, args) )
                args = []
            elif b == 12: # escape: next byte interpreted as additional operators
                additional, buf = ValUtil.ucharpop(buf)
                op = 12<<8|additional
                self.cmds.append( (op, args) )
                args = []
            elif 13 <= b <= 18: # operators
                self.cmds.append( (b, args) )
                args = []
            elif 19 <= b <= 20: # operators (hintmask and cntrmask)
                # XXX: uhh...
                raise
            elif 21 <= b <= 27: # operators
                self.cmds.append( (b, args) )
                args = []
            elif b == 28: # following 2 bytes interpreted as a 16-bit two’s complement number
                v, buf = ValUtil.sshortpop(buf)
                args.append(v)
            elif 29 <= b <= 31: # operators
                self.cmds.append( (b, args) )
                args = []
            elif 32 <= b <= 254: # integers
                v, buf = CffDecorder.decodeInteger(buf, b)
                args.append(v)
            elif b == 255: # next 4 bytes interpreted as a 32-bit two’s-complement number
                v, buf = ValUtil.slongpop(buf)
                args.append(v)
            else:
                raise

    def show(self):
        for op, args in self.cmds:
            print "    ", args, "<< {0} >>".format(Type2Op.to_s(op))

# 5176.CFF.pdf  13 Charsets (p.21)
class CffCharsets(object):
    def __init__(self, buf, nGlyphs):
        self.nGlyphs = nGlyphs
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.format, buf = ValUtil.ucharpop(buf)
        if self.format == 0:
            self.glyph = []
            # the. notdef glyph name is omitted.
            for i in range(self.nGlyphs-1):
                g, buf = ValUtil.ushortpop(buf)
                self.glyph.append(g)
        elif self.format == 1:
            self.Range1 = []
            for i in range(self.nGlyphs-1):
                ran1 = CffCharsetsRange1(buf)
                self.Range1.append(ran1)
                buf = ran1.buf
        elif self.format == 2:
            self.Range2 = []
            for i in range(self.nGlyphs-1):
                ran2 = CffCharsetsRange2(buf)
                self.Range2.append(ran2)
                buf = ran2.buf
        else:
            raise

        return buf

    def show(self):
        print("  [Charsets]")
        if self.format == 0:
            print("    format  = %d" % (self.format))
            print("    glyph    = {0}".format(self.glyph))
        elif self.format == 1:
            print("    format  = %d" % (self.format))
            print("    Range1  = {0}".format([(r.first, r.nLeft) for r in self.Range1]))
        elif self.format == 2:
            print("    format  = %d" % (self.format))
            print("    Range2  = {0}".format([(r.first, r.nLeft) for r in self.Range2]))
        else:
            raise

class CffCharsetsRange1(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.first, buf = ValUtil.ushortpop(buf)
        self.nLeft, buf = ValUtil.ucharpop(buf)
        return buf

class CffCharsetsRange2(object):
    def __init__(self, buf):
        self.buf = self.parse(buf)

    def parse(self, buf):
        self.first, buf = ValUtil.ushortpop(buf)
        self.nLeft, buf = ValUtil.ushortpop(buf)
        return buf

class CffDecorder(object):
    @staticmethod
    def decodeInteger(buf, b0 = None):
        if b0 is None:
            b0, buf = ValUtil.ucharpop(buf)
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
        elif tag.lower() == "cmap":
            self.__table.append( CmapTable(buf, tag) )
        elif tag.lower() == "head":
            self.__table.append( HeadTable(buf, tag) )
        elif tag.lower() == "name":
            self.__table.append( NameTable(buf, tag) )
        elif tag.lower() == "os/2":
            self.__table.append( OS_2Table(buf, tag) )
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
