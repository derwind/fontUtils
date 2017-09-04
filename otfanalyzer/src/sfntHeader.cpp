#include "sfntHeader.h"
#include <cstdio>

static
inline uint16_t ushortValue(const unsigned char* buf)
{
	return (uint16_t)buf[0] << 8 | buf[1];
}

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

int SfntHeader::parse(const unsigned char* buf)
{
	if ( !(buf[0] == 'O' && buf[1] == 'T' && buf[2] == 'T' && buf[3] == 'O') ) {
		return -1;
	}

	int i = 4;
	num_tables_ = ushortValue(&buf[i]);
	i += 2;
	search_range_ = ushortValue(&buf[i]);
	i += 2;
	entry_selector_ = ushortValue(&buf[i]);
	i += 2;
	range_shift_ = ushortValue(&buf[i]);

	return 0;
}

void SfntHeader::show() const
{
	printf("[Header]\n");
	printf("  num_tables    = %u\n", num_tables_);
	printf("  search_range  = %u\n", search_range_);
	printf("  entry_selector= %u\n", entry_selector_);
	printf("  range_shift   = %u\n", range_shift_);
}
