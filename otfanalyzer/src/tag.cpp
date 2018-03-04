#include <cstring>
#include <string>
#include <algorithm>
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

	std::string s1 = str_;
	std::transform(s1.begin(), s1.end(), s1.begin(), ::tolower);

	std::string s2 = tag;
	std::transform(s2.begin(), s2.end(), s2.begin(), ::tolower);


	return ( s1 == s2 );
}

bool Tag::is(const Tag& tag) const
{
	return is(tag.c_str());
}
