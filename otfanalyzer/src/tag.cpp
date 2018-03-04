#include <cstring>
#include "tag.h"

Tag::Tag(uint32_t tag)
:
tag_(tag)
{
	str_[0] = tag_ >>24 & 0xff;
	str_[1] = tag_ >>16 & 0xff;
	str_[2] = tag_ >>8  & 0xff;
	str_[3] = tag_      & 0xff;
	str_[4] = '\0';
}

Tag::~Tag()
{
}

bool Tag::is(const char* tag) const
{
	if ( !tag ) {
		return false;
	}
	return ( strcmp(str_, tag) == 0 );
}
