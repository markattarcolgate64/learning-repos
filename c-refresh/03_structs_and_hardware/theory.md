# Module 03: Structs and Hardware

## Struct Memory Layout

Structs are laid out in memory in declaration order, with padding for alignment:

```c
struct Example {
    char a;      // offset 0, size 1
    // 3 bytes padding (int needs 4-byte alignment)
    int b;       // offset 4, size 4
    char c;      // offset 8, size 1
    // 3 bytes padding (struct size must be multiple of largest alignment)
};  // Total: 12 bytes
```

## Packed Structs

For hardware protocols and network packets, you often need exact byte layouts:

```c
// GCC/Clang packed attribute
struct __attribute__((packed)) SensorPacket {
    uint8_t header;      // offset 0
    uint16_t timestamp;  // offset 1 (no padding!)
    int16_t x;           // offset 3
    int16_t y;           // offset 5
    int16_t z;           // offset 7
    uint8_t checksum;    // offset 9
};  // Total: 10 bytes exactly
```

**Warning:** Packed structs can cause unaligned access on some architectures, leading to performance penalties or even crashes.

## Unions

Unions share memory between members - all members start at the same address:

```c
union Data {
    uint32_t as_u32;
    uint8_t as_bytes[4];
    struct {
        uint16_t low;
        uint16_t high;
    } as_words;
};

union Data d;
d.as_u32 = 0x12345678;

// On little-endian:
// d.as_bytes[0] = 0x78
// d.as_bytes[1] = 0x56
// d.as_words.low = 0x5678
// d.as_words.high = 0x1234
```

## Register Overlays

Unions are commonly used to access hardware registers both as raw values and as bit fields:

```c
typedef union {
    uint8_t raw;
    struct {
        uint8_t enable    : 1;  // bit 0
        uint8_t mode      : 2;  // bits 1-2
        uint8_t prescaler : 3;  // bits 3-5
        uint8_t reserved  : 2;  // bits 6-7
    } bits;
} TimerControl_t;

volatile TimerControl_t *TIMER_CTRL = (TimerControl_t*)0x4000;

// Access as raw value
TIMER_CTRL->raw = 0x15;

// Access individual fields
TIMER_CTRL->bits.enable = 1;
TIMER_CTRL->bits.mode = 2;
TIMER_CTRL->bits.prescaler = 5;
```

**Caution:** Bit field layout is implementation-defined. For portable code, use explicit masks and shifts.

## Memory-Mapped I/O

On microcontrollers, hardware peripherals are controlled through memory-mapped registers:

```c
// Define register addresses
#define GPIO_BASE   0x40020000
#define GPIO_MODER  (*(volatile uint32_t*)(GPIO_BASE + 0x00))
#define GPIO_ODR    (*(volatile uint32_t*)(GPIO_BASE + 0x14))
#define GPIO_IDR    (*(volatile uint32_t*)(GPIO_BASE + 0x10))

// Or use a struct overlay for the entire peripheral
typedef struct {
    volatile uint32_t MODER;    // offset 0x00
    volatile uint32_t OTYPER;   // offset 0x04
    volatile uint32_t OSPEEDR;  // offset 0x08
    volatile uint32_t PUPDR;    // offset 0x0C
    volatile uint32_t IDR;      // offset 0x10
    volatile uint32_t ODR;      // offset 0x14
    // ... more registers
} GPIO_TypeDef;

#define GPIOA ((GPIO_TypeDef*)0x40020000)

// Now access like:
GPIOA->ODR |= (1 << 5);  // Set pin 5 high
```

## Flexible Array Members

For variable-length data (C99):

```c
struct Message {
    uint8_t type;
    uint8_t length;
    uint8_t data[];  // Flexible array member - must be last
};

// Allocate with extra space for data
struct Message *msg = malloc(sizeof(struct Message) + 10);
msg->type = 1;
msg->length = 10;
memcpy(msg->data, "Hello", 5);
```

## Type Punning with Unions

Convert between types without casting:

```c
// Inspect float bits
union FloatInspector {
    float f;
    uint32_t bits;
};

union FloatInspector fi;
fi.f = 3.14159f;
printf("Float bits: 0x%08X\n", fi.bits);

// Extract sign, exponent, mantissa
int sign = (fi.bits >> 31) & 1;
int exponent = (fi.bits >> 23) & 0xFF;
uint32_t mantissa = fi.bits & 0x7FFFFF;
```

## Common Hardware Data Structures

### Sensor Data Structure
```c
struct __attribute__((packed)) IMU_Data {
    int16_t accel_x;
    int16_t accel_y;
    int16_t accel_z;
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
    int16_t temp;
};  // 14 bytes, matches many IMU chip outputs
```

### Command/Response Protocol
```c
struct __attribute__((packed)) Command {
    uint8_t start_byte;   // Always 0xAA
    uint8_t command_id;
    uint16_t payload_len;
    uint8_t payload[64];
    uint16_t crc;
};
```
