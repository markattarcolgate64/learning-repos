"""
Tests for Mini-Batch Gradient Descent.

Run with:
    python -m unittest 07_mini_batch_gradient_descent.test_exercise -v
"""

import unittest
import numpy as np
from .exercise import MiniBatchGD


class TestMiniBatchGD(unittest.TestCase):
    """Comprehensive tests for the MiniBatchGD linear regression optimiser."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _make_linear_data(w_true, b_true, n=200, noise=0.1, seed=0):
        """Generate synthetic linear data: y = X @ w_true + b_true + noise."""
        rng = np.random.RandomState(seed)
        n_features = len(w_true)
        X = rng.randn(n, n_features)
        y = X @ np.array(w_true, dtype=float) + b_true + rng.randn(n) * noise
        return X, y

    # ------------------------------------------------------------------
    # 1. Convergence: loss decreases over epochs
    # ------------------------------------------------------------------

    def test_convergence_loss_decreases(self):
        """Final loss should be strictly less than the initial loss."""
        X, y = self._make_linear_data([3.0], 2.0, n=200)
        model = MiniBatchGD(learning_rate=0.05, batch_size=32, epochs=100, seed=42)
        model.fit(X, y)
        history = model.loss_history
        self.assertGreater(len(history), 0)
        self.assertLess(history[-1], history[0],
                        "Loss did not decrease over training.")

    # ------------------------------------------------------------------
    # 2. Simple linear: y = 3x + 2
    # ------------------------------------------------------------------

    def test_simple_linear_weights(self):
        """Learned weights should be close to true weights for y = 3x + 2."""
        X, y = self._make_linear_data([3.0], 2.0, n=500, noise=0.05)
        model = MiniBatchGD(learning_rate=0.05, batch_size=32, epochs=200, seed=42)
        model.fit(X, y)
        np.testing.assert_allclose(model.w, [3.0], atol=0.5,
                                   err_msg="Weight not close to 3.0")
        self.assertAlmostEqual(model.b, 2.0, delta=0.5,
                               msg="Bias not close to 2.0")

    # ------------------------------------------------------------------
    # 3. Full batch (batch_size = n): behaves like standard GD
    # ------------------------------------------------------------------

    def test_full_batch_converges(self):
        """With batch_size equal to the dataset size, GD should still converge."""
        X, y = self._make_linear_data([1.0, -2.0], 0.5, n=100, noise=0.1)
        n = X.shape[0]
        model = MiniBatchGD(learning_rate=0.05, batch_size=n, epochs=200, seed=7)
        model.fit(X, y)
        history = model.loss_history
        self.assertLess(history[-1], history[0])
        self.assertLess(history[-1], 0.1,
                        "Full-batch GD did not converge to a low loss.")

    # ------------------------------------------------------------------
    # 4. Batch size = 1 (pure SGD): still converges
    # ------------------------------------------------------------------

    def test_sgd_batch_size_one(self):
        """Pure SGD (batch_size=1) should still converge, although noisily."""
        X, y = self._make_linear_data([2.0], 1.0, n=200, noise=0.1)
        model = MiniBatchGD(learning_rate=0.01, batch_size=1, epochs=100, seed=42)
        model.fit(X, y)
        history = model.loss_history
        self.assertLess(history[-1], history[0],
                        "SGD with batch_size=1 did not converge.")

    # ------------------------------------------------------------------
    # 5. loss_history length equals number of epochs
    # ------------------------------------------------------------------

    def test_loss_history_length(self):
        """loss_history should contain exactly one entry per epoch."""
        epochs = 50
        X, y = self._make_linear_data([1.0], 0.0, n=100)
        model = MiniBatchGD(learning_rate=0.01, batch_size=16, epochs=epochs, seed=42)
        model.fit(X, y)
        self.assertEqual(len(model.loss_history), epochs)

    # ------------------------------------------------------------------
    # 6. Predictions close to actual values after training
    # ------------------------------------------------------------------

    def test_predictions_close(self):
        """After training, predictions should be close to the true y values."""
        X, y = self._make_linear_data([3.0], 2.0, n=300, noise=0.05)
        model = MiniBatchGD(learning_rate=0.05, batch_size=32, epochs=200, seed=42)
        model.fit(X, y)
        preds = model.predict(X)
        self.assertEqual(preds.shape, y.shape)
        np.testing.assert_allclose(preds, y, atol=0.5,
                                   err_msg="Predictions are not close to actual values.")

    # ------------------------------------------------------------------
    # 7. Multiple features: works with 3+ features
    # ------------------------------------------------------------------

    def test_multiple_features(self):
        """Model should handle multiple input features correctly."""
        w_true = [1.5, -0.5, 2.0, 0.3]
        b_true = -1.0
        X, y = self._make_linear_data(w_true, b_true, n=500, noise=0.05)
        model = MiniBatchGD(learning_rate=0.05, batch_size=32, epochs=300, seed=42)
        model.fit(X, y)
        np.testing.assert_allclose(model.w, w_true, atol=0.5,
                                   err_msg="Multi-feature weights not learned correctly.")
        self.assertAlmostEqual(model.b, b_true, delta=0.5)

    # ------------------------------------------------------------------
    # 8. Reproducibility: same seed gives same results
    # ------------------------------------------------------------------

    def test_reproducibility(self):
        """Running fit twice with the same seed should produce identical results."""
        X, y = self._make_linear_data([2.0], 1.0, n=100, noise=0.1)

        model_a = MiniBatchGD(learning_rate=0.05, batch_size=16, epochs=50, seed=99)
        model_a.fit(X, y)

        model_b = MiniBatchGD(learning_rate=0.05, batch_size=16, epochs=50, seed=99)
        model_b.fit(X, y)

        np.testing.assert_array_equal(model_a.w, model_b.w,
                                      err_msg="Weights differ across identical runs.")
        self.assertEqual(model_a.b, model_b.b,
                         "Bias differs across identical runs.")
        self.assertEqual(model_a.loss_history, model_b.loss_history,
                         "Loss history differs across identical runs.")


if __name__ == "__main__":
    unittest.main()
