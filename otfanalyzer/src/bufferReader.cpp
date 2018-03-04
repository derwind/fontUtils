#include <cstring>
#include <arpa/inet.h>
#include "bufferReader.h"

BufferReader::BufferReader()
:
buf_(nullptr),
size_(0),
loc_(0)
{
}

BufferReader::BufferReader(unsigned char* buf, unsigned bufSize)
:
buf_(buf),
size_(bufSize),
loc_(buf)
{
}

BufferReader::~BufferReader()
{
}

void BufferReader::setBuffer(unsigned char* buf, unsigned bufSize)
{
	buf_ = buf;
	size_ = bufSize;
	loc_ = buf;
}

uint8_t* BufferReader::readBytes(unsigned size)
{
	uint8_t* value = loc_;
	loc_ += size;

	return value;
}

int8_t BufferReader::readInt8()
{
	return (int8_t)readUint8();
}

uint8_t BufferReader::readUint8()
{
	uint8_t value = *loc_;
	loc_ += 1;

	return value;
}

void BufferReader::readUint8s(uint8_t data[], unsigned dataLen)
{
	for (int i = 0; i < dataLen; ++i) {
		data[i] = readUint8();
	}
}

int16_t BufferReader::readInt16()
{
	return (int16_t)readUint16();
}

uint16_t BufferReader::readUint16()
{
	uint16_t value = *((uint16_t*)loc_);
	loc_ += 2;

	return ntohs(value);
}

int32_t BufferReader::readInt32()
{
	return (int32_t)readUint32();
}

uint32_t BufferReader::readUint32()
{
	uint32_t value = *((uint32_t*)loc_);
	loc_ += 4;

	return ntohl(value);
}

uint32_t BufferReader::readFixed()
{
	uint32_t value = *((uint32_t*)loc_);
	loc_ += 4;

	return ntohl(value);
}

void BufferReader::readTag(char tag[4])
{
	memcpy(tag, loc_, 4);
	loc_ += 4;
}
