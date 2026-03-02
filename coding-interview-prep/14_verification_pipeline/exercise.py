"""
Verification Event Pipeline
============================
Category   : Backend / Fraud Detection
Difficulty : *** (3/5)

Problem
-------
Implement a verification event pipeline that processes biometric verification
events from Orb devices and raises alerts when suspicious patterns are detected.

Each event contains an orb_id, an iris_hash (representing the biometric
commitment), a timestamp, and GPS coordinates.  Your pipeline must detect three
classes of fraud:

1. **Duplicate iris** -- the same iris_hash has been seen in a previous event.
2. **Impossible travel** -- the same orb_id appears at two locations that are
   farther apart than physically possible given the elapsed time and a maximum
   travel speed (default 900 km/h, roughly commercial-jet speed).
3. **Velocity abuse** -- the same orb_id submits more than a threshold number
   of events within a sliding time window (default 20 events in 3600 seconds).

Real-world motivation
---------------------
Tools for Humanity operates a global fleet of Orb devices that perform iris
verifications.  Detecting duplicate biometrics prevents double-registrations,
impossible-travel checks catch cloned or spoofed device identifiers, and
velocity limits flag Orbs that are being used at an unrealistic rate -- all
critical signals for the integrity of the World ID protocol.

Hints
-----
1. The Haversine formula gives great-circle distance between two lat/lon points.
   Use R = 6371 km for the Earth's radius.
2. For impossible travel, compute the required speed to cover the distance in the
   elapsed time and compare against the max_speed_kmh threshold.
3. For velocity abuse, keep a collections.deque of timestamps per orb_id and
   evict entries older than the window before counting.
4. A single event can trigger multiple alert types simultaneously.

Run command
-----------
    python -m unittest 14_verification_pipeline.test_exercise -v
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VerificationEvent:
    """A single biometric verification event from an Orb device."""

    orb_id: str
    iris_hash: str
    timestamp: float  # unix timestamp
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
    """Processes verification events and raises fraud-detection alerts.

    The pipeline tracks seen iris hashes, per-orb locations, and per-orb event
    rates to detect duplicate biometrics, impossible travel, and velocity abuse.
    """

    def __init__(
        self,
        max_speed_kmh: float = 900,
        velocity_window_sec: float = 3600,
        velocity_max_count: int = 20,
    ) -> None:
        """Initialise the pipeline with configurable thresholds.

        Args:
            max_speed_kmh: Maximum plausible travel speed in km/h.  Events
                from the same orb that would require exceeding this speed
                trigger an impossible_travel alert.
            velocity_window_sec: Sliding window duration in seconds for
                velocity abuse detection.
            velocity_max_count: Maximum number of events allowed from a
                single orb within the velocity window before an alert fires.
        """
        raise NotImplementedError("Implement __init__")

    # ------------------------------------------------------------------
    # Haversine helper
    # ------------------------------------------------------------------
    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Return the great-circle distance in km between two points.

        Uses the Haversine formula with R = 6371 km.

        Args:
            lat1: Latitude of point 1 in degrees.
            lon1: Longitude of point 1 in degrees.
            lat2: Latitude of point 2 in degrees.
            lon2: Longitude of point 2 in degrees.

        Returns:
            Distance in kilometres.
        """
        raise NotImplementedError("Implement _haversine")

    # ------------------------------------------------------------------
    # Core processing
    # ------------------------------------------------------------------
    def process_event(self, event: VerificationEvent) -> list:
        """Process a single verification event and return any triggered alerts.

        A single event may trigger zero, one, or several alerts.  The checks
        performed are (in order):

        1. **duplicate_iris** -- ``event.iris_hash`` was already seen.
        2. **impossible_travel** -- the same ``orb_id`` was last seen at a
           location that would require faster-than-threshold travel.
        3. **velocity_abuse** -- the same ``orb_id`` has exceeded the maximum
           number of events within the sliding time window.

        After checks, internal state is updated so future events are compared
        against this one.

        Args:
            event: The verification event to process.

        Returns:
            A list of :class:`Alert` objects (may be empty).
        """
        raise NotImplementedError("Implement process_event")

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    def get_stats(self) -> dict:
        """Return summary statistics for the pipeline.

        Returns:
            A dict with keys:
            - ``"total_events"`` (int): number of events processed.
            - ``"total_alerts"`` (int): number of alerts raised.
            - ``"alerts_by_type"`` (dict): mapping from alert_type str to count.
        """
        raise NotImplementedError("Implement get_stats")
