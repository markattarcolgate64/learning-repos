// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// HTTP Cache Middleware with Stale Data Bug
// ==========================================
//
// This middleware caches HTTP responses in memory keyed by request URL.
// Subsequent identical requests are served from cache without hitting the
// downstream handler, improving response times.
//
// Features:
//   - Caches responses by URL path
//   - Configurable TTL (time to live)
//   - Only caches responses with 2xx status codes
//
// SYMPTOMS:
//   - A POST request to "/api/users" returns the cached response from a
//     previous GET request to "/api/users" instead of hitting the handler.
//   - After a POST creates a new resource, a subsequent GET still returns
//     stale cached data from before the POST.
//   - Different HTTP methods for the same path incorrectly share cache entries.
//
// The bug is that the cache key is derived from the URL path alone, without
// including the HTTP method. This causes GET and POST (and PUT, DELETE, etc.)
// to collide in the cache.

package cachemw

import (
	"bytes"
	"net/http"
	"sync"
	"time"
)

// CachedResponse holds a cached HTTP response.
type CachedResponse struct {
	StatusCode int
	Headers    http.Header
	Body       []byte
	CachedAt   time.Time
}

// Cache is an in-memory HTTP response cache.
type Cache struct {
	mu      sync.RWMutex
	entries map[string]*CachedResponse
	ttl     time.Duration
}

// NewCache creates a new cache with the given TTL.
func NewCache(ttl time.Duration) *Cache {
	return &Cache{
		entries: make(map[string]*CachedResponse),
		ttl:     ttl,
	}
}

// Middleware returns an http.Handler that caches responses from the next handler.
func (c *Cache) Middleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// BUG: cache key uses only the URL path, ignoring the HTTP method.
		// A GET /api/users and POST /api/users will share the same cache entry.
		key := r.URL.Path

		// Check if we have a valid cached response.
		if cached, ok := c.get(key); ok {
			// Serve from cache.
			for k, vals := range cached.Headers {
				for _, v := range vals {
					w.Header().Add(k, v)
				}
			}
			w.Header().Set("X-Cache", "HIT")
			w.WriteHeader(cached.StatusCode)
			w.Write(cached.Body)
			return
		}

		// Cache miss — call the downstream handler with a recording writer.
		rec := &responseRecorder{
			ResponseWriter: w,
			body:           &bytes.Buffer{},
			statusCode:     http.StatusOK,
		}
		next.ServeHTTP(rec, r)

		// Only cache 2xx responses.
		if rec.statusCode >= 200 && rec.statusCode < 300 {
			c.set(key, &CachedResponse{
				StatusCode: rec.statusCode,
				Headers:    rec.Header().Clone(),
				Body:       rec.body.Bytes(),
				CachedAt:   time.Now(),
			})
		}
	})
}

// get retrieves a cached response if it exists and is not expired.
func (c *Cache) get(key string) (*CachedResponse, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, ok := c.entries[key]
	if !ok {
		return nil, false
	}

	if time.Since(entry.CachedAt) > c.ttl {
		// Expired — treat as miss. (Lazy expiration; entry stays until overwritten.)
		return nil, false
	}

	return entry, true
}

// set stores a response in the cache.
func (c *Cache) set(key string, resp *CachedResponse) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.entries[key] = resp
}

// responseRecorder captures the response written by the downstream handler
// so it can be stored in the cache.
type responseRecorder struct {
	http.ResponseWriter
	body       *bytes.Buffer
	statusCode int
	wroteHead  bool
}

func (r *responseRecorder) WriteHeader(code int) {
	if !r.wroteHead {
		r.statusCode = code
		r.wroteHead = true
		r.ResponseWriter.WriteHeader(code)
	}
}

func (r *responseRecorder) Write(b []byte) (int, error) {
	r.body.Write(b)
	return r.ResponseWriter.Write(b)
}
