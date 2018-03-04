#ifndef BUFFER_READER_H
#define BUFFER_READER_H

#include <stdint.h>

typedef struct BufferReader {
	unsigned char* buf_;
	unsigned size_;
	unsigned char* loc_;
} BufferReader;

double BufferReader_fixed2double(uint32_t value);

BufferReader* BufferReader_create(unsigned char* buf, unsigned bufSize);
void BufferReader_delete(BufferReader* bufferReader);

uint8_t* BufferReader_readBytes(BufferReader* bufferReader, unsigned size);
int8_t BufferReader_readInt8(BufferReader* bufferReader);
uint8_t BufferReader_readUint8(BufferReader* bufferReader);
void BufferReader_readUint8s(BufferReader* bufferReader, uint8_t data[], unsigned dataLen);
int16_t BufferReader_readInt16(BufferReader* bufferReader);
uint16_t BufferReader_readUint16(BufferReader* bufferReader);
int32_t BufferReader_readInt32(BufferReader* bufferReader);
uint32_t BufferReader_readUint32(BufferReader* bufferReader);
uint32_t BufferReader_readFixed(BufferReader* bufferReader);
void BufferReader_readTag(BufferReader* bufferReader, char tag[4]);

#endif /* BUFFER_READER_H */
