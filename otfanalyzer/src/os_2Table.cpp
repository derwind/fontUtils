#include <cstdio>
#include <cstring>
#include "os_2Table.h"
#include "bufferReader.h"

OS_2Table::OS_2Table(const Tag* tag)
:
Table(tag),
version_(0),
xAvgCharWidth_(0),
usWeightClass_(0),
usWidthClass_(0),
fsType_(0),
ySubscriptXSize_(0),
ySubscriptYSize_(0),
ySubscriptXOffset_(0),
ySubscriptYOffset_(0),
ySuperscriptXSize_(0),
ySuperscriptYSize_(0),
ySuperscriptXOffset_(0),
ySuperscriptYOffset_(0),
yStrikeoutSize_(0),
yStrikeoutPosition_(0),
sFamilyClass_(0),
ulUnicodeRange1_(0),
ulUnicodeRange2_(0),
ulUnicodeRange3_(0),
ulUnicodeRange4_(0),
fsSelection_(0),
usFirstCharIndex_(0),
usLastCharIndex_(0),
sTypoAscender_(0),
sTypoDescender_(0),
sTypoLineGap_(0),
usWinAscent_(0),
usWinDescent_(0),
ulCodePageRange1_(0),
ulCodePageRange2_(0),
sxHeight_(0),
sCapHeight_(0),
usDefaultChar_(0),
usBreakChar_(0),
usMaxContext_(0),
usLowerOpticalPointSize_(0),
usUpperOpticalPointSize_(0)
{
	memset(panose_, 0, sizeof(panose_));
	memset(achVendID_, 0, sizeof(achVendID_));
}

OS_2Table::~OS_2Table()
{
}

int OS_2Table::parse(unsigned char* buf, unsigned bufSize)
{
	BufferReader reader(buf, bufSize);

	version_ = reader.readUint16();
	xAvgCharWidth_ = reader.readInt16();
	usWeightClass_ = reader.readUint16();
	usWidthClass_ = reader.readUint16();
	fsType_ = reader.readUint16();
	ySubscriptXSize_ = reader.readInt16();
	ySubscriptYSize_ = reader.readInt16();
	ySubscriptXOffset_ = reader.readInt16();
	ySubscriptYOffset_ = reader.readInt16();
	ySuperscriptXSize_ = reader.readInt16();
	ySuperscriptYSize_ = reader.readInt16();
	ySuperscriptXOffset_ = reader.readInt16();
	ySuperscriptYOffset_ = reader.readInt16();
	yStrikeoutSize_ = reader.readInt16();
	yStrikeoutPosition_ = reader.readInt16();
	sFamilyClass_ = reader.readInt16();
	reader.readUint8s(panose_, 10);
	ulUnicodeRange1_ = reader.readUint32();
	ulUnicodeRange2_ = reader.readUint32();
	ulUnicodeRange3_ = reader.readUint32();
	ulUnicodeRange4_ = reader.readUint32();
	reader.readTag(achVendID_);
	fsSelection_ = reader.readUint16();
	usFirstCharIndex_ = reader.readUint16();
	usLastCharIndex_ = reader.readUint16();
	sTypoAscender_ = reader.readInt16();
	sTypoDescender_ = reader.readInt16();
	sTypoLineGap_ = reader.readInt16();
	usWinAscent_ = reader.readUint16();
	usWinDescent_ = reader.readUint16();
	ulCodePageRange1_ = reader.readUint32();
	ulCodePageRange2_ = reader.readUint32();
	sxHeight_ = reader.readInt16();
	sCapHeight_ = reader.readInt16();
	usDefaultChar_ = reader.readUint16();
	usBreakChar_ = reader.readUint16();
	usMaxContext_ = reader.readUint16();
	if ( version_ < 5 ) {
		return 0;
	}

	usLowerOpticalPointSize_ = reader.readUint16();
	usUpperOpticalPointSize_ = reader.readUint16();

	return 0;
}

void OS_2Table::show()
{
	printf("[Table(%s)]\n", tag_->c_str());

	printf("  version             = %d\n", version_);
	printf("  xAvgCharWidth       = %d\n", xAvgCharWidth_);
	printf("  usWeightClass       = %d\n", usWeightClass_);
	printf("  usWidthClass        = %d\n", usWidthClass_);
	printf("  fsType              = %d\n", fsType_);
	printf("  ySubscriptXSize     = %d\n", ySubscriptXSize_);
	printf("  ySubscriptYSize     = %d\n", ySubscriptYSize_);
	printf("  ySubscriptXOffset   = %d\n", ySubscriptXOffset_);
	printf("  ySubscriptYOffset   = %d\n", ySubscriptYOffset_);
	printf("  ySuperscriptXSize   = %d\n", ySuperscriptXSize_);
	printf("  ySuperscriptYSize   = %d\n", ySuperscriptYSize_);
	printf("  ySuperscriptXOffset = %d\n", ySuperscriptXOffset_);
	printf("  ySuperscriptYOffset = %d\n", ySuperscriptYOffset_);
	printf("  yStrikeoutSize      = %d\n", yStrikeoutSize_);
	printf("  yStrikeoutPosition  = %d\n", yStrikeoutPosition_);
	printf("  sFamilyClass        = %d\n", sFamilyClass_);
	printf("  panose              = %d %d %d %d %d %d %d %d %d %d\n", panose_[0], panose_[1], panose_[2], panose_[3], panose_[4], panose_[5], panose_[6], panose_[7], panose_[8], panose_[9]);
	printf("  ulUnicodeRange1     = 0x%08x\n", ulUnicodeRange1_);
	printf("  ulUnicodeRange2     = 0x%08x\n", ulUnicodeRange2_);
	printf("  ulUnicodeRange3     = 0x%08x\n", ulUnicodeRange3_);
	printf("  ulUnicodeRange4     = 0x%08x\n", ulUnicodeRange4_);
	printf("  achVendID           = %s\n", achVendID_);
	printf("  fsSelection         = %d\n", fsSelection_);
	printf("  usFirstCharIndex    = %d\n", usFirstCharIndex_);
	printf("  usLastCharIndex     = %d\n", usLastCharIndex_);
	printf("  sTypoAscender       = %d\n", sTypoAscender_);
	printf("  sTypoDescender      = %d\n", sTypoDescender_);
	printf("  sTypoLineGap        = %d\n", sTypoLineGap_);
	printf("  usWinAscent         = %d\n", usWinAscent_);
	printf("  usWinDescent        = %d\n", usWinDescent_);
	printf("  ulCodePageRange1    = 0x%08x\n", ulCodePageRange1_);
	printf("  ulCodePageRange2    = 0x%08x\n", ulCodePageRange2_);
	printf("  sxHeight            = %d\n", sxHeight_);
	printf("  sCapHeight          = %d\n", sCapHeight_);
	printf("  usDefaultChar       = %d\n", usDefaultChar_);
	printf("  usBreakChar         = %d\n", usBreakChar_);
	printf("  usMaxContext        = %d\n", usMaxContext_);
	if ( version_ < 5 ) {
		return;
	}
	printf("  usLowerOpticalPointSize = %d\n", usLowerOpticalPointSize_);
	printf("  usUpperOpticalPointSize = %d\n", usUpperOpticalPointSize_);
}
