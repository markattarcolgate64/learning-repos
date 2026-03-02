"""
Tests for Exercise 6: Computer Vision - Image Classification.

Run with:
    python -m unittest 06_computer_vision.test_exercise -v
"""

import unittest
import numpy as np
from sklearn.model_selection import train_test_split
from .exercise import (
    load_image_data,
    normalize_pixels,
    train_classifiers,
    evaluate_models,
    compute_confusion,
    find_misclassified,
    find_most_confused_pair,
)


class TestComputerVision(unittest.TestCase):
    """Tests for the computer vision exercise."""

    @classmethod
    def setUpClass(cls):
        cls.data = load_image_data()
        if cls.data['X'] is not None:
            cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(
                cls.data['X'], cls.data['y'], test_size=0.2, random_state=42
            )
        else:
            cls.X_train = cls.X_test = cls.y_train = cls.y_test = None

    # ------------------------------------------------------------------
    # 1. Data loading
    # ------------------------------------------------------------------

    def test_load_image_data_returns_all_keys(self):
        """load_image_data() should return dict with all required keys."""
        for key in ['images', 'X', 'y', 'n_samples', 'n_classes']:
            self.assertIn(key, self.data, f"Missing key: {key}")
            self.assertIsNotNone(self.data[key], f"'{key}' is None")

    def test_load_image_shapes(self):
        """Images should be 8x8, X should be n_samples x 64."""
        self.assertEqual(self.data['images'].shape[1:], (8, 8),
                         "Images should be 8x8 pixels")
        self.assertEqual(self.data['X'].shape[1], 64,
                         "Flattened features should have 64 values (8*8)")

    def test_load_image_counts(self):
        """Should have 1797 samples and 10 digit classes."""
        self.assertEqual(self.data['n_samples'], 1797)
        self.assertEqual(self.data['n_classes'], 10)

    def test_load_image_labels_range(self):
        """Labels should be digits 0-9."""
        unique = set(self.data['y'])
        self.assertEqual(unique, set(range(10)))

    def test_images_and_X_consistent(self):
        """Flattened X should match reshaped images."""
        reshaped = self.data['images'].reshape(-1, 64)
        np.testing.assert_array_equal(reshaped, self.data['X'],
                                      "X should be the flattened version of images")

    # ------------------------------------------------------------------
    # 2. Pixel normalization
    # ------------------------------------------------------------------

    def test_normalize_pixels_range(self):
        """Normalized pixels should be in [0, 1]."""
        self.assertIsNotNone(self.X_train)
        X_train_n, X_test_n, scaler = normalize_pixels(self.X_train, self.X_test)
        self.assertIsNotNone(X_train_n, "X_train_norm is None")
        self.assertAlmostEqual(X_train_n.min(), 0.0, places=5)
        self.assertAlmostEqual(X_train_n.max(), 1.0, places=5)
        self.assertGreaterEqual(X_test_n.min(), -0.5)
        self.assertLessEqual(X_test_n.max(), 1.5)

    def test_normalize_preserves_shape(self):
        """Normalization should not change array shapes."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        self.assertIsNotNone(X_train_n)
        self.assertEqual(X_train_n.shape, self.X_train.shape)
        self.assertEqual(X_test_n.shape, self.X_test.shape)

    def test_normalize_returns_scaler(self):
        """Should return a fitted scaler."""
        _, _, scaler = normalize_pixels(self.X_train, self.X_test)
        self.assertIsNotNone(scaler, "scaler is None")
        self.assertTrue(hasattr(scaler, 'data_min_'),
                        "Scaler does not appear to be fitted")

    # ------------------------------------------------------------------
    # 3. Training classifiers
    # ------------------------------------------------------------------

    def test_train_classifiers_returns_models(self):
        """Should return at least 3 fitted models."""
        X_train_n, _, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        self.assertIsInstance(models, dict)
        self.assertGreaterEqual(len(models), 3,
                                "Should have at least 3 different models")

    def test_train_classifiers_are_fitted(self):
        """All returned models should be fitted (able to predict)."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        for name, model in models.items():
            try:
                preds = model.predict(X_test_n[:5])
                self.assertEqual(len(preds), 5, f"{name} predictions wrong shape")
            except Exception as e:
                self.fail(f"Model '{name}' is not fitted: {e}")

    # ------------------------------------------------------------------
    # 4. Evaluation
    # ------------------------------------------------------------------

    def test_evaluate_models_accuracy(self):
        """All models should achieve > 90% accuracy on digits."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        results = evaluate_models(models, X_test_n, self.y_test)
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), len(models))
        for name, r in results.items():
            self.assertIn('accuracy', r, f"'{name}' result missing 'accuracy'")
            self.assertIn('predictions', r, f"'{name}' result missing 'predictions'")
            self.assertGreater(r['accuracy'], 0.90,
                               f"{name} accuracy {r['accuracy']:.2%} should be > 90%")

    def test_confusion_matrix_shape(self):
        """Confusion matrix should be 10x10 for 10 digit classes."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        results = evaluate_models(models, X_test_n, self.y_test)
        best_name = max(results, key=lambda n: results[n]['accuracy'])
        cm = compute_confusion(self.y_test, results[best_name]['predictions'])
        self.assertIsNotNone(cm, "confusion matrix is None")
        self.assertEqual(cm.shape, (10, 10), "Should be 10x10 for 10 digits")

    def test_confusion_matrix_sums(self):
        """Confusion matrix rows should sum to class counts."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        results = evaluate_models(models, X_test_n, self.y_test)
        best_name = max(results, key=lambda n: results[n]['accuracy'])
        cm = compute_confusion(self.y_test, results[best_name]['predictions'])
        self.assertIsNotNone(cm)
        self.assertEqual(cm.sum(), len(self.y_test),
                         "Confusion matrix total should equal test set size")

    # ------------------------------------------------------------------
    # 5. Misclassification analysis
    # ------------------------------------------------------------------

    def test_find_misclassified(self):
        """Should find indices where predictions differ from truth."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        results = evaluate_models(models, X_test_n, self.y_test)
        best_name = max(results, key=lambda n: results[n]['accuracy'])
        preds = results[best_name]['predictions']

        wrong = find_misclassified(self.y_test, preds)
        self.assertIsNotNone(wrong, "find_misclassified returned None")
        # Verify all returned indices are actual mistakes
        for idx in wrong:
            y_val = self.y_test.iloc[idx] if hasattr(self.y_test, 'iloc') else self.y_test[idx]
            self.assertNotEqual(y_val, preds[idx],
                                f"Index {idx} is not a misclassification")

    def test_find_most_confused_pair(self):
        """Should identify the most confused digit pair."""
        X_train_n, X_test_n, _ = normalize_pixels(self.X_train, self.X_test)
        models = train_classifiers(X_train_n, self.y_train)
        results = evaluate_models(models, X_test_n, self.y_test)
        best_name = max(results, key=lambda n: results[n]['accuracy'])
        cm = compute_confusion(self.y_test, results[best_name]['predictions'])

        true_d, pred_d, count = find_most_confused_pair(cm)
        self.assertIsNotNone(true_d, "true_digit is None")
        self.assertNotEqual(true_d, pred_d,
                            "Most confused pair should be different digits")
        self.assertGreaterEqual(count, 1, "Count should be at least 1")
        # Verify it's actually the max off-diagonal
        cm_copy = cm.copy()
        np.fill_diagonal(cm_copy, 0)
        self.assertEqual(count, cm_copy.max(),
                         "Should be the largest off-diagonal value")


if __name__ == "__main__":
    unittest.main()
