// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// Graceful Shutdown with Context Bug
// ====================================
//
// This package provides a simple HTTP server wrapper with graceful shutdown
// support. When a shutdown signal is received (via the Stop method), the
// server should:
//
//   1. Stop accepting new connections immediately.
//   2. Wait for all in-flight requests to complete (up to a timeout).
//   3. Return only after all handlers have finished or the timeout expires.
//
// SYMPTOMS:
//   - When Stop() is called while a slow handler is in progress, the server
//     does NOT wait for the handler to finish. Instead it shuts down
//     almost immediately, causing the in-flight request to be terminated.
//   - The graceful shutdown timeout (e.g., 5 seconds) appears to be ignored.
//   - In-flight requests receive connection-reset errors instead of completing
//     normally.
//
// The bug is in how the shutdown context is created. The cancel function is
// deferred immediately, which means the context is cancelled as soon as Stop()
// returns from the line that creates the context — BEFORE http.Server.Shutdown
// has a chance to use the full timeout. The Shutdown method sees an already-
// cancelled (or about-to-be-cancelled) context and aborts immediately.

package graceful

import (
	"context"
	"net"
	"net/http"
	"time"
)

// Server wraps an http.Server with graceful shutdown support.
type Server struct {
	httpServer *http.Server
	listener   net.Listener
	timeout    time.Duration
}

// NewServer creates a new graceful server.
//   - addr: the address to listen on (e.g., ":8080" or "127.0.0.1:0")
//   - handler: the HTTP handler (router, mux, etc.)
//   - shutdownTimeout: max time to wait for in-flight requests during shutdown
func NewServer(addr string, handler http.Handler, shutdownTimeout time.Duration) *Server {
	return &Server{
		httpServer: &http.Server{
			Addr:    addr,
			Handler: handler,
		},
		timeout: shutdownTimeout,
	}
}

// Start begins listening and serving HTTP requests. It returns the actual
// address the server is listening on (useful when using port 0) and a channel
// that is closed when the server has fully stopped.
func (s *Server) Start() (addr string, done chan struct{}, err error) {
	ln, err := net.Listen("tcp", s.httpServer.Addr)
	if err != nil {
		return "", nil, err
	}
	s.listener = ln

	done = make(chan struct{})

	go func() {
		defer close(done)
		// Serve blocks until the listener is closed (by Shutdown or Close).
		if err := s.httpServer.Serve(ln); err != http.ErrServerClosed {
			// Unexpected error.
			panic("unexpected serve error: " + err.Error())
		}
	}()

	return ln.Addr().String(), done, nil
}

// Stop initiates a graceful shutdown. It stops accepting new connections and
// waits for in-flight requests to finish, up to the configured timeout.
//
// BUG: The context with timeout is created, and `cancel` is deferred. But
// defer runs when Stop() returns. The problem is that `Shutdown` needs the
// context to remain valid for its entire duration. However, here the
// cancel is called via defer at the end of Stop(), AND more critically,
// the context is created with a zero or incorrect timeout, or the cancel
// races with Shutdown.
//
// The actual bug: we create the context and IMMEDIATELY defer cancel.
// Then we call Shutdown — but in a goroutine (or the cancel fires too early
// due to the function returning). Look closely at the flow below.
func (s *Server) Stop() error {
	ctx, cancel := context.WithTimeout(context.Background(), s.timeout)

	// BUG: This defer cancel() will fire when Stop() returns.
	// But the real problem is below: we launch Shutdown in a goroutine
	// and return immediately, so cancel() fires right away, killing
	// the context before Shutdown can use the full timeout.
	defer cancel()

	// BUG: Shutdown is called in a goroutine, so Stop() returns immediately.
	// The deferred cancel() then fires, cancelling the context. Shutdown sees
	// a cancelled context and aborts without waiting for in-flight requests.
	errCh := make(chan error, 1)
	go func() {
		errCh <- s.httpServer.Shutdown(ctx)
	}()

	// Stop() returns here immediately. The deferred cancel() fires.
	// The goroutine's Shutdown call now has a cancelled context.
	return nil
}

// Addr returns the address the server is listening on, or empty if not started.
func (s *Server) Addr() string {
	if s.listener != nil {
		return s.listener.Addr().String()
	}
	return ""
}
