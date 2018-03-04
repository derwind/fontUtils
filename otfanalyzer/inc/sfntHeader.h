#ifndef SFNT_HEADER_H
#define SFNT_HEADER_H

#include <cstdint>

class SfntHeader {
 public:
	static const unsigned size = 12;

 public:
	SfntHeader();
	~SfntHeader();

	int parse(unsigned char* buf, unsigned bufSize);

	void show() const;

 private:
	uint16_t num_tables_;
	uint16_t search_range_;
	uint16_t entry_selector_;
	uint16_t range_shift_;
};

#endif /* SFNT_HEADER_H */
