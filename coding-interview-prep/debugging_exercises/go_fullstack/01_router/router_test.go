package router

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestExactPathMatch(t *testing.T) {
	r := NewRouter()

	called := false
	r.Handle("GET", "/health", func(w http.ResponseWriter, req *http.Request) {
		called = true
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "ok")
	})

	req := httptest.NewRequest("GET", "/health", nil)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)

	if !called {
		t.Fatal("expected /health handler to be called")
	}
	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if rec.Body.String() != "ok" {
		t.Fatalf("expected body 'ok', got %q", rec.Body.String())
	}
}

func TestParameterizedPathMatch(t *testing.T) {
	r := NewRouter()

	var capturedID string
	r.Handle("GET", "/users/:id", func(w http.ResponseWriter, req *http.Request) {
		p := Params(req)
		capturedID = p["id"]
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "user:%s", capturedID)
	})

	req := httptest.NewRequest("GET", "/users/42", nil)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if capturedID != "42" {
		t.Fatalf("expected param 'id' to be '42', got %q", capturedID)
	}
	if rec.Body.String() != "user:42" {
		t.Fatalf("expected body 'user:42', got %q", rec.Body.String())
	}
}

func TestMultipleParameters(t *testing.T) {
	r := NewRouter()

	var capturedPostID, capturedCommentID string
	r.Handle("GET", "/posts/:pid/comments/:cid", func(w http.ResponseWriter, req *http.Request) {
		p := Params(req)
		capturedPostID = p["pid"]
		capturedCommentID = p["cid"]
		w.WriteHeader(http.StatusOK)
	})

	req := httptest.NewRequest("GET", "/posts/7/comments/99", nil)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}
	if capturedPostID != "7" {
		t.Fatalf("expected param 'pid' to be '7', got %q", capturedPostID)
	}
	if capturedCommentID != "99" {
		t.Fatalf("expected param 'cid' to be '99', got %q", capturedCommentID)
	}
}

func TestNoFalseMatch(t *testing.T) {
	r := NewRouter()

	r.Handle("GET", "/users/:id", func(w http.ResponseWriter, req *http.Request) {
		w.WriteHeader(http.StatusOK)
	})

	// /users/42/profile has more segments than /users/:id — should NOT match.
	req := httptest.NewRequest("GET", "/users/42/profile", nil)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)

	if rec.Code != http.StatusNotFound {
		t.Fatalf("expected 404 for /users/42/profile, got %d", rec.Code)
	}
}

func TestStaticRouteDoesNotMatchParameterized(t *testing.T) {
	r := NewRouter()

	staticCalled := false
	paramCalled := false

	r.Handle("GET", "/users", func(w http.ResponseWriter, req *http.Request) {
		staticCalled = true
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "list")
	})
	r.Handle("GET", "/users/:id", func(w http.ResponseWriter, req *http.Request) {
		paramCalled = true
		p := Params(req)
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "user:%s", p["id"])
	})

	// Request to /users should hit static route.
	req1 := httptest.NewRequest("GET", "/users", nil)
	rec1 := httptest.NewRecorder()
	r.ServeHTTP(rec1, req1)

	if !staticCalled {
		t.Fatal("expected static /users handler to be called")
	}
	if rec1.Body.String() != "list" {
		t.Fatalf("expected body 'list', got %q", rec1.Body.String())
	}

	// Request to /users/5 should hit parameterized route.
	req2 := httptest.NewRequest("GET", "/users/5", nil)
	rec2 := httptest.NewRecorder()
	r.ServeHTTP(rec2, req2)

	if !paramCalled {
		t.Fatal("expected parameterized /users/:id handler to be called")
	}
	if rec2.Body.String() != "user:5" {
		t.Fatalf("expected body 'user:5', got %q", rec2.Body.String())
	}
}

func TestMethodMismatch(t *testing.T) {
	r := NewRouter()

	r.Handle("POST", "/users", func(w http.ResponseWriter, req *http.Request) {
		w.WriteHeader(http.StatusCreated)
	})

	req := httptest.NewRequest("GET", "/users", nil)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)

	if rec.Code != http.StatusNotFound {
		t.Fatalf("expected 404 for GET /users (only POST registered), got %d", rec.Code)
	}
}
