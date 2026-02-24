package cachemw

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"testing"
	"time"
)

func TestGETIsCached(t *testing.T) {
	var callCount int64

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt64(&callCount, 1)
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, `{"users":["alice","bob"]}`)
	})

	cache := NewCache(5 * time.Minute)
	cached := cache.Middleware(handler)

	// First GET — should miss cache.
	req1 := httptest.NewRequest("GET", "/api/users", nil)
	rec1 := httptest.NewRecorder()
	cached.ServeHTTP(rec1, req1)

	if rec1.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec1.Code)
	}
	if rec1.Body.String() != `{"users":["alice","bob"]}` {
		t.Fatalf("unexpected body: %s", rec1.Body.String())
	}
	if atomic.LoadInt64(&callCount) != 1 {
		t.Fatalf("expected handler called once, got %d", atomic.LoadInt64(&callCount))
	}

	// Second GET — should hit cache.
	req2 := httptest.NewRequest("GET", "/api/users", nil)
	rec2 := httptest.NewRecorder()
	cached.ServeHTTP(rec2, req2)

	if rec2.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec2.Code)
	}
	if rec2.Header().Get("X-Cache") != "HIT" {
		t.Fatalf("expected X-Cache=HIT, got %q", rec2.Header().Get("X-Cache"))
	}
	// Handler should NOT have been called again.
	if atomic.LoadInt64(&callCount) != 1 {
		t.Fatalf("expected handler called once (cached), got %d", atomic.LoadInt64(&callCount))
	}
}

func TestPOSTIsNotServedFromGETCache(t *testing.T) {
	var getCount, postCount int64

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "GET":
			atomic.AddInt64(&getCount, 1)
			w.WriteHeader(http.StatusOK)
			fmt.Fprint(w, `{"users":["alice"]}`)
		case "POST":
			atomic.AddInt64(&postCount, 1)
			w.WriteHeader(http.StatusCreated)
			fmt.Fprint(w, `{"created":"charlie"}`)
		}
	})

	cache := NewCache(5 * time.Minute)
	cached := cache.Middleware(handler)

	// Warm the cache with a GET.
	req1 := httptest.NewRequest("GET", "/api/users", nil)
	rec1 := httptest.NewRecorder()
	cached.ServeHTTP(rec1, req1)

	if rec1.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec1.Code)
	}

	// POST to the same path — must NOT return cached GET response.
	req2 := httptest.NewRequest("POST", "/api/users", nil)
	rec2 := httptest.NewRecorder()
	cached.ServeHTTP(rec2, req2)

	if rec2.Code != http.StatusCreated {
		t.Fatalf("expected 201 for POST, got %d (possibly served from GET cache)", rec2.Code)
	}
	if rec2.Body.String() != `{"created":"charlie"}` {
		t.Fatalf("expected POST body, got %q (possibly cached GET body)", rec2.Body.String())
	}
	if atomic.LoadInt64(&postCount) != 1 {
		t.Fatalf("expected POST handler called, got count %d", atomic.LoadInt64(&postCount))
	}
}

func TestDifferentMethodsSamePathDontCollide(t *testing.T) {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "GET":
			w.WriteHeader(http.StatusOK)
			fmt.Fprint(w, "get-response")
		case "PUT":
			w.WriteHeader(http.StatusOK)
			fmt.Fprint(w, "put-response")
		case "DELETE":
			w.WriteHeader(http.StatusNoContent)
		}
	})

	cache := NewCache(5 * time.Minute)
	cached := cache.Middleware(handler)

	// GET /api/item/1
	req1 := httptest.NewRequest("GET", "/api/item/1", nil)
	rec1 := httptest.NewRecorder()
	cached.ServeHTTP(rec1, req1)

	if rec1.Body.String() != "get-response" {
		t.Fatalf("expected 'get-response', got %q", rec1.Body.String())
	}

	// PUT /api/item/1 — should NOT get the cached GET response.
	req2 := httptest.NewRequest("PUT", "/api/item/1", nil)
	rec2 := httptest.NewRecorder()
	cached.ServeHTTP(rec2, req2)

	if rec2.Body.String() != "put-response" {
		t.Fatalf("expected 'put-response', got %q (cached GET leaked)", rec2.Body.String())
	}

	// DELETE /api/item/1 — should NOT get the cached GET response.
	req3 := httptest.NewRequest("DELETE", "/api/item/1", nil)
	rec3 := httptest.NewRecorder()
	cached.ServeHTTP(rec3, req3)

	if rec3.Code != http.StatusNoContent {
		t.Fatalf("expected 204 for DELETE, got %d", rec3.Code)
	}
}

func TestCacheExpiration(t *testing.T) {
	var callCount int64

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt64(&callCount, 1)
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "call-%d", atomic.LoadInt64(&callCount))
	})

	// Very short TTL for testing.
	cache := NewCache(50 * time.Millisecond)
	cached := cache.Middleware(handler)

	// First call.
	req1 := httptest.NewRequest("GET", "/api/data", nil)
	rec1 := httptest.NewRecorder()
	cached.ServeHTTP(rec1, req1)
	if rec1.Body.String() != "call-1" {
		t.Fatalf("expected 'call-1', got %q", rec1.Body.String())
	}

	// Wait for TTL to expire.
	time.Sleep(100 * time.Millisecond)

	// Second call — cache should have expired, handler called again.
	req2 := httptest.NewRequest("GET", "/api/data", nil)
	rec2 := httptest.NewRecorder()
	cached.ServeHTTP(rec2, req2)
	if rec2.Body.String() != "call-2" {
		t.Fatalf("expected 'call-2' after expiration, got %q", rec2.Body.String())
	}
}
