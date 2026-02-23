# Solutions Overview

**Warning:** Try to complete the exercises yourself before looking at solutions!

## Module 01: Memory and Pointers

### Exercise 1.2: Pointer Arithmetic

```c
int sum_array(int *arr, int size) {
    int sum = 0;
    int *end = arr + size;
    for (int *p = arr; p < end; p++) {
        sum += *p;
    }
    return sum;
}

void reverse_array(int *arr, int size) {
    int *start = arr;
    int *end = arr + size - 1;
    while (start < end) {
        int temp = *start;
        *start = *end;
        *end = temp;
        start++;
        end--;
    }
}
```

### Exercise 1.4: Endianness

```c
int is_little_endian(void) {
    uint16_t x = 1;
    return *((uint8_t*)&x) == 1;
}

uint32_t swap_endian_32(uint32_t value) {
    return ((value >> 24) & 0x000000FF) |
           ((value >> 8)  & 0x0000FF00) |
           ((value << 8)  & 0x00FF0000) |
           ((value << 24) & 0xFF000000);
}
```

### Exercise 1.5: Pointer to Pointer

```c
int **create_matrix(int rows, int cols) {
    int **matrix = malloc(rows * sizeof(int*));
    if (!matrix) return NULL;

    for (int i = 0; i < rows; i++) {
        matrix[i] = calloc(cols, sizeof(int));
        if (!matrix[i]) {
            for (int j = 0; j < i; j++) free(matrix[j]);
            free(matrix);
            return NULL;
        }
    }
    return matrix;
}

void free_matrix(int **matrix, int rows) {
    if (!matrix) return;
    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
}
```

---

## Module 02: Bit Manipulation

### Exercise 2.1: Bit Macros

```c
#define BIT(n)                  (1U << (n))
#define SET_BIT(reg, bit)       ((reg) |= BIT(bit))
#define CLEAR_BIT(reg, bit)     ((reg) &= ~BIT(bit))
#define TOGGLE_BIT(reg, bit)    ((reg) ^= BIT(bit))
#define CHECK_BIT(reg, bit)     (((reg) >> (bit)) & 1U)
```

### Exercise 2.3: Bit Field Extraction

```c
uint8_t get_error_code(uint8_t status) {
    return status & 0x0F;
}

uint8_t get_speed_level(uint8_t status) {
    return (status >> 4) & 0x03;
}

uint8_t is_running(uint8_t status) {
    return (status >> 7) & 1;
}

uint8_t get_direction(uint8_t status) {
    return (status >> 6) & 1;
}

uint8_t pack_status(uint8_t running, uint8_t direction, uint8_t speed, uint8_t error) {
    return (running << 7) | (direction << 6) | ((speed & 0x03) << 4) | (error & 0x0F);
}
```

### Exercise 2.4: Bit Counting

```c
int popcount(uint32_t x) {
    int count = 0;
    while (x) {
        count += x & 1;
        x >>= 1;
    }
    return count;
}

int is_power_of_2(uint32_t x) {
    return x != 0 && (x & (x - 1)) == 0;
}

uint32_t next_power_of_2(uint32_t x) {
    if (x == 0) return 1;
    x--;
    x |= x >> 1;
    x |= x >> 2;
    x |= x >> 4;
    x |= x >> 8;
    x |= x >> 16;
    return x + 1;
}

int lowest_set_bit(uint32_t x) {
    if (x == 0) return -1;
    int pos = 0;
    while ((x & 1) == 0) {
        x >>= 1;
        pos++;
    }
    return pos;
}
```

### Exercise 2.5: RGB

```c
uint32_t rgb_pack(uint8_t r, uint8_t g, uint8_t b) {
    return ((uint32_t)r << 16) | ((uint32_t)g << 8) | b;
}

uint8_t rgb_get_red(uint32_t color) { return (color >> 16) & 0xFF; }
uint8_t rgb_get_green(uint32_t color) { return (color >> 8) & 0xFF; }
uint8_t rgb_get_blue(uint32_t color) { return color & 0xFF; }

uint32_t rgb_blend(uint32_t c1, uint32_t c2) {
    uint8_t r = (rgb_get_red(c1) + rgb_get_red(c2)) / 2;
    uint8_t g = (rgb_get_green(c1) + rgb_get_green(c2)) / 2;
    uint8_t b = (rgb_get_blue(c1) + rgb_get_blue(c2)) / 2;
    return rgb_pack(r, g, b);
}
```

---

## Module 03: Structs and Hardware

### Exercise 3.3: Float Inspection

```c
int float_get_sign(float f) {
    union FloatBits fb;
    fb.f = f;
    return (fb.bits >> 31) & 1;
}

int float_get_exponent(float f) {
    union FloatBits fb;
    fb.f = f;
    int biased = (fb.bits >> 23) & 0xFF;
    return biased - 127;
}

int is_negative_zero(float f) {
    union FloatBits fb;
    fb.f = f;
    return fb.bits == 0x80000000;
}
```

---

## Module 04: Buffers and State

### Exercise 4.1: Circular Buffer

```c
void buffer_init(CircularBuffer *buf) {
    buf->head = 0;
    buf->tail = 0;
}

bool buffer_empty(CircularBuffer *buf) {
    return buf->head == buf->tail;
}

bool buffer_full(CircularBuffer *buf) {
    return ((buf->head + 1) % BUFFER_SIZE) == buf->tail;
}

size_t buffer_count(CircularBuffer *buf) {
    if (buf->head >= buf->tail)
        return buf->head - buf->tail;
    return BUFFER_SIZE - buf->tail + buf->head;
}

bool buffer_write(CircularBuffer *buf, uint8_t byte) {
    if (buffer_full(buf)) return false;
    buf->data[buf->head] = byte;
    buf->head = (buf->head + 1) % BUFFER_SIZE;
    return true;
}

bool buffer_read(CircularBuffer *buf, uint8_t *byte) {
    if (buffer_empty(buf)) return false;
    *byte = buf->data[buf->tail];
    buf->tail = (buf->tail + 1) % BUFFER_SIZE;
    return true;
}
```

---

## Module 05: Embedded Patterns

### Exercise 5.4: Fixed-Point

```c
fixed8_t float_to_fixed8(float f) {
    return (fixed8_t)(f * FIXED8_SCALE);
}

float fixed8_to_float(fixed8_t x) {
    return (float)x / FIXED8_SCALE;
}

fixed8_t fixed8_add(fixed8_t a, fixed8_t b) {
    return a + b;
}

fixed8_t fixed8_sub(fixed8_t a, fixed8_t b) {
    return a - b;
}

fixed8_t fixed8_mul(fixed8_t a, fixed8_t b) {
    int32_t result = (int32_t)a * (int32_t)b;
    return (fixed8_t)(result >> FIXED8_SHIFT);
}

fixed8_t fixed8_div(fixed8_t a, fixed8_t b) {
    int32_t temp = (int32_t)a << FIXED8_SHIFT;
    return (fixed8_t)(temp / b);
}
```

### Exercise 5.5: Timers

```c
void timer_start(SoftTimer *timer, uint32_t duration_ticks) {
    timer->start_tick = get_ticks();
    timer->duration = duration_ticks;
    timer->running = true;
}

bool timer_expired(SoftTimer *timer) {
    if (!timer->running) return false;
    return (get_ticks() - timer->start_tick) >= timer->duration;
}

void timer_stop(SoftTimer *timer) {
    timer->running = false;
}

uint32_t timer_remaining(SoftTimer *timer) {
    if (!timer->running) return 0;
    uint32_t elapsed = get_ticks() - timer->start_tick;
    if (elapsed >= timer->duration) return 0;
    return timer->duration - elapsed;
}

void run_scheduler(void) {
    uint32_t now = get_ticks();
    for (int i = 0; tasks[i].task != NULL; i++) {
        if (now - tasks[i].last_run >= tasks[i].period) {
            tasks[i].task();
            tasks[i].last_run = now;
        }
    }
}
```
