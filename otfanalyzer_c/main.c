#include "sfnt.h"
#include <stdio.h>

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

	Sfnt* sfnt = Sfnt_create(argv[1]);
	if ( Sfnt_parse(sfnt) != 0 ) {
		fprintf(stderr, "failed to parse\n");
		return 1;
	}
	Sfnt_show(sfnt);
	Sfnt_delete(sfnt);

	return 0;
}
