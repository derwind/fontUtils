#ifndef MAXP_TABLE_H
#define MAXP_TABLE_H

#include "table.h"

// https://www.microsoft.com/typography/otspec/maxp.htm
typedef struct MaxpTable {
	Table table_;

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
} MaxpTable;

MaxpTable* MaxpTable_create(const Tag* tag);
void MaxpTable_delete(MaxpTable* maxpTable);

int MaxpTable_parse(MaxpTable* maxpTable, unsigned char* buf, unsigned bufSize);

void MaxpTable_show(const MaxpTable* maxpTable);

#endif /* MAXP_TABLE_H */
