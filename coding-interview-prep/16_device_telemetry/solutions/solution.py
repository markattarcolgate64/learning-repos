"""
Device Telemetry Aggregator - Solution

A time-series aggregation service for Orb device health metrics using
ring buffers (deques with maxlen) for bounded memory usage.
"""

from collections import deque
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
    active_devices: int
    avg_cpu_temp: float
    avg_battery_pct: float
    avg_capture_success_rate: float
    total_errors: int


# Names of numeric metrics we track on each heartbeat
_METRIC_FIELDS = [
    "cpu_temp",
    "memory_used_pct",
    "battery_pct",
    "capture_success_rate",
    "error_count",
]


def _percentile(sorted_values: list, pct: float) -> float:
    """Compute a percentile from an already-sorted list of values.

    Uses the index formula: int(pct * (n - 1)).
    """
    n = len(sorted_values)
    if n == 0:
        return 0.0
    idx = int(pct * (n - 1))
    return float(sorted_values[idx])


def _compute_metric_stats(values: list) -> dict:
    """Return min, max, avg, p99 for a list of numeric values."""
    if not values:
        return {"min": 0.0, "max": 0.0, "avg": 0.0, "p99": 0.0}
    sorted_vals = sorted(values)
    return {
        "min": float(sorted_vals[0]),
        "max": float(sorted_vals[-1]),
        "avg": sum(values) / len(values),
        "p99": _percentile(sorted_vals, 0.99),
    }


class TelemetryAggregator:
    """Aggregates Orb device telemetry with bounded memory usage."""

    def __init__(self, max_heartbeats_per_device: int = 1000) -> None:
        self._max = max_heartbeats_per_device
        self._devices: dict[str, deque] = {}

    def ingest(self, heartbeat: Heartbeat) -> None:
        if heartbeat.orb_id not in self._devices:
            self._devices[heartbeat.orb_id] = deque(maxlen=self._max)
        self._devices[heartbeat.orb_id].append(heartbeat)

    def get_device_summary(
        self,
        orb_id: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> Optional[DeviceSummary]:
        if orb_id not in self._devices:
            return None

        heartbeats = list(self._devices[orb_id])

        # Apply time-range filter
        if start_time is not None:
            heartbeats = [h for h in heartbeats if h.timestamp >= start_time]
        if end_time is not None:
            heartbeats = [h for h in heartbeats if h.timestamp <= end_time]

        if not heartbeats:
            return None

        metrics: dict = {}
        for field in _METRIC_FIELDS:
            values = [getattr(h, field) for h in heartbeats]
            metrics[field] = _compute_metric_stats(values)

        timestamps = [h.timestamp for h in heartbeats]
        return DeviceSummary(
            orb_id=orb_id,
            heartbeat_count=len(heartbeats),
            time_range=(min(timestamps), max(timestamps)),
            metrics=metrics,
        )

    def detect_unhealthy(self, thresholds: dict) -> list:
        unhealthy: list[str] = []
        for orb_id, buf in self._devices.items():
            latest = buf[-1]
            flagged = False

            if "cpu_temp_max" in thresholds:
                if latest.cpu_temp > thresholds["cpu_temp_max"]:
                    flagged = True
            if "battery_pct_min" in thresholds:
                if latest.battery_pct < thresholds["battery_pct_min"]:
                    flagged = True
            if "capture_success_rate_min" in thresholds:
                if latest.capture_success_rate < thresholds["capture_success_rate_min"]:
                    flagged = True
            if "error_count_max" in thresholds:
                if latest.error_count > thresholds["error_count_max"]:
                    flagged = True

            if flagged:
                unhealthy.append(orb_id)

        return sorted(unhealthy)

    def fleet_overview(self, active_window_sec: float = 300.0) -> FleetOverview:
        if not self._devices:
            return FleetOverview(
                total_devices=0,
                active_devices=0,
                avg_cpu_temp=0.0,
                avg_battery_pct=0.0,
                avg_capture_success_rate=0.0,
                total_errors=0,
            )

        # Collect latest heartbeat per device
        latest_per_device = {
            orb_id: buf[-1] for orb_id, buf in self._devices.items()
        }

        total_devices = len(latest_per_device)
        global_latest_ts = max(h.timestamp for h in latest_per_device.values())

        active_devices = sum(
            1
            for h in latest_per_device.values()
            if global_latest_ts - h.timestamp <= active_window_sec
        )

        total_errors = sum(h.error_count for h in latest_per_device.values())
        avg_cpu = sum(h.cpu_temp for h in latest_per_device.values()) / total_devices
        avg_bat = sum(h.battery_pct for h in latest_per_device.values()) / total_devices
        avg_cap = sum(
            h.capture_success_rate for h in latest_per_device.values()
        ) / total_devices

        return FleetOverview(
            total_devices=total_devices,
            active_devices=active_devices,
            avg_cpu_temp=avg_cpu,
            avg_battery_pct=avg_bat,
            avg_capture_success_rate=avg_cap,
            total_errors=total_errors,
        )
