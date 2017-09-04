#include "sfnt.h"
#include <cstdio>

void showUsage(const char* programName)
{
	fprintf(stderr, "[usage] %s OTF_PATH\n", programName);
}

int main(int argc, char* argv[])
{
	if (argc < 1 + 1) {
		showUsage(argv[0]);
		return 1;
	}

	Sfnt sfnt(argv[1]);
	if ( sfnt.parse() != 0 ) {
		fprintf(stderr, "failed to parse\n");
		return 1;
	}
	sfnt.show();

	return 0;
}
