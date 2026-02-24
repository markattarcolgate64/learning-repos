"""
Mini-Batch Gradient Descent
============================
Category   : ML Engineering
Difficulty : ** (2/5)

Problem
-------
Implement mini-batch stochastic gradient descent (SGD) for linear regression
from scratch using numpy.  The optimiser should partition the training data
into randomly-shuffled mini-batches, compute gradients on each batch, and
update the model weights accordingly.  Track the training loss after every
epoch so that convergence can be inspected.

Linear regression predicts y = X @ w + b, and we minimise the mean squared
error (MSE) loss.

Real-world motivation
---------------------
Full-batch gradient descent is too slow for large datasets because it
processes every sample before making a single weight update.  Pure SGD
(batch_size=1) is noisy and doesn't benefit from vectorised hardware.
Mini-batch SGD strikes the balance: it is fast, memory-efficient, and
provides enough gradient signal to converge smoothly.  Every modern deep
learning framework uses a variant of this algorithm.

Hints
-----
1. Shuffle the data at the start of each epoch, then slice it into batches.
2. Predictions: y_hat = X_batch @ w + b
3. MSE loss = (1/m) * sum((y_hat - y) ** 2)
4. Gradients:
       dw = (2/m) * X_batch.T @ (y_hat - y)
       db = (2/m) * sum(y_hat - y)
5. Update rule: w = w - lr * dw; b = b - lr * db
6. Record the full-dataset loss once at the end of each epoch (not per batch).

Run command
-----------
    pytest 07_mini_batch_gradient_descent/test_exercise.py -v
"""

import numpy as np


class MiniBatchGD:
    """Mini-batch stochastic gradient descent for linear regression.

    Fits a linear model y = X @ w + b by minimising MSE loss using
    mini-batch gradient updates.
    """

    def __init__(self, learning_rate: float = 0.01, batch_size: int = 32,
                 epochs: int = 100, seed: int = 42):
        """Initialise the optimiser.

        Args:
            learning_rate: Step size for each gradient update.
            batch_size: Number of samples per mini-batch.
            epochs: Number of full passes over the training data.
            seed: Random seed for reproducibility.
        """
        # TODO: Store learning_rate, batch_size, epochs, and seed.
        # TODO: Initialise weights (w), bias (b), and _loss_history to None/[].
        # Hint: self.w and self.b will be set during fit().
        pass

    def _create_batches(self, X: np.ndarray, y: np.ndarray) -> list:
        """Shuffle the data and split it into mini-batches.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Target array of shape (n_samples,).

        Returns:
            A list of (X_batch, y_batch) tuples.
        """
        # TODO: Create a random permutation of indices.
        # TODO: Slice X and y into chunks of size self.batch_size.
        # Hint: indices = np.random.permutation(len(y))
        #       Then iterate in steps of batch_size, slicing X[idx] and y[idx].
        pass

    def _compute_gradients(self, X_batch: np.ndarray,
                           y_batch: np.ndarray) -> tuple:
        """Compute gradients of the MSE loss w.r.t. weights and bias.

        The MSE loss is defined as:
            L = (1/m) * sum((X_batch @ w + b - y_batch) ** 2)

        The gradients are:
            dw = (2/m) * X_batch.T @ (predictions - y_batch)
            db = (2/m) * sum(predictions - y_batch)

        Args:
            X_batch: Feature matrix for this batch, shape (m, n_features).
            y_batch: Target array for this batch, shape (m,).

        Returns:
            A tuple (dw, db) where dw has shape (n_features,) and db is a
            scalar.
        """
        # TODO: Compute predictions = X_batch @ self.w + self.b
        # TODO: Compute error = predictions - y_batch
        # TODO: Compute dw = (2/m) * X_batch.T @ error
        # TODO: Compute db = (2/m) * np.sum(error)
        # Hint: m = len(y_batch)
        pass

    def _compute_loss(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute the MSE loss over the given data.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Target array of shape (n_samples,).

        Returns:
            The mean squared error as a float.
        """
        # TODO: predictions = X @ self.w + self.b
        # TODO: Return np.mean((predictions - y) ** 2)
        pass

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MiniBatchGD':
        """Train the linear model using mini-batch gradient descent.

        Initialises weights to zeros, then for each epoch: creates shuffled
        mini-batches, updates weights on each batch, and records the
        full-dataset MSE loss at the end of the epoch.

        Args:
            X: Training feature matrix of shape (n_samples, n_features).
            y: Training target array of shape (n_samples,).

        Returns:
            self, to allow method chaining.
        """
        # TODO: Set the random seed with np.random.seed(self.seed).
        # TODO: Initialise self.w = np.zeros(n_features) and self.b = 0.0.
        # TODO: Initialise self._loss_history = [].
        # TODO: For each epoch:
        #       1. Create mini-batches.
        #       2. For each batch, compute gradients and update w and b.
        #       3. Compute and record the full-dataset loss.
        # Hint: self.w -= self.learning_rate * dw
        #       self.b -= self.learning_rate * db
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values for the given feature matrix.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predicted values as a numpy array of shape (n_samples,).
        """
        # TODO: Return X @ self.w + self.b
        pass

    @property
    def loss_history(self) -> list:
        """Return the list of MSE losses recorded at the end of each epoch.

        Returns:
            A list of floats, one per epoch.
        """
        # TODO: Return self._loss_history
        pass
