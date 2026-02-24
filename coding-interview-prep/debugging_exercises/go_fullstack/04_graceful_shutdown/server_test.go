package graceful

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestServerHandlesRequests(t *testing.T) {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "hello")
	})

	srv := NewServer("127.0.0.1:0", handler, 5*time.Second)
	addr, done, err := srv.Start()
	if err != nil {
		t.Fatalf("failed to start server: %v", err)
	}
	defer func() {
		srv.Stop()
		<-done
	}()

	resp, err := http.Get("http://" + addr + "/ping")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	if string(body) != "hello" {
		t.Fatalf("expected 'hello', got %q", string(body))
	}
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
}

func TestGracefulShutdownWaitsForInFlight(t *testing.T) {
	// This test verifies that Stop() blocks until in-flight requests complete
	// (or timeout expires).
	//
	// The handler sleeps for 500ms. We start a request, then call Stop().
	// Stop() should wait for the handler to finish (since 500ms < 5s timeout).
	// If the bug is present, Stop() returns immediately and the request is
	// killed mid-flight.

	var handlerCompleted int64

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(500 * time.Millisecond)
		atomic.StoreInt64(&handlerCompleted, 1)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "done")
	})

	srv := NewServer("127.0.0.1:0", handler, 5*time.Second)
	addr, done, err := srv.Start()
	if err != nil {
		t.Fatalf("failed to start server: %v", err)
	}

	// Start an in-flight request.
	var wg sync.WaitGroup
	var reqErr error
	var respBody string

	wg.Add(1)
	go func() {
		defer wg.Done()
		resp, err := http.Get("http://" + addr + "/slow")
		if err != nil {
			reqErr = err
			return
		}
		defer resp.Body.Close()
		b, _ := io.ReadAll(resp.Body)
		respBody = string(b)
	}()

	// Give the request a moment to reach the handler.
	time.Sleep(100 * time.Millisecond)

	// Initiate graceful shutdown. This SHOULD block until the in-flight
	// request completes (handler sleeps 500ms, timeout is 5s).
	stopErr := srv.Stop()
	if stopErr != nil {
		t.Fatalf("Stop() returned error: %v", stopErr)
	}

	// Wait for the server to fully stop.
	<-done

	// Wait for our request goroutine to finish.
	wg.Wait()

	// The handler should have completed successfully.
	if atomic.LoadInt64(&handlerCompleted) != 1 {
		t.Fatal("expected handler to complete, but it was interrupted by shutdown")
	}

	if reqErr != nil {
		t.Fatalf("in-flight request failed (connection killed?): %v", reqErr)
	}

	if respBody != "done" {
		t.Fatalf("expected response 'done', got %q", respBody)
	}
}

func TestShutdownRejectsNewConnections(t *testing.T) {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Slow handler — gives us time to try a second request after shutdown.
		time.Sleep(1 * time.Second)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "ok")
	})

	srv := NewServer("127.0.0.1:0", handler, 3*time.Second)
	addr, done, err := srv.Start()
	if err != nil {
		t.Fatalf("failed to start server: %v", err)
	}

	// Start an in-flight request to keep the server busy.
	go func() {
		http.Get("http://" + addr + "/busy")
	}()

	// Let the request reach the handler.
	time.Sleep(100 * time.Millisecond)

	// Initiate shutdown (blocks until in-flight completes or timeout).
	go func() {
		srv.Stop()
	}()

	// Give shutdown a moment to close the listener.
	time.Sleep(200 * time.Millisecond)

	// New connections after shutdown should fail.
	client := &http.Client{Timeout: 1 * time.Second}
	_, err = client.Get("http://" + addr + "/new")
	if err == nil {
		t.Fatal("expected new connection to be refused after shutdown, but it succeeded")
	}

	// Wait for full shutdown.
	<-done
}
