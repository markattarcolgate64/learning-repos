// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// System: Batch Processor
// Description: Accumulates items into a buffer and flushes them in fixed-size
// batches. When the buffer reaches the batch size, it automatically flushes.
// Manual flushing is also supported for partial batches. A callback function
// is invoked with each flushed batch.
//
// Expected behavior:
//   - Add() appends items to an internal buffer
//   - When the buffer reaches batchSize, the batch is flushed via the callback
//   - Flush() manually flushes whatever is in the buffer
//   - Each flushed batch should be an independent snapshot of the data
//   - Adding new items after a flush must NOT modify previously flushed batches
//
// Symptoms of the bug:
//   - Flushed batch data gets corrupted after new items are added
//   - A batch that was flushed correctly initially has its values overwritten
//   - The first few elements of a new batch match what should be in the old batch
//   - Tests show data corruption: batch contents change after they were already flushed
//
// Hint: This is a classic Go slice gotcha. Think about how slices share
//       underlying arrays and what happens when you "reset" a slice with [:0].

package batchprocessor

// Processor accumulates items and flushes them in batches.
type Processor struct {
	batchSize int
	buffer    []string
	callback  func(batch []string)
}

// New creates a new Processor with the given batch size and flush callback.
func New(batchSize int, callback func(batch []string)) *Processor {
	return &Processor{
		batchSize: batchSize,
		buffer:    make([]string, 0, batchSize),
		callback:  callback,
	}
}

// Add appends an item to the buffer. If the buffer reaches the batch size,
// it is automatically flushed.
func (p *Processor) Add(item string) {
	p.buffer = append(p.buffer, item)

	if len(p.buffer) >= p.batchSize {
		p.flush()
	}
}

// Flush manually flushes the current buffer, regardless of how full it is.
func (p *Processor) Flush() {
	if len(p.buffer) > 0 {
		p.flush()
	}
}

// flush sends the current buffer to the callback and resets the buffer.
func (p *Processor) flush() {
	// Pass the current buffer to the callback
	p.callback(p.buffer)

	// "Reset" the buffer by re-slicing to zero length.
	// This retains the underlying array, so the next append
	// will write into the same memory that was just flushed.
	p.buffer = p.buffer[:0]
}

// BufferLen returns the number of items currently in the buffer.
func (p *Processor) BufferLen() int {
	return len(p.buffer)
}
