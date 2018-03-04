#ifndef TABLE_RECORD_H
#define TABLE_RECORD_H

#include <cstdint>

class Tag;
class Table;

class TableRecord {
 public:
	static const unsigned size = 16;

 public:
	TableRecord();
	~TableRecord();

	int parse(unsigned char* buf, unsigned bufSize);

	inline const Tag* get_tag() const { return tag_; }
	inline uint32_t get_offset() const { return offset_; }
	inline uint32_t get_length() const { return length_; }

	void set_table(Table* table);

	void show() const;

 private:
	Tag* tag_;
	uint32_t check_sum_;
	uint32_t offset_;
	uint32_t length_;

	// corresponding table
	Table* table_;
};

#endif /* TABLE_RECORD_H */
