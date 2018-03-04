#ifndef SFNT_H
#define SFNT_H

#include <string>
#include <vector>
#include "sfntHeader.h"

class TableRecord;

class Sfnt {
 public:
	Sfnt(const char* path);
	~Sfnt();

	int parse();

	void show() const;

 private:
	

 private:
	std::string path_;

	SfntHeader sfntHeader_;
	std::vector<TableRecord*> tableRecords_;
};

#endif /* SFNT_H */
