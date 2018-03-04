#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "tableRecord.h"
#include "tag.h"
//#include "table.h"
#include "bufferReader.h"

#define SAFE_FREE(x) if (x) { free(x); }

const unsigned TableRecord_SIZE = 16;

TableRecord* TableRecord_create(void)
{
	TableRecord* tableRecord = (TableRecord*)malloc(sizeof(TableRecord));
	memset(tableRecord, 0, sizeof(TableRecord));

	return tableRecord;
}

void TableRecord_delete(TableRecord* tableRecord)
{
	if ( !tableRecord ) {
		return;
	}

	SAFE_FREE(tableRecord->tag_);
	SAFE_FREE(tableRecord);
}

int TableRecord_parse(TableRecord* tableRecord, unsigned char* buf, unsigned bufSize)
{
	BufferReader* reader = BufferReader_create(buf, bufSize);

	tableRecord->tag_ = Tag_create(BufferReader_readUint32(reader));
	tableRecord->check_sum_ = BufferReader_readUint32(reader);
	tableRecord->offset_ = BufferReader_readUint32(reader);
	tableRecord->length_ = BufferReader_readUint32(reader);

	BufferReader_delete(reader);

	return 0;
}

const Tag* TableRecord_get_tag(const TableRecord* tableRecord)
{
	return tableRecord->tag_;
}

uint32_t TableRecord_get_offset(const TableRecord* tableRecord)
{
	return tableRecord->offset_;
}

uint32_t TableRecord_get_length(const TableRecord* tableRecord)
{
	return tableRecord->length_;
}

void TableRecord_set_table(TableRecord* tableRecord, struct Table* table)
{
	tableRecord->table_ = table;
}

void TableRecord_show(const TableRecord* tableRecord)
{
	printf("[TableRecord]\n");
	printf("  tag        = %s\n", Tag_str(tableRecord->tag_));
	printf("  check_sum  = 0x%08x\n", tableRecord->check_sum_);
	printf("  offset     = %u\n", tableRecord->offset_);
	printf("  length     = %u\n", tableRecord->length_);

	if ( tableRecord->table_ ) {
		//Table_show(tableRecord->table_);
	}
}
