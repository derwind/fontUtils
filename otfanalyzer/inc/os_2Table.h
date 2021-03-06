#ifndef OS_2_TABLE_H
#define OS_2_TABLE_H

#include "table.h"

// https://www.microsoft.com/typography/otspec/os2.htm
class OS_2Table : public Table {
 public:
	OS_2Table(const Tag* tag);
	virtual ~OS_2Table();

	virtual int parse(unsigned char* buf, unsigned bufSize);

	virtual void show();

 private:
	uint16_t version_;
	int16_t xAvgCharWidth_;
	uint16_t usWeightClass_;
	uint16_t usWidthClass_;
	uint16_t fsType_;
	int16_t ySubscriptXSize_;
	int16_t ySubscriptYSize_;
	int16_t ySubscriptXOffset_;
	int16_t ySubscriptYOffset_;
	int16_t ySuperscriptXSize_;
	int16_t ySuperscriptYSize_;
	int16_t ySuperscriptXOffset_;
	int16_t ySuperscriptYOffset_;
	int16_t yStrikeoutSize_;
	int16_t yStrikeoutPosition_;
	int16_t sFamilyClass_;
	uint8_t panose_[10];
	uint32_t ulUnicodeRange1_;
	uint32_t ulUnicodeRange2_;
	uint32_t ulUnicodeRange3_;
	uint32_t ulUnicodeRange4_;
	char achVendID_[4+1];
	uint16_t fsSelection_;
	uint16_t usFirstCharIndex_;
	uint16_t usLastCharIndex_;
	int16_t sTypoAscender_;
	int16_t sTypoDescender_;
	int16_t sTypoLineGap_;
	uint16_t usWinAscent_;
	uint16_t usWinDescent_;
	uint32_t ulCodePageRange1_;
	uint32_t ulCodePageRange2_;
	int16_t sxHeight_;
	int16_t sCapHeight_;
	uint16_t usDefaultChar_;
	uint16_t usBreakChar_;
	uint16_t usMaxContext_;
	uint16_t usLowerOpticalPointSize_;
	uint16_t usUpperOpticalPointSize_;
};

#endif /* OS_2_TABLE_H */
