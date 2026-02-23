# Module 04: Buffers and State

## Circular Buffers (Ring Buffers)

A circular buffer is a fixed-size buffer that wraps around, commonly used for:
- UART receive/transmit buffers
- Audio sample buffers
- Logging systems
- Producer-consumer queues

```
Write pointer (head) →
                      ┌───┬───┬───┬───┬───┬───┬───┬───┐
                      │ D │ E │ F │   │   │ A │ B │ C │
                      └───┴───┴───┴───┴───┴───┴───┴───┘
                                          ↑
                              Read pointer (tail)
```

### Basic Implementation

```c
#define BUFFER_SIZE 64

typedef struct {
    uint8_t data[BUFFER_SIZE];
    volatile size_t head;  // Write position
    volatile size_t tail;  // Read position
} CircularBuffer;

// Check if buffer is empty
bool buffer_empty(CircularBuffer *buf) {
    return buf->head == buf->tail;
}

// Check if buffer is full
bool buffer_full(CircularBuffer *buf) {
    return ((buf->head + 1) % BUFFER_SIZE) == buf->tail;
}

// Write one byte (returns false if full)
bool buffer_write(CircularBuffer *buf, uint8_t byte) {
    if (buffer_full(buf)) return false;
    buf->data[buf->head] = byte;
    buf->head = (buf->head + 1) % BUFFER_SIZE;
    return true;
}

// Read one byte (returns false if empty)
bool buffer_read(CircularBuffer *buf, uint8_t *byte) {
    if (buffer_empty(buf)) return false;
    *byte = buf->data[buf->tail];
    buf->tail = (buf->tail + 1) % BUFFER_SIZE;
    return true;
}
```

### Power-of-2 Optimization

When buffer size is a power of 2, use bitwise AND instead of modulo:

```c
#define BUFFER_SIZE 64  // Must be power of 2
#define BUFFER_MASK (BUFFER_SIZE - 1)

buf->head = (buf->head + 1) & BUFFER_MASK;  // Faster than % BUFFER_SIZE
```

## Function Pointers

Function pointers store addresses of functions, enabling callbacks and dynamic dispatch.

### Syntax

```c
// Declare a function pointer type
typedef void (*Callback)(int value);

// Declare a variable of that type
Callback my_callback;

// Assign a function to it
void my_handler(int value) {
    printf("Value: %d\n", value);
}
my_callback = my_handler;  // or &my_handler

// Call through the pointer
my_callback(42);  // Prints "Value: 42"
```

### Callback Pattern

```c
typedef void (*EventCallback)(void *context, int event_type);

void register_callback(EventCallback cb, void *ctx) {
    stored_callback = cb;
    stored_context = ctx;
}

// Later, trigger the callback
if (stored_callback) {
    stored_callback(stored_context, EVENT_BUTTON_PRESS);
}
```

### Jump Tables / Dispatch Tables

```c
typedef void (*CommandHandler)(const char *args);

void cmd_help(const char *args);
void cmd_status(const char *args);
void cmd_reset(const char *args);

struct Command {
    const char *name;
    CommandHandler handler;
};

struct Command commands[] = {
    {"help",   cmd_help},
    {"status", cmd_status},
    {"reset",  cmd_reset},
    {NULL,     NULL}  // Sentinel
};

void dispatch(const char *cmd, const char *args) {
    for (int i = 0; commands[i].name != NULL; i++) {
        if (strcmp(cmd, commands[i].name) == 0) {
            commands[i].handler(args);
            return;
        }
    }
    printf("Unknown command\n");
}
```

## State Machines

State machines are essential for robotics: controlling behavior, parsing protocols, debouncing inputs.

### Simple State Machine Pattern

```c
typedef enum {
    STATE_IDLE,
    STATE_MOVING,
    STATE_GRABBING,
    STATE_RETURNING
} RobotState;

typedef enum {
    EVENT_START,
    EVENT_TARGET_FOUND,
    EVENT_ARRIVED,
    EVENT_GRABBED,
    EVENT_HOME
} RobotEvent;

RobotState current_state = STATE_IDLE;

void handle_event(RobotEvent event) {
    switch (current_state) {
        case STATE_IDLE:
            if (event == EVENT_START) {
                current_state = STATE_MOVING;
                start_motors();
            }
            break;

        case STATE_MOVING:
            if (event == EVENT_TARGET_FOUND) {
                current_state = STATE_GRABBING;
                activate_gripper();
            }
            break;

        case STATE_GRABBING:
            if (event == EVENT_GRABBED) {
                current_state = STATE_RETURNING;
                reverse_direction();
            }
            break;

        case STATE_RETURNING:
            if (event == EVENT_HOME) {
                current_state = STATE_IDLE;
                stop_motors();
                release_gripper();
            }
            break;
    }
}
```

### Table-Driven State Machine

More scalable for complex state machines:

```c
typedef void (*StateHandler)(RobotEvent event);

void state_idle(RobotEvent event);
void state_moving(RobotEvent event);
void state_grabbing(RobotEvent event);
void state_returning(RobotEvent event);

StateHandler state_handlers[] = {
    [STATE_IDLE] = state_idle,
    [STATE_MOVING] = state_moving,
    [STATE_GRABBING] = state_grabbing,
    [STATE_RETURNING] = state_returning,
};

void handle_event(RobotEvent event) {
    state_handlers[current_state](event);
}
```

### State Machine with Entry/Exit Actions

```c
typedef struct {
    void (*on_enter)(void);
    void (*on_event)(RobotEvent event);
    void (*on_exit)(void);
} State;

State states[] = {
    [STATE_IDLE] = {
        .on_enter = idle_enter,
        .on_event = idle_event,
        .on_exit = idle_exit
    },
    // ... other states
};

void transition_to(RobotState new_state) {
    if (states[current_state].on_exit) {
        states[current_state].on_exit();
    }
    current_state = new_state;
    if (states[current_state].on_enter) {
        states[current_state].on_enter();
    }
}
```

## Button Debouncing Example

A practical state machine for hardware input:

```c
typedef enum {
    BTN_IDLE,
    BTN_DEBOUNCING,
    BTN_PRESSED,
    BTN_HELD
} ButtonState;

typedef struct {
    ButtonState state;
    uint32_t state_enter_time;
    bool last_raw;
} Button;

#define DEBOUNCE_MS 20
#define HOLD_MS     500

void button_update(Button *btn, bool raw_pressed, uint32_t now_ms) {
    switch (btn->state) {
        case BTN_IDLE:
            if (raw_pressed) {
                btn->state = BTN_DEBOUNCING;
                btn->state_enter_time = now_ms;
            }
            break;

        case BTN_DEBOUNCING:
            if (!raw_pressed) {
                btn->state = BTN_IDLE;
            } else if (now_ms - btn->state_enter_time >= DEBOUNCE_MS) {
                btn->state = BTN_PRESSED;
                on_button_pressed();  // Callback
            }
            break;

        case BTN_PRESSED:
            if (!raw_pressed) {
                btn->state = BTN_IDLE;
                on_button_released();
            } else if (now_ms - btn->state_enter_time >= HOLD_MS) {
                btn->state = BTN_HELD;
                on_button_held();
            }
            break;

        case BTN_HELD:
            if (!raw_pressed) {
                btn->state = BTN_IDLE;
                on_button_released();
            }
            break;
    }
}
```
