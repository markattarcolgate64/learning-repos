package batchprocessor

import (
	"testing"
)

func TestAutoFlushAtBatchSize(t *testing.T) {
	var batches [][]string

	p := New(3, func(batch []string) {
		// Store a reference to the flushed batch
		batches = append(batches, batch)
	})

	p.Add("a")
	p.Add("b")
	p.Add("c") // Should trigger auto-flush

	if len(batches) != 1 {
		t.Fatalf("expected 1 batch flushed, got %d", len(batches))
	}

	expected := []string{"a", "b", "c"}
	for i, v := range batches[0] {
		if v != expected[i] {
			t.Errorf("batch[0][%d] = %q, want %q", i, v, expected[i])
		}
	}
}

func TestManualFlush(t *testing.T) {
	var batches [][]string

	p := New(5, func(batch []string) {
		batches = append(batches, batch)
	})

	p.Add("x")
	p.Add("y")
	p.Flush() // Manual flush with partial buffer

	if len(batches) != 1 {
		t.Fatalf("expected 1 batch, got %d", len(batches))
	}
	if len(batches[0]) != 2 {
		t.Fatalf("expected batch of size 2, got %d", len(batches[0]))
	}
	if batches[0][0] != "x" || batches[0][1] != "y" {
		t.Errorf("batch = %v, want [x, y]", batches[0])
	}
}

func TestFlushEmptyBufferIsNoop(t *testing.T) {
	callCount := 0
	p := New(3, func(batch []string) {
		callCount++
	})

	p.Flush() // Should not call callback

	if callCount != 0 {
		t.Errorf("expected 0 flushes on empty buffer, got %d", callCount)
	}
}

func TestBufferLenTracking(t *testing.T) {
	p := New(3, func(batch []string) {})

	if p.BufferLen() != 0 {
		t.Errorf("expected initial buffer len 0, got %d", p.BufferLen())
	}

	p.Add("a")
	if p.BufferLen() != 1 {
		t.Errorf("expected buffer len 1, got %d", p.BufferLen())
	}

	p.Add("b")
	p.Add("c") // triggers flush, buffer resets

	if p.BufferLen() != 0 {
		t.Errorf("expected buffer len 0 after flush, got %d", p.BufferLen())
	}
}

// TestBatchDataIntegrityAfterNewAdds is the critical test that exposes the
// slice aliasing bug. After a batch is flushed, adding new items should NOT
// modify the previously flushed batch.
func TestBatchDataIntegrityAfterNewAdds(t *testing.T) {
	var batches [][]string

	p := New(3, func(batch []string) {
		// Store the batch. If the processor reuses the underlying array,
		// this reference will see corrupted data later.
		batches = append(batches, batch)
	})

	// Fill and auto-flush the first batch
	p.Add("a")
	p.Add("b")
	p.Add("c") // triggers flush of ["a", "b", "c"]

	// Verify batch 1 immediately
	if len(batches) != 1 {
		t.Fatalf("expected 1 batch, got %d", len(batches))
	}
	if batches[0][0] != "a" || batches[0][1] != "b" || batches[0][2] != "c" {
		t.Fatalf("batch 1 immediately after flush = %v, want [a b c]", batches[0])
	}

	// Now add new items — this is where the bug manifests.
	// If the buffer's underlying array is shared with the flushed batch,
	// these writes corrupt batch 1's data.
	p.Add("d")
	p.Add("e")
	p.Add("f") // triggers flush of ["d", "e", "f"]

	// Verify batch 1 is STILL correct (not corrupted by batch 2's writes)
	if batches[0][0] != "a" || batches[0][1] != "b" || batches[0][2] != "c" {
		t.Errorf("CORRUPTION DETECTED: batch 1 was modified after new items were added!\n"+
			"  batch 1 = %v, want [a b c]\n"+
			"  This is the classic Go slice aliasing bug: the flushed batch and the\n"+
			"  new buffer share the same underlying array.", batches[0])
	}

	// Verify batch 2
	if len(batches) != 2 {
		t.Fatalf("expected 2 batches, got %d", len(batches))
	}
	if batches[1][0] != "d" || batches[1][1] != "e" || batches[1][2] != "f" {
		t.Errorf("batch 2 = %v, want [d e f]", batches[1])
	}
}

// TestMultipleBatchesRemainIndependent tests that many consecutive batches
// don't interfere with each other.
func TestMultipleBatchesRemainIndependent(t *testing.T) {
	var batches [][]string

	p := New(2, func(batch []string) {
		batches = append(batches, batch)
	})

	items := []string{"a", "b", "c", "d", "e", "f"}
	for _, item := range items {
		p.Add(item)
	}

	// Should have 3 batches of size 2
	if len(batches) != 3 {
		t.Fatalf("expected 3 batches, got %d", len(batches))
	}

	expected := [][]string{
		{"a", "b"},
		{"c", "d"},
		{"e", "f"},
	}

	for i, batch := range batches {
		if len(batch) != 2 {
			t.Errorf("batch %d has %d items, want 2", i, len(batch))
			continue
		}
		for j, val := range batch {
			if val != expected[i][j] {
				t.Errorf("batch[%d][%d] = %q, want %q — possible slice aliasing corruption",
					i, j, val, expected[i][j])
			}
		}
	}
}

// TestCallbackReceivesCorrectBatchSize verifies the callback gets exactly
// batchSize items on auto-flush.
func TestCallbackReceivesCorrectBatchSize(t *testing.T) {
	var sizes []int

	p := New(4, func(batch []string) {
		sizes = append(sizes, len(batch))
	})

	for i := 0; i < 10; i++ {
		p.Add("item")
	}
	p.Flush() // flush remaining 2

	// 10 items with batch size 4: 2 auto-flushes (4 each) + 1 manual (2)
	expected := []int{4, 4, 2}
	if len(sizes) != len(expected) {
		t.Fatalf("expected %d flushes, got %d", len(expected), len(sizes))
	}
	for i, s := range sizes {
		if s != expected[i] {
			t.Errorf("flush %d had %d items, want %d", i, s, expected[i])
		}
	}
}
