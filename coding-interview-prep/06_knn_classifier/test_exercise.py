"""Tests for the KNN Classifier exercise."""

import unittest

import numpy as np

from .exercise import KNNClassifier


class TestKNNClassifier(unittest.TestCase):
    """Comprehensive tests for KNNClassifier."""

    # ------------------------------------------------------------------
    # 1. Linearly separable 2D data: perfect classification
    # ------------------------------------------------------------------
    def test_linearly_separable_2d(self):
        """KNN should achieve perfect accuracy on well-separated clusters."""
        # Cluster 0 centred around (0, 0), Cluster 1 centred around (10, 10)
        np.random.seed(42)
        X_train = np.vstack([
            np.random.randn(50, 2) + [0, 0],    # class 0
            np.random.randn(50, 2) + [10, 10],   # class 1
        ])
        y_train = np.array([0] * 50 + [1] * 50)

        X_test = np.array([[0.5, 0.5], [9.5, 9.5]])
        y_test = np.array([0, 1])

        knn = KNNClassifier(k=3, distance_metric="euclidean")
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)

        np.testing.assert_array_equal(predictions, y_test)

    # ------------------------------------------------------------------
    # 2. k=1: memorizes training data perfectly
    # ------------------------------------------------------------------
    def test_k1_memorizes_training_data(self):
        """With k=1, predicting on the training set should be 100% accurate."""
        np.random.seed(0)
        X = np.random.randn(30, 2)
        y = np.array([0] * 10 + [1] * 10 + [2] * 10)

        knn = KNNClassifier(k=1, distance_metric="euclidean")
        knn.fit(X, y)
        predictions = knn.predict(X)

        np.testing.assert_array_equal(
            predictions, y,
            "k=1 should perfectly memorize training data",
        )

    # ------------------------------------------------------------------
    # 3. Euclidean distance works
    # ------------------------------------------------------------------
    def test_euclidean_distance(self):
        """Euclidean metric should classify based on L2 distance."""
        X_train = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [10.0, 10.0]])
        y_train = np.array([0, 0, 0, 1])

        knn = KNNClassifier(k=3, distance_metric="euclidean")
        knn.fit(X_train, y_train)

        # Point near the cluster of 0s
        pred = knn.predict(np.array([[0.5, 0.5]]))
        self.assertEqual(pred[0], 0)

        # Point near the isolated 1
        pred = knn.predict(np.array([[9.5, 9.5]]))
        self.assertEqual(pred[0], 1)

    # ------------------------------------------------------------------
    # 4. Manhattan distance works
    # ------------------------------------------------------------------
    def test_manhattan_distance(self):
        """Manhattan metric should classify based on L1 distance."""
        X_train = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [10.0, 10.0]])
        y_train = np.array([0, 0, 0, 1])

        knn = KNNClassifier(k=3, distance_metric="manhattan")
        knn.fit(X_train, y_train)

        pred = knn.predict(np.array([[0.5, 0.5]]))
        self.assertEqual(pred[0], 0)

        pred = knn.predict(np.array([[9.5, 9.5]]))
        self.assertEqual(pred[0], 1)

    # ------------------------------------------------------------------
    # 5. Multi-class (3+ classes) classification
    # ------------------------------------------------------------------
    def test_multi_class(self):
        """KNN should handle 3 or more classes correctly."""
        np.random.seed(42)
        X_train = np.vstack([
            np.random.randn(30, 2) + [0, 0],     # class 0
            np.random.randn(30, 2) + [10, 0],     # class 1
            np.random.randn(30, 2) + [5, 10],     # class 2
        ])
        y_train = np.array([0] * 30 + [1] * 30 + [2] * 30)

        knn = KNNClassifier(k=5, distance_metric="euclidean")
        knn.fit(X_train, y_train)

        X_test = np.array([[0.0, 0.0], [10.0, 0.0], [5.0, 10.0]])
        predictions = knn.predict(X_test)

        self.assertEqual(predictions[0], 0)
        self.assertEqual(predictions[1], 1)
        self.assertEqual(predictions[2], 2)

    # ------------------------------------------------------------------
    # 6. score() returns correct accuracy
    # ------------------------------------------------------------------
    def test_score_returns_correct_accuracy(self):
        """score() should return the fraction of correct predictions."""
        X_train = np.array([[0.0, 0.0], [1.0, 0.0], [10.0, 10.0], [11.0, 10.0]])
        y_train = np.array([0, 0, 1, 1])

        knn = KNNClassifier(k=1, distance_metric="euclidean")
        knn.fit(X_train, y_train)

        # Test on training data -- should be 100%
        accuracy = knn.score(X_train, y_train)
        self.assertAlmostEqual(accuracy, 1.0)

        # Test with some wrong predictions
        X_test = np.array([[0.5, 0.0], [10.5, 10.0]])
        y_test = np.array([0, 1])
        accuracy = knn.score(X_test, y_test)
        self.assertAlmostEqual(accuracy, 1.0)

    def test_score_partial_accuracy(self):
        """score() should correctly report partial accuracy."""
        X_train = np.array([[0.0, 0.0], [10.0, 10.0]])
        y_train = np.array([0, 1])

        knn = KNNClassifier(k=1, distance_metric="euclidean")
        knn.fit(X_train, y_train)

        # Deliberately provide wrong labels for half
        X_test = np.array([[0.0, 0.0], [10.0, 10.0]])
        y_test_half_wrong = np.array([0, 0])  # second label is wrong
        accuracy = knn.score(X_test, y_test_half_wrong)
        self.assertAlmostEqual(accuracy, 0.5)

    # ------------------------------------------------------------------
    # 7. predict() returns correct shape (numpy array)
    # ------------------------------------------------------------------
    def test_predict_returns_numpy_array(self):
        """predict() should return a numpy array of the right shape."""
        X_train = np.array([[0.0], [1.0], [2.0]])
        y_train = np.array([0, 0, 1])

        knn = KNNClassifier(k=1, distance_metric="euclidean")
        knn.fit(X_train, y_train)

        X_test = np.array([[0.5], [1.5], [0.1], [2.1]])
        result = knn.predict(X_test)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (4,))

    # ------------------------------------------------------------------
    # 8. Different k values affect results
    # ------------------------------------------------------------------
    def test_different_k_values(self):
        """Different k values can produce different predictions for
        ambiguous points."""
        # Set up a scenario where k matters:
        # 1 nearest is class 1, but 3 nearest are majority class 0
        X_train = np.array([
            [0.0, 0.0],   # class 1 (nearest to query)
            [1.0, 0.0],   # class 0
            [1.0, 1.0],   # class 0
            [0.0, 1.0],   # class 0
            [10.0, 10.0], # class 1 (far away)
        ])
        y_train = np.array([1, 0, 0, 0, 1])

        query = np.array([[0.1, 0.1]])

        # k=1: nearest is (0,0) with label 1
        knn_k1 = KNNClassifier(k=1, distance_metric="euclidean")
        knn_k1.fit(X_train, y_train)
        pred_k1 = knn_k1.predict(query)
        self.assertEqual(pred_k1[0], 1)

        # k=3: 3 nearest are (0,0), (1,0), (0,1) with labels [1, 0, 0]
        # Majority vote -> class 0
        knn_k3 = KNNClassifier(k=3, distance_metric="euclidean")
        knn_k3.fit(X_train, y_train)
        pred_k3 = knn_k3.predict(query)
        self.assertEqual(pred_k3[0], 0)


if __name__ == "__main__":
    unittest.main()
