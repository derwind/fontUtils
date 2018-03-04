#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "maxpTable.h"
#include "bufferReader.h"

#define SAFE_FREE(x) if (x) { free(x); }

MaxpTable* MaxpTable_create(const Tag* tag)
{
	if ( !tag ) {
		return NULL;
	}

	MaxpTable* maxpTable = (MaxpTable*)malloc(sizeof(MaxpTable));
	memset(maxpTable, 0, sizeof(MaxpTable));

	Table_create(&maxpTable->table_, tag, (TABLE_DELETE)MaxpTable_delete, (TABLE_PARSE)MaxpTable_parse, (TABLE_SHOW)MaxpTable_show);

	return maxpTable;
}

void MaxpTable_delete(MaxpTable* maxpTable)
{
	SAFE_FREE(maxpTable);
}

int MaxpTable_parse(MaxpTable* maxpTable, unsigned char* buf, unsigned bufSize)
{
	BufferReader* reader = BufferReader_create(buf, bufSize);
	int result = 0;

	maxpTable->version_ = BufferReader_readUint32(reader);
	maxpTable->numGlyphs_ = BufferReader_readUint16(reader);
	if ( maxpTable->version_ < 0x00010000 ) {
		goto end_proc;
	}

	maxpTable->maxPoints_ = BufferReader_readUint16(reader);
	maxpTable->maxContours_ = BufferReader_readUint16(reader);
	maxpTable->maxCompositePoints_ = BufferReader_readUint16(reader);
	maxpTable->maxCompositeContours_ = BufferReader_readUint16(reader);
	maxpTable->maxZones_ = BufferReader_readUint16(reader);
	maxpTable->maxTwilightPoints_ = BufferReader_readUint16(reader);
	maxpTable->maxStorage_ = BufferReader_readUint16(reader);
	maxpTable->maxFunctionDefs_ = BufferReader_readUint16(reader);
	maxpTable->maxInstructionDefs_ = BufferReader_readUint16(reader);
	maxpTable->maxStackElements_ = BufferReader_readUint16(reader);
	maxpTable->maxSizeOfInstructions_ = BufferReader_readUint16(reader);
	maxpTable->maxComponentElements_ = BufferReader_readUint16(reader);
	maxpTable->maxComponentDepth_ = BufferReader_readUint16(reader);

 end_proc:
	BufferReader_delete(reader);

	return result;
}

void MaxpTable_show(const MaxpTable* maxpTable)
{
	printf("[Table(%s)]\n", Tag_str(maxpTable->table_.tag_));
	printf("  version   = 0x%08x\n", maxpTable->version_);
	printf("  numGlyphs = %d\n", maxpTable->numGlyphs_);
	if ( maxpTable->version_ < 0x00010000 ) {
		return;
	}
	printf("  maxPoints             = %d\n", maxpTable->maxPoints_);
	printf("  maxContours           = %d\n", maxpTable->maxContours_);
	printf("  maxCompositePoints    = %d\n", maxpTable->maxCompositePoints_);
	printf("  maxCompositeContours  = %d\n", maxpTable->maxCompositeContours_);
	printf("  maxZones              = %d\n", maxpTable->maxZones_);
	printf("  maxTwilightPoints     = %d\n", maxpTable->maxTwilightPoints_);
	printf("  maxStorage            = %d\n", maxpTable->maxStorage_);
	printf("  maxFunctionDefs       = %d\n", maxpTable->maxFunctionDefs_);
	printf("  maxInstructionDefs    = %d\n", maxpTable->maxInstructionDefs_);
	printf("  maxStackElements      = %d\n", maxpTable->maxStackElements_);
	printf("  maxSizeOfInstructions = %d\n", maxpTable->maxSizeOfInstructions_);
	printf("  maxComponentElements  = %d\n", maxpTable->maxComponentElements_);
	printf("  maxComponentDepth     = %d\n", maxpTable->maxComponentDepth_);
}
