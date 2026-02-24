package respbuilder

import (
	"encoding/json"
	"testing"
)

// Payload is a sample struct used in tests.
type Payload struct {
	Name  string `json:"name"`
	Count int    `json:"count"`
}

func TestBuildWithData(t *testing.T) {
	data := &Payload{Name: "widget", Count: 5}

	b, err := NewBuilder().SetData(data).ToJSON()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var result map[string]any
	if err := json.Unmarshal(b, &result); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if result["success"] != true {
		t.Fatalf("expected success=true, got %v", result["success"])
	}

	dataMap, ok := result["data"].(map[string]any)
	if !ok {
		t.Fatalf("expected data to be a map, got %T", result["data"])
	}
	if dataMap["name"] != "widget" {
		t.Fatalf("expected data.name='widget', got %v", dataMap["name"])
	}
	if dataMap["count"] != float64(5) {
		t.Fatalf("expected data.count=5, got %v", dataMap["count"])
	}
}

func TestBuildWithUntypedNil(t *testing.T) {
	// Passing a plain nil should omit the data field entirely.
	b, err := NewBuilder().SetData(nil).ToJSON()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var result map[string]any
	if err := json.Unmarshal(b, &result); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if _, exists := result["data"]; exists {
		t.Fatalf("expected 'data' field to be omitted for nil, but it was present: %v", result["data"])
	}
}

func TestBuildWithTypedNilPointer(t *testing.T) {
	// This is the critical test. A typed nil pointer should be treated the
	// same as an untyped nil — the data field should be omitted.
	//
	// In Go, `var p *Payload = nil` creates an interface value with type
	// information (*Payload) but a nil underlying pointer. A naive
	// `data != nil` check will pass because the interface is not nil.
	var p *Payload = nil

	b, err := NewBuilder().SetData(p).ToJSON()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var result map[string]any
	if err := json.Unmarshal(b, &result); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	// The data field should be absent, NOT "null".
	if _, exists := result["data"]; exists {
		t.Fatalf("expected 'data' field to be omitted for typed nil, but it was present: %v", result["data"])
	}
}

func TestBuildWithError(t *testing.T) {
	b, err := NewBuilder().SetError("not found").ToJSON()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var result map[string]any
	if err := json.Unmarshal(b, &result); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if result["success"] != false {
		t.Fatalf("expected success=false, got %v", result["success"])
	}
	if result["error"] != "not found" {
		t.Fatalf("expected error='not found', got %v", result["error"])
	}
}

func TestBuildWithMeta(t *testing.T) {
	data := &Payload{Name: "item", Count: 1}

	b, err := NewBuilder().
		SetData(data).
		SetMeta("page", 1).
		SetMeta("total", 100).
		ToJSON()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var result map[string]any
	if err := json.Unmarshal(b, &result); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	meta, ok := result["meta"].(map[string]any)
	if !ok {
		t.Fatalf("expected meta to be a map, got %T", result["meta"])
	}
	if meta["page"] != float64(1) {
		t.Fatalf("expected meta.page=1, got %v", meta["page"])
	}
	if meta["total"] != float64(100) {
		t.Fatalf("expected meta.total=100, got %v", meta["total"])
	}
}

func TestBuildNoData(t *testing.T) {
	// Not calling SetData at all — data should be omitted.
	b, err := NewBuilder().ToJSON()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var result map[string]any
	if err := json.Unmarshal(b, &result); err != nil {
		t.Fatalf("failed to unmarshal response: %v", err)
	}

	if _, exists := result["data"]; exists {
		t.Fatalf("expected 'data' field to be omitted when not set, but it was present")
	}
	if result["success"] != true {
		t.Fatalf("expected success=true, got %v", result["success"])
	}
}
