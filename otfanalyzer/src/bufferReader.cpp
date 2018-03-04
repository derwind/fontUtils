#include "bufferReader.h"
#include <arpa/inet.h>

BufferReader::BufferReader()
:
buf_(0),
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

uint8_t BufferReader::readUint8()
{
	uint8_t value = *loc_;
	loc_ += 1;

	return value;
}

uint16_t BufferReader::readUint16()
{
	uint16_t value = *((uint16_t*)loc_);
	loc_ += 2;

	return ntohs(value);
}

uint32_t BufferReader::readUint32()
{
	uint32_t value = *((uint32_t*)loc_);
	loc_ += 4;

	return ntohl(value);
}
