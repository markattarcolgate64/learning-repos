# C Refresher with Hardware Focus

A concise C refresher covering essential low-level concepts for robotics and embedded systems.

## Prerequisites

- Basic C syntax (variables, functions, control flow)
- gcc installed (`gcc --version` to check)

## Setup

```bash
# Build all exercises
make all

# Build specific module
make module01

# Clean build artifacts
make clean
```

## Course Structure

```
c-refresh/
├── 01_memory_and_pointers/   # Memory layout, pointer arithmetic
├── 02_bit_manipulation/      # Bitwise ops, register patterns
├── 03_structs_and_hardware/  # Packed structs, memory-mapped I/O
├── 04_buffers_and_state/     # Circular buffers, state machines
├── 05_embedded_patterns/     # volatile, ISR patterns, fixed-point
└── solutions/                # Reference implementations
```

## Learning Path

| Module | Topic | Key Concepts |
|--------|-------|--------------|
| 01 | Memory & Pointers | Stack/heap, pointer arithmetic, alignment, endianness |
| 02 | Bit Manipulation | Bitwise ops, masks, GPIO simulation |
| 03 | Structs & Hardware | Packed structs, unions, register overlays |
| 04 | Buffers & State | Ring buffers, function pointers, state machines |
| 05 | Embedded Patterns | volatile, ISR flags, fixed-point basics |

## How to Use

1. Read `theory.md` in each module
2. Complete TODOs in `exercises.c`
3. Build and test: `make module01 && ./bin/module01`
4. Check `solutions/` only after attempting

## Module Format

Each module contains:
- `theory.md` - Conceptual overview with examples
- `exercises.c` - TODO-based coding exercises
- `Makefile` - Module-specific build rules
