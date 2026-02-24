package workerpool

import (
	"fmt"
	"sort"
	"sync"
	"testing"
	"time"
)

func TestPoolProcessesAllJobs(t *testing.T) {
	pool := New(4)

	numJobs := 20
	for i := 0; i < numJobs; i++ {
		pool.Submit(Job{ID: i, Payload: fmt.Sprintf("job-%d", i)})
	}

	// Give workers time to process
	time.Sleep(100 * time.Millisecond)

	// Shutdown should complete without hanging
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
		t.Errorf("expected %d results, got %d", numJobs, len(results))
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

func TestPoolConcurrentSubmitAndShutdown(t *testing.T) {
	pool := New(8)

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := 0; i < 50; i++ {
			// Submit may fail after shutdown; that's okay for this test.
			func() {
				defer func() { recover() }() // recover from send on closed channel
				pool.Submit(Job{ID: i, Payload: fmt.Sprintf("concurrent-%d", i)})
			}()
		}
	}()

	// Give some jobs time to be submitted
	time.Sleep(10 * time.Millisecond)

	done := make(chan struct{})
	go func() {
		pool.Shutdown()
		close(done)
	}()

	select {
	case <-done:
		// Success
	case <-time.After(5 * time.Second):
		t.Fatal("Shutdown() deadlocked during concurrent submit — timed out after 5 seconds")
	}

	wg.Wait()
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
