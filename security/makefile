# Compiler
CC := gcc

# Source file
SRC := security.c

# Output directory
OUT_DIR := ./bin/security

# Output file name
ifeq ($(OS),Windows_NT)
	OUT_FILE := security.exe
else
	OUT_FILE := security
endif

# Compiler flags
CFLAGS := -o $(OUT_DIR)/$(OUT_FILE)

# Default target
all: $(OUT_DIR)/$(OUT_FILE)

# Compile the source file
$(OUT_DIR)/$(OUT_FILE): $(SRC)
	$(CC) $(CFLAGS) $(SRC)

# Clean the output directory
clean:
	rm -rf $(OUT_DIR)