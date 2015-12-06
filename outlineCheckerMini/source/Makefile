TARGET=outlineCheckCore.so
#TARGET=outlineCheckCore

OBJS = outlineCheckCore.o

# /usr/include/python2.7
CXXFLAGS += -I`python -c 'from distutils.sysconfig import *; print get_python_inc()'`

INC += -I. -I./core -I/opt/boost_1_58_0/include

CXXFLAGS += $(INC) -fPIC
LIBS += -L/opt/boost_1_58_0/lib -lboost_python
STATIC_LIB += core/oc_core.a
LDFLAGS += -shared $(LIBS)
#LDFLAGS += $(LIBS)

################################################################################

.PHONY: all
all: $(TARGET)

$(TARGET): $(STATIC_LIB) $(OBJS) 
	$(CXX) -Wall -o $(TARGET) $(OBJS) $(STATIC_LIB) $(LDFLAGS)

$(STATIC_LIB):
	make -C core

.cpp.o:
	$(CXX) $(CXXFLAGS) -c $<

.PHONY: clean
clean:
	rm -rf $(TARGET) $(OBJS) $(STATIC_LIBS)
	make clean -C core
