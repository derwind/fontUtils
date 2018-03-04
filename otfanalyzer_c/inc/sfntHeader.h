#ifndef SFNT_HEADER_H
#define SFNT_HEADER_H

#include <stdint.h>

typedef struct SfntHeader {
	uint16_t num_tables_;
	uint16_t search_range_;
	uint16_t entry_selector_;
	uint16_t range_shift_;
} SfntHeader;

#define SfntHeader_SIZE (12)

SfntHeader* SfntHeader_create(void);
void SfntHeader_delete(SfntHeader* sfntHeader);

int SfntHeader_parse(SfntHeader* sfntHeader, unsigned char* buf, unsigned bufSize);
uint16_t SfntHeader_get_num_tables(const SfntHeader* sfntHeader);
void SfntHeader_show(const SfntHeader* sfntHeader);

#endif /* SFNT_HEADER_H */
