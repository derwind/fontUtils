#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "sfnt.h"
#include "tableRecord.h"
#include "table.h"
#include "tag.h"
#include "maxpTable.h"

#define SAFE_FREE(x) if (x) { free(x); }

static int Sfnt_create_tableRecords(Sfnt* sfnt, FILE* fp);
static int Sfnt_create_tables(Sfnt* sfnt, FILE* fp);
static TableRecord* Sfnt_find_maxp_record(Sfnt* sfnt);
static void Sfnt_create_table(Sfnt* sfnt, FILE* fp, TableRecord* record);

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
		Table_delete(sfnt->tables_[i]);
	}
	SAFE_FREE(sfnt->tables_);

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
	if ( Sfnt_create_tables(sfnt, fp) != 0 ) {
		result = -1;
		goto end_proc;
	}

 end_proc:
	fclose(fp);

	return result;
}

int Sfnt_create_tableRecords(Sfnt* sfnt, FILE* fp)
{
	uint16_t num_tables = SfntHeader_get_num_tables(sfnt->sfntHeader_);
	sfnt->tableRecordsLen_ = num_tables;
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

int Sfnt_create_tables(Sfnt* sfnt, FILE* fp)
{
	uint16_t num_tables = SfntHeader_get_num_tables(sfnt->sfntHeader_);
	sfnt->tablesLen_ = num_tables;
	sfnt->tables_ = (Table**)malloc(sizeof(Table*) * num_tables);

	// create mxap first to know the number of glyphs
	TableRecord* maxp_record = Sfnt_find_maxp_record(sfnt);
	if ( !maxp_record ) {
		return -1;
	}
	Sfnt_create_table(sfnt, fp, maxp_record);

	int i;
	for (i = 0; i < sfnt->tableRecordsIdx_; ++i) {
		if ( !Tag_is(TableRecord_get_tag(sfnt->tableRecords_[i]), "maxp") ) {
			Sfnt_create_table(sfnt, fp, sfnt->tableRecords_[i]);
		}
	}

	return 0;
}

TableRecord* Sfnt_find_maxp_record(Sfnt* sfnt)
{
	int i;
	for (i = 0; i < sfnt->tableRecordsIdx_; ++i) {
		if ( Tag_is(TableRecord_get_tag(sfnt->tableRecords_[i]), "maxp") ) {
			return sfnt->tableRecords_[i];
		}
	}

	return NULL;
}

void Sfnt_create_table(Sfnt* sfnt, FILE* fp, TableRecord* record)
{
	uint32_t offset = TableRecord_get_offset(record);
	uint32_t length = TableRecord_get_length(record);
	fseek(fp, (long)offset, SEEK_SET);
	unsigned char* buf = (unsigned char*)malloc(length);
	fread(buf, 1, length, fp);
	Table* table = NULL;

	if ( Tag_is(TableRecord_get_tag(record), "maxp") ) {
		table = (Table*)MaxpTable_create(TableRecord_get_tag(record));
	}

	if ( table ) {
		Table_parse(table, buf, length);
		TableRecord_set_table(record, table);
		sfnt->tables_[sfnt->tablesIdx_] = table;
		++sfnt->tablesIdx_;
	}

	SAFE_FREE(buf);
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
