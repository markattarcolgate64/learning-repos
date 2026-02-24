"""
KNN Classifier
==============
Category   : ML Engineering
Difficulty : * (1/5)

Problem
-------
Implement a K-Nearest Neighbors classifier from scratch using numpy.  The
classifier should support both euclidean and manhattan distance metrics and
use majority voting among the k closest training examples to predict the
class of a new data point.

KNN is one of the simplest supervised learning algorithms and is widely used
as a baseline classifier.  It requires no explicit training phase -- all
computation happens at prediction time.

Real-world motivation
---------------------
KNN is used in recommendation systems (find similar users/items), anomaly
detection (points far from all neighbours are suspicious), and as a quick
baseline when prototyping ML pipelines.  Understanding it deeply also builds
intuition for more advanced neighbour-based methods like locality-sensitive
hashing and approximate nearest-neighbour search.

Hints
-----
1. Euclidean distance: sqrt(sum((a - b) ** 2))
2. Manhattan distance: sum(|a - b|)
3. Use numpy broadcasting to compute distances from one point to all training
   points in a single operation.
4. np.argsort gives you the indices that would sort the distance array --
   take the first k.
5. collections.Counter.most_common(1) returns the majority vote.

Run command
-----------
    pytest 06_knn_classifier/test_exercise.py -v
"""

import numpy as np
from collections import Counter


class KNNClassifier:
    """A K-Nearest Neighbors classifier.

    Stores training data and classifies new points by majority vote among the
    k closest training examples using the chosen distance metric.
    """

    def __init__(self, k: int = 3, distance_metric: str = 'euclidean'):
        """Initialise the KNN classifier.

        Args:
            k: Number of nearest neighbours to consider.
            distance_metric: One of 'euclidean' or 'manhattan'.
        """
        # TODO: Store k and distance_metric.
        # TODO: Initialise X_train and y_train to None.
        # Hint: Validate that distance_metric is one of the two supported
        #       values.
        pass

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'KNNClassifier':
        """Store the training data.

        KNN is a lazy learner -- fit simply memorises the data.

        Args:
            X: Training feature matrix of shape (n_samples, n_features).
            y: Training label array of shape (n_samples,).

        Returns:
            self, to allow method chaining.
        """
        # TODO: Store X and y as instance attributes.
        # Hint: self.X_train = X; self.y_train = y; return self
        pass

    def _compute_distances(self, x: np.ndarray) -> np.ndarray:
        """Compute distances from a single point to all training points.

        Args:
            x: A single sample of shape (n_features,).

        Returns:
            A 1-D numpy array of distances of shape (n_train_samples,).
        """
        # TODO: If metric is 'euclidean', compute sqrt(sum((x - X_train)**2))
        #       for each training point.
        # TODO: If metric is 'manhattan', compute sum(|x - X_train|) for each
        #       training point.
        # Hint: Use np.sqrt(np.sum((self.X_train - x) ** 2, axis=1)) for
        #       euclidean.
        pass

    def _predict_single(self, x: np.ndarray) -> int:
        """Predict the class label for a single sample.

        Args:
            x: A single sample of shape (n_features,).

        Returns:
            The predicted class label (int).
        """
        # TODO: Compute distances to all training points.
        # TODO: Find the indices of the k smallest distances.
        # TODO: Gather the labels of those k neighbours.
        # TODO: Return the most common label (majority vote).
        # Hint: k_indices = np.argsort(distances)[:self.k]
        #       Counter(labels).most_common(1)[0][0]
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for multiple samples.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            A numpy array of predicted labels of shape (n_samples,).
        """
        # TODO: Apply _predict_single to every row of X.
        # Hint: np.array([self._predict_single(x) for x in X])
        pass

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute the classification accuracy on the given data.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: True label array of shape (n_samples,).

        Returns:
            Accuracy as a float between 0.0 and 1.0.
        """
        # TODO: Predict labels for X and compare with y.
        # Hint: return np.mean(self.predict(X) == y)
        pass
