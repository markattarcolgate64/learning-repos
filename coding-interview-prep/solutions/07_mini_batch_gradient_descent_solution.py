"""
Mini-Batch Gradient Descent - Solution

Implements mini-batch stochastic gradient descent for linear regression.
Partitions data into shuffled mini-batches, computes gradients per batch,
updates weights, and tracks MSE loss each epoch.
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
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs
        self.seed = seed
        self.w = None
        self.b = None
        self._loss_history = []

    def _create_batches(self, X: np.ndarray, y: np.ndarray) -> list:
        """Shuffle the data and split it into mini-batches.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Target array of shape (n_samples,).

        Returns:
            A list of (X_batch, y_batch) tuples.
        """
        n = len(y)
        indices = np.random.permutation(n)
        batches = []
        for start in range(0, n, self.batch_size):
            idx = indices[start:start + self.batch_size]
            batches.append((X[idx], y[idx]))
        return batches

    def _compute_gradients(self, X_batch: np.ndarray,
                           y_batch: np.ndarray) -> tuple:
        """Compute gradients of the MSE loss w.r.t. weights and bias.

        Args:
            X_batch: Feature matrix for this batch, shape (m, n_features).
            y_batch: Target array for this batch, shape (m,).

        Returns:
            A tuple (dw, db) where dw has shape (n_features,) and db is a
            scalar.
        """
        m = len(y_batch)
        predictions = X_batch @ self.w + self.b
        error = predictions - y_batch
        dw = (2.0 / m) * (X_batch.T @ error)
        db = (2.0 / m) * np.sum(error)
        return dw, db

    def _compute_loss(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute the MSE loss over the given data.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Target array of shape (n_samples,).

        Returns:
            The mean squared error as a float.
        """
        predictions = X @ self.w + self.b
        return float(np.mean((predictions - y) ** 2))

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MiniBatchGD':
        """Train the linear model using mini-batch gradient descent.

        Args:
            X: Training feature matrix of shape (n_samples, n_features).
            y: Training target array of shape (n_samples,).

        Returns:
            self, to allow method chaining.
        """
        np.random.seed(self.seed)
        n_features = X.shape[1]
        self.w = np.zeros(n_features)
        self.b = 0.0
        self._loss_history = []

        for _ in range(self.epochs):
            batches = self._create_batches(X, y)
            for X_batch, y_batch in batches:
                dw, db = self._compute_gradients(X_batch, y_batch)
                self.w -= self.learning_rate * dw
                self.b -= self.learning_rate * db
            loss = self._compute_loss(X, y)
            self._loss_history.append(loss)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values for the given feature matrix.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predicted values as a numpy array of shape (n_samples,).
        """
        return X @ self.w + self.b

    @property
    def loss_history(self) -> list:
        """Return the list of MSE losses recorded at the end of each epoch."""
        return self._loss_history
