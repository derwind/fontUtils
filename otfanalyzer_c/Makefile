CC = clang

INC += -I. -I./inc
CFLAGS += $(INC) -O2

TARGET = otfanalyzer

OBJS = main.o
STATIC_LIB += src/libotfanalyzer.a

################################################################################

all: $(TARGET)

$(TARGET): $(STATIC_LIB) $(OBJS)
	$(CC) -Wall -o $@ $(OBJS) $(STATIC_LIB)

$(STATIC_LIB):
	make -C src

.cpp.o:
	$(CC) -Wall $(CFLAGS) -c $<

.PHONY: clean
clean:
	make clean -C src
	rm -rf $(TARGET) $(OBJS)
