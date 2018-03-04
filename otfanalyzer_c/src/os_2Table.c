#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "os_2Table.h"
#include "bufferReader.h"

#define SAFE_FREE(x) if (x) { free(x); }

OS_2Table* OS_2Table_create(const Tag* tag)
{
	if ( !tag ) {
		return NULL;
	}

	OS_2Table* os_2Table = (OS_2Table*)malloc(sizeof(OS_2Table));
	memset(os_2Table, 0, sizeof(OS_2Table));

	Table_create(&os_2Table->table_, tag, (TABLE_DELETE)OS_2Table_delete, (TABLE_PARSE)OS_2Table_parse, (TABLE_SHOW)OS_2Table_show);

	return os_2Table;
}

void OS_2Table_delete(OS_2Table* os_2Table)
{
	SAFE_FREE(os_2Table);
}

int OS_2Table_parse(OS_2Table* os_2Table, unsigned char* buf, unsigned bufSize)
{
	BufferReader* reader = BufferReader_create(buf, bufSize);

	os_2Table->version_ = BufferReader_readUint16(reader);
	os_2Table->xAvgCharWidth_ = BufferReader_readInt16(reader);
	os_2Table->usWeightClass_ = BufferReader_readUint16(reader);
	os_2Table->usWidthClass_ = BufferReader_readUint16(reader);
	os_2Table->fsType_ = BufferReader_readUint16(reader);
	os_2Table->ySubscriptXSize_ = BufferReader_readInt16(reader);
	os_2Table->ySubscriptYSize_ = BufferReader_readInt16(reader);
	os_2Table->ySubscriptXOffset_ = BufferReader_readInt16(reader);
	os_2Table->ySubscriptYOffset_ = BufferReader_readInt16(reader);
	os_2Table->ySuperscriptXSize_ = BufferReader_readInt16(reader);
	os_2Table->ySuperscriptYSize_ = BufferReader_readInt16(reader);
	os_2Table->ySuperscriptXOffset_ = BufferReader_readInt16(reader);
	os_2Table->ySuperscriptYOffset_ = BufferReader_readInt16(reader);
	os_2Table->yStrikeoutSize_ = BufferReader_readInt16(reader);
	os_2Table->yStrikeoutPosition_ = BufferReader_readInt16(reader);
	os_2Table->sFamilyClass_ = BufferReader_readInt16(reader);
	BufferReader_readUint8s(reader, os_2Table->panose_, 10);
	os_2Table->ulUnicodeRange1_ = BufferReader_readUint32(reader);
	os_2Table->ulUnicodeRange2_ = BufferReader_readUint32(reader);
	os_2Table->ulUnicodeRange3_ = BufferReader_readUint32(reader);
	os_2Table->ulUnicodeRange4_ = BufferReader_readUint32(reader);
	BufferReader_readTag(reader, os_2Table->achVendID_);
	os_2Table->fsSelection_ = BufferReader_readUint16(reader);
	os_2Table->usFirstCharIndex_ = BufferReader_readUint16(reader);
	os_2Table->usLastCharIndex_ = BufferReader_readUint16(reader);
	os_2Table->sTypoAscender_ = BufferReader_readInt16(reader);
	os_2Table->sTypoDescender_ = BufferReader_readInt16(reader);
	os_2Table->sTypoLineGap_ = BufferReader_readInt16(reader);
	os_2Table->usWinAscent_ = BufferReader_readUint16(reader);
	os_2Table->usWinDescent_ = BufferReader_readUint16(reader);
	os_2Table->ulCodePageRange1_ = BufferReader_readUint32(reader);
	os_2Table->ulCodePageRange2_ = BufferReader_readUint32(reader);
	os_2Table->sxHeight_ = BufferReader_readInt16(reader);
	os_2Table->sCapHeight_ = BufferReader_readInt16(reader);
	os_2Table->usDefaultChar_ = BufferReader_readUint16(reader);
	os_2Table->usBreakChar_ = BufferReader_readUint16(reader);
	os_2Table->usMaxContext_ = BufferReader_readUint16(reader);
	if ( os_2Table->version_ < 5 ) {
		return 0;
	}

	os_2Table->usLowerOpticalPointSize_ = BufferReader_readUint16(reader);
	os_2Table->usUpperOpticalPointSize_ = BufferReader_readUint16(reader);

	return 0;
}

void OS_2Table_show(const OS_2Table* os_2Table)
{
	printf("[Table(%s)]\n", Tag_str(os_2Table->table_.tag_));

	printf("  version             = %d\n", os_2Table->version_);
	printf("  xAvgCharWidth       = %d\n", os_2Table->xAvgCharWidth_);
	printf("  usWeightClass       = %d\n", os_2Table->usWeightClass_);
	printf("  usWidthClass        = %d\n", os_2Table->usWidthClass_);
	printf("  fsType              = %d\n", os_2Table->fsType_);
	printf("  ySubscriptXSize     = %d\n", os_2Table->ySubscriptXSize_);
	printf("  ySubscriptYSize     = %d\n", os_2Table->ySubscriptYSize_);
	printf("  ySubscriptXOffset   = %d\n", os_2Table->ySubscriptXOffset_);
	printf("  ySubscriptYOffset   = %d\n", os_2Table->ySubscriptYOffset_);
	printf("  ySuperscriptXSize   = %d\n", os_2Table->ySuperscriptXSize_);
	printf("  ySuperscriptYSize   = %d\n", os_2Table->ySuperscriptYSize_);
	printf("  ySuperscriptXOffset = %d\n", os_2Table->ySuperscriptXOffset_);
	printf("  ySuperscriptYOffset = %d\n", os_2Table->ySuperscriptYOffset_);
	printf("  yStrikeoutSize      = %d\n", os_2Table->yStrikeoutSize_);
	printf("  yStrikeoutPosition  = %d\n", os_2Table->yStrikeoutPosition_);
	printf("  sFamilyClass        = %d\n", os_2Table->sFamilyClass_);
	printf("  panose              = %d %d %d %d %d %d %d %d %d %d\n", os_2Table->panose_[0], os_2Table->panose_[1], os_2Table->panose_[2], os_2Table->panose_[3], os_2Table->panose_[4], os_2Table->panose_[5], os_2Table->panose_[6], os_2Table->panose_[7], os_2Table->panose_[8], os_2Table->panose_[9]);
	printf("  ulUnicodeRange1     = 0x%08x\n", os_2Table->ulUnicodeRange1_);
	printf("  ulUnicodeRange2     = 0x%08x\n", os_2Table->ulUnicodeRange2_);
	printf("  ulUnicodeRange3     = 0x%08x\n", os_2Table->ulUnicodeRange3_);
	printf("  ulUnicodeRange4     = 0x%08x\n", os_2Table->ulUnicodeRange4_);
	printf("  achVendID           = %s\n", os_2Table->achVendID_);
	printf("  fsSelection         = %d\n", os_2Table->fsSelection_);
	printf("  usFirstCharIndex    = %d\n", os_2Table->usFirstCharIndex_);
	printf("  usLastCharIndex     = %d\n", os_2Table->usLastCharIndex_);
	printf("  sTypoAscender       = %d\n", os_2Table->sTypoAscender_);
	printf("  sTypoDescender      = %d\n", os_2Table->sTypoDescender_);
	printf("  sTypoLineGap        = %d\n", os_2Table->sTypoLineGap_);
	printf("  usWinAscent         = %d\n", os_2Table->usWinAscent_);
	printf("  usWinDescent        = %d\n", os_2Table->usWinDescent_);
	printf("  ulCodePageRange1    = 0x%08x\n", os_2Table->ulCodePageRange1_);
	printf("  ulCodePageRange2    = 0x%08x\n", os_2Table->ulCodePageRange2_);
	printf("  sxHeight            = %d\n", os_2Table->sxHeight_);
	printf("  sCapHeight          = %d\n", os_2Table->sCapHeight_);
	printf("  usDefaultChar       = %d\n", os_2Table->usDefaultChar_);
	printf("  usBreakChar         = %d\n", os_2Table->usBreakChar_);
	printf("  usMaxContext        = %d\n", os_2Table->usMaxContext_);
	if ( os_2Table->version_ < 5 ) {
		return;
	}
	printf("  usLowerOpticalPointSize = %d\n", os_2Table->usLowerOpticalPointSize_);
	printf("  usUpperOpticalPointSize = %d\n", os_2Table->usUpperOpticalPointSize_);
}
