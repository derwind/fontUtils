TARGET=libotfanalyzer.a

OBJS = sfnt.o sfntHeader.o

INC += -I. -I../inc

CXXFLAGS += $(INC) -O2

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
