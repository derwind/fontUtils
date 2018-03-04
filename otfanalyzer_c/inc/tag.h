#ifndef TAG_H
#define TAG_H

#include <stdint.h>
#include <stdbool.h>

typedef struct Tag {
	uint32_t tag_;
	char str_[4+1];
} Tag;

Tag* Tag_create(uint32_t tagValue);
void Tag_delete(Tag* tag);

const char* Tag_str(const Tag* tag);
bool Tag_is(const Tag* tag, const char* str);

#endif /* TAG_H */
