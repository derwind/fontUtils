#ifndef SFNT_H
#define SFNT_H

#include "sfntHeader.h"

struct TableRecord;
struct Table;

typedef struct Sfnt {
	char* path_;

	SfntHeader* sfntHeader_;
	struct TableRecord** tableRecords_;
	unsigned tableRecordsIdx_;
	unsigned tableRecordsLen_;
	struct Table** tables_;
	unsigned tablesIdx_;
	unsigned tablesLen_;
} Sfnt;

Sfnt* Sfnt_create(const char* path);
void Sfnt_delete(Sfnt* sfnt);

int Sfnt_parse(Sfnt* sfnt);
void Sfnt_show(const Sfnt* sfnt);

#endif /* SFNT_H */
