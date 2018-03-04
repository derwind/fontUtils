TARGET=libotfanalyzer.a

OBJS = sfnt.o sfntHeader.o bufferReader.o tableRecord.o tag.o table.o maxpTable.o

INC += -I. -I../inc

CXXFLAGS += $(INC) -O2 -std=c++11

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

.cpp.o:
	$(CXX) -Wall $(CXXFLAGS) -c $<

.PHONY: clean
clean:
	rm -rf $(TARGET) $(OBJS)
