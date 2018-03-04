#ifndef BUFFER_READER_H
#define BUFFER_READER_H

#include <cstdint>

class BufferReader {
 public:
	static double fixed2double(uint32_t value) { return 1.0 * value / 65536; }

 public:
	BufferReader();
	BufferReader(unsigned char* buf, unsigned bufSize);
	~BufferReader();

	void setBuffer(unsigned char* buf, unsigned bufSize);

	uint8_t* readBytes(unsigned size);
	uint8_t readUint8();
	uint16_t readUint16();
	uint32_t readUint32();
	uint32_t readFixed();

 private:
	unsigned char* buf_;
	unsigned size_;
	unsigned char* loc_;
};

#endif /* BUFFER_READER_H */
