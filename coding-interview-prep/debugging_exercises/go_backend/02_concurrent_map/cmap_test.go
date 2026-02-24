package cmap

import (
	"fmt"
	"sort"
	"sync"
	"testing"
)

func TestBasicSetAndGet(t *testing.T) {
	m := New()
	m.Set("hello", "world")

	val, ok := m.Get("hello")
	if !ok {
		t.Fatal("expected key 'hello' to exist")
	}
	if val != "world" {
		t.Errorf("expected 'world', got %v", val)
	}
}

func TestGetMissingKey(t *testing.T) {
	m := New()
	_, ok := m.Get("missing")
	if ok {
		t.Error("expected key 'missing' to not exist")
	}
}

func TestDelete(t *testing.T) {
	m := New()
	m.Set("key", "value")
	m.Delete("key")

	_, ok := m.Get("key")
	if ok {
		t.Error("expected key to be deleted")
	}
}

func TestKeys(t *testing.T) {
	m := New()
	m.Set("c", 3)
	m.Set("a", 1)
	m.Set("b", 2)

	keys := m.Keys()
	sort.Strings(keys)

	expected := []string{"a", "b", "c"}
	if len(keys) != len(expected) {
		t.Fatalf("expected %d keys, got %d", len(expected), len(keys))
	}
	for i, k := range keys {
		if k != expected[i] {
			t.Errorf("keys[%d] = %q, want %q", i, k, expected[i])
		}
	}
}

func TestLen(t *testing.T) {
	m := New()
	if m.Len() != 0 {
		t.Errorf("expected len 0, got %d", m.Len())
	}
	m.Set("a", 1)
	m.Set("b", 2)
	if m.Len() != 2 {
		t.Errorf("expected len 2, got %d", m.Len())
	}
}

// TestConcurrentReadWrite runs concurrent reads and writes.
// This test will FAIL with -race flag due to the bug.
// Run with: go test -race -count=1 ./...
func TestConcurrentReadWrite(t *testing.T) {
	m := New()
	var wg sync.WaitGroup

	// Writers
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				key := fmt.Sprintf("writer-%d-key-%d", id, j)
				m.Set(key, j)
			}
		}(i)
	}

	// Readers using Get
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				key := fmt.Sprintf("writer-%d-key-%d", id, j)
				m.Get(key)
			}
		}(i)
	}

	// Readers using Keys
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 50; j++ {
				m.Keys()
			}
		}()
	}

	wg.Wait()
}

// TestConcurrentDeleteAndRead verifies no races during concurrent delete and read.
func TestConcurrentDeleteAndRead(t *testing.T) {
	m := New()

	// Pre-populate
	for i := 0; i < 100; i++ {
		m.Set(fmt.Sprintf("key-%d", i), i)
	}

	var wg sync.WaitGroup

	// Deleters
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(start int) {
			defer wg.Done()
			for j := start; j < 100; j += 5 {
				m.Delete(fmt.Sprintf("key-%d", j))
			}
		}(i)
	}

	// Readers
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 100; j++ {
				m.Get(fmt.Sprintf("key-%d", j))
			}
		}()
	}

	// Key listers
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < 20; j++ {
				m.Keys()
			}
		}()
	}

	wg.Wait()
}

// TestDataIntegrity verifies data isn't corrupted after concurrent access.
func TestDataIntegrity(t *testing.T) {
	m := New()
	var wg sync.WaitGroup

	numWriters := 10
	writesPerWriter := 50

	for i := 0; i < numWriters; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < writesPerWriter; j++ {
				key := fmt.Sprintf("w%d", id)
				m.Set(key, id*1000+j)
			}
		}(i)
	}

	wg.Wait()

	// Each writer wrote to its own key, so we should have exactly numWriters keys.
	if m.Len() != numWriters {
		t.Errorf("expected %d keys, got %d", numWriters, m.Len())
	}

	// Verify each key has a valid value (the last write from that writer).
	for i := 0; i < numWriters; i++ {
		key := fmt.Sprintf("w%d", i)
		val, ok := m.Get(key)
		if !ok {
			t.Errorf("key %q not found", key)
			continue
		}
		v, ok := val.(int)
		if !ok {
			t.Errorf("key %q has non-int value: %v", key, val)
			continue
		}
		// Value should be between i*1000 and i*1000 + writesPerWriter - 1
		if v < i*1000 || v >= i*1000+writesPerWriter {
			t.Errorf("key %q has unexpected value %d", key, v)
		}
	}
}
