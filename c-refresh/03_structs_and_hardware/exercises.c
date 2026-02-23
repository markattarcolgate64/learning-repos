/**
 * Module 03: Structs and Hardware Exercises
 *
 * Build: make module03
 * Run:   ./bin/module03
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

/* =============================================================================
 * Exercise 3.1: Struct Padding Analysis
 *
 * Predict struct sizes and understand padding
 * =============================================================================
 */

struct Padded1 {
    char a;
    int b;
    char c;
};

struct Padded2 {
    int b;
    char a;
    char c;
};

struct Padded3 {
    char a;
    short b;
    char c;
    int d;
};

void exercise_3_1(void) {
    printf("=== Exercise 3.1: Struct Padding Analysis ===\n");

    // TODO: Before looking at output, predict the sizes:
    // Padded1: ___ bytes (char + int + char with padding)
    // Padded2: ___ bytes (int + char + char with padding)
    // Padded3: ___ bytes (char + short + char + int with padding)

    printf("sizeof(Padded1) = %zu bytes\n", sizeof(struct Padded1));
    printf("sizeof(Padded2) = %zu bytes\n", sizeof(struct Padded2));
    printf("sizeof(Padded3) = %zu bytes\n", sizeof(struct Padded3));

    // Print member offsets
    struct Padded3 p3;
    printf("\nPadded3 member offsets:\n");
    printf("  a: %ld\n", (long)((char*)&p3.a - (char*)&p3));
    printf("  b: %ld\n", (long)((char*)&p3.b - (char*)&p3));
    printf("  c: %ld\n", (long)((char*)&p3.c - (char*)&p3));
    printf("  d: %ld\n", (long)((char*)&p3.d - (char*)&p3));

    printf("\n");
}

/* =============================================================================
 * Exercise 3.2: Packed Sensor Data Structure
 *
 * Create a packed struct for sensor data transmission
 * =============================================================================
 */

/*
 * Design a packet structure for transmitting IMU sensor data:
 * - Header byte: 0xAA
 * - Sequence number: 8-bit
 * - Timestamp: 32-bit (ms since boot)
 * - Accelerometer X, Y, Z: 16-bit signed each
 * - Gyroscope X, Y, Z: 16-bit signed each
 * - Checksum: 8-bit (XOR of all previous bytes)
 *
 * Total should be exactly 18 bytes with no padding
 */

// TODO: Define the packed struct
struct __attribute__((packed)) IMU_Packet {
    // TODO: Add members in the order specified above
    uint8_t placeholder;  // Remove this and add real members
};

// TODO: Calculate XOR checksum of all bytes except the checksum field
uint8_t calculate_checksum(struct IMU_Packet *pkt) {
    (void)pkt;
    // TODO: XOR all bytes from header through gyro_z
    return 0;
}

// TODO: Fill in the packet with given values
void pack_imu_data(struct IMU_Packet *pkt, uint8_t seq, uint32_t timestamp,
                   int16_t ax, int16_t ay, int16_t az,
                   int16_t gx, int16_t gy, int16_t gz) {
    (void)pkt; (void)seq; (void)timestamp;
    (void)ax; (void)ay; (void)az;
    (void)gx; (void)gy; (void)gz;
    // TODO: Fill in all fields including checksum
}

void exercise_3_2(void) {
    printf("=== Exercise 3.2: Packed Sensor Data ===\n");

    printf("sizeof(IMU_Packet) = %zu bytes (expected: 18)\n", sizeof(struct IMU_Packet));

    struct IMU_Packet pkt;
    pack_imu_data(&pkt, 42, 1234567, 100, -200, 9800, 10, -20, 30);

    printf("Packet bytes: ");
    uint8_t *bytes = (uint8_t*)&pkt;
    for (size_t i = 0; i < sizeof(pkt); i++) {
        printf("%02X ", bytes[i]);
    }
    printf("\n");

    // Verify checksum
    uint8_t calc_checksum = calculate_checksum(&pkt);
    printf("Checksum valid: %s\n",
           (sizeof(struct IMU_Packet) > 1) ? "check implementation" : "not implemented");
    (void)calc_checksum;

    printf("\n");
}

/* =============================================================================
 * Exercise 3.3: Union for Type Punning
 *
 * Use unions to inspect binary representations
 * =============================================================================
 */

// TODO: Create a union to inspect float bits
union FloatBits {
    float f;
    uint32_t bits;
    uint8_t bytes[4];
};

// TODO: Extract the sign bit (bit 31)
int float_get_sign(float f) {
    (void)f;
    // TODO: Use union to extract sign bit
    return 0;
}

// TODO: Extract the exponent (bits 30:23)
int float_get_exponent(float f) {
    (void)f;
    // TODO: Use union to extract and unbias the exponent
    // IEEE 754 uses bias of 127
    return 0;
}

// TODO: Check if float is negative zero
int is_negative_zero(float f) {
    (void)f;
    // TODO: -0.0f has bit pattern 0x80000000
    return 0;
}

void exercise_3_3(void) {
    printf("=== Exercise 3.3: Union Type Punning ===\n");

    union FloatBits fb;

    fb.f = 3.14159f;
    printf("Float %.5f has bits: 0x%08X\n", fb.f, fb.bits);
    printf("  Bytes (little-endian): ");
    for (int i = 0; i < 4; i++) {
        printf("%02X ", fb.bytes[i]);
    }
    printf("\n");

    printf("\nSign of 3.14159: %d (expected: 0)\n", float_get_sign(3.14159f));
    printf("Sign of -3.14159: %d (expected: 1)\n", float_get_sign(-3.14159f));

    printf("\nExponent of 8.0: %d (expected: 3, since 8=2^3)\n", float_get_exponent(8.0f));
    printf("Exponent of 0.5: %d (expected: -1, since 0.5=2^-1)\n", float_get_exponent(0.5f));

    printf("\nis_negative_zero(-0.0f): %d (expected: 1)\n", is_negative_zero(-0.0f));
    printf("is_negative_zero(0.0f): %d (expected: 0)\n", is_negative_zero(0.0f));

    printf("\n");
}

/* =============================================================================
 * Exercise 3.4: Register Overlay Pattern
 *
 * Simulate hardware register access using struct/union overlays
 * =============================================================================
 */

/*
 * Timer Control Register (8-bit):
 * Bit 7:    ENABLE  - Timer enable
 * Bit 6:    IRQ_EN  - Interrupt enable
 * Bits 5:4: MODE    - Timer mode (0=one-shot, 1=periodic, 2=PWM, 3=capture)
 * Bits 3:0: PRESCALER - Clock prescaler (0-15)
 */

// TODO: Create a union with raw access and bit field access
typedef union {
    uint8_t raw;
    struct {
        // TODO: Define bit fields
        // Note: Bit field order is implementation-defined
        // On most little-endian systems, list LSB first
        uint8_t placeholder : 8;  // Remove and add real fields
    } bits;
} TimerControl_t;

// Simulated register (in real hardware, this would be a memory-mapped address)
static TimerControl_t sim_timer_ctrl;

// TODO: Initialize timer with given settings
void timer_init(uint8_t prescaler, uint8_t mode, uint8_t irq_enable) {
    (void)prescaler; (void)mode; (void)irq_enable;
    // TODO: Set the bit fields
    sim_timer_ctrl.raw = 0;  // For now, just clear
}

// TODO: Enable the timer
void timer_enable(void) {
    // TODO: Set the ENABLE bit
}

// TODO: Disable the timer
void timer_disable(void) {
    // TODO: Clear the ENABLE bit
}

// TODO: Get current prescaler value
uint8_t timer_get_prescaler(void) {
    // TODO: Return the prescaler field
    return 0;
}

void exercise_3_4(void) {
    printf("=== Exercise 3.4: Register Overlay Pattern ===\n");

    printf("sizeof(TimerControl_t) = %zu (expected: 1)\n", sizeof(TimerControl_t));

    // Initialize: prescaler=5, mode=1 (periodic), IRQ enabled
    timer_init(5, 1, 1);
    printf("After init: raw=0x%02X\n", sim_timer_ctrl.raw);

    timer_enable();
    printf("After enable: raw=0x%02X\n", sim_timer_ctrl.raw);

    printf("Prescaler: %d (expected: 5)\n", timer_get_prescaler());

    timer_disable();
    printf("After disable: raw=0x%02X\n", sim_timer_ctrl.raw);

    printf("\n");
}

/* =============================================================================
 * Exercise 3.5: Message Protocol with Variable Payload
 *
 * Parse and create protocol messages with different payload types
 * =============================================================================
 */

#define MSG_TYPE_PING       0x01
#define MSG_TYPE_SENSOR     0x02
#define MSG_TYPE_MOTOR_CMD  0x03
#define MSG_TYPE_ACK        0x04

// Header for all messages
struct __attribute__((packed)) MessageHeader {
    uint8_t start_byte;   // Always 0xAA
    uint8_t msg_type;
    uint8_t length;       // Payload length
};

// Payload for sensor data message
struct __attribute__((packed)) SensorPayload {
    uint16_t sensor_id;
    int32_t value;
    uint8_t status;
};

// Payload for motor command message
struct __attribute__((packed)) MotorPayload {
    uint8_t motor_id;
    int16_t speed;        // -1000 to +1000
    uint8_t flags;
};

// TODO: Parse a message header from raw bytes
// Return 1 if valid (start_byte == 0xAA), 0 otherwise
int parse_header(const uint8_t *data, struct MessageHeader *header) {
    (void)data; (void)header;
    // TODO: Copy bytes to header struct and validate start_byte
    return 0;
}

// TODO: Parse sensor payload from raw bytes (after header)
void parse_sensor_payload(const uint8_t *data, struct SensorPayload *payload) {
    (void)data; (void)payload;
    // TODO: Copy bytes to payload struct
}

// TODO: Serialize a motor command to bytes
// Returns total message size (header + payload)
int serialize_motor_cmd(uint8_t motor_id, int16_t speed, uint8_t flags,
                        uint8_t *buffer, size_t buffer_size) {
    (void)motor_id; (void)speed; (void)flags;
    (void)buffer; (void)buffer_size;
    // TODO: Write header + payload to buffer
    return 0;
}

void exercise_3_5(void) {
    printf("=== Exercise 3.5: Message Protocol ===\n");

    // Simulate receiving a sensor message
    uint8_t raw_sensor_msg[] = {
        0xAA,             // Start byte
        MSG_TYPE_SENSOR,  // Type
        0x07,             // Payload length
        0x01, 0x00,       // Sensor ID = 1
        0x39, 0x30, 0x00, 0x00,  // Value = 12345
        0x01              // Status = 1
    };

    struct MessageHeader header;
    if (parse_header(raw_sensor_msg, &header)) {
        printf("Valid message received\n");
        printf("  Type: 0x%02X\n", header.msg_type);
        printf("  Payload length: %d\n", header.length);

        if (header.msg_type == MSG_TYPE_SENSOR) {
            struct SensorPayload sensor;
            parse_sensor_payload(raw_sensor_msg + sizeof(struct MessageHeader), &sensor);
            printf("  Sensor ID: %d\n", sensor.sensor_id);
            printf("  Value: %d\n", sensor.value);
            printf("  Status: %d\n", sensor.status);
        }
    } else {
        printf("parse_header not implemented or invalid message\n");
    }

    // Create a motor command
    uint8_t motor_buffer[32];
    int len = serialize_motor_cmd(2, 500, 0x01, motor_buffer, sizeof(motor_buffer));
    printf("\nSerialized motor command (%d bytes): ", len);
    for (int i = 0; i < len && i < 10; i++) {
        printf("%02X ", motor_buffer[i]);
    }
    printf("\n");

    printf("\n");
}

/* =============================================================================
 * Main
 * =============================================================================
 */

int main(void) {
    printf("Module 03: Structs and Hardware\n");
    printf("================================\n\n");

    exercise_3_1();
    exercise_3_2();
    exercise_3_3();
    exercise_3_4();
    exercise_3_5();

    return 0;
}
