/**
 * Module 04: Buffers and State Exercises
 *
 * Build: make module04
 * Run:   ./bin/module04
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

/* =============================================================================
 * Exercise 4.1: Basic Circular Buffer
 *
 * Implement a circular buffer for bytes
 * =============================================================================
 */

#define BUFFER_SIZE 8  // Small for easy testing

typedef struct {
    uint8_t data[BUFFER_SIZE];
    size_t head;  // Write position
    size_t tail;  // Read position
} CircularBuffer;

// TODO: Initialize the buffer
void buffer_init(CircularBuffer *buf) {
    (void)buf;
    // TODO: Set head and tail to 0
}

// TODO: Check if buffer is empty
bool buffer_empty(CircularBuffer *buf) {
    (void)buf;
    // TODO: Empty when head == tail
    return true;
}

// TODO: Check if buffer is full
// Note: We sacrifice one slot to distinguish full from empty
bool buffer_full(CircularBuffer *buf) {
    (void)buf;
    // TODO: Full when (head + 1) % SIZE == tail
    return false;
}

// TODO: Get number of bytes in buffer
size_t buffer_count(CircularBuffer *buf) {
    (void)buf;
    // TODO: Handle wraparound case
    return 0;
}

// TODO: Write one byte, return true on success
bool buffer_write(CircularBuffer *buf, uint8_t byte) {
    (void)buf; (void)byte;
    // TODO: Check if full, write byte, advance head
    return false;
}

// TODO: Read one byte, return true on success
bool buffer_read(CircularBuffer *buf, uint8_t *byte) {
    (void)buf; (void)byte;
    // TODO: Check if empty, read byte, advance tail
    return false;
}

// TODO: Peek at next byte without removing it
bool buffer_peek(CircularBuffer *buf, uint8_t *byte) {
    (void)buf; (void)byte;
    // TODO: Like read but don't advance tail
    return false;
}

void exercise_4_1(void) {
    printf("=== Exercise 4.1: Basic Circular Buffer ===\n");

    CircularBuffer buf;
    buffer_init(&buf);

    printf("Empty after init: %s (expected: true)\n",
           buffer_empty(&buf) ? "true" : "false");

    // Write some data
    for (uint8_t i = 1; i <= 5; i++) {
        bool ok = buffer_write(&buf, i * 10);
        printf("Write %d: %s\n", i * 10, ok ? "ok" : "failed");
    }

    printf("Count: %zu (expected: 5)\n", buffer_count(&buf));
    printf("Full: %s (expected: false)\n", buffer_full(&buf) ? "true" : "false");

    // Fill remaining space (remember, one slot is sacrificed)
    buffer_write(&buf, 60);
    buffer_write(&buf, 70);
    printf("Full after 7 writes: %s (expected: true)\n",
           buffer_full(&buf) ? "true" : "false");

    // Try to write when full
    bool overflow = buffer_write(&buf, 80);
    printf("Write when full: %s (expected: failed)\n",
           overflow ? "ok" : "failed");

    // Read all data
    printf("\nReading: ");
    uint8_t byte;
    while (buffer_read(&buf, &byte)) {
        printf("%d ", byte);
    }
    printf("(expected: 10 20 30 40 50 60 70)\n");

    printf("Empty after reading all: %s (expected: true)\n\n",
           buffer_empty(&buf) ? "true" : "false");
}

/* =============================================================================
 * Exercise 4.2: UART-style Buffer with ISR Simulation
 *
 * Simulate interrupt-driven UART receive buffer
 * =============================================================================
 */

// Global buffer simulating UART RX buffer
static CircularBuffer uart_rx_buffer;

// Simulated ISR - called when a byte is "received"
void uart_rx_isr(uint8_t byte) {
    // In real code, this runs in interrupt context
    if (!buffer_write(&uart_rx_buffer, byte)) {
        // Buffer overflow - byte is lost
        printf("[ISR] Overflow! Lost byte: 0x%02X\n", byte);
    }
}

// TODO: Check if data is available
bool uart_available(void) {
    // TODO: Return true if buffer has data
    return false;
}

// TODO: Read one byte (blocking-style, but we'll poll)
int uart_read_byte(void) {
    // TODO: Return byte if available, -1 if not
    return -1;
}

// TODO: Read multiple bytes into buffer
size_t uart_read(uint8_t *dest, size_t max_len) {
    (void)dest; (void)max_len;
    // TODO: Read up to max_len bytes, return actual count
    return 0;
}

void exercise_4_2(void) {
    printf("=== Exercise 4.2: UART Buffer Simulation ===\n");

    buffer_init(&uart_rx_buffer);

    // Simulate receiving "Hello" via interrupts
    const char *msg = "Hello";
    printf("Simulating ISR receiving: \"%s\"\n", msg);
    for (size_t i = 0; i < strlen(msg); i++) {
        uart_rx_isr((uint8_t)msg[i]);
    }

    printf("Data available: %s (expected: true)\n",
           uart_available() ? "true" : "false");

    // Read character by character
    printf("Reading bytes: ");
    int ch;
    while ((ch = uart_read_byte()) != -1) {
        printf("%c", ch);
    }
    printf(" (expected: Hello)\n");

    // Test bulk read
    buffer_init(&uart_rx_buffer);
    const char *msg2 = "World!";
    for (size_t i = 0; i < strlen(msg2); i++) {
        uart_rx_isr((uint8_t)msg2[i]);
    }

    uint8_t read_buf[10] = {0};
    size_t n = uart_read(read_buf, sizeof(read_buf));
    printf("Bulk read %zu bytes: %s (expected: World!)\n\n", n, read_buf);
}

/* =============================================================================
 * Exercise 4.3: Function Pointers and Callbacks
 *
 * Implement a callback system for button events
 * =============================================================================
 */

typedef void (*ButtonCallback)(int button_id, bool pressed);

#define MAX_CALLBACKS 4

static ButtonCallback button_callbacks[MAX_CALLBACKS];
static int num_callbacks = 0;

// TODO: Register a callback function
bool register_button_callback(ButtonCallback cb) {
    (void)cb;
    // TODO: Add callback to array if space available
    return false;
}

// TODO: Notify all callbacks of a button event
void notify_button_event(int button_id, bool pressed) {
    (void)button_id; (void)pressed;
    // TODO: Call each registered callback
}

// Example callback functions
void led_handler(int button_id, bool pressed) {
    printf("  LED handler: button %d %s\n",
           button_id, pressed ? "pressed" : "released");
}

void buzzer_handler(int button_id, bool pressed) {
    if (pressed) {
        printf("  Buzzer handler: beep for button %d\n", button_id);
    }
}

void log_handler(int button_id, bool pressed) {
    printf("  Log handler: button=%d, state=%d\n", button_id, pressed);
}

void exercise_4_3(void) {
    printf("=== Exercise 4.3: Function Pointers and Callbacks ===\n");

    num_callbacks = 0;  // Reset

    // Register handlers
    register_button_callback(led_handler);
    register_button_callback(buzzer_handler);
    register_button_callback(log_handler);

    printf("Registered %d callbacks\n\n", num_callbacks);

    // Simulate button press
    printf("Button 1 pressed:\n");
    notify_button_event(1, true);

    printf("\nButton 1 released:\n");
    notify_button_event(1, false);

    printf("\n");
}

/* =============================================================================
 * Exercise 4.4: Command Dispatcher with Jump Table
 *
 * Implement a command parser using function pointers
 * =============================================================================
 */

typedef void (*CommandFunc)(const char *args);

typedef struct {
    const char *name;
    const char *help;
    CommandFunc func;
} Command;

// Command implementations
void cmd_help(const char *args);
void cmd_led(const char *args);
void cmd_motor(const char *args);
void cmd_status(const char *args);

// TODO: Define the command table
Command commands[] = {
    // TODO: Add command entries: {"name", "help text", function_pointer}
    // Example: {"help", "Show available commands", cmd_help},
    {NULL, NULL, NULL}  // Sentinel - marks end of array
};

void cmd_help(const char *args) {
    (void)args;
    printf("Available commands:\n");
    for (int i = 0; commands[i].name != NULL; i++) {
        printf("  %-10s - %s\n", commands[i].name,
               commands[i].help ? commands[i].help : "No description");
    }
}

void cmd_led(const char *args) {
    printf("LED command with args: '%s'\n", args ? args : "");
}

void cmd_motor(const char *args) {
    printf("Motor command with args: '%s'\n", args ? args : "");
}

void cmd_status(const char *args) {
    (void)args;
    printf("System status: OK\n");
}

// TODO: Find and execute a command by name
void dispatch_command(const char *cmd_name, const char *args) {
    (void)cmd_name; (void)args;
    // TODO: Search commands array for matching name
    // If found, call the function with args
    // If not found, print "Unknown command"
    printf("dispatch_command not implemented\n");
}

void exercise_4_4(void) {
    printf("=== Exercise 4.4: Command Dispatcher ===\n");

    dispatch_command("help", NULL);
    printf("\n");

    dispatch_command("led", "on");
    dispatch_command("motor", "speed 50");
    dispatch_command("status", NULL);
    dispatch_command("unknown", NULL);

    printf("\n");
}

/* =============================================================================
 * Exercise 4.5: State Machine - Traffic Light Controller
 *
 * Implement a simple traffic light state machine
 * =============================================================================
 */

typedef enum {
    LIGHT_RED,
    LIGHT_RED_YELLOW,  // Some countries show red+yellow before green
    LIGHT_GREEN,
    LIGHT_YELLOW,
    LIGHT_NUM_STATES
} LightState;

typedef enum {
    EVENT_TIMER,       // Timer expired
    EVENT_PEDESTRIAN,  // Pedestrian button pressed
    EVENT_EMERGENCY,   // Emergency vehicle detected
    EVENT_CLEAR        // Emergency cleared
} LightEvent;

static LightState current_light_state = LIGHT_RED;
static bool emergency_mode = false;

const char *state_names[] = {
    "RED", "RED+YELLOW", "GREEN", "YELLOW"
};

// TODO: Implement state transitions
// Normal cycle: RED -> RED_YELLOW -> GREEN -> YELLOW -> RED
// Emergency: Any state -> RED (and stay there until cleared)
LightState get_next_state(LightState current, LightEvent event) {
    (void)current; (void)event;

    // TODO: Implement state transition logic
    // Handle both normal timer events and emergency events

    return current;  // No change by default
}

// TODO: Process an event and update state
void traffic_light_event(LightEvent event) {
    (void)event;

    // TODO: Call get_next_state and update current_light_state
    // Print state transitions
}

void exercise_4_5(void) {
    printf("=== Exercise 4.5: Traffic Light State Machine ===\n");

    current_light_state = LIGHT_RED;
    emergency_mode = false;

    printf("Initial state: %s\n\n", state_names[current_light_state]);

    printf("Normal cycle:\n");
    traffic_light_event(EVENT_TIMER);  // RED -> RED_YELLOW
    traffic_light_event(EVENT_TIMER);  // RED_YELLOW -> GREEN
    traffic_light_event(EVENT_TIMER);  // GREEN -> YELLOW
    traffic_light_event(EVENT_TIMER);  // YELLOW -> RED

    printf("\nEmergency during GREEN:\n");
    current_light_state = LIGHT_GREEN;
    printf("Current: %s\n", state_names[current_light_state]);
    traffic_light_event(EVENT_EMERGENCY);  // -> RED
    traffic_light_event(EVENT_TIMER);      // Stay RED
    traffic_light_event(EVENT_CLEAR);      // Can resume

    printf("\n");
}

/* =============================================================================
 * Exercise 4.6: Robot Behavior State Machine
 *
 * Implement a state machine for a simple pick-and-place robot
 * =============================================================================
 */

typedef enum {
    ROBOT_IDLE,
    ROBOT_SEARCHING,
    ROBOT_APPROACHING,
    ROBOT_GRABBING,
    ROBOT_RETURNING,
    ROBOT_DROPPING,
    ROBOT_NUM_STATES
} RobotState;

typedef enum {
    ROBOT_EVT_START,
    ROBOT_EVT_OBJECT_FOUND,
    ROBOT_EVT_ARRIVED,
    ROBOT_EVT_GRABBED,
    ROBOT_EVT_HOME,
    ROBOT_EVT_DROPPED,
    ROBOT_EVT_ERROR
} RobotEvent;

static RobotState robot_state = ROBOT_IDLE;

const char *robot_state_names[] = {
    "IDLE", "SEARCHING", "APPROACHING", "GRABBING", "RETURNING", "DROPPING"
};

const char *robot_event_names[] = {
    "START", "OBJECT_FOUND", "ARRIVED", "GRABBED", "HOME", "DROPPED", "ERROR"
};

// Action functions (simulated)
void robot_start_search(void) { printf("  [Action] Starting search pattern\n"); }
void robot_move_to_target(void) { printf("  [Action] Moving to target\n"); }
void robot_activate_gripper(void) { printf("  [Action] Activating gripper\n"); }
void robot_return_home(void) { printf("  [Action] Returning to home position\n"); }
void robot_release_gripper(void) { printf("  [Action] Releasing gripper\n"); }
void robot_stop_all(void) { printf("  [Action] Emergency stop!\n"); }

// TODO: Implement the robot state machine
void robot_handle_event(RobotEvent event) {
    printf("State: %s, Event: %s\n",
           robot_state_names[robot_state],
           robot_event_names[event]);

    // TODO: Implement state transitions with appropriate actions
    // IDLE + START -> SEARCHING (call robot_start_search)
    // SEARCHING + OBJECT_FOUND -> APPROACHING (call robot_move_to_target)
    // APPROACHING + ARRIVED -> GRABBING (call robot_activate_gripper)
    // GRABBING + GRABBED -> RETURNING (call robot_return_home)
    // RETURNING + HOME -> DROPPING (call robot_release_gripper)
    // DROPPING + DROPPED -> IDLE
    // Any state + ERROR -> IDLE (call robot_stop_all)

    printf("  -> New state: %s\n\n", robot_state_names[robot_state]);
}

void exercise_4_6(void) {
    printf("=== Exercise 4.6: Robot State Machine ===\n\n");

    robot_state = ROBOT_IDLE;

    // Normal operation sequence
    robot_handle_event(ROBOT_EVT_START);
    robot_handle_event(ROBOT_EVT_OBJECT_FOUND);
    robot_handle_event(ROBOT_EVT_ARRIVED);
    robot_handle_event(ROBOT_EVT_GRABBED);
    robot_handle_event(ROBOT_EVT_HOME);
    robot_handle_event(ROBOT_EVT_DROPPED);

    printf("--- Testing error handling ---\n\n");

    robot_state = ROBOT_APPROACHING;
    robot_handle_event(ROBOT_EVT_ERROR);
}

/* =============================================================================
 * Main
 * =============================================================================
 */

int main(void) {
    printf("Module 04: Buffers and State\n");
    printf("============================\n\n");

    exercise_4_1();
    exercise_4_2();
    exercise_4_3();
    exercise_4_4();
    exercise_4_5();
    exercise_4_6();

    return 0;
}
