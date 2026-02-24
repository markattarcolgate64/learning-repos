"""
K-Nearest Neighbors Classifier - Solution

A KNN classifier that supports euclidean and manhattan distance metrics.
Uses numpy for efficient vectorized distance computation.
"""

from collections import Counter
from typing import Literal

import numpy as np


class KNNClassifier:
    def __init__(self, k: int = 3, distance_metric: Literal["euclidean", "manhattan"] = "euclidean"):
        """
        Initialize the KNN classifier.

        Args:
            k: Number of nearest neighbors to use for prediction.
            distance_metric: Distance metric to use ('euclidean' or 'manhattan').

        Raises:
            ValueError: If an unsupported distance metric is provided.
        """
        if distance_metric not in ("euclidean", "manhattan"):
            raise ValueError(f"Unsupported distance metric: {distance_metric}. Use 'euclidean' or 'manhattan'.")
        self.k = k
        self.distance_metric = distance_metric
        self.X_train = None
        self.y_train = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        """
        Store the training data.

        Args:
            X: Training feature matrix of shape (n_samples, n_features).
            y: Training labels of shape (n_samples,).

        Returns:
            self
        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)
        return self

    def _compute_distances(self, x: np.ndarray) -> np.ndarray:
        """
        Compute distances from a single point to all training points.

        Args:
            x: A single feature vector of shape (n_features,).

        Returns:
            Array of distances of shape (n_train_samples,).
        """
        if self.distance_metric == "euclidean":
            return np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        else:  # manhattan
            return np.sum(np.abs(self.X_train - x), axis=1)

    def _predict_single(self, x: np.ndarray):
        """
        Predict the class label for a single sample.

        Args:
            x: A single feature vector of shape (n_features,).

        Returns:
            The predicted class label.
        """
        distances = self._compute_distances(x)
        nearest_indices = np.argsort(distances)[: self.k]
        nearest_labels = self.y_train[nearest_indices]
        counter = Counter(nearest_labels)
        return counter.most_common(1)[0][0]

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for a set of samples.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predicted labels of shape (n_samples,).
        """
        X = np.array(X)
        return np.array([self._predict_single(x) for x in X])

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Compute the classification accuracy on the given data.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: True labels of shape (n_samples,).

        Returns:
            Accuracy as a float between 0 and 1.
        """
        predictions = self.predict(X)
        return float(np.mean(predictions == np.array(y)))
