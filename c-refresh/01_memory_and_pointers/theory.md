# Module 01: Memory and Pointers

## Memory Layout

A C program's memory is organized into segments:

```
High Address
┌─────────────────┐
│      Stack      │  ← Local variables, function calls (grows down)
│        ↓        │
├─────────────────┤
│                 │
│   (free space)  │
│                 │
├─────────────────┤
│        ↑        │
│      Heap       │  ← malloc/free (grows up)
├─────────────────┤
│       BSS       │  ← Uninitialized globals (zeroed)
├─────────────────┤
│      Data       │  ← Initialized globals
├─────────────────┤
│      Text       │  ← Program code (read-only)
└─────────────────┘
Low Address
```

**Why it matters for hardware:** On embedded systems, you often have limited RAM and must carefully manage stack size and avoid heap fragmentation.

## Pointer Arithmetic

Pointer arithmetic operates in units of the pointed-to type:

```c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;

p + 1;      // Points to arr[1], advances by sizeof(int) bytes
*(p + 2);   // Value at arr[2] = 30
p[3];       // Same as *(p + 3) = 40
```

**Key insight:** `arr[i]` is syntactic sugar for `*(arr + i)`.

## Array Decay

Arrays "decay" to pointers when passed to functions:

```c
void func(int arr[]) {     // arr is actually int*
    sizeof(arr);           // Size of pointer, NOT array!
}

int main() {
    int arr[10];
    sizeof(arr);           // 40 bytes (10 * 4)
    func(arr);             // arr decays to &arr[0]
}
```

## Struct Padding and Alignment

CPUs access memory most efficiently at aligned addresses. The compiler inserts padding:

```c
struct Misaligned {
    char a;      // 1 byte
    // 3 bytes padding
    int b;       // 4 bytes (must be 4-byte aligned)
    char c;      // 1 byte
    // 3 bytes padding
};  // Total: 12 bytes, not 6!

struct Optimized {
    int b;       // 4 bytes
    char a;      // 1 byte
    char c;      // 1 byte
    // 2 bytes padding
};  // Total: 8 bytes
```

**Hardware relevance:** Many microcontrollers require aligned access. Unaligned access can cause faults or performance penalties.

## Endianness

Multi-byte values can be stored in two orders:

```
Value: 0x12345678

Little-Endian (x86, ARM default):
Address:  0x00  0x01  0x02  0x03
Value:    0x78  0x56  0x34  0x12  (LSB first)

Big-Endian (Network byte order, some ARM modes):
Address:  0x00  0x01  0x02  0x03
Value:    0x12  0x34  0x56  0x78  (MSB first)
```

**Hardware relevance:** When reading sensor data or communicating over networks, you must handle endianness correctly.

## Practice Concepts

1. Draw the memory layout for a given program
2. Calculate struct sizes with padding
3. Trace pointer arithmetic expressions
4. Convert between endianness
