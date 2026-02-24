// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// System: Concurrent Map
// Description: A thread-safe map that supports concurrent reads and writes.
// Uses sync.RWMutex to allow multiple concurrent readers while ensuring
// exclusive access for writers.
//
// Expected behavior:
//   - Set() stores a key-value pair safely
//   - Get() retrieves a value by key safely
//   - Delete() removes a key safely
//   - Keys() returns all keys safely
//   - Concurrent access from multiple goroutines should not cause data races
//
// Symptoms of the bug:
//   - Running with `go test -race` reports data races
//   - Concurrent reads and writes cause panics ("concurrent map read and map write")
//   - Intermittent crashes under high concurrency
//
// Hint: Think about how sync.RWMutex works and Go's rules about copying mutexes.

package cmap

import (
	"sync"
)

// ConcurrentMap is a thread-safe map implementation.
type ConcurrentMap struct {
	mu   sync.RWMutex
	data map[string]interface{}
}

// New creates a new ConcurrentMap.
func New() *ConcurrentMap {
	return &ConcurrentMap{
		data: make(map[string]interface{}),
	}
}

// Set stores a key-value pair in the map.
func (m *ConcurrentMap) Set(key string, value interface{}) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.data[key] = value
}

// Get retrieves the value for a key. Returns the value and whether the key exists.
func (m ConcurrentMap) Get(key string) (interface{}, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	val, ok := m.data[key]
	return val, ok
}

// Delete removes a key from the map.
func (m *ConcurrentMap) Delete(key string) {
	m.mu.Lock()
	defer m.mu.Unlock()
	delete(m.data, key)
}

// Keys returns all keys in the map.
func (m ConcurrentMap) Keys() []string {
	m.mu.RLock()
	defer m.mu.RUnlock()
	keys := make([]string, 0, len(m.data))
	for k := range m.data {
		keys = append(keys, k)
	}
	return keys
}

// Len returns the number of entries in the map.
func (m *ConcurrentMap) Len() int {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return len(m.data)
}

// ForEach calls the given function for each key-value pair in the map.
func (m *ConcurrentMap) ForEach(fn func(key string, value interface{})) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	for k, v := range m.data {
		fn(k, v)
	}
}
