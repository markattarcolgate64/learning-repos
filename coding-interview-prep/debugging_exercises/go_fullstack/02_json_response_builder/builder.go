// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// JSON Response Builder with Nil Interface Bug
// ==============================================
//
// This is a response builder for JSON API responses. It constructs a standard
// envelope with optional fields:
//
//   {
//     "success": true,
//     "data": { ... },
//     "error": "...",
//     "meta": { ... }
//   }
//
// The builder allows callers to set data, error messages, and metadata.
// When data is nil, the "data" field should be omitted from the JSON output
// (or rendered as null), NOT cause a panic.
//
// SYMPTOMS:
//   - Calling SetData with a typed nil pointer (e.g., `var p *MyStruct = nil;
//     builder.SetData(p)`) does NOT trigger the nil guard in SetData.
//   - The response is built with a non-nil interface holding a nil pointer,
//     which can cause unexpected behavior during JSON marshaling or downstream
//     nil checks.
//   - Tests that pass a typed nil expect the data field to be omitted, but
//     instead it either panics or produces `"data": null` inconsistently.
//
// This is the classic Go gotcha: an interface holding a typed nil pointer
// is NOT equal to nil.

package respbuilder

import (
	"encoding/json"
)

// Response is the JSON envelope returned by the API.
type Response struct {
	Success bool            `json:"success"`
	Data    json.RawMessage `json:"data,omitempty"`
	Error   string          `json:"error,omitempty"`
	Meta    map[string]any  `json:"meta,omitempty"`
}

// Builder constructs a Response step by step.
type Builder struct {
	success bool
	data    any
	hasData bool
	err     string
	meta    map[string]any
}

// NewBuilder creates a new response builder defaulting to success=true.
func NewBuilder() *Builder {
	return &Builder{
		success: true,
	}
}

// SetData sets the data payload. If data is nil, it will be omitted.
// BUG: This nil check only catches an untyped nil (i.e., a bare `nil`).
// A typed nil pointer (e.g., `var p *MyStruct = nil`) passes through because
// the interface value is non-nil (it has type information), even though the
// underlying pointer is nil.
func (b *Builder) SetData(data any) *Builder {
	if data != nil {
		b.data = data
		b.hasData = true
	}
	return b
}

// SetError sets the error message and marks the response as unsuccessful.
func (b *Builder) SetError(msg string) *Builder {
	b.err = msg
	b.success = false
	return b
}

// SetMeta sets metadata key-value pairs on the response.
func (b *Builder) SetMeta(key string, value any) *Builder {
	if b.meta == nil {
		b.meta = make(map[string]any)
	}
	b.meta[key] = value
	return b
}

// Build constructs the final Response, marshaling the data payload into
// json.RawMessage.
func (b *Builder) Build() (*Response, error) {
	resp := &Response{
		Success: b.success,
		Error:   b.err,
		Meta:    b.meta,
	}

	if b.hasData {
		raw, err := json.Marshal(b.data)
		if err != nil {
			return nil, err
		}
		resp.Data = raw
	}

	return resp, nil
}

// ToJSON is a convenience method that builds and marshals the response to JSON bytes.
func (b *Builder) ToJSON() ([]byte, error) {
	resp, err := b.Build()
	if err != nil {
		return nil, err
	}
	return json.Marshal(resp)
}
