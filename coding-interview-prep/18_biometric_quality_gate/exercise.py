"""
Biometric Quality Gate
=======================
Category   : ML / Signal Processing
Difficulty : *** (3/5)

Problem
-------
Build an image quality assessment pipeline for iris capture. The Orb device
captures iris images and must decide in real-time whether an image is good
enough for iris code extraction, or if recapture is needed.

Rather than processing actual images, you'll work with extracted quality
metadata (sharpness, exposure, occlusion, etc.) and build a scoring and
decision system that combines multiple quality dimensions into an overall
accept/reject decision.

Real-world motivation
---------------------
Tools for Humanity's Orb captures iris images under varying conditions —
different lighting, distances, eye openness, gaze angles. A poor-quality
image produces an unreliable iris code, which could cause false matches
or false rejections. The quality gate ensures only good images proceed
to iris code extraction.

Hints
-----
1. Start with a simple weighted average for scoring — each dimension gets
   a weight and the score is the weighted sum normalized to 0-100.
2. For calibration, you can use a simple approach: compute the mean quality
   scores for accepted vs rejected examples and adjust weights accordingly.
3. Consider that some quality dimensions are "hard gates" — e.g., if
   occlusion is above 50%, reject regardless of other scores.

Run command
-----------
    python -m unittest 18_biometric_quality_gate.test_exercise -v
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
        """Initialise the quality gate with optional custom weights and hard gates.

        Args:
            weights: A dict mapping dimension names to their weights.
                Weights should sum to 1.0.  If *None*, DEFAULT_WEIGHTS is used.
            hard_gates: A dict of hard gate thresholds.  Keys are:
                - ``"occlusion_pct_max"`` -- reject if occlusion_pct exceeds this.
                - ``"iris_visible_pct_min"`` -- reject if iris_visible_pct is below this.
                - ``"gaze_deviation_max"`` -- reject if gaze_deviation exceeds this.
                If *None*, DEFAULT_HARD_GATES is used.
        """
        raise NotImplementedError("Implement __init__")

    # ------------------------------------------------------------------
    # Normalisation
    # ------------------------------------------------------------------
    def _normalize_dimension(self, name: str, value: float) -> float:
        """Convert a raw quality dimension value to a 0-100 score where 100 is best.

        Mapping rules:
        - **sharpness**: already 0-100, higher is better -> return as-is.
        - **exposure**: 50 is ideal -> ``score = max(0, 100 - 2 * abs(value - 50))``.
        - **occlusion_pct**: lower is better -> ``score = 100 - value``.
        - **gaze_deviation**: lower is better -> ``score = max(0, 100 - (value / 90) * 100)``.
        - **motion_blur**: lower is better -> ``score = 100 - value``.
        - **iris_visible_pct**: higher is better -> return as-is.

        Args:
            name: The dimension name (e.g. ``"sharpness"``).
            value: The raw measurement value.

        Returns:
            A normalised score in the range [0, 100].
        """
        raise NotImplementedError("Implement _normalize_dimension")

    # ------------------------------------------------------------------
    # Scoring & decision
    # ------------------------------------------------------------------
    def score(self, metadata: ImageMetadata) -> QualityResult:
        """Compute the overall quality score for a single image.

        Steps:
        1. Normalise each quality dimension via :meth:`_normalize_dimension`.
        2. Check hard gates -- if any fail, the image is rejected immediately
           and the corresponding reason(s) are added to *rejection_reasons*.
        3. Compute the weighted average of all normalised scores.
        4. Accept if the overall score >= 50; otherwise reject.

        Args:
            metadata: Extracted quality metadata for one image.

        Returns:
            A :class:`QualityResult` with dimension scores, overall score,
            acceptance decision, and any rejection reasons.
        """
        raise NotImplementedError("Implement score")

    def decide(self, metadata: ImageMetadata, min_quality: float = 50) -> QualityResult:
        """Score an image and apply a custom quality threshold.

        Behaves identically to :meth:`score` except the acceptance threshold
        can be overridden via *min_quality*.

        Args:
            metadata: Extracted quality metadata for one image.
            min_quality: Minimum overall score to accept (default 50).

        Returns:
            A :class:`QualityResult`.
        """
        raise NotImplementedError("Implement decide")

    # ------------------------------------------------------------------
    # Batch processing
    # ------------------------------------------------------------------
    def batch_process(
        self,
        metadata_list: list,
        min_quality: float = 50,
    ) -> BatchResult:
        """Process a batch of images and return aggregate statistics.

        Uses :meth:`decide` for each image.  The quality distribution buckets
        are:
        - ``"excellent"``: overall_score > 80
        - ``"good"``:      60 < overall_score <= 80
        - ``"fair"``:      40 < overall_score <= 60
        - ``"poor"``:      overall_score <= 40

        Args:
            metadata_list: A list of :class:`ImageMetadata` objects.
            min_quality: Minimum overall score to accept.

        Returns:
            A :class:`BatchResult` with per-image results and aggregates.
        """
        raise NotImplementedError("Implement batch_process")

    # ------------------------------------------------------------------
    # Calibration
    # ------------------------------------------------------------------
    def calibrate(self, examples: list) -> None:
        """Adjust weights using labelled examples.

        For each quality dimension, compute the mean normalised score for
        *good* examples (label ``True``) and *bad* examples (label ``False``).
        The gap ``mean_good - mean_bad`` indicates how predictive that
        dimension is.  Dimensions with a larger gap receive a higher weight.

        Steps:
        1. For each dimension, collect normalised scores for good and bad sets.
        2. Compute ``gap = mean_good - mean_bad`` for each dimension.
        3. Clamp negative gaps to 0 (dimension is not predictive).
        4. Normalise gaps so they sum to 1.0 to produce new weights.
        5. If all gaps are zero, keep the current weights unchanged.

        Args:
            examples: A list of ``(ImageMetadata, bool)`` tuples where the
                bool indicates whether the image is *good* (True) or *bad*
                (False).
        """
        raise NotImplementedError("Implement calibrate")
