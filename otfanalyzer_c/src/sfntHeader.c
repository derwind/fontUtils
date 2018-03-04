#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "sfntHeader.h"
#include "bufferReader.h"

#define SAFE_FREE(x) if (x) { free(x); }

const int SfntHeader_SIZE = 12;

SfntHeader* SfntHeader_create(void)
{
	SfntHeader* sfntHeader = (SfntHeader*)malloc(sizeof(SfntHeader));
	memset(sfntHeader, 0, sizeof(SfntHeader));

	return sfntHeader;
}

void SfntHeader_delete(SfntHeader* sfntHeader)
{
	SAFE_FREE(sfntHeader);
}

int SfntHeader_parse(SfntHeader* sfntHeader, unsigned char* buf, unsigned bufSize)
{
	BufferReader* reader = BufferReader_create(buf, bufSize);
	int result = 0;

	uint32_t sfntVersion = BufferReader_readUint32(reader);
	if ( sfntVersion != 0x4F54544F ) {
		result = -1;
		goto end_proc;
	}

	sfntHeader->num_tables_ = BufferReader_readUint16(reader);
	sfntHeader->search_range_ = BufferReader_readUint16(reader);
	sfntHeader->entry_selector_ = BufferReader_readUint16(reader);
	sfntHeader->range_shift_ = BufferReader_readUint16(reader);

 end_proc:
	BufferReader_delete(reader);

	return result;
}

uint16_t SfntHeader_get_num_tables(const SfntHeader* sfntHeader)
{
	return sfntHeader->num_tables_;
}

void SfntHeader_show(const SfntHeader* sfntHeader)
{
	printf("[sfntHeader]\n");
	printf("  num_tables    = %u\n", sfntHeader->num_tables_);
	printf("  search_range  = %u\n", sfntHeader->search_range_);
	printf("  entry_selector= %u\n", sfntHeader->entry_selector_);
	printf("  range_shift   = %u\n", sfntHeader->range_shift_);
}
