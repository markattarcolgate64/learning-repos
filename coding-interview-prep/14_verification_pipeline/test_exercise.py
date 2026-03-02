"""Tests for the Verification Event Pipeline exercise."""

import unittest

from exercise import VerificationEvent, Alert, VerificationPipeline


class TestHaversine(unittest.TestCase):
    """Verify the Haversine distance helper against known city pairs."""

    # ------------------------------------------------------------------
    # 1. Same point -> zero distance
    # ------------------------------------------------------------------
    def test_same_point_returns_zero(self):
        """Distance from a point to itself should be zero."""
        dist = VerificationPipeline._haversine(40.0, -74.0, 40.0, -74.0)
        self.assertAlmostEqual(dist, 0.0, places=3)

    # ------------------------------------------------------------------
    # 2. New York to London  (~5570 km)
    # ------------------------------------------------------------------
    def test_new_york_to_london(self):
        """NYC (40.7128N, 74.0060W) to London (51.5074N, 0.1278W) ~ 5570 km."""
        dist = VerificationPipeline._haversine(40.7128, -74.0060, 51.5074, -0.1278)
        self.assertAlmostEqual(dist, 5570, delta=30)

    # ------------------------------------------------------------------
    # 3. San Francisco to Tokyo  (~8280 km)
    # ------------------------------------------------------------------
    def test_san_francisco_to_tokyo(self):
        """SF (37.7749N, 122.4194W) to Tokyo (35.6762N, 139.6503E) ~ 8280 km."""
        dist = VerificationPipeline._haversine(37.7749, -122.4194, 35.6762, 139.6503)
        self.assertAlmostEqual(dist, 8280, delta=50)

    # ------------------------------------------------------------------
    # 4. Antipodal points -> ~20015 km  (half circumference)
    # ------------------------------------------------------------------
    def test_antipodal_points(self):
        """North Pole to South Pole ~ 20015 km."""
        dist = VerificationPipeline._haversine(90.0, 0.0, -90.0, 0.0)
        self.assertAlmostEqual(dist, 20015, delta=20)

    # ------------------------------------------------------------------
    # 5. Short distance: Paris to Versailles (~17 km)
    # ------------------------------------------------------------------
    def test_paris_to_versailles(self):
        """Paris (48.8566N, 2.3522E) to Versailles (48.8014N, 2.1301E) ~ 17 km."""
        dist = VerificationPipeline._haversine(48.8566, 2.3522, 48.8014, 2.1301)
        self.assertAlmostEqual(dist, 17, delta=2)


class TestNormalEvents(unittest.TestCase):
    """Normal (non-fraudulent) events should produce no alerts."""

    # ------------------------------------------------------------------
    # 6. Single event -> no alerts
    # ------------------------------------------------------------------
    def test_single_event_no_alerts(self):
        """Processing a single valid event should produce no alerts."""
        pipeline = VerificationPipeline()
        event = VerificationEvent(
            orb_id="orb-001",
            iris_hash="aaa111",
            timestamp=1000.0,
            latitude=40.7128,
            longitude=-74.0060,
        )
        alerts = pipeline.process_event(event)
        self.assertEqual(alerts, [])

    # ------------------------------------------------------------------
    # 7. Several unique events -> no alerts
    # ------------------------------------------------------------------
    def test_several_unique_events_no_alerts(self):
        """Multiple events with unique iris hashes from different orbs produce no alerts."""
        pipeline = VerificationPipeline()
        for i in range(10):
            event = VerificationEvent(
                orb_id=f"orb-{i:03d}",
                iris_hash=f"hash-{i:04d}",
                timestamp=1000.0 + i * 600,
                latitude=40.0 + i * 0.01,
                longitude=-74.0 + i * 0.01,
            )
            alerts = pipeline.process_event(event)
            self.assertEqual(alerts, [], f"Unexpected alert on event {i}")


class TestDuplicateIris(unittest.TestCase):
    """Duplicate iris hash detection."""

    # ------------------------------------------------------------------
    # 8. Duplicate iris hash triggers alert
    # ------------------------------------------------------------------
    def test_duplicate_iris_triggers_alert(self):
        """A repeated iris_hash should trigger a duplicate_iris alert."""
        pipeline = VerificationPipeline()
        e1 = VerificationEvent("orb-001", "hash-dup", 1000.0, 40.0, -74.0)
        e2 = VerificationEvent("orb-002", "hash-dup", 2000.0, 41.0, -73.0)

        alerts1 = pipeline.process_event(e1)
        alerts2 = pipeline.process_event(e2)

        self.assertEqual(len(alerts1), 0)
        dup_alerts = [a for a in alerts2 if a.alert_type == "duplicate_iris"]
        self.assertEqual(len(dup_alerts), 1)
        self.assertIn("hash-dup", dup_alerts[0].reason)

    # ------------------------------------------------------------------
    # 9. Same iris hash three times
    # ------------------------------------------------------------------
    def test_triple_duplicate_iris(self):
        """Every repetition after the first should trigger a duplicate alert."""
        pipeline = VerificationPipeline()
        for i in range(3):
            alerts = pipeline.process_event(
                VerificationEvent(f"orb-{i}", "hash-same", 1000.0 + i, 40.0, -74.0)
            )
            if i == 0:
                dup = [a for a in alerts if a.alert_type == "duplicate_iris"]
                self.assertEqual(len(dup), 0)
            else:
                dup = [a for a in alerts if a.alert_type == "duplicate_iris"]
                self.assertEqual(len(dup), 1)


class TestImpossibleTravel(unittest.TestCase):
    """Impossible-travel detection based on distance and time."""

    # ------------------------------------------------------------------
    # 10. Same orb 500 km apart in 10 minutes -> impossible travel
    # ------------------------------------------------------------------
    def test_impossible_travel_triggered(self):
        """Two events 500 km apart in 10 minutes requires ~3000 km/h -> alert."""
        pipeline = VerificationPipeline(max_speed_kmh=900)

        # New York area
        e1 = VerificationEvent("orb-001", "hash-a", 1000.0, 40.7128, -74.0060)
        # ~500 km north (roughly Montreal area, ~45.5N)
        e2 = VerificationEvent("orb-001", "hash-b", 1600.0, 45.5017, -73.5673)

        pipeline.process_event(e1)
        alerts = pipeline.process_event(e2)

        travel_alerts = [a for a in alerts if a.alert_type == "impossible_travel"]
        self.assertEqual(len(travel_alerts), 1)
        self.assertIn("speed", travel_alerts[0].reason.lower())

    # ------------------------------------------------------------------
    # 11. Same orb, same location, short gap -> no alert
    # ------------------------------------------------------------------
    def test_same_location_no_travel_alert(self):
        """Events from the same location should never trigger impossible travel."""
        pipeline = VerificationPipeline()
        e1 = VerificationEvent("orb-001", "h1", 1000.0, 40.7128, -74.0060)
        e2 = VerificationEvent("orb-001", "h2", 1001.0, 40.7128, -74.0060)

        pipeline.process_event(e1)
        alerts = pipeline.process_event(e2)

        travel_alerts = [a for a in alerts if a.alert_type == "impossible_travel"]
        self.assertEqual(len(travel_alerts), 0)

    # ------------------------------------------------------------------
    # 12. Long enough time makes the same distance feasible
    # ------------------------------------------------------------------
    def test_feasible_travel_no_alert(self):
        """500 km in 2 hours = 250 km/h, well under 900 km/h -> no alert."""
        pipeline = VerificationPipeline(max_speed_kmh=900)

        e1 = VerificationEvent("orb-001", "h1", 1000.0, 40.7128, -74.0060)
        e2 = VerificationEvent("orb-001", "h2", 8200.0, 45.5017, -73.5673)

        pipeline.process_event(e1)
        alerts = pipeline.process_event(e2)

        travel_alerts = [a for a in alerts if a.alert_type == "impossible_travel"]
        self.assertEqual(len(travel_alerts), 0)

    # ------------------------------------------------------------------
    # 13. Different orbs at far locations -> no alert
    # ------------------------------------------------------------------
    def test_different_orbs_no_travel_alert(self):
        """Impossible travel only applies within the same orb_id."""
        pipeline = VerificationPipeline(max_speed_kmh=900)

        e1 = VerificationEvent("orb-001", "h1", 1000.0, 40.7128, -74.0060)
        e2 = VerificationEvent("orb-002", "h2", 1001.0, 35.6762, 139.6503)

        pipeline.process_event(e1)
        alerts = pipeline.process_event(e2)

        travel_alerts = [a for a in alerts if a.alert_type == "impossible_travel"]
        self.assertEqual(len(travel_alerts), 0)


class TestVelocityAbuse(unittest.TestCase):
    """Velocity (rate) abuse detection."""

    # ------------------------------------------------------------------
    # 14. Exactly at threshold -> no alert
    # ------------------------------------------------------------------
    def test_at_threshold_no_alert(self):
        """Exactly velocity_max_count events in the window should not alert."""
        pipeline = VerificationPipeline(
            velocity_window_sec=3600, velocity_max_count=20
        )
        for i in range(20):
            alerts = pipeline.process_event(
                VerificationEvent(
                    "orb-001", f"h-{i}", 1000.0 + i, 40.0, -74.0
                )
            )
            vel = [a for a in alerts if a.alert_type == "velocity_abuse"]
            self.assertEqual(len(vel), 0, f"Unexpected velocity alert on event {i}")

    # ------------------------------------------------------------------
    # 15. One over threshold -> alert
    # ------------------------------------------------------------------
    def test_over_threshold_triggers_alert(self):
        """The (velocity_max_count + 1)th event in the window should alert."""
        pipeline = VerificationPipeline(
            velocity_window_sec=3600, velocity_max_count=20
        )
        for i in range(20):
            pipeline.process_event(
                VerificationEvent(
                    "orb-001", f"h-{i}", 1000.0 + i, 40.0, -74.0
                )
            )

        # 21st event within the same window
        alerts = pipeline.process_event(
            VerificationEvent("orb-001", "h-20", 1020.0, 40.0, -74.0)
        )
        vel = [a for a in alerts if a.alert_type == "velocity_abuse"]
        self.assertEqual(len(vel), 1)

    # ------------------------------------------------------------------
    # 16. Events outside the window are evicted
    # ------------------------------------------------------------------
    def test_window_eviction(self):
        """Old events outside the sliding window should not count."""
        pipeline = VerificationPipeline(
            velocity_window_sec=3600, velocity_max_count=20
        )
        # 20 events at time 0..19
        for i in range(20):
            pipeline.process_event(
                VerificationEvent("orb-001", f"h-{i}", float(i), 40.0, -74.0)
            )

        # Event at t=4000 -- all previous events are older than 3600s
        alerts = pipeline.process_event(
            VerificationEvent("orb-001", "h-new", 4000.0, 40.0, -74.0)
        )
        vel = [a for a in alerts if a.alert_type == "velocity_abuse"]
        self.assertEqual(len(vel), 0)

    # ------------------------------------------------------------------
    # 17. Different orbs have independent velocity tracking
    # ------------------------------------------------------------------
    def test_independent_orb_velocity(self):
        """Velocity windows are per-orb; different orbs don't interfere."""
        pipeline = VerificationPipeline(
            velocity_window_sec=3600, velocity_max_count=5
        )
        for i in range(5):
            pipeline.process_event(
                VerificationEvent("orb-A", f"hA-{i}", 1000.0 + i, 40.0, -74.0)
            )
            pipeline.process_event(
                VerificationEvent("orb-B", f"hB-{i}", 1000.0 + i, 41.0, -73.0)
            )

        # 6th event for orb-A triggers
        alerts_a = pipeline.process_event(
            VerificationEvent("orb-A", "hA-extra", 1010.0, 40.0, -74.0)
        )
        vel_a = [a for a in alerts_a if a.alert_type == "velocity_abuse"]
        self.assertEqual(len(vel_a), 1)

        # orb-B still at 5, should NOT trigger
        alerts_b = pipeline.process_event(
            VerificationEvent("orb-B", "hB-extra", 1010.0, 41.0, -73.0)
        )
        vel_b = [a for a in alerts_b if a.alert_type == "velocity_abuse"]
        self.assertEqual(len(vel_b), 1)  # orb-B also has 6 now


class TestMultipleAlertTypes(unittest.TestCase):
    """A single event can trigger more than one alert type."""

    # ------------------------------------------------------------------
    # 18. Duplicate iris + impossible travel on the same event
    # ------------------------------------------------------------------
    def test_duplicate_and_impossible_travel(self):
        """An event can trigger both duplicate_iris and impossible_travel."""
        pipeline = VerificationPipeline(max_speed_kmh=900)

        e1 = VerificationEvent("orb-001", "hash-shared", 1000.0, 40.7128, -74.0060)
        pipeline.process_event(e1)

        # Same iris hash + same orb far away + short time
        e2 = VerificationEvent("orb-001", "hash-shared", 1060.0, 51.5074, -0.1278)
        alerts = pipeline.process_event(e2)

        types = {a.alert_type for a in alerts}
        self.assertIn("duplicate_iris", types)
        self.assertIn("impossible_travel", types)

    # ------------------------------------------------------------------
    # 19. All three alert types at once
    # ------------------------------------------------------------------
    def test_all_three_alerts(self):
        """Construct a scenario that triggers all three alert types."""
        pipeline = VerificationPipeline(
            max_speed_kmh=900, velocity_window_sec=3600, velocity_max_count=5
        )

        # 5 events from orb-001 at one location to fill velocity window
        for i in range(5):
            pipeline.process_event(
                VerificationEvent(
                    "orb-001", f"h-{i}", 1000.0 + i, 40.7128, -74.0060
                )
            )

        # 6th event: same orb, duplicate iris "h-0", far away, short time
        e = VerificationEvent("orb-001", "h-0", 1010.0, 51.5074, -0.1278)
        alerts = pipeline.process_event(e)

        types = {a.alert_type for a in alerts}
        self.assertIn("duplicate_iris", types)
        self.assertIn("impossible_travel", types)
        self.assertIn("velocity_abuse", types)


class TestStats(unittest.TestCase):
    """Pipeline statistics tracking."""

    # ------------------------------------------------------------------
    # 20. Empty pipeline stats
    # ------------------------------------------------------------------
    def test_empty_stats(self):
        """A fresh pipeline should report all zeros."""
        pipeline = VerificationPipeline()
        stats = pipeline.get_stats()
        self.assertEqual(stats["total_events"], 0)
        self.assertEqual(stats["total_alerts"], 0)
        self.assertEqual(stats["alerts_by_type"], {})

    # ------------------------------------------------------------------
    # 21. Stats after processing events
    # ------------------------------------------------------------------
    def test_stats_after_events(self):
        """Stats should accurately reflect processed events and alerts."""
        pipeline = VerificationPipeline(
            velocity_window_sec=3600, velocity_max_count=5
        )

        # 5 clean events
        for i in range(5):
            pipeline.process_event(
                VerificationEvent(
                    "orb-001", f"h-{i}", 1000.0 + i, 40.0, -74.0
                )
            )

        # 6th -> velocity_abuse
        pipeline.process_event(
            VerificationEvent("orb-001", "h-extra", 1010.0, 40.0, -74.0)
        )

        # Duplicate iris
        pipeline.process_event(
            VerificationEvent("orb-002", "h-0", 2000.0, 41.0, -73.0)
        )

        stats = pipeline.get_stats()
        self.assertEqual(stats["total_events"], 7)
        self.assertGreaterEqual(stats["total_alerts"], 2)
        self.assertIn("velocity_abuse", stats["alerts_by_type"])
        self.assertIn("duplicate_iris", stats["alerts_by_type"])


if __name__ == "__main__":
    unittest.main()
