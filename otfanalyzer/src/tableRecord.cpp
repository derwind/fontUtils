#include <cstdio>
#include "tableRecord.h"
#include "bufferReader.h"

TableRecord::TableRecord()
{
}

TableRecord::~TableRecord()
{
}

int TableRecord::parse(unsigned char* buf, unsigned bufSize)
{
	BufferReader reader(buf, bufSize);

	tag_ = reader.readUint32();
	check_sum_ = reader.readUint32();
	offset_ = reader.readUint32();
	length_ = reader.readUint32();

	return 0;
}

void TableRecord::show() const
{
	printf("[TableRecord]\n");
	printf("  tag        = %c%c%c%c\n", tag_>>24&0xff, tag_>>16&0xff, tag_>>8&0xff, tag_&0xff);
	printf("  check_sum  = 0x%08x\n", check_sum_);
	printf("  offset     = %u\n", offset_);
	printf("  length     = %u\n", length_);
}
