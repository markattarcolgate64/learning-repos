"""
Tests for Priority Job Queue.

Run with:
    python -m unittest 10_job_queue.test_exercise -v
"""

import unittest
from .exercise import JobQueue, JobStatus, Job


class TestJobQueue(unittest.TestCase):
    """Comprehensive tests for the priority job queue with lifecycle management."""

    # ------------------------------------------------------------------
    # 1. Basic enqueue/dequeue: FIFO when same priority
    # ------------------------------------------------------------------

    def test_fifo_same_priority(self):
        """Jobs with the same priority should be dequeued in FIFO order."""
        q = JobQueue()
        q.enqueue("j1", {"task": "a"}, priority=0)
        q.enqueue("j2", {"task": "b"}, priority=0)
        q.enqueue("j3", {"task": "c"}, priority=0)

        self.assertEqual(q.dequeue().job_id, "j1")
        self.assertEqual(q.dequeue().job_id, "j2")
        self.assertEqual(q.dequeue().job_id, "j3")

    # ------------------------------------------------------------------
    # 2. Priority ordering: higher priority dequeued first
    # ------------------------------------------------------------------

    def test_priority_ordering(self):
        """Higher-priority jobs should be dequeued before lower-priority ones."""
        q = JobQueue()
        q.enqueue("low", {"task": "low"}, priority=1)
        q.enqueue("high", {"task": "high"}, priority=10)
        q.enqueue("med", {"task": "med"}, priority=5)

        self.assertEqual(q.dequeue().job_id, "high")
        self.assertEqual(q.dequeue().job_id, "med")
        self.assertEqual(q.dequeue().job_id, "low")

    # ------------------------------------------------------------------
    # 3. Job lifecycle: PENDING -> PROCESSING -> COMPLETED
    # ------------------------------------------------------------------

    def test_lifecycle_pending_processing_completed(self):
        """A job should transition through PENDING -> PROCESSING -> COMPLETED."""
        q = JobQueue()
        job = q.enqueue("j1", {"task": "test"})
        self.assertEqual(job.status, JobStatus.PENDING)

        job = q.dequeue()
        self.assertEqual(job.status, JobStatus.PROCESSING)

        job = q.complete("j1")
        self.assertEqual(job.status, JobStatus.COMPLETED)

    # ------------------------------------------------------------------
    # 4. Retry on failure: failed job re-enqueued, retries incremented
    # ------------------------------------------------------------------

    def test_retry_on_failure(self):
        """A failed job with retries remaining should be re-enqueued as PENDING."""
        q = JobQueue()
        q.enqueue("j1", {"task": "flaky"}, max_retries=3)
        job = q.dequeue()
        self.assertEqual(job.status, JobStatus.PROCESSING)

        job = q.fail("j1", "timeout")
        self.assertEqual(job.status, JobStatus.PENDING)
        self.assertEqual(job.retries, 1)
        self.assertEqual(job.error, "timeout")

        # Should be dequeueable again
        job = q.dequeue()
        self.assertIsNotNone(job)
        self.assertEqual(job.job_id, "j1")
        self.assertEqual(job.status, JobStatus.PROCESSING)

    # ------------------------------------------------------------------
    # 5. Max retries exceeded: job permanently FAILED
    # ------------------------------------------------------------------

    def test_max_retries_exceeded(self):
        """When retries reach max_retries, the job should be permanently FAILED."""
        q = JobQueue()
        q.enqueue("j1", {"task": "always-fails"}, max_retries=2)

        # Attempt 1
        q.dequeue()
        q.fail("j1", "error 1")  # retries=1, still < 2 -> re-enqueued

        # Attempt 2
        q.dequeue()
        q.fail("j1", "error 2")  # retries=2, 2 >= 2 -> permanently FAILED

        job = q.get_job("j1")
        self.assertEqual(job.status, JobStatus.FAILED)
        self.assertEqual(job.retries, 2)

        # Queue should be empty now
        self.assertIsNone(q.dequeue())

    # ------------------------------------------------------------------
    # 6. Empty queue: dequeue returns None
    # ------------------------------------------------------------------

    def test_empty_dequeue(self):
        """Dequeuing from an empty queue should return None."""
        q = JobQueue()
        self.assertIsNone(q.dequeue())

    # ------------------------------------------------------------------
    # 7. get_stats: correct counts per status
    # ------------------------------------------------------------------

    def test_get_stats(self):
        """get_stats should return accurate counts per status."""
        q = JobQueue()
        q.enqueue("j1", {}, priority=1)
        q.enqueue("j2", {}, priority=2)
        q.enqueue("j3", {}, priority=3, max_retries=0)

        # j3 -> processing
        q.dequeue()
        q.complete("j3")

        # j2 -> processing
        q.dequeue()

        # j2 -> fail permanently (max_retries=3 by default, so it retries)
        q.fail("j2", "oops")

        stats = q.get_stats()
        # j1=PENDING, j2=PENDING (retried), j3=COMPLETED
        self.assertEqual(stats["pending"], 2)  # j1 + j2 (retried)
        self.assertEqual(stats["completed"], 1)  # j3
        self.assertEqual(stats["processing"], 0)

    # ------------------------------------------------------------------
    # 8. get_job: retrieves by ID
    # ------------------------------------------------------------------

    def test_get_job(self):
        """get_job should return the correct Job by ID."""
        q = JobQueue()
        q.enqueue("abc", {"data": 42}, priority=5)
        job = q.get_job("abc")
        self.assertEqual(job.job_id, "abc")
        self.assertEqual(job.payload, {"data": 42})
        self.assertEqual(job.priority, 5)

    def test_get_job_missing_raises(self):
        """get_job for a nonexistent ID should raise KeyError."""
        q = JobQueue()
        with self.assertRaises(KeyError):
            q.get_job("nonexistent")

    # ------------------------------------------------------------------
    # 9. Multiple priorities: mixed priority ordering
    # ------------------------------------------------------------------

    def test_mixed_priorities(self):
        """Jobs with various priorities should be dequeued in correct order."""
        q = JobQueue()
        q.enqueue("p0", {}, priority=0)
        q.enqueue("p5a", {}, priority=5)
        q.enqueue("p3", {}, priority=3)
        q.enqueue("p5b", {}, priority=5)
        q.enqueue("p10", {}, priority=10)

        order = []
        while True:
            job = q.dequeue()
            if job is None:
                break
            order.append(job.job_id)

        self.assertEqual(order, ["p10", "p5a", "p5b", "p3", "p0"])

    # ------------------------------------------------------------------
    # 10. get_pending_count accurate
    # ------------------------------------------------------------------

    def test_get_pending_count(self):
        """get_pending_count should reflect the number of PENDING jobs."""
        q = JobQueue()
        self.assertEqual(q.get_pending_count(), 0)

        q.enqueue("j1", {})
        q.enqueue("j2", {})
        q.enqueue("j3", {})
        self.assertEqual(q.get_pending_count(), 3)

        q.dequeue()  # j1 -> PROCESSING
        self.assertEqual(q.get_pending_count(), 2)

        q.dequeue()  # j2 -> PROCESSING
        self.assertEqual(q.get_pending_count(), 1)


if __name__ == "__main__":
    unittest.main()
