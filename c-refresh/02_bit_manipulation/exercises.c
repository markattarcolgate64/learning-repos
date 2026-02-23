/**
 * Module 02: Bit Manipulation Exercises
 *
 * Build: make module02
 * Run:   ./bin/module02
 */

#include <stdio.h>
#include <stdint.h>

/* =============================================================================
 * Exercise 2.1: Bit Manipulation Macros
 *
 * Implement the fundamental bit manipulation macros
 * =============================================================================
 */

// TODO: Implement these macros
#define BIT(n)                  (0)  // Create mask with bit n set
#define SET_BIT(reg, bit)       (0)  // Set bit in reg
#define CLEAR_BIT(reg, bit)     (0)  // Clear bit in reg
#define TOGGLE_BIT(reg, bit)    (0)  // Toggle bit in reg
#define CHECK_BIT(reg, bit)     (0)  // Return 1 if bit is set, 0 otherwise

void exercise_2_1(void) {
    printf("=== Exercise 2.1: Bit Manipulation Macros ===\n");

    uint8_t reg = 0x00;

    // Test SET_BIT
    reg = 0x00;
    SET_BIT(reg, 3);
    printf("SET_BIT(0x00, 3) = 0x%02X (expected: 0x08)\n", reg);

    // Test CLEAR_BIT
    reg = 0xFF;
    CLEAR_BIT(reg, 3);
    printf("CLEAR_BIT(0xFF, 3) = 0x%02X (expected: 0xF7)\n", reg);

    // Test TOGGLE_BIT
    reg = 0x08;
    TOGGLE_BIT(reg, 3);
    printf("TOGGLE_BIT(0x08, 3) = 0x%02X (expected: 0x00)\n", reg);
    TOGGLE_BIT(reg, 3);
    printf("TOGGLE_BIT(0x00, 3) = 0x%02X (expected: 0x08)\n", reg);

    // Test CHECK_BIT
    reg = 0x08;
    printf("CHECK_BIT(0x08, 3) = %d (expected: 1)\n", CHECK_BIT(reg, 3));
    printf("CHECK_BIT(0x08, 2) = %d (expected: 0)\n", CHECK_BIT(reg, 2));

    printf("\n");
}

/* =============================================================================
 * Exercise 2.2: Simulated GPIO Control
 *
 * Control a simulated 8-bit GPIO port for an LED and button
 * =============================================================================
 */

// Simulated hardware registers
static uint8_t GPIO_PORT = 0x00;    // Output register
static uint8_t GPIO_DDR = 0x00;     // Data Direction Register (1=output, 0=input)
static uint8_t GPIO_PIN = 0x00;     // Input register (simulated external input)

// Pin assignments
#define LED_RED     0
#define LED_GREEN   1
#define LED_BLUE    2
#define BUZZER      3
#define BUTTON_A    4
#define BUTTON_B    5
#define SENSOR      6
#define MOTOR       7

// TODO: Configure pin as output (set bit in DDR)
void gpio_set_output(uint8_t pin) {
    (void)pin; // Remove this line when implementing
    // TODO: Set the pin bit in GPIO_DDR
}

// TODO: Configure pin as input (clear bit in DDR)
void gpio_set_input(uint8_t pin) {
    (void)pin;
    // TODO: Clear the pin bit in GPIO_DDR
}

// TODO: Set pin high
void gpio_write_high(uint8_t pin) {
    (void)pin;
    // TODO: Set the pin bit in GPIO_PORT
}

// TODO: Set pin low
void gpio_write_low(uint8_t pin) {
    (void)pin;
    // TODO: Clear the pin bit in GPIO_PORT
}

// TODO: Toggle pin state
void gpio_toggle(uint8_t pin) {
    (void)pin;
    // TODO: Toggle the pin bit in GPIO_PORT
}

// TODO: Read pin state (from GPIO_PIN for inputs, GPIO_PORT for outputs)
uint8_t gpio_read(uint8_t pin) {
    (void)pin;
    // TODO: Return 1 if pin is high, 0 if low
    // Use GPIO_PIN for reading external state
    return 0;
}

void exercise_2_2(void) {
    printf("=== Exercise 2.2: Simulated GPIO Control ===\n");

    // Reset registers
    GPIO_PORT = 0x00;
    GPIO_DDR = 0x00;
    GPIO_PIN = 0x00;

    // Configure LEDs and buzzer as outputs
    gpio_set_output(LED_RED);
    gpio_set_output(LED_GREEN);
    gpio_set_output(LED_BLUE);
    gpio_set_output(BUZZER);

    // Configure buttons and sensor as inputs
    gpio_set_input(BUTTON_A);
    gpio_set_input(BUTTON_B);
    gpio_set_input(SENSOR);

    printf("DDR after config: 0x%02X (expected: 0x0F - lower 4 bits as outputs)\n", GPIO_DDR);

    // Turn on red LED
    gpio_write_high(LED_RED);
    printf("PORT after LED_RED on: 0x%02X (expected: 0x01)\n", GPIO_PORT);

    // Turn on all LEDs
    gpio_write_high(LED_GREEN);
    gpio_write_high(LED_BLUE);
    printf("PORT after all LEDs on: 0x%02X (expected: 0x07)\n", GPIO_PORT);

    // Toggle red LED
    gpio_toggle(LED_RED);
    printf("PORT after toggle RED: 0x%02X (expected: 0x06)\n", GPIO_PORT);

    // Simulate button press (external input)
    GPIO_PIN = 0x10;  // Button A pressed
    printf("Button A state: %d (expected: 1)\n", gpio_read(BUTTON_A));
    printf("Button B state: %d (expected: 0)\n", gpio_read(BUTTON_B));

    printf("\n");
}

/* =============================================================================
 * Exercise 2.3: Bit Field Extraction and Packing
 *
 * Work with a motor controller status register
 * =============================================================================
 */

/*
 * Motor Status Register (8 bits):
 * +---+---+---+---+---+---+---+---+
 * | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
 * +---+---+---+---+---+---+---+---+
 *   |   |   |   |   |   |   |   |
 *   |   |   |   |   +---+---+---+-- Error code (4 bits, 0-15)
 *   |   |   +---+------------------ Speed level (2 bits, 0-3)
 *   |   +-------------------------- Direction (1 bit, 0=CW, 1=CCW)
 *   +------------------------------ Running (1 bit, 0=stopped, 1=running)
 */

#define ERROR_MASK      0x0F
#define ERROR_SHIFT     0
#define SPEED_MASK      0x30
#define SPEED_SHIFT     4
#define DIRECTION_BIT   6
#define RUNNING_BIT     7

// TODO: Extract error code from status register
uint8_t get_error_code(uint8_t status) {
    (void)status;
    // TODO: Mask and shift to extract bits 3:0
    return 0;
}

// TODO: Extract speed level from status register
uint8_t get_speed_level(uint8_t status) {
    (void)status;
    // TODO: Mask and shift to extract bits 5:4
    return 0;
}

// TODO: Check if motor is running
uint8_t is_running(uint8_t status) {
    (void)status;
    // TODO: Check bit 7
    return 0;
}

// TODO: Get direction (0=CW, 1=CCW)
uint8_t get_direction(uint8_t status) {
    (void)status;
    // TODO: Check bit 6
    return 0;
}

// TODO: Pack values into status register
uint8_t pack_status(uint8_t running, uint8_t direction, uint8_t speed, uint8_t error) {
    (void)running; (void)direction; (void)speed; (void)error;
    // TODO: Combine all fields into one byte
    // running in bit 7, direction in bit 6, speed in bits 5:4, error in bits 3:0
    return 0;
}

void exercise_2_3(void) {
    printf("=== Exercise 2.3: Bit Field Extraction ===\n");

    // Status: running=1, direction=1(CCW), speed=2, error=5
    // Binary: 1 1 10 0101 = 0xE5
    uint8_t status = 0xE5;

    printf("Status register: 0x%02X\n", status);
    printf("Error code: %d (expected: 5)\n", get_error_code(status));
    printf("Speed level: %d (expected: 2)\n", get_speed_level(status));
    printf("Running: %d (expected: 1)\n", is_running(status));
    printf("Direction: %d (expected: 1=CCW)\n", get_direction(status));

    // Pack a new status
    uint8_t new_status = pack_status(1, 0, 3, 0);  // running, CW, max speed, no error
    printf("\nPacked status: 0x%02X (expected: 0xB0)\n", new_status);

    printf("\n");
}

/* =============================================================================
 * Exercise 2.4: Bit Counting and Power of 2
 *
 * Implement common bit manipulation algorithms
 * =============================================================================
 */

// TODO: Count the number of set bits (population count)
int popcount(uint32_t x) {
    (void)x;
    // TODO: Count how many bits are 1
    // Simple approach: loop through each bit
    return 0;
}

// TODO: Check if x is a power of 2
int is_power_of_2(uint32_t x) {
    (void)x;
    // TODO: A power of 2 has exactly one bit set
    // Hint: x & (x-1) clears the lowest set bit
    return 0;
}

// TODO: Find the next power of 2 >= x
uint32_t next_power_of_2(uint32_t x) {
    (void)x;
    // TODO: Round up to nearest power of 2
    // Hint: Subtract 1, then propagate the highest bit down, then add 1
    return 0;
}

// TODO: Return position of lowest set bit (0-indexed), or -1 if x is 0
int lowest_set_bit(uint32_t x) {
    (void)x;
    // TODO: Find the position of the rightmost 1 bit
    return -1;
}

void exercise_2_4(void) {
    printf("=== Exercise 2.4: Bit Counting and Power of 2 ===\n");

    printf("popcount(0b10110101) = %d (expected: 5)\n", popcount(0b10110101));
    printf("popcount(0xFFFF) = %d (expected: 16)\n", popcount(0xFFFF));
    printf("popcount(0) = %d (expected: 0)\n", popcount(0));

    printf("\nis_power_of_2(16) = %d (expected: 1)\n", is_power_of_2(16));
    printf("is_power_of_2(17) = %d (expected: 0)\n", is_power_of_2(17));
    printf("is_power_of_2(1) = %d (expected: 1)\n", is_power_of_2(1));
    printf("is_power_of_2(0) = %d (expected: 0)\n", is_power_of_2(0));

    printf("\nnext_power_of_2(5) = %u (expected: 8)\n", next_power_of_2(5));
    printf("next_power_of_2(16) = %u (expected: 16)\n", next_power_of_2(16));
    printf("next_power_of_2(17) = %u (expected: 32)\n", next_power_of_2(17));

    printf("\nlowest_set_bit(0b10100) = %d (expected: 2)\n", lowest_set_bit(0b10100));
    printf("lowest_set_bit(0b10000) = %d (expected: 4)\n", lowest_set_bit(0b10000));
    printf("lowest_set_bit(1) = %d (expected: 0)\n", lowest_set_bit(1));

    printf("\n");
}

/* =============================================================================
 * Exercise 2.5: RGB LED PWM Simulation
 *
 * Pack and unpack RGB values using bit manipulation
 * =============================================================================
 */

/*
 * 24-bit RGB color format:
 * +--------+--------+--------+
 * |   R    |   G    |   B    |
 * +--------+--------+--------+
 *  23    16 15     8 7      0
 */

// TODO: Pack R, G, B values into a 24-bit color
uint32_t rgb_pack(uint8_t r, uint8_t g, uint8_t b) {
    (void)r; (void)g; (void)b;
    // TODO: R in bits 23:16, G in bits 15:8, B in bits 7:0
    return 0;
}

// TODO: Extract red component
uint8_t rgb_get_red(uint32_t color) {
    (void)color;
    return 0;
}

// TODO: Extract green component
uint8_t rgb_get_green(uint32_t color) {
    (void)color;
    return 0;
}

// TODO: Extract blue component
uint8_t rgb_get_blue(uint32_t color) {
    (void)color;
    return 0;
}

// TODO: Blend two colors (average each component)
uint32_t rgb_blend(uint32_t color1, uint32_t color2) {
    (void)color1; (void)color2;
    // TODO: Average each R, G, B component separately
    return 0;
}

void exercise_2_5(void) {
    printf("=== Exercise 2.5: RGB Color Manipulation ===\n");

    uint32_t red = rgb_pack(255, 0, 0);
    uint32_t green = rgb_pack(0, 255, 0);
    uint32_t blue = rgb_pack(0, 0, 255);
    uint32_t white = rgb_pack(255, 255, 255);

    printf("Red:   0x%06X (expected: 0xFF0000)\n", red);
    printf("Green: 0x%06X (expected: 0x00FF00)\n", green);
    printf("Blue:  0x%06X (expected: 0x0000FF)\n", blue);
    printf("White: 0x%06X (expected: 0xFFFFFF)\n", white);

    uint32_t color = 0xAB12CD;
    printf("\nColor 0x%06X components:\n", color);
    printf("  Red:   %d (expected: 171)\n", rgb_get_red(color));
    printf("  Green: %d (expected: 18)\n", rgb_get_green(color));
    printf("  Blue:  %d (expected: 205)\n", rgb_get_blue(color));

    uint32_t blended = rgb_blend(0xFF0000, 0x0000FF);  // Red + Blue
    printf("\nBlend red+blue: 0x%06X (expected: 0x7F007F)\n", blended);

    printf("\n");
}

/* =============================================================================
 * Main
 * =============================================================================
 */

int main(void) {
    printf("Module 02: Bit Manipulation\n");
    printf("===========================\n\n");

    exercise_2_1();
    exercise_2_2();
    exercise_2_3();
    exercise_2_4();
    exercise_2_5();

    return 0;
}
