TARGET=oc_core.a

OBJS = Glyph.o Contour.o

INC += -I.

CXXFLAGS += $(INC) -fPIC

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

.cpp.o:
	$(CXX) $(CXXFLAGS) -c $<

.PHONY: clean
clean:
	rm -rf $(TARGET) $(OBJS)
