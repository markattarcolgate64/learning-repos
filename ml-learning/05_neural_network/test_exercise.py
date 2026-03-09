"""
Tests for Exercise 5: Neural Network from Scratch.

Run with:
    python -m unittest 05_neural_network.test_exercise -v
"""

import unittest
import numpy as np
from .exercise import (
    make_circles,
    sigmoid,
    sigmoid_derivative,
    initialize_weights,
    forward,
    compute_loss,
    backward,
    train,
    predict,
)


class TestNeuralNetwork(unittest.TestCase):
    """Tests for the neural network exercise."""

    @classmethod
    def setUpClass(cls):
        cls.X, cls.y = make_circles(n_samples=300, noise=0.1, seed=42)

    # ------------------------------------------------------------------
    # 1. Weight initialization
    # ------------------------------------------------------------------

    def test_initialize_weights_shapes(self):
        """Weights and biases should have correct shapes."""
        params = initialize_weights(2, 8, 1)
        self.assertIsNotNone(params['W1'], "W1 is None")
        self.assertEqual(params['W1'].shape, (2, 8), "W1 should be (input, hidden)")
        self.assertEqual(params['b1'].shape, (1, 8), "b1 should be (1, hidden)")
        self.assertEqual(params['W2'].shape, (8, 1), "W2 should be (hidden, output)")
        self.assertEqual(params['b2'].shape, (1, 1), "b2 should be (1, output)")

    def test_initialize_weights_biases_zero(self):
        """Biases should be initialized to zero."""
        params = initialize_weights(2, 8, 1)
        self.assertIsNotNone(params['b1'])
        np.testing.assert_array_equal(params['b1'], np.zeros((1, 8)))
        np.testing.assert_array_equal(params['b2'], np.zeros((1, 1)))

    def test_initialize_weights_not_zero(self):
        """Weights should NOT be all zeros (need symmetry breaking)."""
        params = initialize_weights(2, 8, 1)
        self.assertIsNotNone(params['W1'])
        self.assertFalse(np.all(params['W1'] == 0), "W1 should not be all zeros")
        self.assertFalse(np.all(params['W2'] == 0), "W2 should not be all zeros")

    # ------------------------------------------------------------------
    # 2. Forward pass
    # ------------------------------------------------------------------

    def test_forward_output_shape(self):
        """Forward pass output should have shape (n_samples, 1)."""
        params = initialize_weights(2, 8, 1)
        self.assertIsNotNone(params['W1'])
        cache = forward(self.X, params)
        self.assertIsNotNone(cache['a2'], "a2 is None - implement forward()")
        self.assertEqual(cache['a2'].shape, (300, 1), "Output should be (n_samples, 1)")

    def test_forward_output_in_range(self):
        """Forward pass output (sigmoid) should be between 0 and 1."""
        params = initialize_weights(2, 8, 1)
        cache = forward(self.X, params)
        self.assertIsNotNone(cache['a2'])
        self.assertTrue(np.all(cache['a2'] >= 0), "Sigmoid output should be >= 0")
        self.assertTrue(np.all(cache['a2'] <= 1), "Sigmoid output should be <= 1")

    def test_forward_hidden_shape(self):
        """Hidden layer should have shape (n_samples, hidden_size)."""
        params = initialize_weights(2, 8, 1)
        cache = forward(self.X, params)
        self.assertIsNotNone(cache['a1'], "a1 is None")
        self.assertEqual(cache['a1'].shape, (300, 8))

    # ------------------------------------------------------------------
    # 3. Loss computation
    # ------------------------------------------------------------------

    def test_compute_loss_positive(self):
        """Binary cross-entropy loss should be positive."""
        params = initialize_weights(2, 8, 1)
        cache = forward(self.X, params)
        self.assertIsNotNone(cache['a2'])
        loss = compute_loss(self.y, cache['a2'])
        self.assertIsNotNone(loss, "Loss is None - implement compute_loss()")
        self.assertGreater(loss, 0, "Loss should be positive")

    def test_compute_loss_perfect_predictions(self):
        """Loss should be near 0 for perfect predictions."""
        perfect_pred = self.y.copy().astype(float)
        # Avoid exact 0 or 1 for numerical stability
        perfect_pred[perfect_pred == 0] = 0.001
        perfect_pred[perfect_pred == 1] = 0.999
        loss = compute_loss(self.y, perfect_pred)
        self.assertIsNotNone(loss)
        self.assertLess(loss, 0.01, "Loss should be near 0 for perfect predictions")

    # ------------------------------------------------------------------
    # 4. Backpropagation
    # ------------------------------------------------------------------

    def test_backward_gradient_shapes(self):
        """Gradients should have the same shapes as the corresponding weights."""
        params = initialize_weights(2, 8, 1)
        cache = forward(self.X, params)
        grads = backward(self.X, self.y, params, cache)
        self.assertIsNotNone(grads['dW1'], "dW1 is None - implement backward()")
        self.assertEqual(grads['dW1'].shape, params['W1'].shape, "dW1 shape mismatch")
        self.assertEqual(grads['db1'].shape, params['b1'].shape, "db1 shape mismatch")
        self.assertEqual(grads['dW2'].shape, params['W2'].shape, "dW2 shape mismatch")
        self.assertEqual(grads['db2'].shape, params['b2'].shape, "db2 shape mismatch")

    def test_backward_gradients_not_zero(self):
        """Gradients should not be all zeros (that means no learning)."""
        params = initialize_weights(2, 8, 1)
        cache = forward(self.X, params)
        grads = backward(self.X, self.y, params, cache)
        self.assertIsNotNone(grads['dW1'])
        self.assertFalse(np.all(grads['dW1'] == 0), "dW1 should not be all zeros")
        self.assertFalse(np.all(grads['dW2'] == 0), "dW2 should not be all zeros")

    # ------------------------------------------------------------------
    # 5. Training
    # ------------------------------------------------------------------

    def test_training_loss_decreases(self):
        """Loss should decrease over training epochs."""
        params, loss_history = train(self.X, self.y, hidden_size=8,
                                     learning_rate=1.0, epochs=500, seed=42)
        self.assertGreater(len(loss_history), 0, "loss_history is empty")
        self.assertLess(loss_history[-1], loss_history[0],
                        "Loss should decrease over training")

    def test_training_achieves_good_accuracy(self):
        """Network should achieve > 80% accuracy after training."""
        params, _ = train(self.X, self.y, hidden_size=8,
                          learning_rate=1.0, epochs=1000, seed=42)
        self.assertIsNotNone(params)
        preds = predict(self.X, params)
        self.assertIsNotNone(preds, "predict() returned None")
        accuracy = np.mean(preds == self.y)
        self.assertGreater(accuracy, 0.80,
                           f"Accuracy {accuracy:.2%} should be > 80%")

    # ------------------------------------------------------------------
    # 6. Predictions
    # ------------------------------------------------------------------

    def test_predictions_are_binary(self):
        """Predictions should be 0 or 1."""
        params, _ = train(self.X, self.y, hidden_size=8,
                          learning_rate=1.0, epochs=500, seed=42)
        preds = predict(self.X, params)
        self.assertIsNotNone(preds)
        unique = set(preds.ravel().tolist())
        self.assertTrue(unique.issubset({0, 1}),
                        f"Predictions should be 0 or 1, got {unique}")

    def test_predictions_shape(self):
        """Predictions should have shape (n_samples, 1)."""
        params, _ = train(self.X, self.y, hidden_size=8,
                          learning_rate=1.0, epochs=100, seed=42)
        preds = predict(self.X, params)
        self.assertIsNotNone(preds)
        self.assertEqual(preds.shape, (300, 1))


if __name__ == "__main__":
    unittest.main()
