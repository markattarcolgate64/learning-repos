"""
Priority Job Queue - Solution

An in-memory priority job queue with lifecycle management. Jobs are enqueued
with a priority (higher = dequeued first) and tracked through states:
PENDING -> PROCESSING -> COMPLETED or FAILED. Failed jobs are retried
automatically up to max_retries.
"""

import time
import heapq
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
        """Initialise the job queue."""
        self._heap = []
        self._jobs = {}
        self._counter = 0

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
        job = Job(
            job_id=job_id,
            payload=payload,
            priority=priority,
            max_retries=max_retries,
        )
        self._jobs[job_id] = job
        heapq.heappush(self._heap, (-priority, self._counter, job_id))
        self._counter += 1
        return job

    def dequeue(self) -> Job:
        """Remove and return the highest-priority pending job.

        The returned job's status is changed to PROCESSING.

        Returns:
            The highest-priority Job, or None if no pending jobs exist.
        """
        while self._heap:
            neg_priority, counter, job_id = heapq.heappop(self._heap)
            job = self._jobs[job_id]
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.PROCESSING
                return job
        return None

    def complete(self, job_id: str) -> Job:
        """Mark a job as successfully completed.

        Args:
            job_id: The ID of the job to complete.

        Returns:
            The updated Job instance.

        Raises:
            KeyError: If the job_id does not exist.
        """
        job = self._jobs[job_id]
        job.status = JobStatus.COMPLETED
        return job

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
        job = self._jobs[job_id]
        job.error = error
        job.retries += 1

        if job.retries < job.max_retries:
            job.status = JobStatus.PENDING
            heapq.heappush(self._heap, (-job.priority, self._counter, job_id))
            self._counter += 1
        else:
            job.status = JobStatus.FAILED

        return job

    def get_job(self, job_id: str) -> Job:
        """Retrieve a job by its ID.

        Args:
            job_id: The ID of the job to look up.

        Returns:
            The Job instance.

        Raises:
            KeyError: If the job_id does not exist.
        """
        return self._jobs[job_id]

    def get_stats(self) -> dict:
        """Return a summary of job counts by status.

        Returns:
            A dict with keys 'pending', 'processing', 'completed', 'failed'
            and integer counts as values.
        """
        stats = {"pending": 0, "processing": 0, "completed": 0, "failed": 0}
        for job in self._jobs.values():
            stats[job.status.value.lower()] += 1
        return stats

    def get_pending_count(self) -> int:
        """Return the number of jobs currently in PENDING status.

        Returns:
            The count of pending jobs.
        """
        return sum(1 for job in self._jobs.values() if job.status == JobStatus.PENDING)
