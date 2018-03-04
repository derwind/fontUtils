#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "sfnt.h"
#include "tableRecord.h"
#include "tag.h"

#define SAFE_FREE(x) if (x) { free(x); }

static int Sfnt_create_tableRecords(Sfnt* sfnt, FILE* fp);

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
	for (i = 0; i < sfnt->tableRecordsIdx_; ++i) {
		TableRecord_delete(sfnt->tableRecords_[i]);
	}
	SAFE_FREE(sfnt->tableRecords_);
	for (i = 0; i < sfnt->tablesIdx_; ++i) {
		//Table_delete(sfnt->table_[i]);
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
	unsigned char buf[SfntHeader_SIZE];
	fread(buf, 1, SfntHeader_SIZE, fp);
	if ( SfntHeader_parse(sfnt->sfntHeader_, buf, SfntHeader_SIZE) != 0 ) {
		result = -1;
		goto end_proc;
	}
	if ( Sfnt_create_tableRecords(sfnt, fp) != 0 ) {
		result = -1;
		goto end_proc;
	}
	/*
	if ( Sfnt_create_tables(sfnt, fp) != 0 ) {
		result = -1;
		goto end_proc;
	}
	*/

 end_proc:
	fclose(fp);

	return result;
}

int Sfnt_create_tableRecords(Sfnt* sfnt, FILE* fp)
{
	uint16_t num_tables = SfntHeader_get_num_tables(sfnt->sfntHeader_);
	sfnt->tableRecordsLen_ = sfnt->tablesLen_ = num_tables;
	sfnt->tableRecords_ = (TableRecord**)malloc(sizeof(TableRecord*) * num_tables);

	unsigned char buf[TableRecord_SIZE];
	int i;
	for (i = 0; i < num_tables; ++i) {
		fread(buf, 1, TableRecord_SIZE, fp);
		TableRecord* record = TableRecord_create();
		if ( TableRecord_parse(record, buf, TableRecord_SIZE) != 0 ) {
			return -1;
		}
		sfnt->tableRecords_[sfnt->tableRecordsIdx_] = record;
		++sfnt->tableRecordsIdx_;
	}

	return 0;
}

void Sfnt_show(const Sfnt* sfnt)
{
	SfntHeader_show(sfnt->sfntHeader_);

	int i;
	for (i = 0; i < sfnt->tableRecordsLen_; ++i) {
		puts("--------------------");
		TableRecord_show(sfnt->tableRecords_[i]);
	}
}
