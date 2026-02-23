# Module 02: Bit Manipulation

## Bitwise Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `&` | AND | `0b1100 & 0b1010` | `0b1000` |
| `\|` | OR | `0b1100 \| 0b1010` | `0b1110` |
| `^` | XOR | `0b1100 ^ 0b1010` | `0b0110` |
| `~` | NOT | `~0b1100` | `0b0011` (inverts all bits) |
| `<<` | Left Shift | `0b0011 << 2` | `0b1100` |
| `>>` | Right Shift | `0b1100 >> 2` | `0b0011` |

## Common Bit Manipulation Patterns

### Creating a Mask for Bit N

```c
#define BIT(n) (1U << (n))

BIT(0)  // 0b00000001
BIT(3)  // 0b00001000
BIT(7)  // 0b10000000
```

### Setting a Bit (Turn ON)

```c
#define SET_BIT(reg, bit) ((reg) |= BIT(bit))

uint8_t port = 0b00000000;
SET_BIT(port, 3);  // port = 0b00001000
```

### Clearing a Bit (Turn OFF)

```c
#define CLEAR_BIT(reg, bit) ((reg) &= ~BIT(bit))

uint8_t port = 0b11111111;
CLEAR_BIT(port, 3);  // port = 0b11110111
```

### Toggling a Bit (Flip)

```c
#define TOGGLE_BIT(reg, bit) ((reg) ^= BIT(bit))

uint8_t port = 0b00001000;
TOGGLE_BIT(port, 3);  // port = 0b00000000
TOGGLE_BIT(port, 3);  // port = 0b00001000
```

### Checking a Bit (Read)

```c
#define CHECK_BIT(reg, bit) (((reg) >> (bit)) & 1U)

uint8_t port = 0b00001000;
CHECK_BIT(port, 3);  // Returns 1
CHECK_BIT(port, 2);  // Returns 0
```

## Hardware Register Example

A typical GPIO port register (8 pins):

```
Bit:    7    6    5    4    3    2    1    0
      +----+----+----+----+----+----+----+----+
      | P7 | P6 | P5 | P4 | P3 | P2 | P1 | P0 |
      +----+----+----+----+----+----+----+----+
```

```c
#define LED_PIN     3
#define BUTTON_PIN  5

volatile uint8_t *GPIO_PORT = (uint8_t*)0x1000;  // Memory-mapped I/O

// Turn LED on
SET_BIT(*GPIO_PORT, LED_PIN);

// Check button (active low)
if (!CHECK_BIT(*GPIO_PORT, BUTTON_PIN)) {
    // Button pressed
}
```

## Extracting Bit Fields

Extract multiple bits from a value:

```c
// Status register: [7:6]=mode, [5:4]=speed, [3:0]=error_code
uint8_t status = 0b10110101;

// Extract error code (bits 3:0)
uint8_t error = status & 0x0F;           // Mask lower 4 bits

// Extract speed (bits 5:4)
uint8_t speed = (status >> 4) & 0x03;    // Shift right, mask 2 bits

// Extract mode (bits 7:6)
uint8_t mode = (status >> 6) & 0x03;
```

## Packing Bit Fields

Combine multiple values into one register:

```c
// Pack: mode=2, speed=1, error=5
uint8_t status = 0;
status |= (2 << 6);  // Mode in bits 7:6
status |= (1 << 4);  // Speed in bits 5:4
status |= 5;         // Error in bits 3:0
// Result: 0b10010101
```

## Common Idioms

```c
// Check if power of 2
#define IS_POWER_OF_2(x) (((x) != 0) && (((x) & ((x) - 1)) == 0))

// Round up to next power of 2 (32-bit)
uint32_t next_power_of_2(uint32_t x) {
    x--;
    x |= x >> 1;
    x |= x >> 2;
    x |= x >> 4;
    x |= x >> 8;
    x |= x >> 16;
    return x + 1;
}

// Count set bits (population count)
int popcount(uint32_t x) {
    int count = 0;
    while (x) {
        count += x & 1;
        x >>= 1;
    }
    return count;
}
```

## Signed vs Unsigned Shifts

```c
int8_t signed_val = -8;     // 0b11111000
signed_val >> 2;            // 0b11111110 = -2 (arithmetic shift, preserves sign)

uint8_t unsigned_val = 248; // 0b11111000
unsigned_val >> 2;          // 0b00111110 = 62 (logical shift, fills with 0)
```

**Always use unsigned types for bit manipulation to avoid undefined behavior.**
