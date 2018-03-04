#ifndef MAXP_TABLE_H
#define MAXP_TABLE_H

#include "table.h"

// https://www.microsoft.com/typography/otspec/maxp.htm
class MaxpTable : public Table {
 public:
	MaxpTable(const Tag* tag);
	virtual ~MaxpTable();

	virtual int parse(unsigned char* buf, unsigned bufSize);

	virtual void show();

 private:
	uint32_t version_;
	uint16_t numGlyphs_;
	uint16_t maxPoints_;
	uint16_t maxContours_;
	uint16_t maxCompositePoints_;
	uint16_t maxCompositeContours_;
	uint16_t maxZones_;
	uint16_t maxTwilightPoints_;
	uint16_t maxStorage_;
	uint16_t maxFunctionDefs_;
	uint16_t maxInstructionDefs_;
	uint16_t maxStackElements_;
	uint16_t maxSizeOfInstructions_;
	uint16_t maxComponentElements_;
	uint16_t maxComponentDepth_;
};

#endif /* MAXP_TABLE_H */
