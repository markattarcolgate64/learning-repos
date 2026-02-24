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
//   - Shutdown() stops accepting new jobs, waits for all pending jobs to be
//     processed, then returns
//   - After Shutdown(), Results() returns all processed results
//
// Symptoms of the bug:
//   - Not all submitted jobs appear in the results after Shutdown()
//   - The number of results is less than the number of submitted jobs
//   - Tests report "expected 20 results, got N" where N < 20
//   - The problem is worse when the job channel has buffered (pending) jobs
//
// Hint: Look at what happens to jobs sitting in the channel buffer when
//       Shutdown() is called. Does the worker finish processing them?

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
	quit       chan struct{}
	wg         sync.WaitGroup
	results    []Result
	mu         sync.Mutex
}

// New creates a new worker pool with the given number of workers.
func New(numWorkers int) *Pool {
	p := &Pool{
		numWorkers: numWorkers,
		jobs:       make(chan Job, 100),
		quit:       make(chan struct{}),
		results:    make([]Result, 0),
	}
	p.start()
	return p
}

// start launches the worker goroutines.
func (p *Pool) start() {
	for i := 0; i < p.numWorkers; i++ {
		p.wg.Add(1)
		go p.worker(i)
	}
}

// worker processes jobs from the jobs channel.
func (p *Pool) worker(id int) {
	defer p.wg.Done()

	for {
		select {
		case <-p.quit:
			return
		case job := <-p.jobs:
			result := Result{
				JobID:  job.ID,
				Output: processJob(job),
			}
			p.mu.Lock()
			p.results = append(p.results, result)
			p.mu.Unlock()
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
	close(p.quit)
	p.wg.Wait()
}

// Results returns all processed results.
func (p *Pool) Results() []Result {
	p.mu.Lock()
	defer p.mu.Unlock()
	return append([]Result{}, p.results...)
}
