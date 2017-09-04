#ifndef SFNT_H
#define SFNT_H

#include <string>
#include "sfntHeader.h"

class Sfnt {
 public:
	Sfnt(const char* path);
	~Sfnt();

	int parse();

	void show() const;

 private:
	std::string path_;

	SfntHeader sfntHeader_;
};

#endif /* SFNT_H */
