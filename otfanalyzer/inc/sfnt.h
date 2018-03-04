#ifndef SFNT_H
#define SFNT_H

#include <string>
#include <fstream>
#include <vector>
#include "sfntHeader.h"

class TableRecord;
class Table;

class Sfnt {
 public:
	Sfnt(const char* path);
	~Sfnt();

	int parse();

	void show() const;

 private:
	int create_tableRecords(std::fstream& ifs);
	int create_tables(std::fstream& ifs);

	TableRecord* find_maxp_record();
	void create_table(std::fstream& ifs, TableRecord* record);

 private:
	std::string path_;

	SfntHeader sfntHeader_;
	std::vector<TableRecord*> tableRecords_;
	std::vector<Table*> tables_;
};

#endif /* SFNT_H */
