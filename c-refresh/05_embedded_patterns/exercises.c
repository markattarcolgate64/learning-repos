/**
 * Module 05: Embedded Patterns Exercises
 *
 * Build: make module05
 * Run:   ./bin/module05
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

/* =============================================================================
 * Exercise 5.1: volatile Keyword
 *
 * Understand when and how to use volatile
 * =============================================================================
 */

// Simulated hardware register (in real code, this would be memory-mapped)
static uint32_t sim_status_register = 0;

// Simulated ISR that modifies a flag
static bool isr_flag = false;  // BUG: Should be volatile!

// Simulated ISR
void simulate_isr(void) {
    isr_flag = true;
}

void exercise_5_1(void) {
    printf("=== Exercise 5.1: volatile Keyword ===\n");

    // Question 1: Why is volatile needed here?
    printf("\nQ1: Given this code:\n");
    printf("  uint32_t *status = (uint32_t*)0x40000000;\n");
    printf("  while (*status & 0x01) { }\n");
    printf("\nWhat problem might occur without volatile?\n");
    printf("Your answer: _________________________________\n");

    // Question 2: Identify the bug
    printf("\nQ2: This code has a bug. Identify it:\n");
    printf("  static bool flag = false;\n");
    printf("  void ISR(void) { flag = true; }\n");
    printf("  void main(void) { while (!flag) { } }\n");
    printf("\nWhat's the bug? _________________________________\n");

    // Demonstrate the pattern
    printf("\nDemonstration:\n");
    isr_flag = false;

    // In optimized code, this loop might be optimized incorrectly
    // We simulate the ISR being called
    int iterations = 0;
    printf("Waiting for ISR flag...\n");
    while (!isr_flag && iterations < 1000000) {
        iterations++;
        if (iterations == 500000) {
            simulate_isr();  // Simulated interrupt
        }
    }
    printf("Flag detected after %d iterations\n", iterations);
    printf("(In real optimized code without volatile, this could hang forever)\n\n");
}

/* =============================================================================
 * Exercise 5.2: ISR Flag Pattern
 *
 * Implement proper ISR flag handling
 * =============================================================================
 */

// Event flags (TODO: add volatile keyword)
static uint8_t event_flags = 0;

#define FLAG_BUTTON_A   (1 << 0)
#define FLAG_BUTTON_B   (1 << 1)
#define FLAG_TIMER      (1 << 2)
#define FLAG_UART_RX    (1 << 3)
#define FLAG_ADC_DONE   (1 << 4)

// Simulated ISRs - these would be called by hardware interrupts
void Button_A_ISR(void) {
    event_flags |= FLAG_BUTTON_A;
}

void Button_B_ISR(void) {
    event_flags |= FLAG_BUTTON_B;
}

void Timer_ISR(void) {
    event_flags |= FLAG_TIMER;
}

void UART_RX_ISR(void) {
    event_flags |= FLAG_UART_RX;
}

void ADC_ISR(void) {
    event_flags |= FLAG_ADC_DONE;
}

// TODO: Check if a specific flag is set
bool is_flag_set(uint8_t flag) {
    (void)flag;
    // TODO: Return true if flag is set in event_flags
    return false;
}

// TODO: Clear a specific flag
void clear_flag(uint8_t flag) {
    (void)flag;
    // TODO: Clear the flag bit(s)
}

// TODO: Check and clear a flag atomically
bool check_and_clear_flag(uint8_t flag) {
    (void)flag;
    // TODO: If flag is set, clear it and return true
    // This should ideally be done with interrupts disabled
    return false;
}

void handle_button_a(void) { printf("  Handling Button A press\n"); }
void handle_button_b(void) { printf("  Handling Button B press\n"); }
void handle_timer(void) { printf("  Handling Timer tick\n"); }
void handle_uart(void) { printf("  Handling UART data\n"); }
void handle_adc(void) { printf("  Handling ADC conversion\n"); }

void exercise_5_2(void) {
    printf("=== Exercise 5.2: ISR Flag Pattern ===\n");

    event_flags = 0;

    // Simulate multiple interrupts occurring
    printf("Simulating interrupts...\n");
    Button_A_ISR();
    Timer_ISR();
    UART_RX_ISR();
    ADC_ISR();

    printf("Event flags: 0x%02X\n", event_flags);

    // Process all pending events
    printf("\nProcessing events:\n");

    if (check_and_clear_flag(FLAG_BUTTON_A)) {
        handle_button_a();
    }
    if (check_and_clear_flag(FLAG_BUTTON_B)) {
        handle_button_b();
    }
    if (check_and_clear_flag(FLAG_TIMER)) {
        handle_timer();
    }
    if (check_and_clear_flag(FLAG_UART_RX)) {
        handle_uart();
    }
    if (check_and_clear_flag(FLAG_ADC_DONE)) {
        handle_adc();
    }

    printf("\nEvent flags after processing: 0x%02X (expected: 0x00)\n\n", event_flags);
}

/* =============================================================================
 * Exercise 5.3: Critical Sections (Simulated)
 *
 * Implement critical section macros
 * =============================================================================
 */

// Simulated interrupt state
static bool interrupts_enabled = true;
static int interrupt_disable_count = 0;

// Simulated interrupt control (real code uses __disable_irq/__enable_irq)
void sim_disable_interrupts(void) {
    interrupts_enabled = false;
    interrupt_disable_count++;
}

void sim_enable_interrupts(void) {
    interrupts_enabled = true;
}

bool sim_get_interrupt_state(void) {
    return interrupts_enabled;
}

void sim_set_interrupt_state(bool state) {
    interrupts_enabled = state;
}

// TODO: Implement macros for nested critical sections
// These should save/restore interrupt state to support nesting
#define ENTER_CRITICAL()  /* TODO: Save state and disable */
#define EXIT_CRITICAL()   /* TODO: Restore saved state */

// Shared data protected by critical section
static int32_t shared_counter = 0;

// TODO: Safely increment the shared counter
void safe_increment(void) {
    // TODO: Use critical section to protect the increment
    shared_counter++;
}

// TODO: Safely read and clear the counter
int32_t safe_read_and_clear(void) {
    int32_t value;
    // TODO: Use critical section to read and clear atomically
    value = shared_counter;
    shared_counter = 0;
    return value;
}

void exercise_5_3(void) {
    printf("=== Exercise 5.3: Critical Sections ===\n");

    shared_counter = 0;
    interrupts_enabled = true;

    // Simulate multiple increments
    printf("Incrementing counter 5 times...\n");
    for (int i = 0; i < 5; i++) {
        safe_increment();
    }

    printf("Counter value: %d (expected: 5)\n", shared_counter);

    // Read and clear
    int32_t value = safe_read_and_clear();
    printf("Read and clear returned: %d, counter now: %d\n",
           value, shared_counter);

    printf("Total interrupt disables: %d\n\n", interrupt_disable_count);
}

/* =============================================================================
 * Exercise 5.4: Fixed-Point Arithmetic
 *
 * Implement basic fixed-point math operations
 * =============================================================================
 */

// Q8.8 format: 8 integer bits, 8 fractional bits
typedef int16_t fixed8_t;

#define FIXED8_SHIFT 8
#define FIXED8_SCALE (1 << FIXED8_SHIFT)  // 256

// TODO: Convert float to Q8.8 fixed-point
fixed8_t float_to_fixed8(float f) {
    (void)f;
    // TODO: Multiply by scale and cast
    return 0;
}

// TODO: Convert Q8.8 fixed-point to float
float fixed8_to_float(fixed8_t x) {
    (void)x;
    // TODO: Divide by scale
    return 0.0f;
}

// TODO: Add two fixed-point numbers
fixed8_t fixed8_add(fixed8_t a, fixed8_t b) {
    (void)a; (void)b;
    // TODO: Simple addition (same as integer)
    return 0;
}

// TODO: Subtract two fixed-point numbers
fixed8_t fixed8_sub(fixed8_t a, fixed8_t b) {
    (void)a; (void)b;
    // TODO: Simple subtraction (same as integer)
    return 0;
}

// TODO: Multiply two fixed-point numbers
fixed8_t fixed8_mul(fixed8_t a, fixed8_t b) {
    (void)a; (void)b;
    // TODO: Multiply, then shift right to correct scale
    // Use int32_t for intermediate result to avoid overflow
    return 0;
}

// TODO: Divide two fixed-point numbers
fixed8_t fixed8_div(fixed8_t a, fixed8_t b) {
    (void)a; (void)b;
    // TODO: Shift dividend left first, then divide
    // Use int32_t for intermediate result
    return 0;
}

void exercise_5_4(void) {
    printf("=== Exercise 5.4: Fixed-Point Arithmetic ===\n");

    // Test conversions
    float test_values[] = {1.0f, 0.5f, 3.14159f, -2.5f, 0.125f};

    printf("Float to Fixed8 to Float:\n");
    for (int i = 0; i < 5; i++) {
        fixed8_t fixed = float_to_fixed8(test_values[i]);
        float back = fixed8_to_float(fixed);
        printf("  %.5f -> 0x%04X -> %.5f\n",
               test_values[i], (uint16_t)fixed, back);
    }

    // Test arithmetic
    printf("\nArithmetic operations:\n");

    fixed8_t a = float_to_fixed8(2.5f);
    fixed8_t b = float_to_fixed8(1.5f);

    printf("  2.5 + 1.5 = %.4f (expected: 4.0)\n",
           fixed8_to_float(fixed8_add(a, b)));
    printf("  2.5 - 1.5 = %.4f (expected: 1.0)\n",
           fixed8_to_float(fixed8_sub(a, b)));
    printf("  2.5 * 1.5 = %.4f (expected: 3.75)\n",
           fixed8_to_float(fixed8_mul(a, b)));
    printf("  2.5 / 1.5 = %.4f (expected: 1.6667)\n",
           fixed8_to_float(fixed8_div(a, b)));

    printf("\n");
}

/* =============================================================================
 * Exercise 5.5: Software Timer System
 *
 * Implement a simple timer/scheduler system
 * =============================================================================
 */

// Simulated system tick counter
static volatile uint32_t system_ticks = 0;

void sim_tick(void) {
    system_ticks++;
}

uint32_t get_ticks(void) {
    return system_ticks;
}

// Timer structure
typedef struct {
    uint32_t start_tick;
    uint32_t duration;
    bool running;
} SoftTimer;

// TODO: Initialize and start a timer
void timer_start(SoftTimer *timer, uint32_t duration_ticks) {
    (void)timer; (void)duration_ticks;
    // TODO: Record start time and duration, set running
}

// TODO: Check if timer has expired
bool timer_expired(SoftTimer *timer) {
    (void)timer;
    // TODO: Return true if (current_tick - start_tick) >= duration
    // Handle wraparound correctly!
    return false;
}

// TODO: Stop a timer
void timer_stop(SoftTimer *timer) {
    (void)timer;
    // TODO: Set running to false
}

// TODO: Get remaining ticks
uint32_t timer_remaining(SoftTimer *timer) {
    (void)timer;
    // TODO: Return remaining ticks, 0 if expired
    return 0;
}

// Task scheduler
typedef struct {
    const char *name;
    void (*task)(void);
    uint32_t period;
    uint32_t last_run;
} ScheduledTask;

int task1_count = 0;
int task2_count = 0;
int task3_count = 0;

void task1(void) { task1_count++; }
void task2(void) { task2_count++; }
void task3(void) { task3_count++; }

ScheduledTask tasks[] = {
    {"Fast",   task1, 10,  0},
    {"Medium", task2, 50,  0},
    {"Slow",   task3, 100, 0},
    {NULL, NULL, 0, 0}
};

// TODO: Run the scheduler - execute tasks whose period has elapsed
void run_scheduler(void) {
    // TODO: Check each task, run if period elapsed, update last_run
}

void exercise_5_5(void) {
    printf("=== Exercise 5.5: Software Timer System ===\n");

    // Test single timer
    SoftTimer timer;
    system_ticks = 0;

    timer_start(&timer, 100);
    printf("Timer started for 100 ticks\n");

    // Simulate time passing
    for (int i = 0; i < 50; i++) sim_tick();
    printf("After 50 ticks - expired: %s, remaining: %u\n",
           timer_expired(&timer) ? "yes" : "no",
           timer_remaining(&timer));

    for (int i = 0; i < 50; i++) sim_tick();
    printf("After 100 ticks - expired: %s\n",
           timer_expired(&timer) ? "yes" : "no");

    for (int i = 0; i < 10; i++) sim_tick();
    printf("After 110 ticks - expired: %s\n",
           timer_expired(&timer) ? "yes" : "no");

    // Test scheduler
    printf("\nScheduler test (200 ticks):\n");
    system_ticks = 0;
    task1_count = task2_count = task3_count = 0;

    // Initialize task last_run times
    for (int i = 0; tasks[i].task != NULL; i++) {
        tasks[i].last_run = 0;
    }

    // Run for 200 ticks
    for (int tick = 0; tick < 200; tick++) {
        sim_tick();
        run_scheduler();
    }

    printf("Task1 (period 10) ran %d times (expected: ~20)\n", task1_count);
    printf("Task2 (period 50) ran %d times (expected: ~4)\n", task2_count);
    printf("Task3 (period 100) ran %d times (expected: ~2)\n", task3_count);

    printf("\n");
}

/* =============================================================================
 * Exercise 5.6: Double Buffering Pattern
 *
 * Implement double buffering for display data
 * =============================================================================
 */

#define DISPLAY_WIDTH  16
#define DISPLAY_HEIGHT 4

typedef struct {
    char pixels[DISPLAY_HEIGHT][DISPLAY_WIDTH + 1];  // +1 for null terminator
} DisplayBuffer;

static DisplayBuffer display_buffers[2];
static volatile int front_buffer = 0;  // Currently displayed

// TODO: Get the buffer to draw to (back buffer)
DisplayBuffer *get_draw_buffer(void) {
    // TODO: Return pointer to the non-displayed buffer
    return NULL;
}

// TODO: Get the buffer being displayed (front buffer)
DisplayBuffer *get_display_buffer(void) {
    // TODO: Return pointer to the displayed buffer
    return NULL;
}

// TODO: Swap buffers (call after drawing is complete)
void swap_buffers(void) {
    // TODO: Switch which buffer is front
}

// Clear a buffer
void clear_buffer(DisplayBuffer *buf) {
    for (int y = 0; y < DISPLAY_HEIGHT; y++) {
        memset(buf->pixels[y], ' ', DISPLAY_WIDTH);
        buf->pixels[y][DISPLAY_WIDTH] = '\0';
    }
}

// Draw a string to a buffer
void draw_string(DisplayBuffer *buf, int x, int y, const char *str) {
    if (y < 0 || y >= DISPLAY_HEIGHT) return;
    for (int i = 0; str[i] && (x + i) < DISPLAY_WIDTH; i++) {
        if (x + i >= 0) {
            buf->pixels[y][x + i] = str[i];
        }
    }
}

// Print buffer contents
void print_buffer(DisplayBuffer *buf, const char *label) {
    printf("%s:\n", label);
    printf("+");
    for (int i = 0; i < DISPLAY_WIDTH; i++) printf("-");
    printf("+\n");

    for (int y = 0; y < DISPLAY_HEIGHT; y++) {
        printf("|%s|\n", buf->pixels[y]);
    }

    printf("+");
    for (int i = 0; i < DISPLAY_WIDTH; i++) printf("-");
    printf("+\n");
}

void exercise_5_6(void) {
    printf("=== Exercise 5.6: Double Buffering ===\n\n");

    // Initialize both buffers
    clear_buffer(&display_buffers[0]);
    clear_buffer(&display_buffers[1]);
    front_buffer = 0;

    // Draw initial frame to front buffer
    draw_string(&display_buffers[0], 0, 0, "Frame 1");
    draw_string(&display_buffers[0], 0, 1, "Hello World!");

    printf("Initial display:\n");
    DisplayBuffer *display = get_display_buffer();
    if (display) {
        print_buffer(display, "Front Buffer");
    } else {
        printf("get_display_buffer not implemented\n");
    }

    // Draw next frame to back buffer while displaying current
    printf("\nDrawing Frame 2 to back buffer...\n");
    DisplayBuffer *draw = get_draw_buffer();
    if (draw) {
        clear_buffer(draw);
        draw_string(draw, 0, 0, "Frame 2");
        draw_string(draw, 0, 1, "Updated!");
        draw_string(draw, 0, 2, "No tearing :)");
    } else {
        printf("get_draw_buffer not implemented\n");
    }

    // Swap buffers
    printf("Swapping buffers...\n\n");
    swap_buffers();

    display = get_display_buffer();
    if (display) {
        print_buffer(display, "After Swap (new Front)");
    }

    printf("\n");
}

/* =============================================================================
 * Main
 * =============================================================================
 */

int main(void) {
    printf("Module 05: Embedded Patterns\n");
    printf("============================\n\n");

    exercise_5_1();
    exercise_5_2();
    exercise_5_3();
    exercise_5_4();
    exercise_5_5();
    exercise_5_6();

    return 0;
}
