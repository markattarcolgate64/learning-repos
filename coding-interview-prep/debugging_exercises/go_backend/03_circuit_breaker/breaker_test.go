package breaker

import (
	"errors"
	"testing"
	"time"
)

var errService = errors.New("service unavailable")

func TestStartsClosed(t *testing.T) {
	cb := New(3, 2, 100*time.Millisecond)
	if cb.GetState() != StateClosed {
		t.Errorf("expected initial state Closed, got %s", cb.GetState())
	}
}

func TestOpensAfterFailureThreshold(t *testing.T) {
	cb := New(3, 2, 100*time.Millisecond)

	// Three failures should open the breaker
	for i := 0; i < 3; i++ {
		err := cb.Execute(func() error { return errService })
		if err != errService {
			t.Fatalf("expected service error, got %v", err)
		}
	}

	if cb.GetState() != StateOpen {
		t.Errorf("expected state Open after %d failures, got %s", 3, cb.GetState())
	}
}

func TestOpenRejectsRequests(t *testing.T) {
	cb := New(3, 2, 100*time.Millisecond)

	// Open the breaker
	for i := 0; i < 3; i++ {
		cb.Execute(func() error { return errService })
	}

	// Should reject immediately
	err := cb.Execute(func() error { return nil })
	if !errors.Is(err, ErrCircuitOpen) {
		t.Errorf("expected ErrCircuitOpen, got %v", err)
	}
}

func TestTransitionsToHalfOpenAfterTimeout(t *testing.T) {
	cb := New(3, 2, 50*time.Millisecond)

	// Open the breaker
	for i := 0; i < 3; i++ {
		cb.Execute(func() error { return errService })
	}

	// Wait for timeout
	time.Sleep(60 * time.Millisecond)

	// Next call should go through (half-open allows it)
	err := cb.Execute(func() error { return nil })
	if err != nil {
		t.Errorf("expected nil error in half-open, got %v", err)
	}

	// State should now be half-open (or closed if the success transitioned it)
	state := cb.GetState()
	if state != StateHalfOpen && state != StateClosed {
		t.Errorf("expected HalfOpen or Closed after timeout + success, got %s", state)
	}
}

func TestHalfOpenClosesAfterConsecutiveSuccesses(t *testing.T) {
	cb := New(3, 3, 50*time.Millisecond)

	// Open the breaker
	for i := 0; i < 3; i++ {
		cb.Execute(func() error { return errService })
	}

	if cb.GetState() != StateOpen {
		t.Fatalf("expected Open, got %s", cb.GetState())
	}

	// Wait for timeout to allow half-open
	time.Sleep(60 * time.Millisecond)

	// Three consecutive successes should close the breaker.
	// (successThreshold = 3)
	for i := 0; i < 3; i++ {
		err := cb.Execute(func() error { return nil })
		if err != nil {
			t.Fatalf("success call %d in half-open returned error: %v", i+1, err)
		}
	}

	if cb.GetState() != StateClosed {
		t.Errorf("expected Closed after %d consecutive successes in half-open, got %s",
			3, cb.GetState())
	}
}

func TestHalfOpenReopensOnFailure(t *testing.T) {
	cb := New(3, 3, 50*time.Millisecond)

	// Open the breaker
	for i := 0; i < 3; i++ {
		cb.Execute(func() error { return errService })
	}

	time.Sleep(60 * time.Millisecond)

	// One success, then a failure
	cb.Execute(func() error { return nil })
	cb.Execute(func() error { return errService })

	if cb.GetState() != StateOpen {
		t.Errorf("expected Open after failure in half-open, got %s", cb.GetState())
	}
}

func TestClosedBreakerResetsFailureCount(t *testing.T) {
	// This tests the second bug: when the breaker transitions from HalfOpen
	// to Closed, the failure count should be reset. Otherwise, a single new
	// failure in the Closed state causes the breaker to immediately re-open.
	cb := New(3, 2, 50*time.Millisecond)

	// Open the breaker with exactly 3 failures
	for i := 0; i < 3; i++ {
		cb.Execute(func() error { return errService })
	}
	if cb.GetState() != StateOpen {
		t.Fatalf("expected Open, got %s", cb.GetState())
	}

	time.Sleep(60 * time.Millisecond)

	// Recover: 2 consecutive successes should close it
	for i := 0; i < 2; i++ {
		err := cb.Execute(func() error { return nil })
		if err != nil {
			t.Fatalf("recovery success %d returned error: %v", i+1, err)
		}
	}

	if cb.GetState() != StateClosed {
		t.Fatalf("expected Closed after recovery, got %s", cb.GetState())
	}

	// Now in Closed state: a SINGLE failure should NOT re-open the breaker
	// (threshold is 3). If failure count wasn't reset, the old count of 3
	// plus this new failure = 4, which exceeds the threshold immediately.
	cb.Execute(func() error { return errService })

	if cb.GetState() != StateClosed {
		t.Errorf("expected Closed after single failure (threshold=3), got %s — "+
			"failure count was likely not reset during HalfOpen->Closed transition",
			cb.GetState())
	}

	failures, _ := cb.Counters()
	if failures > 1 {
		t.Errorf("expected failure count to be 1 after reset + one failure, got %d", failures)
	}
}

func TestSuccessesInClosedDontAffectState(t *testing.T) {
	cb := New(3, 2, 50*time.Millisecond)

	for i := 0; i < 10; i++ {
		err := cb.Execute(func() error { return nil })
		if err != nil {
			t.Errorf("unexpected error on success: %v", err)
		}
	}

	if cb.GetState() != StateClosed {
		t.Errorf("expected Closed after all successes, got %s", cb.GetState())
	}
}
