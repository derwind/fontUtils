#include <cstdio>
#include <fstream>
#include "sfnt.h"

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
	ifs.read((char*)buf, SfntHeader::size);
	if ( sfntHeader_.parse(buf, SfntHeader::size) != 0 ) {
		return -1;
	}

	return 0;
}

void Sfnt::show() const
{
	sfntHeader_.show();
}
