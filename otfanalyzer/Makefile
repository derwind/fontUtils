CXX = clang++

INC += -I. -I./inc
CXXFLAGS += $(INC) -O2 -std=c++11

TARGET = otfanalyzer

OBJS = main.o
STATIC_LIB += src/libotfanalyzer.a

################################################################################

all: $(TARGET)

$(TARGET): $(STATIC_LIB) $(OBJS)
	$(CXX) -Wall -o $@ $(OBJS) $(STATIC_LIB)

$(STATIC_LIB):
	make -C src

.cpp.o:
	$(CXX) -Wall $(CXXFLAGS) -c $<

.PHONY: clean
clean:
	make clean -C src
	rm -rf $(TARGET) $(OBJS)
