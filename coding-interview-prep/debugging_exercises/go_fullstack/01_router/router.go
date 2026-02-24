// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// HTTP Router with Path Parameter Matching
// =========================================
//
// This is a simple HTTP router that supports:
//   - Exact path matching (e.g., "/users", "/health")
//   - Parameterized path matching (e.g., "/users/:id", "/posts/:id/comments/:cid")
//   - Extracting path parameters into a map accessible by handlers
//
// SYMPTOMS:
//   - Parameterized routes like "/users/:id" never match — requests to
//     "/users/42" either 404 or incorrectly match the static "/users" route.
//   - When a parameterized route does match, the extracted parameter values
//     are wrong (e.g., ":id" maps to the wrong path segment).
//
// The router stores routes and iterates through them to find a match.
// Parameters should be extracted from the URL and passed to the handler.

package router

import (
	"context"
	"net/http"
	"strings"
)

type ctxKey string

const ParamsKey ctxKey = "params"

// Handler is a standard http.HandlerFunc
type Handler = http.HandlerFunc

// Route represents a registered route with its pattern and handler.
type Route struct {
	Method  string
	Pattern string   // e.g., "/users/:id"
	Parts   []string // split pattern segments
	Handler Handler
}

// Router holds registered routes and dispatches incoming requests.
type Router struct {
	routes []Route
}

// NewRouter creates a new Router instance.
func NewRouter() *Router {
	return &Router{}
}

// Handle registers a new route for the given method and pattern.
func (r *Router) Handle(method, pattern string, handler Handler) {
	parts := splitPath(pattern)
	r.routes = append(r.routes, Route{
		Method:  method,
		Pattern: pattern,
		Parts:   parts,
		Handler: handler,
	})
}

// ServeHTTP dispatches the request to the matching route handler.
func (r *Router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	reqParts := splitPath(req.URL.Path)

	for _, route := range r.routes {
		if req.Method != route.Method {
			continue
		}

		params, ok := matchRoute(route.Parts, reqParts)
		if !ok {
			continue
		}

		// Attach params to context
		ctx := context.WithValue(req.Context(), ParamsKey, params)
		route.Handler(w, req.WithContext(ctx))
		return
	}

	http.NotFound(w, req)
}

// Params extracts the route parameters from the request context.
func Params(r *http.Request) map[string]string {
	if params, ok := r.Context().Value(ParamsKey).(map[string]string); ok {
		return params
	}
	return map[string]string{}
}

// splitPath splits a URL path into segments, ignoring empty strings from
// leading/trailing slashes.
func splitPath(path string) []string {
	var parts []string
	for _, p := range strings.Split(path, "/") {
		if p != "" {
			parts = append(parts, p)
		}
	}
	return parts
}

// BUG IS HERE: matchRoute tries to match route pattern parts against request
// path parts, extracting named parameters along the way.
func matchRoute(routeParts, reqParts []string) (map[string]string, bool) {
	// Length must match for a valid route match.
	if len(routeParts) != len(reqParts) {
		return nil, false
	}

	params := make(map[string]string)

	for i, routePart := range routeParts {
		if strings.HasPrefix(routePart, ":") {
			// This is a parameter segment — extract the value.
			// BUG: uses routePart (the pattern like ":id") instead of reqParts[i]
			// (the actual value like "42"). The parameter name key is also wrong:
			// it should strip the leading ":" from routePart.
			paramName := routePart // should be routePart[1:] to strip ":"
			paramValue := routeParts[i] // should be reqParts[i]
			params[paramName] = paramValue
			continue
		}

		// Static segment — must match exactly.
		if routePart != reqParts[i] {
			return nil, false
		}
	}

	return params, true
}
