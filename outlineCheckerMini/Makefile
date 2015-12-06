CORE_LIB=outlineCheckCore.so
PY_SCRIPT=outlineCheckMini.py

.PHONY: all
all: $(CORE_LIB) $(PY_SCRIPT)

$(CORE_LIB):
	make -C source || exit 1
	cp source/$(CORE_LIB) .

$(PY_SCRIPT):
	cp py/$(PY_SCRIPT) .

.PHONY: clean
clean:
	make clean -C source
	rm -rf $(CORE_LIB) $(PY_SCRIPT)
