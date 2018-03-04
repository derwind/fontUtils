#ifndef TABLE_H
#define TABLE_H

#include <cstdint>
#include "tag.h"

class Table {
 public:
	Table(const Tag* tag);
	virtual ~Table();

	virtual int parse(unsigned char* buf, unsigned bufSize);

	virtual void show();

 protected:
	const Tag* tag_;
};

#endif /* TABLE_H */
