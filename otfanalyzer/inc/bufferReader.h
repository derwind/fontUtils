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
	int8_t readInt8();
	uint8_t readUint8();
	void readUint8s(uint8_t data[], unsigned dataLen);
	int16_t readInt16();
	uint16_t readUint16();
	int32_t readInt32();
	uint32_t readUint32();
	uint32_t readFixed();
	void readTag(char tag[4]);

 private:
	unsigned char* buf_;
	unsigned size_;
	unsigned char* loc_;
};

#endif /* BUFFER_READER_H */
