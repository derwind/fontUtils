#include "sfnt.h"
#include <cstdio>
#include <fstream>

Sfnt::Sfnt(const char* path)
:
path_(path)
{
}

Sfnt::~Sfnt()
{
}

int Sfnt::parse()
{
	std::fstream ifs(path_, std::ios::binary | std::ios::in);
	if (!ifs) {
		return -1;
	}

	unsigned char buf[256];
	ifs.read((char*)buf, 12);
	if ( sfntHeader_.parse(buf) != 0 ) {
		return -1;
	}

	return 0;
}

void Sfnt::show() const
{
	sfntHeader_.show();
}
