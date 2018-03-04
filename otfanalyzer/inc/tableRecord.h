#ifndef TABLE_RECORD_H
#define TABLE_RECORD_H

#include <cstdint>

class TableRecord {
 public:
	static const unsigned size = 16;

 public:
	TableRecord();
	~TableRecord();

	int parse(unsigned char* buf, unsigned bufSize);

	void show() const;

 private:
	uint32_t tag_;
	uint32_t check_sum_;
	uint32_t offset_;
	uint32_t length_;
};

#endif /* TABLE_RECORD_H */
