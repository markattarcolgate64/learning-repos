// DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
//
// System: Worker Pool
// Description: A worker pool that processes jobs concurrently using a fixed number
// of goroutines. Jobs are submitted via Submit(), processed by worker goroutines,
// and results are collected. The pool can be shut down gracefully via Shutdown().
//
// Expected behavior:
//   - Submit() sends jobs to the pool for processing
//   - Workers process jobs concurrently and store results
//   - Shutdown() stops all workers and waits for them to finish
//   - After Shutdown(), Results() returns all processed results
//
// Symptoms of the bug:
//   - Shutdown() hangs forever (deadlock)
//   - The program never terminates when the pool is shut down
//   - Tests timeout waiting for Shutdown() to return
//
// Hint: Look carefully at how workers signal completion and how Shutdown() waits.

package workerpool

import (
	"sync"
)

// Job represents a unit of work to be processed.
type Job struct {
	ID      int
	Payload string
}

// Result represents the output of processing a Job.
type Result struct {
	JobID  int
	Output string
}

// Pool manages a set of worker goroutines that process jobs.
type Pool struct {
	numWorkers int
	jobs       chan Job
	done       chan struct{}
	results    []Result
	mu         sync.Mutex
	shutdown   chan struct{}
}

// New creates a new worker pool with the given number of workers.
func New(numWorkers int) *Pool {
	p := &Pool{
		numWorkers: numWorkers,
		jobs:       make(chan Job, 100),
		done:       make(chan struct{}),
		results:    make([]Result, 0),
		shutdown:   make(chan struct{}),
	}
	p.start()
	return p
}

// start launches the worker goroutines.
func (p *Pool) start() {
	for i := 0; i < p.numWorkers; i++ {
		go p.worker(i)
	}
}

// worker processes jobs from the jobs channel until shutdown is signaled.
func (p *Pool) worker(id int) {
	for {
		select {
		case job, ok := <-p.jobs:
			if !ok {
				p.done <- struct{}{}
				return
			}
			result := Result{
				JobID:  job.ID,
				Output: processJob(job),
			}
			p.mu.Lock()
			p.results = append(p.results, result)
			p.mu.Unlock()
		case <-p.shutdown:
			p.done <- struct{}{}
			return
		}
	}
}

// processJob simulates processing a job.
func processJob(j Job) string {
	return "processed:" + j.Payload
}

// Submit adds a job to the pool for processing.
func (p *Pool) Submit(job Job) {
	p.jobs <- job
}

// Shutdown gracefully stops the pool and waits for all workers to finish.
func (p *Pool) Shutdown() {
	close(p.shutdown)
	close(p.jobs)

	// Wait for all workers to signal completion
	for i := 0; i < p.numWorkers; i++ {
		<-p.done
	}
}

// Results returns all processed results.
func (p *Pool) Results() []Result {
	p.mu.Lock()
	defer p.mu.Unlock()
	return append([]Result{}, p.results...)
}
