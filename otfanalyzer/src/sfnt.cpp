#include <cstdio>
#include "sfnt.h"
#include "tableRecord.h"
#include "tag.h"
#include "maxpTable.h"

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

	unsigned char buf[SfntHeader::size];
	ifs.read((char*)buf, SfntHeader::size);
	if ( sfntHeader_.parse(buf, SfntHeader::size) != 0 ) {
		return -1;
	}
	if ( create_tableRecords(ifs) != 0 ) {
		return -1;
	}
	if ( create_tables(ifs) != 0 ) {
		return -1;
	}

	return 0;
}

int Sfnt::create_tableRecords(std::fstream& ifs)
{
	uint16_t num_tables = sfntHeader_.get_num_tables();
	unsigned char buf[TableRecord::size];
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

int Sfnt::create_tables(std::fstream& ifs)
{
	TableRecord* maxp_record = find_maxp_record();
	if ( !maxp_record ) {
		return -1;
	}
	create_maxp_table(ifs, maxp_record);

	return 0;
}

TableRecord* Sfnt::find_maxp_record()
{
	for (auto it = tableRecords_.begin(); it != tableRecords_.end(); ++it) {
		if ( (*it)->get_tag()->is("maxp") ) {
			return *it;
		}
	}

	return nullptr;
}

void Sfnt::create_maxp_table(std::fstream& ifs, TableRecord* maxp_record)
{
	uint32_t offset = maxp_record->get_offset();
	uint32_t length = maxp_record->get_length();
	ifs.seekg(offset, std::ios_base::beg);
	unsigned char* buf = new unsigned char[length];
	ifs.read((char*)buf, length);
	MaxpTable* maxp_table = new MaxpTable(maxp_record->get_tag());
	maxp_table->parse(buf, length);
	maxp_record->set_table(maxp_table);
	delete [] buf;
}

void Sfnt::show() const
{
	sfntHeader_.show();

	for (auto it = tableRecords_.begin(); it != tableRecords_.end(); ++it) {
		puts("--------------------");
		(*it)->show();
	}
}
