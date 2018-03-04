#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "tag.h"

#define SAFE_FREE(x) if (x) { free(x); }

Tag* Tag_create(uint32_t tagValue)
{
	Tag* tag = (Tag*)malloc(sizeof(Tag));
	memset(tag, 0, sizeof(Tag));

	tag->tag_ = tagValue;

	tag->str_[0] = tagValue >>24 & 0xff;
	tag->str_[1] = tagValue >>16 & 0xff;
	tag->str_[2] = tagValue >>8  & 0xff;
	tag->str_[3] = tagValue      & 0xff;
	tag->str_[4] = '\0';

	return tag;
}

void Tag_delete(Tag* tag)
{
	SAFE_FREE(tag);
}

const char* Tag_str(const Tag* tag)
{
	return tag->str_;
}

bool Tag_is(const Tag* tag, const char* str)
{
	if ( !str ) {
		return false;
	}

	char s1[4+1] = {0};
	char s2[4+1] = {0};

	int i;
	for (i = 0; i < 4; ++i) {
		s1[i] = tolower(tag->str_[i]);
	}
	int len = strlen(str);
	if ( len > 4 ) {
		len = 4;
	}
	for (i = 0; i < len; ++i) {
		s2[i] = tolower(str[i]);
	}

	return ( strcmp(s1, s2) == 0 );
}
