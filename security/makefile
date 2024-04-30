# Compiler
CC := gcc

# Source file
SRC := security.c

# Output directory, file name
ifeq ($(OS),Windows_NT)
	OUT_DIR := .\bin
	OUT_FILE := security.exe
	DIR_SEP := \\
else
	OUT_FILE := security
	OUT_DIR := ./bin
	DIR_SEP := /
endif

# Compiler flags
CFLAGS := -o $(OUT_DIR)$(DIR_SEP)$(OUT_FILE)

# Default target
all: $(OUT_DIR)$(DIR_SEP)$(OUT_FILE)

# Create the output directory and compile the source file
$(OUT_DIR)$(DIR_SEP)$(OUT_FILE): $(SRC)
ifeq ($(OS),Windows_NT)
	if not exist $(OUT_DIR) mkdir $(OUT_DIR)
else
	mkdir -p $(OUT_DIR)
endif
	$(CC) $(CFLAGS) $(SRC)

# Clean the output directory
clean:
ifeq ($(OS),Windows_NT)
	rmdir /S /Q $(OUT_DIR)
else
	rm -rf $(OUT_DIR)
endif