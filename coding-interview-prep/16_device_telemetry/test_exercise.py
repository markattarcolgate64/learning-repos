"""Tests for the Device Telemetry Aggregator exercise."""

import unittest

from exercise import (
    FleetOverview,
    Heartbeat,
    DeviceSummary,
    TelemetryAggregator,
)


def _hb(orb_id="orb-001", timestamp=1000.0, cpu_temp=55.0,
        memory_used_pct=40.0, battery_pct=90.0,
        capture_success_rate=0.95, error_count=0):
    """Helper to create a Heartbeat with sensible defaults."""
    return Heartbeat(
        orb_id=orb_id,
        timestamp=timestamp,
        cpu_temp=cpu_temp,
        memory_used_pct=memory_used_pct,
        battery_pct=battery_pct,
        capture_success_rate=capture_success_rate,
        error_count=error_count,
    )


class TestTelemetryAggregator(unittest.TestCase):
    """Comprehensive tests for TelemetryAggregator."""

    # ------------------------------------------------------------------
    # 1. Ingest and retrieve summary for a single device
    # ------------------------------------------------------------------
    def test_single_device_summary(self):
        """Ingest several heartbeats and verify the summary statistics."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(timestamp=100, cpu_temp=50.0, battery_pct=80.0,
                        capture_success_rate=0.9, error_count=1))
        agg.ingest(_hb(timestamp=200, cpu_temp=60.0, battery_pct=70.0,
                        capture_success_rate=0.95, error_count=2))
        agg.ingest(_hb(timestamp=300, cpu_temp=70.0, battery_pct=60.0,
                        capture_success_rate=1.0, error_count=0))

        summary = agg.get_device_summary("orb-001")
        self.assertIsNotNone(summary)
        self.assertEqual(summary.orb_id, "orb-001")
        self.assertEqual(summary.heartbeat_count, 3)
        self.assertEqual(summary.time_range, (100, 300))

        cpu = summary.metrics["cpu_temp"]
        self.assertAlmostEqual(cpu["min"], 50.0)
        self.assertAlmostEqual(cpu["max"], 70.0)
        self.assertAlmostEqual(cpu["avg"], 60.0)

    # ------------------------------------------------------------------
    # 2. Time range filtering
    # ------------------------------------------------------------------
    def test_time_range_filtering(self):
        """Only heartbeats within [start_time, end_time] are included."""
        agg = TelemetryAggregator()
        for t in range(0, 500, 50):
            agg.ingest(_hb(timestamp=float(t), cpu_temp=40.0 + t / 50))

        # Filter to [100, 250]
        summary = agg.get_device_summary("orb-001", start_time=100, end_time=250)
        self.assertIsNotNone(summary)
        # timestamps: 100, 150, 200, 250 => 4 heartbeats
        self.assertEqual(summary.heartbeat_count, 4)
        self.assertEqual(summary.time_range, (100, 250))

    def test_start_time_only(self):
        """Filtering with only start_time includes everything from that point."""
        agg = TelemetryAggregator()
        for t in [100, 200, 300, 400]:
            agg.ingest(_hb(timestamp=float(t)))

        summary = agg.get_device_summary("orb-001", start_time=250)
        self.assertEqual(summary.heartbeat_count, 2)
        self.assertEqual(summary.time_range, (300, 400))

    def test_end_time_only(self):
        """Filtering with only end_time includes everything up to that point."""
        agg = TelemetryAggregator()
        for t in [100, 200, 300, 400]:
            agg.ingest(_hb(timestamp=float(t)))

        summary = agg.get_device_summary("orb-001", end_time=250)
        self.assertEqual(summary.heartbeat_count, 2)
        self.assertEqual(summary.time_range, (100, 200))

    # ------------------------------------------------------------------
    # 3. Ring buffer bounds
    # ------------------------------------------------------------------
    def test_ring_buffer_bounds(self):
        """With max_heartbeats_per_device=1000, ingesting 2000 keeps only 1000."""
        agg = TelemetryAggregator(max_heartbeats_per_device=1000)
        for i in range(2000):
            agg.ingest(_hb(timestamp=float(i), cpu_temp=20.0 + (i % 80)))

        summary = agg.get_device_summary("orb-001")
        self.assertEqual(summary.heartbeat_count, 1000)
        # Earliest should be timestamp 1000 (the first 1000 were evicted)
        self.assertEqual(summary.time_range[0], 1000.0)
        self.assertEqual(summary.time_range[1], 1999.0)

    def test_ring_buffer_small(self):
        """With max_heartbeats_per_device=5, only last 5 are retained."""
        agg = TelemetryAggregator(max_heartbeats_per_device=5)
        for i in range(20):
            agg.ingest(_hb(timestamp=float(i), cpu_temp=float(i)))

        summary = agg.get_device_summary("orb-001")
        self.assertEqual(summary.heartbeat_count, 5)
        self.assertAlmostEqual(summary.metrics["cpu_temp"]["min"], 15.0)
        self.assertAlmostEqual(summary.metrics["cpu_temp"]["max"], 19.0)

    # ------------------------------------------------------------------
    # 4. Detect unhealthy devices
    # ------------------------------------------------------------------
    def test_detect_unhealthy_high_cpu(self):
        """Device with high CPU temp is flagged as unhealthy."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="hot-orb", cpu_temp=85.0))
        agg.ingest(_hb(orb_id="cool-orb", cpu_temp=45.0))

        unhealthy = agg.detect_unhealthy({"cpu_temp_max": 80.0})
        self.assertIn("hot-orb", unhealthy)
        self.assertNotIn("cool-orb", unhealthy)

    def test_detect_unhealthy_low_battery(self):
        """Device with low battery is flagged."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="dying-orb", battery_pct=5.0))
        agg.ingest(_hb(orb_id="charged-orb", battery_pct=90.0))

        unhealthy = agg.detect_unhealthy({"battery_pct_min": 10.0})
        self.assertIn("dying-orb", unhealthy)
        self.assertNotIn("charged-orb", unhealthy)

    def test_detect_unhealthy_low_capture_rate(self):
        """Device with low capture success rate is flagged."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="bad-orb", capture_success_rate=0.5))
        agg.ingest(_hb(orb_id="good-orb", capture_success_rate=0.99))

        unhealthy = agg.detect_unhealthy({"capture_success_rate_min": 0.8})
        self.assertIn("bad-orb", unhealthy)
        self.assertNotIn("good-orb", unhealthy)

    def test_detect_unhealthy_high_errors(self):
        """Device with high error count is flagged."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="error-orb", error_count=100))
        agg.ingest(_hb(orb_id="clean-orb", error_count=2))

        unhealthy = agg.detect_unhealthy({"error_count_max": 50})
        self.assertIn("error-orb", unhealthy)
        self.assertNotIn("clean-orb", unhealthy)

    def test_detect_unhealthy_multiple_thresholds(self):
        """A device violating ANY threshold is flagged."""
        agg = TelemetryAggregator()
        # Only battery is bad
        agg.ingest(_hb(orb_id="orb-A", cpu_temp=50.0, battery_pct=5.0,
                        capture_success_rate=0.95, error_count=0))
        # Everything is fine
        agg.ingest(_hb(orb_id="orb-B", cpu_temp=50.0, battery_pct=90.0,
                        capture_success_rate=0.95, error_count=0))

        thresholds = {
            "cpu_temp_max": 80.0,
            "battery_pct_min": 10.0,
            "capture_success_rate_min": 0.8,
            "error_count_max": 50,
        }
        unhealthy = agg.detect_unhealthy(thresholds)
        self.assertEqual(unhealthy, ["orb-A"])

    def test_detect_unhealthy_healthy_fleet(self):
        """When all devices are healthy, return an empty list."""
        agg = TelemetryAggregator()
        for i in range(5):
            agg.ingest(_hb(orb_id=f"orb-{i}", cpu_temp=50.0, battery_pct=90.0,
                            capture_success_rate=0.95, error_count=0))

        thresholds = {
            "cpu_temp_max": 80.0,
            "battery_pct_min": 10.0,
            "capture_success_rate_min": 0.8,
            "error_count_max": 50,
        }
        self.assertEqual(agg.detect_unhealthy(thresholds), [])

    def test_detect_unhealthy_uses_latest_heartbeat(self):
        """Health check uses only the most recent heartbeat."""
        agg = TelemetryAggregator()
        # First heartbeat: unhealthy CPU
        agg.ingest(_hb(orb_id="orb-X", timestamp=100, cpu_temp=90.0))
        # Second heartbeat: healthy CPU
        agg.ingest(_hb(orb_id="orb-X", timestamp=200, cpu_temp=50.0))

        unhealthy = agg.detect_unhealthy({"cpu_temp_max": 80.0})
        self.assertNotIn("orb-X", unhealthy)

    # ------------------------------------------------------------------
    # 5. Fleet overview
    # ------------------------------------------------------------------
    def test_fleet_overview_multiple_devices(self):
        """Fleet overview aggregates across multiple devices correctly."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="orb-A", timestamp=1000.0, cpu_temp=50.0,
                        battery_pct=80.0, capture_success_rate=0.9, error_count=10))
        agg.ingest(_hb(orb_id="orb-B", timestamp=1000.0, cpu_temp=60.0,
                        battery_pct=90.0, capture_success_rate=1.0, error_count=5))

        overview = agg.fleet_overview(active_window_sec=300.0)
        self.assertEqual(overview.total_devices, 2)
        self.assertEqual(overview.active_devices, 2)
        self.assertAlmostEqual(overview.avg_cpu_temp, 55.0)
        self.assertAlmostEqual(overview.avg_battery_pct, 85.0)
        self.assertAlmostEqual(overview.avg_capture_success_rate, 0.95)
        self.assertEqual(overview.total_errors, 15)

    def test_fleet_overview_active_window(self):
        """Only devices with recent heartbeats count as active."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="orb-active", timestamp=1000.0, error_count=1))
        agg.ingest(_hb(orb_id="orb-stale", timestamp=100.0, error_count=2))

        overview = agg.fleet_overview(active_window_sec=300.0)
        self.assertEqual(overview.total_devices, 2)
        # Only orb-active is within 300s of the global latest (1000.0)
        self.assertEqual(overview.active_devices, 1)

    def test_fleet_overview_empty(self):
        """Fleet overview of an empty aggregator."""
        agg = TelemetryAggregator()
        overview = agg.fleet_overview()
        self.assertEqual(overview.total_devices, 0)
        self.assertEqual(overview.active_devices, 0)
        self.assertAlmostEqual(overview.avg_cpu_temp, 0.0)
        self.assertAlmostEqual(overview.avg_battery_pct, 0.0)
        self.assertAlmostEqual(overview.avg_capture_success_rate, 0.0)
        self.assertEqual(overview.total_errors, 0)

    # ------------------------------------------------------------------
    # 6. Unknown device returns None
    # ------------------------------------------------------------------
    def test_unknown_device_returns_none(self):
        """Requesting a summary for an unknown device returns None."""
        agg = TelemetryAggregator()
        self.assertIsNone(agg.get_device_summary("nonexistent"))

    # ------------------------------------------------------------------
    # 7. Percentile calculation
    # ------------------------------------------------------------------
    def test_percentile_p99(self):
        """P99 calculation is correct for a known distribution."""
        agg = TelemetryAggregator()
        # Ingest 100 heartbeats with cpu_temp = 1, 2, ..., 100
        for i in range(1, 101):
            agg.ingest(_hb(timestamp=float(i), cpu_temp=float(i)))

        summary = agg.get_device_summary("orb-001")
        # p99 index = int(0.99 * 99) = int(98.01) = 98 => value at sorted[98] = 99
        self.assertAlmostEqual(summary.metrics["cpu_temp"]["p99"], 99.0)

    def test_percentile_single_heartbeat(self):
        """P99 of a single value is that value itself."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(cpu_temp=42.0))

        summary = agg.get_device_summary("orb-001")
        # int(0.99 * 0) = 0 => sorted[0] = 42.0
        self.assertAlmostEqual(summary.metrics["cpu_temp"]["p99"], 42.0)

    # ------------------------------------------------------------------
    # 8. Empty time range returns empty summary
    # ------------------------------------------------------------------
    def test_empty_time_range_returns_none(self):
        """If no heartbeats fall in the time range, return None."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(timestamp=100.0))
        agg.ingest(_hb(timestamp=200.0))

        # Range that contains no heartbeats
        summary = agg.get_device_summary("orb-001", start_time=300, end_time=400)
        self.assertIsNone(summary)

    # ------------------------------------------------------------------
    # 9. Detect unhealthy returns sorted orb_ids
    # ------------------------------------------------------------------
    def test_detect_unhealthy_sorted(self):
        """Unhealthy device list is sorted alphabetically."""
        agg = TelemetryAggregator()
        agg.ingest(_hb(orb_id="orb-Z", cpu_temp=90.0))
        agg.ingest(_hb(orb_id="orb-A", cpu_temp=90.0))
        agg.ingest(_hb(orb_id="orb-M", cpu_temp=90.0))

        unhealthy = agg.detect_unhealthy({"cpu_temp_max": 80.0})
        self.assertEqual(unhealthy, ["orb-A", "orb-M", "orb-Z"])


if __name__ == "__main__":
    unittest.main()
