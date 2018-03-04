CC = clang

TARGET=libotfanalyzer.a

OBJS = sfnt.o sfntHeader.o bufferReader.o tableRecord.o tag.o table.o maxpTable.o os_2Table.o

INC += -I. -I../inc

CFLAGS += $(INC) -O2

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

.c.o:
	$(CC) -Wall $(CFLAGS) -c $<

.PHONY: clean
clean:
	rm -rf $(TARGET) $(OBJS)
