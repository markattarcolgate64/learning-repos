"""
Device Telemetry Aggregator
============================
Category   : Infrastructure / Monitoring
Difficulty : *** (3/5)

Problem
-------
Build a time-series aggregation service for Orb device health metrics.
Each Orb sends periodic heartbeats with metrics. Your service must ingest
heartbeats, compute aggregated statistics over time ranges, detect unhealthy
devices, and provide fleet-wide overviews — all with bounded memory usage.

Real-world motivation
---------------------
Tools for Humanity deploys thousands of Orb devices worldwide for iris
scanning. Each device streams telemetry data back to a central service.
Engineers need real-time visibility into device health, anomaly detection,
and fleet-wide trends to ensure reliable operation.

Hints
-----
1. Use collections.deque with maxlen for ring buffers — this gives you
   bounded memory per device automatically.
2. For percentile calculation, sort the values and index at the right position.
3. Consider what "unhealthy" means — it could be a single metric out of range,
   or a combination of metrics indicating a pattern.

Run command
-----------
    python -m unittest 16_device_telemetry.test_exercise -v
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Heartbeat:
    """A single telemetry heartbeat from an Orb device."""
    orb_id: str
    timestamp: float
    cpu_temp: float             # Celsius
    memory_used_pct: float      # 0-100
    battery_pct: float          # 0-100
    capture_success_rate: float  # 0.0-1.0
    error_count: int


@dataclass
class DeviceSummary:
    """Aggregated summary of a single device's telemetry."""
    orb_id: str
    heartbeat_count: int
    time_range: tuple  # (earliest, latest) timestamps
    metrics: dict      # metric_name -> {"min": float, "max": float, "avg": float, "p99": float}


@dataclass
class FleetOverview:
    """Fleet-wide telemetry overview."""
    total_devices: int
    active_devices: int         # devices with heartbeat in last N seconds
    avg_cpu_temp: float
    avg_battery_pct: float
    avg_capture_success_rate: float
    total_errors: int


class TelemetryAggregator:
    """Aggregates Orb device telemetry with bounded memory usage.

    Uses ring buffers (fixed-size deques) to store a limited history of
    heartbeats per device, enabling summary statistics, health checks,
    and fleet-wide overviews.
    """

    def __init__(self, max_heartbeats_per_device: int = 1000) -> None:
        """Initialise the aggregator.

        Args:
            max_heartbeats_per_device: Maximum number of heartbeats to retain
                per device. Oldest heartbeats are discarded when this limit
                is exceeded.
        """
        # TODO: Store the max size and create a dict to hold per-device
        #       deques of Heartbeat objects.
        raise NotImplementedError

    def ingest(self, heartbeat: Heartbeat) -> None:
        """Ingest a single heartbeat from an Orb device.

        If this is the first heartbeat for this orb_id, create a new ring
        buffer for it. Append the heartbeat to the device's buffer.

        Args:
            heartbeat: The heartbeat to ingest.
        """
        # TODO: Create deque with maxlen if new device, then append heartbeat.
        raise NotImplementedError

    def get_device_summary(
        self,
        orb_id: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> Optional[DeviceSummary]:
        """Compute aggregated statistics for a single device.

        If start_time and/or end_time are provided, only include heartbeats
        within that range (inclusive on both ends). If the device is unknown,
        return None.

        The metrics dict should contain keys: "cpu_temp", "memory_used_pct",
        "battery_pct", "capture_success_rate", "error_count". Each maps to a
        dict with keys "min", "max", "avg", and "p99".

        For p99: sort the values and take the element at index int(0.99 * (n - 1))
        where n is the number of values.

        Args:
            orb_id: The device identifier.
            start_time: Optional lower bound on timestamp (inclusive).
            end_time: Optional upper bound on timestamp (inclusive).

        Returns:
            A DeviceSummary, or None if the device has not been seen.
        """
        # TODO: Filter heartbeats by time range, compute min/max/avg/p99 for
        #       each metric, and return a DeviceSummary.
        raise NotImplementedError

    def detect_unhealthy(self, thresholds: dict) -> list:
        """Detect unhealthy devices based on their latest heartbeat.

        A device is unhealthy if ANY threshold is violated by its most recent
        heartbeat. Supported threshold keys:
            - "cpu_temp_max": flag if latest cpu_temp > value
            - "battery_pct_min": flag if latest battery_pct < value
            - "capture_success_rate_min": flag if latest capture_success_rate < value
            - "error_count_max": flag if latest error_count > value

        Args:
            thresholds: Dict mapping threshold names to their values.

        Returns:
            List of orb_id strings for unhealthy devices (sorted alphabetically).
        """
        # TODO: For each device, check its latest heartbeat against thresholds.
        raise NotImplementedError

    def fleet_overview(self, active_window_sec: float = 300.0) -> FleetOverview:
        """Produce a fleet-wide overview of all tracked devices.

        A device is "active" if its most recent heartbeat timestamp is within
        active_window_sec seconds of the most recent heartbeat across the
        entire fleet.

        Averages are computed across the latest heartbeat of each device.

        Returns:
            A FleetOverview summarising the entire fleet.
        """
        # TODO: Iterate all devices, find the global latest timestamp,
        #       determine active devices, and compute fleet-wide averages.
        raise NotImplementedError
