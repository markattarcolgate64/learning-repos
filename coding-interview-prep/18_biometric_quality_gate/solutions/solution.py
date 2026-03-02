"""
Biometric Quality Gate - Reference Solution

An image quality assessment pipeline for iris capture that combines multiple
quality dimensions into an overall accept/reject decision using weighted
scoring and hard gates.
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ImageMetadata:
    """Quality metadata extracted from an iris capture image."""

    sharpness: float        # 0-100, higher is sharper
    exposure: float         # 0-100, 50 is ideal, deviation is bad
    occlusion_pct: float    # 0-100, percentage of iris occluded (lower is better)
    gaze_deviation: float   # 0-90 degrees, lower is better (0 = looking straight)
    motion_blur: float      # 0-100, lower is better
    iris_visible_pct: float # 0-100, percentage of iris visible (higher is better)


@dataclass
class QualityResult:
    """Result of a single image quality assessment."""

    overall_score: float            # 0-100
    dimension_scores: dict          # dimension_name -> individual score (0-100)
    accepted: bool
    rejection_reasons: list = field(default_factory=list)  # empty if accepted


@dataclass
class BatchResult:
    """Result of processing a batch of images."""

    results: list               # list[QualityResult]
    acceptance_rate: float      # 0.0-1.0
    avg_quality: float          # average overall_score
    quality_distribution: dict  # "excellent"/"good"/"fair"/"poor" -> count


# ---------------------------------------------------------------------------
# Quality gate
# ---------------------------------------------------------------------------

class QualityGate:
    """Image quality assessment pipeline for iris capture.

    Combines multiple quality dimensions into an overall accept/reject
    decision using weighted scoring and hard gates.
    """

    DEFAULT_WEIGHTS = {
        "sharpness": 0.25,
        "exposure": 0.20,
        "occlusion_pct": 0.15,
        "gaze_deviation": 0.15,
        "motion_blur": 0.15,
        "iris_visible_pct": 0.10,
    }

    DEFAULT_HARD_GATES = {
        "occlusion_pct_max": 50,
        "iris_visible_pct_min": 30,
        "gaze_deviation_max": 45,
    }

    def __init__(
        self,
        weights: Optional[dict] = None,
        hard_gates: Optional[dict] = None,
    ) -> None:
        self.weights = dict(weights) if weights is not None else dict(self.DEFAULT_WEIGHTS)
        self.hard_gates = dict(hard_gates) if hard_gates is not None else dict(self.DEFAULT_HARD_GATES)

    # ------------------------------------------------------------------
    # Normalisation
    # ------------------------------------------------------------------
    def _normalize_dimension(self, name: str, value: float) -> float:
        if name == "sharpness":
            return float(value)
        elif name == "exposure":
            return max(0.0, 100.0 - 2.0 * abs(value - 50.0))
        elif name == "occlusion_pct":
            return 100.0 - value
        elif name == "gaze_deviation":
            return max(0.0, 100.0 - (value / 90.0) * 100.0)
        elif name == "motion_blur":
            return 100.0 - value
        elif name == "iris_visible_pct":
            return float(value)
        else:
            return float(value)

    # ------------------------------------------------------------------
    # Hard gate checks
    # ------------------------------------------------------------------
    def _check_hard_gates(self, metadata: ImageMetadata) -> list:
        """Return a list of rejection reason strings for failed hard gates."""
        reasons = []
        occlusion_max = self.hard_gates.get("occlusion_pct_max", 50)
        if metadata.occlusion_pct > occlusion_max:
            reasons.append(
                f"Occlusion too high: {metadata.occlusion_pct:.1f}% exceeds max {occlusion_max}%"
            )

        iris_min = self.hard_gates.get("iris_visible_pct_min", 30)
        if metadata.iris_visible_pct < iris_min:
            reasons.append(
                f"Iris visibility too low: {metadata.iris_visible_pct:.1f}% below min {iris_min}%"
            )

        gaze_max = self.hard_gates.get("gaze_deviation_max", 45)
        if metadata.gaze_deviation > gaze_max:
            reasons.append(
                f"Gaze deviation too high: {metadata.gaze_deviation:.1f} degrees exceeds max {gaze_max} degrees"
            )

        return reasons

    # ------------------------------------------------------------------
    # Scoring & decision
    # ------------------------------------------------------------------
    def score(self, metadata: ImageMetadata) -> QualityResult:
        return self.decide(metadata, min_quality=50.0)

    def decide(self, metadata: ImageMetadata, min_quality: float = 50.0) -> QualityResult:
        # 1. Normalise each dimension
        dimension_scores = {}
        dimension_names = [
            "sharpness", "exposure", "occlusion_pct",
            "gaze_deviation", "motion_blur", "iris_visible_pct",
        ]
        raw_values = {
            "sharpness": metadata.sharpness,
            "exposure": metadata.exposure,
            "occlusion_pct": metadata.occlusion_pct,
            "gaze_deviation": metadata.gaze_deviation,
            "motion_blur": metadata.motion_blur,
            "iris_visible_pct": metadata.iris_visible_pct,
        }
        for name in dimension_names:
            dimension_scores[name] = self._normalize_dimension(name, raw_values[name])

        # 2. Check hard gates
        rejection_reasons = self._check_hard_gates(metadata)

        # 3. Compute weighted average
        overall_score = 0.0
        for name in dimension_names:
            weight = self.weights.get(name, 0.0)
            overall_score += weight * dimension_scores[name]

        # 4. Determine acceptance
        if rejection_reasons:
            accepted = False
        else:
            accepted = overall_score >= min_quality
            if not accepted:
                rejection_reasons.append(
                    f"Overall quality score {overall_score:.1f} below threshold {min_quality:.1f}"
                )

        return QualityResult(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            accepted=accepted,
            rejection_reasons=rejection_reasons,
        )

    # ------------------------------------------------------------------
    # Batch processing
    # ------------------------------------------------------------------
    def batch_process(
        self,
        metadata_list: list,
        min_quality: float = 50.0,
    ) -> BatchResult:
        if not metadata_list:
            return BatchResult(
                results=[],
                acceptance_rate=0.0,
                avg_quality=0.0,
                quality_distribution={"excellent": 0, "good": 0, "fair": 0, "poor": 0},
            )

        results = [self.decide(m, min_quality) for m in metadata_list]
        accepted_count = sum(1 for r in results if r.accepted)
        acceptance_rate = accepted_count / len(results)
        avg_quality = sum(r.overall_score for r in results) / len(results)

        distribution = {"excellent": 0, "good": 0, "fair": 0, "poor": 0}
        for r in results:
            if r.overall_score > 80:
                distribution["excellent"] += 1
            elif r.overall_score > 60:
                distribution["good"] += 1
            elif r.overall_score > 40:
                distribution["fair"] += 1
            else:
                distribution["poor"] += 1

        return BatchResult(
            results=results,
            acceptance_rate=acceptance_rate,
            avg_quality=avg_quality,
            quality_distribution=distribution,
        )

    # ------------------------------------------------------------------
    # Calibration
    # ------------------------------------------------------------------
    def calibrate(self, examples: list) -> None:
        dimension_names = [
            "sharpness", "exposure", "occlusion_pct",
            "gaze_deviation", "motion_blur", "iris_visible_pct",
        ]

        good_scores = {name: [] for name in dimension_names}
        bad_scores = {name: [] for name in dimension_names}

        for metadata, is_good in examples:
            raw_values = {
                "sharpness": metadata.sharpness,
                "exposure": metadata.exposure,
                "occlusion_pct": metadata.occlusion_pct,
                "gaze_deviation": metadata.gaze_deviation,
                "motion_blur": metadata.motion_blur,
                "iris_visible_pct": metadata.iris_visible_pct,
            }
            target = good_scores if is_good else bad_scores
            for name in dimension_names:
                normalized = self._normalize_dimension(name, raw_values[name])
                target[name].append(normalized)

        # Compute gaps
        gaps = {}
        for name in dimension_names:
            mean_good = sum(good_scores[name]) / len(good_scores[name]) if good_scores[name] else 0.0
            mean_bad = sum(bad_scores[name]) / len(bad_scores[name]) if bad_scores[name] else 0.0
            gaps[name] = max(0.0, mean_good - mean_bad)

        total_gap = sum(gaps.values())
        if total_gap == 0:
            # No predictive signal -- keep current weights
            return

        # Normalise to sum to 1.0
        for name in dimension_names:
            self.weights[name] = gaps[name] / total_gap
