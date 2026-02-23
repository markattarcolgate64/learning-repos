/**
 * Module 01: Memory and Pointers Exercises
 *
 * Build: make module01
 * Run:   ./bin/module01
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

/* =============================================================================
 * Exercise 1.1: Memory Regions
 *
 * Identify which memory region each variable lives in.
 * Print the address and determine: stack, heap, data, or bss
 * =============================================================================
 */

int global_initialized = 42;      // Data segment
int global_uninitialized;         // BSS segment

void exercise_1_1(void) {
    printf("=== Exercise 1.1: Memory Regions ===\n");

    int local_var = 10;
    static int static_var = 20;
    int *heap_var = malloc(sizeof(int));
    *heap_var = 30; 

    printf("global_initialized: %p\n", (void*)&global_initialized);
    printf("global_uninitialized: %p\n", (void*)&global_uninitialized);
    printf("local_var: %p\n", (void*)&local_var);
    printf("static_var: %p\n", (void*)&static_var);
    printf("heap_var points to: %p\n", (void*)heap_var);

    // TODO: Based on the addresses, identify which region each variable is in
    // Hint: Stack addresses are typically high, heap is lower, data/bss even lower
    // Print your analysis below:
    printf("\nYour analysis:\n");
    printf("global_initialized is in: _____ segment\n");
    printf("global_uninitialized is in: _____ segment\n");
    printf("local_var is in: stack segment\n");
    printf("static_var is in:  segment\n");
    printf("*heap_var is in: heap segment\n");

    free(heap_var);
    printf("\n");
}

/* =============================================================================
 * Exercise 1.2: Pointer Arithmetic
 *
 * Complete the functions using ONLY pointer arithmetic (no [] notation)
 * =============================================================================
 */

// TODO: Return the sum of all elements using pointer arithmetic
int sum_array(int *arr, int size) {
    int sum = 0;
    // TODO: Implement using pointer arithmetic
    // Hint: Use a pointer to traverse, increment with ptr++

    return sum;
}

// TODO: Reverse the array in-place using pointers
void reverse_array(int *arr, int size) {
    // TODO: Use two pointers (start and end), swap and move toward center
    // Hint: int *start = arr; int *end = arr + size - 1;

}

void exercise_1_2(void) {
    printf("=== Exercise 1.2: Pointer Arithmetic ===\n");

    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);

    printf("Sum: %d (expected: 15)\n", sum_array(arr, size));

    reverse_array(arr, size);
    printf("Reversed: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("(expected: 5 4 3 2 1)\n\n");
}

/* =============================================================================
 * Exercise 1.3: Struct Padding
 *
 * Predict and verify struct sizes with different member ordering
 * =============================================================================
 */

struct SensorData_Bad {
    uint8_t id;           // 1 byte
    uint32_t timestamp;   // 4 bytes
    uint8_t status;       // 1 byte
    uint16_t value;       // 2 bytes
};

struct SensorData_Good {
    uint32_t timestamp;   // 4 bytes
    uint16_t value;       // 2 bytes
    uint8_t id;           // 1 byte
    uint8_t status;       // 1 byte
};

void exercise_1_3(void) {
    printf("=== Exercise 1.3: Struct Padding ===\n");

    // TODO: Before running, predict the sizes:
    // SensorData_Bad predicted size: ___ bytes
    // SensorData_Good predicted size: ___ bytes

    printf("SensorData_Bad size: %zu bytes\n", sizeof(struct SensorData_Bad));
    printf("SensorData_Good size: %zu bytes\n", sizeof(struct SensorData_Good));

    // TODO: Calculate the padding in SensorData_Bad
    // Draw the memory layout showing where padding bytes are inserted
    printf("\nDraw the memory layout of SensorData_Bad:\n");
    printf("Offset 0: id (1 byte)\n");
    printf("Offset 1-3: ??? \n");
    printf("Offset 4-7: ???\n");
    printf("... complete the layout ...\n\n");
}

/* =============================================================================
 * Exercise 1.4: Endianness
 *
 * Detect system endianness and convert between formats
 * =============================================================================
 */

// TODO: Return 1 if little-endian, 0 if big-endian
int is_little_endian(void) {
    // TODO: Use a union or pointer cast to check byte order
    // Hint: Store 0x01 in a uint16_t, check if first byte is 0x01

    return -1; // Replace with your implementation
}

// TODO: Swap bytes in a 32-bit value (convert between endianness)
uint32_t swap_endian_32(uint32_t value) {
    // TODO: Swap byte order
    // Hint: Use shifts and masks: (value >> 24), ((value >> 8) & 0xFF00), etc.

    return value; // Replace with your implementation
}

void exercise_1_4(void) {
    printf("=== Exercise 1.4: Endianness ===\n");

    int endian = is_little_endian();
    if (endian == 1) {
        printf("System is little-endian\n");
    } else if (endian == 0) {
        printf("System is big-endian\n");
    } else {
        printf("Endianness detection not implemented\n");
    }

    uint32_t original = 0x12345678;
    uint32_t swapped = swap_endian_32(original);
    printf("Original: 0x%08X\n", original);
    printf("Swapped:  0x%08X (expected: 0x78563412)\n\n", swapped);
}

/* =============================================================================
 * Exercise 1.5: Pointer to Pointer
 *
 * Understand multi-level indirection (common in dynamic 2D arrays)
 * =============================================================================
 */

// TODO: Allocate a 2D array using pointer-to-pointer
// rows x cols matrix, initialize all elements to 0
int **create_matrix(int rows, int cols) {
    // TODO:
    // 1. Allocate array of row pointers: int **matrix = malloc(rows * sizeof(int*))
    // 2. For each row, allocate the columns: matrix[i] = malloc(cols * sizeof(int))
    // 3. Initialize all elements to 0

    return NULL; // Replace with your implementation
}

// TODO: Free the 2D array
void free_matrix(int **matrix, int rows) {
    // TODO: Free each row, then free the row pointer array
    (void)matrix;
    (void)rows;
}

void exercise_1_5(void) {
    printf("=== Exercise 1.5: Pointer to Pointer ===\n");

    int rows = 3, cols = 4;
    int **matrix = create_matrix(rows, cols);

    if (matrix == NULL) {
        printf("create_matrix not implemented\n\n");
        return;
    }

    // Set some values
    matrix[0][0] = 1;
    matrix[1][2] = 5;
    matrix[2][3] = 9;

    // Print matrix
    printf("Matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }

    free_matrix(matrix, rows);
    printf("\n");
}

/* =============================================================================
 * Main
 * =============================================================================
 */

int main(void) {
    printf("Module 01: Memory and Pointers\n");
    printf("==============================\n\n");

    exercise_1_1();
    exercise_1_2();
    exercise_1_3();
    exercise_1_4();
    exercise_1_5();

    return 0;
}
