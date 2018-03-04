#ifndef TAG_H
#define TAG_H

#include <cstdint>

class Tag {
 public:
	Tag(uint32_t tag);
	~Tag();

	inline const char* c_str() const { return str_; };
	bool is(const char* tag) const;
	bool is(const Tag& tag) const;

	bool operator==(const Tag& tag) { return is(tag); }
	bool operator!=(const Tag& tag) { return !is(tag); }

 private:
	uint32_t tag_;
	char str_[4+1];
};

#endif /* TAG_H */
