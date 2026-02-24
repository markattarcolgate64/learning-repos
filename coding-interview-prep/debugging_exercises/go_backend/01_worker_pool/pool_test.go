package workerpool

import (
	"fmt"
	"sort"
	"testing"
	"time"
)

func TestPoolProcessesAllJobs(t *testing.T) {
	pool := New(4)

	numJobs := 50
	for i := 0; i < numJobs; i++ {
		pool.Submit(Job{ID: i + 1, Payload: fmt.Sprintf("job-%d", i+1)})
	}

	// Shutdown should wait for ALL pending jobs to be processed.
	done := make(chan struct{})
	go func() {
		pool.Shutdown()
		close(done)
	}()

	select {
	case <-done:
		// Success - shutdown completed
	case <-time.After(5 * time.Second):
		t.Fatal("Shutdown() deadlocked — timed out after 5 seconds")
	}

	results := pool.Results()
	if len(results) != numJobs {
		t.Errorf("expected %d results, got %d — some jobs were dropped during shutdown",
			numJobs, len(results))
	}
}

func TestPoolShutdownWithNoJobs(t *testing.T) {
	pool := New(3)

	// Immediately shut down without submitting any jobs
	done := make(chan struct{})
	go func() {
		pool.Shutdown()
		close(done)
	}()

	select {
	case <-done:
		// Success
	case <-time.After(5 * time.Second):
		t.Fatal("Shutdown() deadlocked with no jobs — timed out after 5 seconds")
	}

	results := pool.Results()
	if len(results) != 0 {
		t.Errorf("expected 0 results, got %d", len(results))
	}
}

func TestPoolDrainsBufferedJobs(t *testing.T) {
	// This test specifically targets the bug: submit many jobs to the
	// buffered channel, then immediately shutdown. The pool MUST process
	// all buffered jobs before returning from Shutdown().
	pool := New(2)

	numJobs := 30
	for i := 0; i < numJobs; i++ {
		pool.Submit(Job{ID: i + 1, Payload: fmt.Sprintf("buffered-%d", i+1)})
	}

	// No sleep! Shutdown immediately while jobs are still in the buffer.
	done := make(chan struct{})
	go func() {
		pool.Shutdown()
		close(done)
	}()

	select {
	case <-done:
	case <-time.After(5 * time.Second):
		t.Fatal("Shutdown() deadlocked — timed out after 5 seconds")
	}

	results := pool.Results()
	if len(results) != numJobs {
		t.Errorf("expected %d results but got %d — buffered jobs were dropped "+
			"during shutdown instead of being drained", numJobs, len(results))
	}
}

func TestPoolResultsCorrectness(t *testing.T) {
	pool := New(2)

	jobs := []Job{
		{ID: 1, Payload: "alpha"},
		{ID: 2, Payload: "beta"},
		{ID: 3, Payload: "gamma"},
	}

	for _, j := range jobs {
		pool.Submit(j)
	}

	// Give workers time to process all jobs
	time.Sleep(100 * time.Millisecond)

	done := make(chan struct{})
	go func() {
		pool.Shutdown()
		close(done)
	}()

	select {
	case <-done:
	case <-time.After(5 * time.Second):
		t.Fatal("Shutdown() deadlocked — timed out after 5 seconds")
	}

	results := pool.Results()
	sort.Slice(results, func(i, j int) bool {
		return results[i].JobID < results[j].JobID
	})

	expected := []Result{
		{JobID: 1, Output: "processed:alpha"},
		{JobID: 2, Output: "processed:beta"},
		{JobID: 3, Output: "processed:gamma"},
	}

	if len(results) != len(expected) {
		t.Fatalf("expected %d results, got %d", len(expected), len(results))
	}

	for i, r := range results {
		if r != expected[i] {
			t.Errorf("result[%d] = %+v, want %+v", i, r, expected[i])
		}
	}
}

func TestPoolManyWorkersOneJob(t *testing.T) {
	// More workers than jobs — all workers must still shut down cleanly.
	pool := New(10)

	pool.Submit(Job{ID: 1, Payload: "only-one"})
	time.Sleep(50 * time.Millisecond)

	done := make(chan struct{})
	go func() {
		pool.Shutdown()
		close(done)
	}()

	select {
	case <-done:
	case <-time.After(5 * time.Second):
		t.Fatal("Shutdown() deadlocked with many workers and few jobs — timed out after 5 seconds")
	}

	results := pool.Results()
	if len(results) != 1 {
		t.Errorf("expected 1 result, got %d", len(results))
	}
}
