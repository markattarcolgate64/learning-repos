"""
Priority Job Queue
==================
Category   : Full-Stack / Systems
Difficulty : ** (2/5)

Problem
-------
Implement an in-memory priority job queue with full lifecycle management.
Jobs are enqueued with a priority (higher number = higher priority) and
dequeued in priority order.  Each job tracks its status through a lifecycle:
PENDING -> PROCESSING -> COMPLETED or FAILED.

Failed jobs are automatically retried up to a configurable maximum number of
retries before being marked permanently FAILED.

Real-world motivation
---------------------
Job queues are a fundamental building block in backend systems:
  - Celery, Sidekiq, and Bull all implement priority-based task scheduling.
  - Cloud services like AWS SQS and Google Cloud Tasks use similar patterns
    for reliable asynchronous processing.
  - Retry-with-backoff is essential for resilient microservice architectures
    where downstream services may be temporarily unavailable.

Understanding how to build one from scratch helps you reason about ordering
guarantees, state machines, and failure handling in distributed systems.

Hints
-----
1. A max-heap (or sorted structure) gives efficient highest-priority-first
   dequeue.  Python's heapq is a *min*-heap, so negate the priority or use
   a wrapper to get max-heap behaviour.
2. Track all jobs in a dict keyed by job_id for O(1) lookup.
3. On failure, increment the retry counter.  If retries < max_retries,
   re-enqueue the job as PENDING; otherwise mark it FAILED permanently.
4. get_stats should iterate over all jobs and count by status.

Run command
-----------
    pytest 10_job_queue/test_exercise.py -v
"""

import time
from enum import Enum
from dataclasses import dataclass, field


class JobStatus(Enum):
    """Lifecycle states a job can be in."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Job:
    """A single unit of work in the queue.

    Attributes:
        job_id: Unique identifier for the job.
        payload: Arbitrary dict describing the work to be done.
        priority: Scheduling priority (higher number = dequeued first).
        status: Current lifecycle state.
        retries: Number of times this job has been retried after failure.
        max_retries: Maximum retry attempts before permanent failure.
        created_at: Unix timestamp when the job was created.
        error: Description of the most recent failure, or None.
    """

    job_id: str
    payload: dict
    priority: int = 0
    status: JobStatus = JobStatus.PENDING
    retries: int = 0
    max_retries: int = 3
    created_at: float = field(default_factory=time.time)
    error: str = None


class JobQueue:
    """An in-memory priority job queue with lifecycle management.

    Jobs are enqueued with a priority and dequeued highest-priority-first.
    Failed jobs are retried automatically until they exceed max_retries.
    """

    def __init__(self) -> None:
        """Initialise the job queue.

        Sets up data structures for priority-ordered pending jobs and a
        lookup table for all jobs by ID.
        """
        # TODO: Create a data structure for pending jobs ordered by priority.
        # TODO: Create a dict mapping job_id -> Job for O(1) lookup.
        # Hint: Python's heapq is a min-heap.  To get max-priority-first,
        #       push tuples of (-priority, insertion_counter, job_id) and
        #       keep a counter to break ties in FIFO order.
        pass

    def enqueue(
        self, job_id: str, payload: dict, priority: int = 0, max_retries: int = 3
    ) -> Job:
        """Create a new job and add it to the pending queue.

        Args:
            job_id: Unique identifier for the job.
            payload: Arbitrary dict describing the work.
            priority: Scheduling priority (higher = dequeued sooner).
            max_retries: Maximum number of retry attempts on failure.

        Returns:
            The newly created Job instance.
        """
        # TODO: Create a Job with PENDING status and the given parameters.
        # TODO: Add the job to the lookup dict.
        # TODO: Push the job into the priority-ordered pending structure.
        # Hint: heapq.heappush(self._heap, (-priority, self._counter, job_id))
        pass

    def dequeue(self) -> Job:
        """Remove and return the highest-priority pending job.

        The returned job's status is changed to PROCESSING.

        Returns:
            The highest-priority Job, or None if no pending jobs exist.
        """
        # TODO: Pop from the priority structure until you find a job that is
        #       still PENDING (skip jobs that were already processed or failed).
        # TODO: Mark the job as PROCESSING and return it.
        # Hint: Jobs may have been re-enqueued or cancelled between push and
        #       pop, so always verify the status after popping.
        pass

    def complete(self, job_id: str) -> Job:
        """Mark a job as successfully completed.

        Args:
            job_id: The ID of the job to complete.

        Returns:
            The updated Job instance.

        Raises:
            KeyError: If the job_id does not exist.
        """
        # TODO: Look up the job by ID.
        # TODO: Set its status to COMPLETED.
        # TODO: Return the job.
        pass

    def fail(self, job_id: str, error: str) -> Job:
        """Record a job failure and retry or permanently fail.

        If the job has not exceeded its max_retries, increments the retry
        counter, sets the status back to PENDING, and re-enqueues it.
        Otherwise marks the job as permanently FAILED.

        Args:
            job_id: The ID of the job that failed.
            error: A description of what went wrong.

        Returns:
            The updated Job instance.

        Raises:
            KeyError: If the job_id does not exist.
        """
        # TODO: Look up the job, store the error message.
        # TODO: Increment retries.
        # TODO: If retries < max_retries, set status to PENDING and
        #       re-enqueue into the priority structure.
        # TODO: Otherwise set status to FAILED.
        # Hint: Re-enqueue with the same priority so it competes fairly.
        pass

    def get_job(self, job_id: str) -> Job:
        """Retrieve a job by its ID.

        Args:
            job_id: The ID of the job to look up.

        Returns:
            The Job instance.

        Raises:
            KeyError: If the job_id does not exist.
        """
        # TODO: Return the job from the lookup dict.
        pass

    def get_stats(self) -> dict:
        """Return a summary of job counts by status.

        Returns:
            A dict with keys 'pending', 'processing', 'completed', 'failed'
            and integer counts as values.
        """
        # TODO: Iterate over all jobs and count each status.
        # Hint: {status.value.lower(): count for ...} or use Counter.
        pass

    def get_pending_count(self) -> int:
        """Return the number of jobs currently in PENDING status.

        Returns:
            The count of pending jobs.
        """
        # TODO: Count jobs with status == JobStatus.PENDING.
        pass
