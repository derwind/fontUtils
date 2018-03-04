#include <cstdio>
#include "maxpTable.h"
#include "bufferReader.h"

MaxpTable::MaxpTable(const Tag* tag)
:
Table(tag),
version_(0),
numGlyphs_(0),
maxPoints_(0),
maxContours_(0),
maxCompositePoints_(0),
maxCompositeContours_(0),
maxZones_(0),
maxTwilightPoints_(0),
maxStorage_(0),
maxFunctionDefs_(0),
maxInstructionDefs_(0),
maxStackElements_(0),
maxSizeOfInstructions_(0),
maxComponentElements_(0),
maxComponentDepth_(0)
{
}

MaxpTable::~MaxpTable()
{
}

int MaxpTable::parse(unsigned char* buf, unsigned bufSize)
{
	BufferReader reader(buf, bufSize);

	version_ = reader.readUint32();
	numGlyphs_ = reader.readUint16();
	if ( version_ < 0x00010000 ) {
		return 0;
	}

	maxPoints_ = reader.readUint16();
	maxContours_ = reader.readUint16();
	maxCompositePoints_ = reader.readUint16();
	maxCompositeContours_ = reader.readUint16();
	maxZones_ = reader.readUint16();
	maxTwilightPoints_ = reader.readUint16();
	maxStorage_ = reader.readUint16();
	maxFunctionDefs_ = reader.readUint16();
	maxInstructionDefs_ = reader.readUint16();
	maxStackElements_ = reader.readUint16();
	maxSizeOfInstructions_ = reader.readUint16();
	maxComponentElements_ = reader.readUint16();
	maxComponentDepth_ = reader.readUint16();

	return 0;
}

void MaxpTable::show()
{
	printf("[Table(%s)]\n", tag_->c_str());
	printf("  version   = 0x%08x\n", version_);
	printf("  numGlyphs = %d\n", numGlyphs_);
	if ( version_ < 0x00010000 ) {
		return;
	}
	printf("  maxPoints             = %d\n", maxPoints_);
	printf("  maxContours           = %d\n", maxContours_);
	printf("  maxCompositePoints    = %d\n", maxCompositePoints_);
	printf("  maxCompositeContours  = %d\n", maxCompositeContours_);
	printf("  maxZones              = %d\n", maxZones_);
	printf("  maxTwilightPoints     = %d\n", maxTwilightPoints_);
	printf("  maxStorage            = %d\n", maxStorage_);
	printf("  maxFunctionDefs       = %d\n", maxFunctionDefs_);
	printf("  maxInstructionDefs    = %d\n", maxInstructionDefs_);
	printf("  maxStackElements      = %d\n", maxStackElements_);
	printf("  maxSizeOfInstructions = %d\n", maxSizeOfInstructions_);
	printf("  maxComponentElements  = %d\n", maxComponentElements_);
	printf("  maxComponentDepth     = %d\n", maxComponentDepth_);
}
