#ifndef TABLE_H
#define TABLE_H

#include <stdint.h>
#include "tag.h"

struct Table;

typedef void (*TABLE_DELETE)(const struct Table* table);
typedef int (*TABLE_PARSE)(struct Table* table, unsigned char* buf, unsigned bufSize);
typedef void (*TABLE_SHOW)(const struct Table* table);

typedef struct Table {
	const Tag* tag_;

	// emulate vtable
	TABLE_DELETE delete_;
	TABLE_PARSE parse_;
	TABLE_SHOW show_;
} Table;

void Table_create(Table* table, const Tag* tag, TABLE_DELETE fnDelete, TABLE_PARSE fnParse, TABLE_SHOW fnShow);
void Table_delete(Table* table);

int Table_parse(Table* table, unsigned char* buf, unsigned bufSize);
void Table_show(const Table* table);

#endif /* TABLE_H */
