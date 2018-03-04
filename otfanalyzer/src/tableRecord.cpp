#include <cstdio>
#include "tableRecord.h"
#include "tag.h"
#include "table.h"
#include "bufferReader.h"

TableRecord::TableRecord()
:
tag_(nullptr),
check_sum_(0),
offset_(0),
length_(0),
table_(nullptr)
{
}

TableRecord::~TableRecord()
{
	if ( table_ ) {
		delete table_;
	}
	if ( tag_ ) {
		delete tag_;
	}
}

int TableRecord::parse(unsigned char* buf, unsigned bufSize)
{
	BufferReader reader(buf, bufSize);

	tag_ = new Tag(reader.readUint32());
	check_sum_ = reader.readUint32();
	offset_ = reader.readUint32();
	length_ = reader.readUint32();

	return 0;
}

void TableRecord::set_table(Table* table)
{
	table_ = table;
}

void TableRecord::show() const
{
	printf("[TableRecord]\n");
	printf("  tag        = %s\n", tag_->c_str());
	printf("  check_sum  = 0x%08x\n", check_sum_);
	printf("  offset     = %u\n", offset_);
	printf("  length     = %u\n", length_);

	if ( table_ ) {
		table_->show();
	}
}
