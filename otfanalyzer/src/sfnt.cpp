#include <cstdio>
#include <fstream>
#include "sfnt.h"
#include "tableRecord.h"

Sfnt::Sfnt(const char* path)
:
path_(path)
{
}

Sfnt::~Sfnt()
{
	for (auto it = tableRecords_.begin(); it != tableRecords_.end(); ++it) {
		delete *it;
	}
}

int Sfnt::parse()
{
	std::fstream ifs(path_, std::ios::binary | std::ios::in);
	if ( !ifs ) {
		return -1;
	}

	unsigned char buf[256];
	ifs.read((char*)buf, SfntHeader::size);
	if ( sfntHeader_.parse(buf, SfntHeader::size) != 0 ) {
		return -1;
	}
	uint16_t num_tables = sfntHeader_.get_num_tables();
	for (int i = 0; i < num_tables; ++i) {
		ifs.read((char*)buf, TableRecord::size);
		TableRecord* record = new TableRecord;
		if ( record->parse(buf, TableRecord::size) != 0 ) {
			return -1;
		}
		tableRecords_.push_back(record);
	}

	return 0;
}

void Sfnt::show() const
{
	sfntHeader_.show();

	for (auto it = tableRecords_.begin(); it != tableRecords_.end(); ++it) {
		puts("--------------------");
		(*it)->show();
	}
}
