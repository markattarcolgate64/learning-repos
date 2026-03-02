"""Tests for the Biometric Quality Gate exercise."""

import unittest

from exercise import ImageMetadata, QualityResult, BatchResult, QualityGate


class TestNormalizeDimension(unittest.TestCase):
    """Tests for the _normalize_dimension helper."""

    def setUp(self):
        self.gate = QualityGate()

    # ------------------------------------------------------------------
    # Sharpness: already 0-100, higher is better
    # ------------------------------------------------------------------
    def test_sharpness_passthrough(self):
        """Sharpness values should pass through unchanged."""
        self.assertAlmostEqual(self.gate._normalize_dimension("sharpness", 0), 0)
        self.assertAlmostEqual(self.gate._normalize_dimension("sharpness", 50), 50)
        self.assertAlmostEqual(self.gate._normalize_dimension("sharpness", 100), 100)

    # ------------------------------------------------------------------
    # Exposure: 50 is ideal, score = max(0, 100 - 2*abs(value - 50))
    # ------------------------------------------------------------------
    def test_exposure_ideal(self):
        """Exposure of 50 should yield a perfect score of 100."""
        self.assertAlmostEqual(self.gate._normalize_dimension("exposure", 50), 100)

    def test_exposure_zero(self):
        """Exposure of 0 should yield a score of 0."""
        self.assertAlmostEqual(self.gate._normalize_dimension("exposure", 0), 0)

    def test_exposure_max(self):
        """Exposure of 100 should yield a score of 0."""
        self.assertAlmostEqual(self.gate._normalize_dimension("exposure", 100), 0)

    def test_exposure_quarter(self):
        """Exposure of 25 should yield a score of 50."""
        self.assertAlmostEqual(self.gate._normalize_dimension("exposure", 25), 50)

    def test_exposure_75(self):
        """Exposure of 75 should yield a score of 50."""
        self.assertAlmostEqual(self.gate._normalize_dimension("exposure", 75), 50)

    # ------------------------------------------------------------------
    # Occlusion: lower is better -> score = 100 - value
    # ------------------------------------------------------------------
    def test_occlusion_zero(self):
        """Zero occlusion should yield a perfect score."""
        self.assertAlmostEqual(self.gate._normalize_dimension("occlusion_pct", 0), 100)

    def test_occlusion_full(self):
        """Full occlusion should yield zero."""
        self.assertAlmostEqual(self.gate._normalize_dimension("occlusion_pct", 100), 0)

    # ------------------------------------------------------------------
    # Gaze deviation: lower is better -> max(0, 100 - (value/90)*100)
    # ------------------------------------------------------------------
    def test_gaze_straight(self):
        """Gaze deviation of 0 degrees should be a perfect score."""
        self.assertAlmostEqual(self.gate._normalize_dimension("gaze_deviation", 0), 100)

    def test_gaze_max(self):
        """Gaze deviation of 90 degrees should yield zero."""
        self.assertAlmostEqual(self.gate._normalize_dimension("gaze_deviation", 90), 0)

    def test_gaze_45(self):
        """Gaze deviation of 45 degrees should yield 50."""
        self.assertAlmostEqual(self.gate._normalize_dimension("gaze_deviation", 45), 50)

    # ------------------------------------------------------------------
    # Motion blur: lower is better -> score = 100 - value
    # ------------------------------------------------------------------
    def test_blur_none(self):
        """No motion blur should be a perfect score."""
        self.assertAlmostEqual(self.gate._normalize_dimension("motion_blur", 0), 100)

    def test_blur_max(self):
        """Maximum blur should yield zero."""
        self.assertAlmostEqual(self.gate._normalize_dimension("motion_blur", 100), 0)

    # ------------------------------------------------------------------
    # Iris visible: already 0-100, higher is better
    # ------------------------------------------------------------------
    def test_iris_visible_passthrough(self):
        """Iris visible percentage should pass through unchanged."""
        self.assertAlmostEqual(self.gate._normalize_dimension("iris_visible_pct", 95), 95)
        self.assertAlmostEqual(self.gate._normalize_dimension("iris_visible_pct", 0), 0)


class TestScorePerfectImage(unittest.TestCase):
    """Test scoring of an ideal iris capture."""

    def test_perfect_image_high_score(self):
        """A near-perfect image should receive a high overall score."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=95,
            exposure=50,
            occlusion_pct=5,
            gaze_deviation=2,
            motion_blur=5,
            iris_visible_pct=95,
        )
        result = gate.score(metadata)
        self.assertGreater(result.overall_score, 90)
        self.assertTrue(result.accepted)
        self.assertEqual(len(result.rejection_reasons), 0)

    def test_perfect_image_dimension_scores(self):
        """Each dimension score should be high for a perfect image."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=95,
            exposure=50,
            occlusion_pct=5,
            gaze_deviation=2,
            motion_blur=5,
            iris_visible_pct=95,
        )
        result = gate.score(metadata)
        for name, score in result.dimension_scores.items():
            self.assertGreater(score, 85, f"Dimension '{name}' unexpectedly low: {score}")


class TestScoreTerribleImage(unittest.TestCase):
    """Test scoring of a terrible iris capture."""

    def test_terrible_image_low_score(self):
        """A terrible image should receive a low overall score and be rejected."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=5,
            exposure=0,
            occlusion_pct=90,
            gaze_deviation=80,
            motion_blur=95,
            iris_visible_pct=5,
        )
        result = gate.score(metadata)
        self.assertLess(result.overall_score, 20)
        self.assertFalse(result.accepted)
        self.assertGreater(len(result.rejection_reasons), 0)


class TestHardGates(unittest.TestCase):
    """Test hard gate rejection logic."""

    def test_occlusion_hard_gate(self):
        """Occlusion above the hard gate should cause rejection."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=95,
            exposure=50,
            occlusion_pct=60,  # exceeds default max of 50
            gaze_deviation=2,
            motion_blur=5,
            iris_visible_pct=95,
        )
        result = gate.score(metadata)
        self.assertFalse(result.accepted)
        self.assertTrue(
            any("occlusion" in r.lower() for r in result.rejection_reasons),
            f"Expected occlusion reason in {result.rejection_reasons}",
        )

    def test_iris_visible_hard_gate(self):
        """Iris visible below the hard gate should cause rejection."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=95,
            exposure=50,
            occlusion_pct=5,
            gaze_deviation=2,
            motion_blur=5,
            iris_visible_pct=20,  # below default min of 30
        )
        result = gate.score(metadata)
        self.assertFalse(result.accepted)
        self.assertTrue(
            any("iris" in r.lower() for r in result.rejection_reasons),
            f"Expected iris visibility reason in {result.rejection_reasons}",
        )

    def test_gaze_hard_gate(self):
        """Gaze deviation above the hard gate should cause rejection."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=95,
            exposure=50,
            occlusion_pct=5,
            gaze_deviation=60,  # exceeds default max of 45
            motion_blur=5,
            iris_visible_pct=95,
        )
        result = gate.score(metadata)
        self.assertFalse(result.accepted)
        self.assertTrue(
            any("gaze" in r.lower() for r in result.rejection_reasons),
            f"Expected gaze reason in {result.rejection_reasons}",
        )

    def test_multiple_hard_gate_violations(self):
        """Multiple hard gate violations should produce multiple reasons."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=95,
            exposure=50,
            occlusion_pct=60,   # violates occlusion gate
            gaze_deviation=60,  # violates gaze gate
            motion_blur=5,
            iris_visible_pct=20,  # violates iris visible gate
        )
        result = gate.score(metadata)
        self.assertFalse(result.accepted)
        self.assertGreaterEqual(len(result.rejection_reasons), 3)

    def test_hard_gate_at_boundary_accepted(self):
        """Values exactly at the hard gate boundary should be accepted."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=80,
            exposure=50,
            occlusion_pct=50,       # exactly at max (not exceeding)
            gaze_deviation=45,      # exactly at max (not exceeding)
            motion_blur=10,
            iris_visible_pct=30,    # exactly at min (not below)
        )
        result = gate.score(metadata)
        # No hard gate reasons should fire for boundary values
        hard_gate_reasons = [
            r for r in result.rejection_reasons
            if "occlusion" in r.lower()
            or "iris" in r.lower()
            or "gaze" in r.lower()
        ]
        self.assertEqual(
            len(hard_gate_reasons), 0,
            f"Boundary values should not trigger hard gates: {hard_gate_reasons}",
        )


class TestDecide(unittest.TestCase):
    """Test the decide method with custom thresholds."""

    def test_custom_threshold_higher(self):
        """A stricter threshold should reject a middling image."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=60,
            exposure=40,
            occlusion_pct=20,
            gaze_deviation=20,
            motion_blur=30,
            iris_visible_pct=70,
        )
        # With default threshold (50) the image may pass
        result_default = gate.decide(metadata, min_quality=50)
        # With a very high threshold it should fail
        result_strict = gate.decide(metadata, min_quality=90)
        self.assertFalse(result_strict.accepted)
        # Scores should be identical regardless of threshold
        self.assertAlmostEqual(
            result_default.overall_score, result_strict.overall_score, places=5
        )

    def test_custom_threshold_lower(self):
        """A lenient threshold should accept a lower-quality image."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=40,
            exposure=35,
            occlusion_pct=30,
            gaze_deviation=25,
            motion_blur=40,
            iris_visible_pct=50,
        )
        result = gate.decide(metadata, min_quality=30)
        # With a very lenient threshold and no hard gate violations
        # the image should be accepted if the score exceeds 30
        if result.overall_score >= 30:
            self.assertTrue(result.accepted)


class TestBatchProcess(unittest.TestCase):
    """Test batch processing and statistics."""

    def _make_batch(self):
        """Create a mixed batch of images."""
        perfect = ImageMetadata(
            sharpness=95, exposure=50, occlusion_pct=5,
            gaze_deviation=2, motion_blur=5, iris_visible_pct=95,
        )
        good = ImageMetadata(
            sharpness=75, exposure=45, occlusion_pct=15,
            gaze_deviation=10, motion_blur=15, iris_visible_pct=80,
        )
        fair = ImageMetadata(
            sharpness=50, exposure=35, occlusion_pct=30,
            gaze_deviation=25, motion_blur=40, iris_visible_pct=55,
        )
        poor = ImageMetadata(
            sharpness=10, exposure=5, occlusion_pct=80,
            gaze_deviation=70, motion_blur=90, iris_visible_pct=10,
        )
        return [perfect, good, fair, poor]

    def test_batch_result_count(self):
        """Batch should return one result per image."""
        gate = QualityGate()
        batch = self._make_batch()
        result = gate.batch_process(batch)
        self.assertEqual(len(result.results), len(batch))

    def test_batch_acceptance_rate(self):
        """Acceptance rate should be between 0 and 1."""
        gate = QualityGate()
        batch = self._make_batch()
        result = gate.batch_process(batch)
        self.assertGreaterEqual(result.acceptance_rate, 0.0)
        self.assertLessEqual(result.acceptance_rate, 1.0)

    def test_batch_acceptance_rate_correct(self):
        """Acceptance rate should match accepted / total."""
        gate = QualityGate()
        batch = self._make_batch()
        result = gate.batch_process(batch)
        accepted_count = sum(1 for r in result.results if r.accepted)
        expected_rate = accepted_count / len(batch)
        self.assertAlmostEqual(result.acceptance_rate, expected_rate)

    def test_batch_avg_quality(self):
        """Average quality should be the mean of individual overall scores."""
        gate = QualityGate()
        batch = self._make_batch()
        result = gate.batch_process(batch)
        expected_avg = sum(r.overall_score for r in result.results) / len(batch)
        self.assertAlmostEqual(result.avg_quality, expected_avg, places=5)

    def test_batch_quality_distribution(self):
        """Quality distribution buckets should sum to total count."""
        gate = QualityGate()
        batch = self._make_batch()
        result = gate.batch_process(batch)
        dist = result.quality_distribution
        total = dist.get("excellent", 0) + dist.get("good", 0) + \
                dist.get("fair", 0) + dist.get("poor", 0)
        self.assertEqual(total, len(batch))

    def test_batch_distribution_categories(self):
        """All four distribution categories should be present."""
        gate = QualityGate()
        batch = self._make_batch()
        result = gate.batch_process(batch)
        for cat in ("excellent", "good", "fair", "poor"):
            self.assertIn(cat, result.quality_distribution)

    def test_batch_empty(self):
        """An empty batch should return sensible defaults."""
        gate = QualityGate()
        result = gate.batch_process([])
        self.assertEqual(len(result.results), 0)
        self.assertAlmostEqual(result.acceptance_rate, 0.0)
        self.assertAlmostEqual(result.avg_quality, 0.0)


class TestCalibrate(unittest.TestCase):
    """Test the weight calibration mechanism."""

    def test_calibrate_increases_important_weight(self):
        """After calibration where sharpness separates good/bad, its weight should increase."""
        gate = QualityGate()
        original_sharpness_weight = gate.weights["sharpness"]

        # Good examples: high sharpness, moderate everything else
        good_examples = [
            (ImageMetadata(sharpness=90, exposure=50, occlusion_pct=20,
                           gaze_deviation=15, motion_blur=20, iris_visible_pct=70), True),
            (ImageMetadata(sharpness=85, exposure=45, occlusion_pct=25,
                           gaze_deviation=18, motion_blur=25, iris_visible_pct=65), True),
            (ImageMetadata(sharpness=95, exposure=48, occlusion_pct=15,
                           gaze_deviation=10, motion_blur=15, iris_visible_pct=75), True),
        ]
        # Bad examples: low sharpness, moderate everything else
        bad_examples = [
            (ImageMetadata(sharpness=10, exposure=50, occlusion_pct=20,
                           gaze_deviation=15, motion_blur=20, iris_visible_pct=70), False),
            (ImageMetadata(sharpness=15, exposure=45, occlusion_pct=25,
                           gaze_deviation=18, motion_blur=25, iris_visible_pct=65), False),
            (ImageMetadata(sharpness=5, exposure=48, occlusion_pct=15,
                           gaze_deviation=10, motion_blur=15, iris_visible_pct=75), False),
        ]
        examples = good_examples + bad_examples
        gate.calibrate(examples)

        self.assertGreater(
            gate.weights["sharpness"],
            original_sharpness_weight,
            "Sharpness weight should increase after calibration with sharpness-dominant examples",
        )

    def test_calibrate_weights_sum_to_one(self):
        """Weights should sum to 1.0 after calibration."""
        gate = QualityGate()
        examples = [
            (ImageMetadata(sharpness=90, exposure=50, occlusion_pct=10,
                           gaze_deviation=5, motion_blur=10, iris_visible_pct=90), True),
            (ImageMetadata(sharpness=10, exposure=50, occlusion_pct=10,
                           gaze_deviation=5, motion_blur=10, iris_visible_pct=90), False),
        ]
        gate.calibrate(examples)
        total = sum(gate.weights.values())
        self.assertAlmostEqual(total, 1.0, places=5)

    def test_calibrate_no_change_when_no_gap(self):
        """If good and bad examples have equal scores, weights stay unchanged."""
        gate = QualityGate()
        original_weights = dict(gate.weights)
        # Both good and bad examples have the same metadata
        examples = [
            (ImageMetadata(sharpness=50, exposure=50, occlusion_pct=20,
                           gaze_deviation=15, motion_blur=20, iris_visible_pct=70), True),
            (ImageMetadata(sharpness=50, exposure=50, occlusion_pct=20,
                           gaze_deviation=15, motion_blur=20, iris_visible_pct=70), False),
        ]
        gate.calibrate(examples)
        for dim in original_weights:
            self.assertAlmostEqual(
                gate.weights[dim], original_weights[dim], places=5,
                msg=f"Weight for {dim} should not change when there is no gap",
            )


class TestCustomWeights(unittest.TestCase):
    """Test that custom weights are applied correctly."""

    def test_custom_weights_sharpness_dominant(self):
        """With sharpness weight = 1.0, score should equal normalised sharpness."""
        weights = {
            "sharpness": 1.0,
            "exposure": 0.0,
            "occlusion_pct": 0.0,
            "gaze_deviation": 0.0,
            "motion_blur": 0.0,
            "iris_visible_pct": 0.0,
        }
        gate = QualityGate(weights=weights)
        metadata = ImageMetadata(
            sharpness=75, exposure=0, occlusion_pct=0,
            gaze_deviation=0, motion_blur=0, iris_visible_pct=100,
        )
        result = gate.score(metadata)
        self.assertAlmostEqual(result.overall_score, 75.0, places=1)


class TestEdgeCases(unittest.TestCase):
    """Edge-case tests."""

    def test_all_zeros(self):
        """Metadata with all zeros should produce a low score."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=0, exposure=0, occlusion_pct=0,
            gaze_deviation=0, motion_blur=0, iris_visible_pct=0,
        )
        result = gate.score(metadata)
        # sharpness=0 -> 0, exposure=0 -> 0, occlusion=0 -> 100,
        # gaze=0 -> 100, blur=0 -> 100, iris_visible=0 -> 0
        # iris_visible=0 < 30 triggers hard gate, so rejected
        self.assertFalse(result.accepted)

    def test_all_hundreds(self):
        """Metadata with all 100s should have mixed dimension scores."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=100, exposure=100, occlusion_pct=100,
            gaze_deviation=90, motion_blur=100, iris_visible_pct=100,
        )
        result = gate.score(metadata)
        # occlusion_pct=100 triggers hard gate (>50), gaze=90 triggers (>45)
        self.assertFalse(result.accepted)
        self.assertGreaterEqual(len(result.rejection_reasons), 2)

    def test_result_dataclass_fields(self):
        """QualityResult should have all expected fields."""
        gate = QualityGate()
        metadata = ImageMetadata(
            sharpness=50, exposure=50, occlusion_pct=10,
            gaze_deviation=10, motion_blur=10, iris_visible_pct=80,
        )
        result = gate.score(metadata)
        self.assertIsInstance(result.overall_score, float)
        self.assertIsInstance(result.dimension_scores, dict)
        self.assertIsInstance(result.accepted, bool)
        self.assertIsInstance(result.rejection_reasons, list)
        self.assertEqual(len(result.dimension_scores), 6)

    def test_batch_result_dataclass_fields(self):
        """BatchResult should have all expected fields."""
        gate = QualityGate()
        images = [
            ImageMetadata(sharpness=80, exposure=50, occlusion_pct=10,
                          gaze_deviation=5, motion_blur=10, iris_visible_pct=90),
        ]
        result = gate.batch_process(images)
        self.assertIsInstance(result.results, list)
        self.assertIsInstance(result.acceptance_rate, float)
        self.assertIsInstance(result.avg_quality, float)
        self.assertIsInstance(result.quality_distribution, dict)


if __name__ == "__main__":
    unittest.main()
