// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// System: Circuit Breaker
// Description: Implements the circuit breaker pattern for protecting downstream
// services. The breaker has three states: Closed (requests flow through),
// Open (requests are blocked), and HalfOpen (limited requests to test recovery).
//
// State transitions:
//   - Closed -> Open:     when failure count reaches the threshold
//   - Open -> HalfOpen:   after a timeout period elapses
//   - HalfOpen -> Closed: after N consecutive successes
//   - HalfOpen -> Open:   on any failure
//
// Expected behavior:
//   - In Closed state, requests pass through; failures are counted
//   - In Open state, requests fail immediately with ErrCircuitOpen
//   - In HalfOpen state, limited requests pass through to test if the service recovered
//   - After enough consecutive successes in HalfOpen, the breaker transitions to Closed
//   - When transitioning to Closed, the failure count resets to zero
//   - A freshly-closed breaker should tolerate failures up to the full threshold again
//
// Symptoms of the bug:
//   - The circuit breaker never transitions from HalfOpen back to Closed
//   - Even after many successful calls in HalfOpen, it stays HalfOpen forever
//   - OR: the breaker transitions to Closed but immediately re-opens on a single failure
//
// Hint: Trace the success counter logic in HalfOpen state carefully.
//       Also check what happens to counters during state transitions.

package breaker

import (
	"errors"
	"sync"
	"time"
)

// State represents the circuit breaker state.
type State int

const (
	StateClosed   State = iota
	StateOpen
	StateHalfOpen
)

func (s State) String() string {
	switch s {
	case StateClosed:
		return "closed"
	case StateOpen:
		return "open"
	case StateHalfOpen:
		return "half-open"
	default:
		return "unknown"
	}
}

// ErrCircuitOpen is returned when the circuit breaker is open.
var ErrCircuitOpen = errors.New("circuit breaker is open")

// CircuitBreaker implements the circuit breaker pattern.
type CircuitBreaker struct {
	mu sync.Mutex

	state            State
	failureCount     int
	successCount     int
	failureThreshold int           // failures before opening
	successThreshold int           // successes in half-open before closing
	timeout          time.Duration // how long to stay open before half-open
	lastFailureTime  time.Time
}

// New creates a new CircuitBreaker.
func New(failureThreshold, successThreshold int, timeout time.Duration) *CircuitBreaker {
	return &CircuitBreaker{
		state:            StateClosed,
		failureThreshold: failureThreshold,
		successThreshold: successThreshold,
		timeout:          timeout,
	}
}

// Execute runs the given function through the circuit breaker.
func (cb *CircuitBreaker) Execute(fn func() error) error {
	cb.mu.Lock()

	switch cb.state {
	case StateOpen:
		if time.Since(cb.lastFailureTime) > cb.timeout {
			cb.state = StateHalfOpen
			cb.successCount = 0
			cb.mu.Unlock()
			return cb.doExecute(fn)
		}
		cb.mu.Unlock()
		return ErrCircuitOpen

	case StateHalfOpen:
		cb.mu.Unlock()
		return cb.doExecute(fn)

	case StateClosed:
		cb.mu.Unlock()
		return cb.doExecute(fn)
	}

	cb.mu.Unlock()
	return nil
}

// doExecute actually runs the function and handles the result.
func (cb *CircuitBreaker) doExecute(fn func() error) error {
	err := fn()

	cb.mu.Lock()
	defer cb.mu.Unlock()

	if err != nil {
		cb.recordFailure()
		return err
	}

	cb.recordSuccess()
	return nil
}

// recordFailure handles a failed execution.
func (cb *CircuitBreaker) recordFailure() {
	cb.failureCount++
	cb.lastFailureTime = time.Now()

	switch cb.state {
	case StateClosed:
		if cb.failureCount >= cb.failureThreshold {
			cb.state = StateOpen
		}
	case StateHalfOpen:
		cb.state = StateOpen
	}
}

// recordSuccess handles a successful execution.
func (cb *CircuitBreaker) recordSuccess() {
	switch cb.state {
	case StateHalfOpen:
		cb.successCount = 1
		if cb.successCount >= cb.successThreshold {
			cb.state = StateClosed
		}
	case StateClosed:
		// No action needed on success in closed state.
	}
}

// GetState returns the current state of the circuit breaker.
func (cb *CircuitBreaker) GetState() State {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	return cb.state
}

// Counters returns the current failure and success counts (for testing).
func (cb *CircuitBreaker) Counters() (failures, successes int) {
	cb.mu.Lock()
	defer cb.mu.Unlock()
	return cb.failureCount, cb.successCount
}
