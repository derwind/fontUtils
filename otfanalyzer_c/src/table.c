#include "table.h"

void Table_create(Table* table, const Tag* tag, TABLE_DELETE fnDelete, TABLE_PARSE fnParse, TABLE_SHOW fnShow)
{
	table->tag_ = tag;
	table->delete_ = fnDelete;
	table->parse_ = fnParse;
	table->show_ = fnShow;
}

void Table_delete(Table* table)
{
	table->delete_(table);
}

int Table_parse(Table* table, unsigned char* buf, unsigned bufSize)
{
	return table->parse_(table, buf, bufSize);
}

void Table_show(const Table* table)
{
	table->show_(table);
}
