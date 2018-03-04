#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "sfnt.h"
//#include "tableRecord.h"
//#include "tag.h"

#define SAFE_FREE(x) if (x) { free(x); }

Sfnt* Sfnt_create(const char* path)
{
	if ( !path ) {
		return NULL;
	}
	unsigned len = strlen(path);

	Sfnt* sfnt = (Sfnt*)malloc(sizeof(Sfnt));
	memset(sfnt, 0, sizeof(Sfnt));

	sfnt->path_ = (char*)malloc(len+1);
	strcpy(sfnt->path_, path);

	sfnt->sfntHeader_ = SfntHeader_create();

	return sfnt;
}

void Sfnt_delete(Sfnt* sfnt)
{
	if ( !sfnt ) {
		return;
	}

	int i;
	for (i = 0; i < sfnt->tableRecordsLen_; ++i) {
		SAFE_FREE(sfnt->tableRecords_[i]);
	}
	SAFE_FREE(sfnt->tableRecords_);
	for (i = 0; i < sfnt->tablesLen_; ++i) {
		SAFE_FREE(sfnt->table_[i]);
	}
	SAFE_FREE(sfnt->table_);

	SfntHeader_delete(sfnt->sfntHeader_);
	SAFE_FREE(sfnt->path_);
	SAFE_FREE(sfnt);
}

int Sfnt_parse(Sfnt* sfnt)
{
	FILE* fp = fopen(sfnt->path_, "rb");
	if ( !fp ) {
		return -1;
	}

	int result = 0;
	unsigned char* buf = (unsigned char*)malloc(SfntHeader_SIZE);
	fread(buf, 1, SfntHeader_SIZE, fp);
	if ( SfntHeader_parse(sfnt->sfntHeader_, buf, SfntHeader_SIZE) != 0 ) {
		result = -1;
		goto end_proc;
	}
	/*
	if ( Sfnt_create_tableRecords(sfnt, fp) != 0 ) {
		result = -1;
		goto end_proc;
	}
	if ( Sfnt_create_tables(sfnt, fp) != 0 ) {
		result = -1;
		goto end_proc;
	}
	*/

 end_proc:
	SAFE_FREE(buf);
	fclose(fp);

	return result;
}

void Sfnt_show(const Sfnt* sfnt)
{
	SfntHeader_show(sfnt->sfntHeader_);

	/*
	int i;
	for (i = 0; i < sfnt->tableRecordsLen_; ++i) {
		puts("--------------------");
		TableRecord_show(sfnt->tableRecords_[i]);
	}
	*/
}
