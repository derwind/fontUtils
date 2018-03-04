#ifndef TABLE_RECORD_H
#define TABLE_RECORD_H

#include <stdint.h>

struct Tag;
struct Table;

typedef struct TableRecord {
	struct Tag* tag_;
	uint32_t check_sum_;
	uint32_t offset_;
	uint32_t length_;

	// corresponding table
	struct Table* table_;
} TableRecord;

#define TableRecord_SIZE (16)

TableRecord* TableRecord_create(void);
void TableRecord_delete(TableRecord* tableRecord);

int TableRecord_parse(TableRecord* tableRecord, unsigned char* buf, unsigned bufSize);

const struct Tag* TableRecord_get_tag(const TableRecord* tableRecord);
uint32_t TableRecord_get_offset(const TableRecord* tableRecord);
uint32_t TableRecord_get_length(const TableRecord* tableRecord);

void TableRecord_set_table(TableRecord* tableRecord, struct Table* table);

void TableRecord_show(const TableRecord* tableRecord);

#endif /* TABLE_RECORD_H */
