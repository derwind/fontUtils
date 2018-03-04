#include <string.h>
#include <stdlib.h>
#include "bufferReader.h"

#ifdef WIN32
#include <Winsock2.h>
#else /* !WIN32 */
#include <arpa/inet.h>
#endif /* !WIN32 */

#define SAFE_FREE(x) if (x) { free(x); }

double BufferReader_fixed2double(uint32_t value)
{
	return 1.0 * value / 65536;
}

BufferReader* BufferReader_create(unsigned char* buf, unsigned bufSize)
{
	if ( !buf ) {
		return NULL;
	}

	BufferReader* bufferReader = (BufferReader*)malloc(sizeof(BufferReader));
	memset(bufferReader, 0, sizeof(BufferReader));

	bufferReader->buf_ = buf;
	bufferReader->size_ = bufSize;
	bufferReader->loc_ = buf;

	return bufferReader;
}

void BufferReader_delete(BufferReader* bufferReader)
{
	SAFE_FREE(bufferReader);
}

uint8_t* BufferReader_readBytes(BufferReader* bufferReader, unsigned size)
{
	uint8_t* value = bufferReader->loc_;
	bufferReader->loc_ += size;

	return value;
}

int8_t BufferReader_readInt8(BufferReader* bufferReader)
{
	return (int8_t)BufferReader_readUint8(bufferReader);
}

uint8_t BufferReader_readUint8(BufferReader* bufferReader)
{
	uint8_t value = *bufferReader->loc_;
	bufferReader->loc_ += 1;

	return value;
}

void BufferReader_readUint8s(BufferReader* bufferReader, uint8_t data[], unsigned dataLen)
{
	int i;
	for (i = 0; i < dataLen; ++i) {
		data[i] = BufferReader_readUint8(bufferReader);
	}
}

int16_t BufferReader_readInt16(BufferReader* bufferReader)
{
	return (int16_t)BufferReader_readUint16(bufferReader);
}

uint16_t BufferReader_readUint16(BufferReader* bufferReader)
{
	uint16_t value = *((uint16_t*)bufferReader->loc_);
	bufferReader->loc_ += 2;

	return ntohs(value);
}

int32_t BufferReader_readInt32(BufferReader* bufferReader)
{
	return (int32_t)BufferReader_readUint32(bufferReader);
}

uint32_t BufferReader_readUint32(BufferReader* bufferReader)
{
	uint32_t value = *((uint32_t*)bufferReader->loc_);
	bufferReader->loc_ += 4;

	return ntohl(value);
}

uint32_t BufferReader_readFixed(BufferReader* bufferReader)
{
	uint32_t value = *((uint32_t*)bufferReader->loc_);
	bufferReader->loc_ += 4;

	return ntohl(value);
}

void BufferReader_readTag(BufferReader* bufferReader, char tag[4])
{
	memcpy(tag, bufferReader->loc_, 4);
	bufferReader->loc_ += 4;
}
