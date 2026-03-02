"""
Verification Event Pipeline - Solution

Processes biometric verification events from Orb devices and raises alerts
when duplicate iris hashes, impossible travel, or velocity abuse are detected.
"""

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VerificationEvent:
    """A single biometric verification event from an Orb device."""

    orb_id: str
    iris_hash: str
    timestamp: float
    latitude: float
    longitude: float


@dataclass
class Alert:
    """An alert raised by the verification pipeline."""

    alert_type: str  # "duplicate_iris", "impossible_travel", "velocity_abuse"
    event: VerificationEvent
    reason: str
    evidence: dict


class VerificationPipeline:
    """Processes verification events and raises fraud-detection alerts."""

    def __init__(
        self,
        max_speed_kmh: float = 900,
        velocity_window_sec: float = 3600,
        velocity_max_count: int = 20,
    ) -> None:
        self.max_speed_kmh = max_speed_kmh
        self.velocity_window_sec = velocity_window_sec
        self.velocity_max_count = velocity_max_count

        # State tracking
        self._seen_iris: set[str] = set()
        self._orb_last_location: dict[str, tuple[float, float, float]] = {}
        self._orb_event_times: dict[str, deque] = {}

        # Stats
        self._total_events = 0
        self._total_alerts = 0
        self._alerts_by_type: dict[str, int] = {}

    # ------------------------------------------------------------------
    # Haversine helper
    # ------------------------------------------------------------------
    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Return great-circle distance in km between two lat/lon points."""
        R = 6371.0  # Earth radius in km

        lat1_r = math.radians(lat1)
        lat2_r = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    # ------------------------------------------------------------------
    # Core processing
    # ------------------------------------------------------------------
    def process_event(self, event: VerificationEvent) -> list:
        """Process a single event and return any triggered alerts."""
        alerts: list[Alert] = []

        # --- Check 1: duplicate iris ---
        if event.iris_hash in self._seen_iris:
            alerts.append(
                Alert(
                    alert_type="duplicate_iris",
                    event=event,
                    reason=f"Iris hash {event.iris_hash} has already been registered",
                    evidence={"iris_hash": event.iris_hash},
                )
            )
        self._seen_iris.add(event.iris_hash)

        # --- Check 2: impossible travel ---
        if event.orb_id in self._orb_last_location:
            prev_lat, prev_lon, prev_ts = self._orb_last_location[event.orb_id]
            elapsed_sec = event.timestamp - prev_ts

            if elapsed_sec > 0:
                dist_km = self._haversine(
                    prev_lat, prev_lon, event.latitude, event.longitude
                )
                elapsed_hr = elapsed_sec / 3600.0
                required_speed = dist_km / elapsed_hr

                if required_speed > self.max_speed_kmh:
                    alerts.append(
                        Alert(
                            alert_type="impossible_travel",
                            event=event,
                            reason=(
                                f"Orb {event.orb_id} would need {required_speed:.0f} km/h "
                                f"(speed limit {self.max_speed_kmh} km/h) to cover "
                                f"{dist_km:.1f} km in {elapsed_sec:.0f}s"
                            ),
                            evidence={
                                "distance_km": round(dist_km, 2),
                                "elapsed_sec": elapsed_sec,
                                "required_speed_kmh": round(required_speed, 2),
                                "max_speed_kmh": self.max_speed_kmh,
                            },
                        )
                    )

        # Update last known location for this orb
        self._orb_last_location[event.orb_id] = (
            event.latitude,
            event.longitude,
            event.timestamp,
        )

        # --- Check 3: velocity abuse ---
        if event.orb_id not in self._orb_event_times:
            self._orb_event_times[event.orb_id] = deque()

        dq = self._orb_event_times[event.orb_id]

        # Evict events outside the sliding window
        window_start = event.timestamp - self.velocity_window_sec
        while dq and dq[0] < window_start:
            dq.popleft()

        # Add current event timestamp
        dq.append(event.timestamp)

        if len(dq) > self.velocity_max_count:
            alerts.append(
                Alert(
                    alert_type="velocity_abuse",
                    event=event,
                    reason=(
                        f"Orb {event.orb_id} has {len(dq)} events in the last "
                        f"{self.velocity_window_sec}s (limit {self.velocity_max_count})"
                    ),
                    evidence={
                        "orb_id": event.orb_id,
                        "event_count": len(dq),
                        "window_sec": self.velocity_window_sec,
                        "max_count": self.velocity_max_count,
                    },
                )
            )

        # --- Update stats ---
        self._total_events += 1
        self._total_alerts += len(alerts)
        for alert in alerts:
            self._alerts_by_type[alert.alert_type] = (
                self._alerts_by_type.get(alert.alert_type, 0) + 1
            )

        return alerts

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    def get_stats(self) -> dict:
        """Return summary statistics."""
        return {
            "total_events": self._total_events,
            "total_alerts": self._total_alerts,
            "alerts_by_type": dict(self._alerts_by_type),
        }
