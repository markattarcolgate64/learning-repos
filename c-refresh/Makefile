CC = gcc
# Use -Wno-unused-parameter for exercises (TODOs have unused params)
# Remove this flag when checking completed solutions
CFLAGS = -Wall -Wextra -std=c11 -g -Wno-unused-parameter
CFLAGS_STRICT = -Wall -Wextra -Werror -std=c11 -g
BIN_DIR = bin

# Create bin directory
$(shell mkdir -p $(BIN_DIR))

.PHONY: all clean module01 module02 module03 module04 module05

all: module01 module02 module03 module04 module05

module01: 01_memory_and_pointers/exercises.c
	$(CC) $(CFLAGS) -o $(BIN_DIR)/module01 $<

module02: 02_bit_manipulation/exercises.c
	$(CC) $(CFLAGS) -o $(BIN_DIR)/module02 $<

module03: 03_structs_and_hardware/exercises.c
	$(CC) $(CFLAGS) -o $(BIN_DIR)/module03 $<

module04: 04_buffers_and_state/exercises.c
	$(CC) $(CFLAGS) -o $(BIN_DIR)/module04 $<

module05: 05_embedded_patterns/exercises.c
	$(CC) $(CFLAGS) -o $(BIN_DIR)/module05 $<

# Build with address sanitizer for debugging
debug: CFLAGS += -fsanitize=address -fsanitize=undefined
debug: all

clean:
	rm -rf $(BIN_DIR)
