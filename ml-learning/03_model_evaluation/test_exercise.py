"""
Tests for Exercise 3: Model Evaluation and Comparison.

Run with:
    python -m unittest 03_model_evaluation.test_exercise -v
"""

import unittest
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from .exercise import (
    load_and_split,
    compute_confusion_matrix,
    compute_metrics,
    cross_validate_model,
    create_models,
    compare_models,
    select_best_model,
)


class TestModelEvaluation(unittest.TestCase):
    """Tests for the model evaluation exercise."""

    @classmethod
    def setUpClass(cls):
        """Set up shared test data."""
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = load_and_split()
        cls.baseline = DecisionTreeClassifier(random_state=42)
        cls.baseline.fit(cls.X_train, cls.y_train)
        cls.y_pred = cls.baseline.predict(cls.X_test)

    # ------------------------------------------------------------------
    # 1. Confusion matrix
    # ------------------------------------------------------------------

    def test_confusion_matrix_shape(self):
        """Confusion matrix should be 2x2 for binary classification."""
        cm = compute_confusion_matrix(self.y_test, self.y_pred)
        self.assertIsNotNone(cm, "confusion_matrix returned None")
        self.assertEqual(cm.shape, (2, 2), "Confusion matrix should be 2x2")

    def test_confusion_matrix_sums_to_total(self):
        """All values in confusion matrix should sum to the test set size."""
        cm = compute_confusion_matrix(self.y_test, self.y_pred)
        self.assertIsNotNone(cm)
        self.assertEqual(cm.sum(), len(self.y_test),
                         "Confusion matrix values should sum to test set size")

    def test_confusion_matrix_values_non_negative(self):
        """All confusion matrix values should be non-negative."""
        cm = compute_confusion_matrix(self.y_test, self.y_pred)
        self.assertIsNotNone(cm)
        self.assertTrue(np.all(cm >= 0), "Confusion matrix values should be >= 0")

    # ------------------------------------------------------------------
    # 2. Precision, Recall, F1
    # ------------------------------------------------------------------

    def test_metrics_in_valid_range(self):
        """Precision, recall, and F1 should all be between 0 and 1."""
        prec, rec, f1 = compute_metrics(self.y_test, self.y_pred)
        self.assertIsNotNone(prec, "precision is None")
        self.assertIsNotNone(rec, "recall is None")
        self.assertIsNotNone(f1, "f1 is None")
        for name, val in [("precision", prec), ("recall", rec), ("f1", f1)]:
            self.assertGreaterEqual(val, 0.0, f"{name} should be >= 0")
            self.assertLessEqual(val, 1.0, f"{name} should be <= 1")

    def test_f1_is_harmonic_mean(self):
        """F1 should be approximately the harmonic mean of precision and recall."""
        prec, rec, f1 = compute_metrics(self.y_test, self.y_pred)
        self.assertIsNotNone(f1)
        if prec > 0 and rec > 0:
            expected_f1 = 2 * (prec * rec) / (prec + rec)
            self.assertAlmostEqual(f1, expected_f1, places=3,
                                   msg="F1 should be the harmonic mean of precision and recall")

    # ------------------------------------------------------------------
    # 3. Cross-validation
    # ------------------------------------------------------------------

    def test_cross_validation_returns_5_scores(self):
        """5-fold CV should return exactly 5 scores."""
        model = DecisionTreeClassifier(random_state=42)
        scores = cross_validate_model(model, self.X_train, self.y_train, cv=5)
        self.assertIsNotNone(scores, "cross_validate_model returned None")
        self.assertEqual(len(scores), 5, "Should return one score per fold")

    def test_cross_validation_scores_in_range(self):
        """All CV scores should be between 0 and 1."""
        model = DecisionTreeClassifier(random_state=42)
        scores = cross_validate_model(model, self.X_train, self.y_train)
        self.assertIsNotNone(scores)
        for s in scores:
            self.assertGreaterEqual(s, 0.0)
            self.assertLessEqual(s, 1.0)

    # ------------------------------------------------------------------
    # 4. Model creation
    # ------------------------------------------------------------------

    def test_create_models_returns_dict(self):
        """create_models() should return a dict with at least 3 models."""
        models = create_models()
        self.assertIsNotNone(models, "create_models() returned None")
        self.assertIsInstance(models, dict)
        self.assertGreaterEqual(len(models), 3,
                                "Should have at least 3 different models")

    def test_create_models_has_different_types(self):
        """Models should be of different types."""
        models = create_models()
        self.assertIsNotNone(models)
        model_types = set(type(m).__name__ for m in models.values())
        self.assertGreaterEqual(len(model_types), 3,
                                "Should have at least 3 different model types")

    # ------------------------------------------------------------------
    # 5. Model comparison
    # ------------------------------------------------------------------

    def test_compare_models_returns_scores(self):
        """compare_models should return a dict of scores for each model."""
        models = create_models()
        self.assertIsNotNone(models)
        results = compare_models(models, self.X_train, self.y_train)
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), len(models),
                         "Should have a score for each model")
        for name, score in results.items():
            self.assertGreaterEqual(score, 0.0, f"{name} score should be >= 0")
            self.assertLessEqual(score, 1.0, f"{name} score should be <= 1")

    def test_select_best_model(self):
        """select_best_model should return the name of the highest-scoring model."""
        models = create_models()
        self.assertIsNotNone(models)
        results = compare_models(models, self.X_train, self.y_train)
        best = select_best_model(results)
        self.assertIsNotNone(best, "select_best_model returned None")
        self.assertIn(best, results, "Best model name should be one of the models")
        # Verify it actually has the highest score
        self.assertEqual(results[best], max(results.values()),
                         "Best model should have the highest score")


if __name__ == "__main__":
    unittest.main()
