#include <cstdio>
#include "sfntHeader.h"
#include "bufferReader.h"

SfntHeader::SfntHeader()
:
num_tables_(0),
search_range_(0),
entry_selector_(0),
range_shift_(0)
{
}

SfntHeader::~SfntHeader()
{
}

int SfntHeader::parse(unsigned char* buf, unsigned bufSize)
{
	BufferReader reader(buf, bufSize);

	uint32_t sfntVersion = reader.readUint32();

	if ( sfntVersion != 0x4F54544F ) {
		return -1;
	}

	num_tables_ = reader.readUint16();
	search_range_ = reader.readUint16();
	entry_selector_ = reader.readUint16();
	range_shift_ = reader.readUint16();

	return 0;
}

void SfntHeader::show() const
{
	printf("[sfntHeader]\n");
	printf("  num_tables    = %u\n", num_tables_);
	printf("  search_range  = %u\n", search_range_);
	printf("  entry_selector= %u\n", entry_selector_);
	printf("  range_shift   = %u\n", range_shift_);
}
