# Module 05: Embedded Patterns

## The `volatile` Keyword

`volatile` tells the compiler that a variable may change unexpectedly (by hardware or another thread), so it must:
- Always read from memory (no caching in registers)
- Always write to memory (no write optimization)
- Preserve order of volatile accesses

### When to Use volatile

```c
// 1. Memory-mapped hardware registers
volatile uint32_t *GPIO_PORT = (volatile uint32_t*)0x40020000;

// 2. Variables modified by interrupt handlers
volatile bool flag = false;

void ISR_Timer(void) {
    flag = true;  // Set by ISR
}

void main_loop(void) {
    while (!flag) {  // Without volatile, compiler might optimize to while(true)
        // wait
    }
}

// 3. Variables shared between threads (though volatile alone isn't enough for thread safety)
```

### volatile Does NOT Provide

- Atomicity (a 32-bit write can be interrupted)
- Memory barriers (other CPUs may not see changes)
- Thread safety (need mutexes for that)

### Common Bug: Missing volatile

```c
// BUG: Compiler may optimize away the loop
uint32_t *status = (uint32_t*)0x40000000;
while (*status & 0x01) { }  // May become infinite loop

// FIX: Use volatile
volatile uint32_t *status = (volatile uint32_t*)0x40000000;
while (*status & 0x01) { }  // Always reads from memory
```

## ISR (Interrupt Service Routine) Patterns

### Flag-Based Communication

```c
// ISR sets flag, main loop clears and processes
volatile uint8_t event_flags = 0;

#define FLAG_BUTTON   (1 << 0)
#define FLAG_TIMER    (1 << 1)
#define FLAG_UART_RX  (1 << 2)

void Button_ISR(void) {
    event_flags |= FLAG_BUTTON;  // Set flag
    // Don't do heavy processing here!
}

void main_loop(void) {
    while (1) {
        if (event_flags & FLAG_BUTTON) {
            event_flags &= ~FLAG_BUTTON;  // Clear flag
            handle_button();              // Process outside ISR
        }
    }
}
```

### Shared Data Protection

```c
volatile int16_t sensor_value;
volatile bool data_ready = false;

void ADC_ISR(void) {
    sensor_value = ADC_DATA_REG;
    data_ready = true;
}

int16_t read_sensor(void) {
    while (!data_ready) { }
    data_ready = false;

    // Disable interrupts for atomic read
    __disable_irq();
    int16_t value = sensor_value;
    __enable_irq();

    return value;
}
```

### ISR Design Rules

1. **Keep ISRs short** - Do minimal work, set flags for main loop
2. **No blocking** - Never wait in an ISR (no delays, no waiting for flags)
3. **Be reentrant** - Don't rely on global state being consistent
4. **Use volatile** - For all variables shared with main code
5. **Protect critical sections** - Disable interrupts when accessing shared data

## Critical Sections

A critical section is code that must run without interruption:

```c
// Simple critical section (single-core)
void critical_section_example(void) {
    uint32_t primask = __get_PRIMASK();  // Save interrupt state
    __disable_irq();                      // Disable interrupts

    // Critical section - no interrupts here
    shared_variable++;

    __set_PRIMASK(primask);  // Restore interrupt state
}

// Macro version
#define ENTER_CRITICAL()  uint32_t _primask = __get_PRIMASK(); __disable_irq()
#define EXIT_CRITICAL()   __set_PRIMASK(_primask)

void example(void) {
    ENTER_CRITICAL();
    // Critical code
    EXIT_CRITICAL();
}
```

## Fixed-Point Arithmetic Basics

Many microcontrollers lack floating-point hardware. Fixed-point is a fast alternative.

### Q-Format Notation

Q8.8 means 8 integer bits, 8 fractional bits (in a 16-bit value):
- Range: -128.0 to +127.996 (approximately)
- Resolution: 1/256 = 0.00390625

```c
typedef int16_t fixed_t;  // Q8.8 format

#define FIXED_SHIFT 8
#define FIXED_SCALE (1 << FIXED_SHIFT)  // 256

// Convert float to fixed
fixed_t float_to_fixed(float f) {
    return (fixed_t)(f * FIXED_SCALE);
}

// Convert fixed to float
float fixed_to_float(fixed_t x) {
    return (float)x / FIXED_SCALE;
}

// Fixed-point multiplication
// Result needs to be shifted back
fixed_t fixed_mul(fixed_t a, fixed_t b) {
    int32_t result = (int32_t)a * (int32_t)b;
    return (fixed_t)(result >> FIXED_SHIFT);
}

// Fixed-point division
fixed_t fixed_div(fixed_t a, fixed_t b) {
    int32_t temp = (int32_t)a << FIXED_SHIFT;
    return (fixed_t)(temp / b);
}
```

### Example: Temperature Calculation

```c
// Convert 10-bit ADC reading to temperature
// Formula: temp = (adc_value * 3.3 / 1024 - 0.5) * 100
// In fixed-point Q8.8:

#define ADC_SCALE_FIXED   3277  // 3.3 * 256 * 256 / 1024
#define OFFSET_FIXED      128   // 0.5 * 256
#define TEMP_SCALE_FIXED  25600 // 100 * 256

fixed_t adc_to_temp(uint16_t adc_value) {
    int32_t voltage = (int32_t)adc_value * ADC_SCALE_FIXED >> 8;
    int32_t offset_voltage = voltage - OFFSET_FIXED;
    return (fixed_t)((offset_voltage * TEMP_SCALE_FIXED) >> 8);
}
```

## Timer Patterns

### Software Timer Using Ticks

```c
volatile uint32_t system_ticks = 0;

void SysTick_ISR(void) {
    system_ticks++;
}

uint32_t get_ticks(void) {
    return system_ticks;
}

// Non-blocking delay check
bool timeout_expired(uint32_t start, uint32_t timeout_ms) {
    return (get_ticks() - start) >= timeout_ms;
}

// Usage
void example(void) {
    uint32_t start = get_ticks();

    while (!timeout_expired(start, 100)) {
        // Do something for up to 100ms
    }
}
```

### Periodic Task Scheduler

```c
typedef struct {
    void (*task)(void);
    uint32_t period_ms;
    uint32_t last_run;
} ScheduledTask;

ScheduledTask tasks[] = {
    {read_sensors, 10, 0},    // Every 10ms
    {update_display, 100, 0}, // Every 100ms
    {check_buttons, 50, 0},   // Every 50ms
    {NULL, 0, 0}
};

void run_scheduler(void) {
    uint32_t now = get_ticks();

    for (int i = 0; tasks[i].task != NULL; i++) {
        if (now - tasks[i].last_run >= tasks[i].period_ms) {
            tasks[i].task();
            tasks[i].last_run = now;
        }
    }
}

void main_loop(void) {
    while (1) {
        run_scheduler();
    }
}
```

## Watchdog Timer Pattern

```c
// Watchdog prevents system hangs
void watchdog_init(uint32_t timeout_ms) {
    // Configure watchdog hardware (platform-specific)
}

void watchdog_feed(void) {
    // Reset watchdog counter (platform-specific)
    // Must be called regularly or system resets
}

void main_loop(void) {
    while (1) {
        run_scheduler();
        watchdog_feed();  // Prove we're still running
    }
}
```

## Double Buffering

For data that takes time to update (display, DMA):

```c
typedef struct {
    uint8_t data[BUFFER_SIZE];
} Buffer;

Buffer buffers[2];
volatile int active_buffer = 0;

Buffer *get_display_buffer(void) {
    return &buffers[active_buffer];
}

Buffer *get_draw_buffer(void) {
    return &buffers[1 - active_buffer];
}

void swap_buffers(void) {
    // Called after drawing is complete
    active_buffer = 1 - active_buffer;
}
```
