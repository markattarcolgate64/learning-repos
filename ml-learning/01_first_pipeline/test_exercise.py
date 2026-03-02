"""
Tests for Exercise 1: Your First ML Pipeline.

Run with:
    python -m unittest 01_first_pipeline.test_exercise -v
"""

import unittest
import numpy as np
from .exercise import (
    load_data,
    separate_features_target,
    split_data,
    train_model,
    evaluate_model,
    check_overfitting,
)


class TestFirstPipeline(unittest.TestCase):
    """Tests for the first ML pipeline exercise."""

    # ------------------------------------------------------------------
    # 1. Data loading
    # ------------------------------------------------------------------

    def test_load_data_returns_dataframe(self):
        """load_data() should return a pandas DataFrame."""
        df = load_data()
        self.assertIsNotNone(df, "load_data() returned None - did you implement it?")
        self.assertEqual(type(df).__name__, "DataFrame")

    def test_load_data_correct_shape(self):
        """Dataset should have 200 rows and 6 columns."""
        df = load_data()
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (200, 6))

    def test_load_data_correct_columns(self):
        """Dataset should have the expected column names."""
        df = load_data()
        self.assertIsNotNone(df)
        expected = {"study_hours", "attendance_rate", "previous_gpa",
                    "sleep_hours", "practice_tests", "passed"}
        self.assertEqual(set(df.columns), expected)

    # ------------------------------------------------------------------
    # 2. Feature/target separation
    # ------------------------------------------------------------------

    def test_separate_features_target(self):
        """X should have 5 feature columns, y should be the 'passed' column."""
        df = load_data()
        self.assertIsNotNone(df)
        X, y = separate_features_target(df)
        self.assertIsNotNone(X, "X is None - did you implement separate_features_target()?")
        self.assertIsNotNone(y, "y is None - did you implement separate_features_target()?")
        self.assertEqual(X.shape[1], 5, "X should have 5 feature columns")
        self.assertEqual(len(y), 200, "y should have 200 values")
        self.assertNotIn("passed", X.columns, "X should NOT contain the target column 'passed'")

    # ------------------------------------------------------------------
    # 3. Train/test split
    # ------------------------------------------------------------------

    def test_split_data_sizes(self):
        """80/20 split of 200 rows should give 160 train and 40 test."""
        df = load_data()
        X, y = separate_features_target(df)
        self.assertIsNotNone(X)
        X_train, X_test, y_train, y_test = split_data(X, y)
        self.assertIsNotNone(X_train, "X_train is None - did you implement split_data()?")
        self.assertEqual(len(X_train), 160, "Training set should have 160 samples (80%)")
        self.assertEqual(len(X_test), 40, "Test set should have 40 samples (20%)")
        self.assertEqual(len(y_train), 160)
        self.assertEqual(len(y_test), 40)

    def test_split_data_no_overlap(self):
        """Training and test indices should not overlap."""
        df = load_data()
        X, y = separate_features_target(df)
        self.assertIsNotNone(X)
        X_train, X_test, y_train, y_test = split_data(X, y)
        self.assertIsNotNone(X_train)
        train_indices = set(X_train.index)
        test_indices = set(X_test.index)
        overlap = train_indices & test_indices
        self.assertEqual(len(overlap), 0, "Train and test sets should not share any rows!")

    # ------------------------------------------------------------------
    # 4. Model training
    # ------------------------------------------------------------------

    def test_train_model_returns_fitted_model(self):
        """train_model() should return a fitted DecisionTreeClassifier."""
        df = load_data()
        X, y = separate_features_target(df)
        X_train, X_test, y_train, y_test = split_data(X, y)
        self.assertIsNotNone(X_train)
        model = train_model(X_train, y_train)
        self.assertIsNotNone(model, "train_model() returned None - did you implement it?")
        self.assertEqual(type(model).__name__, "DecisionTreeClassifier")
        # Check the model has been fitted (has learned attributes)
        self.assertTrue(
            hasattr(model, "tree_"),
            "Model does not appear to be fitted. Did you call model.fit(X_train, y_train)?"
        )

    # ------------------------------------------------------------------
    # 5. Evaluation
    # ------------------------------------------------------------------

    def test_evaluate_model_accuracy(self):
        """Model should achieve at least 60% accuracy on the test set."""
        df = load_data()
        X, y = separate_features_target(df)
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        self.assertIsNotNone(model)
        predictions, accuracy = evaluate_model(model, X_test, y_test)
        self.assertIsNotNone(predictions, "predictions is None - did you implement evaluate_model()?")
        self.assertIsNotNone(accuracy, "accuracy is None - did you implement evaluate_model()?")
        self.assertEqual(len(predictions), len(y_test), "Should have one prediction per test sample")
        self.assertGreaterEqual(accuracy, 0.6, "Accuracy should be at least 60%")
        self.assertLessEqual(accuracy, 1.0, "Accuracy should be at most 100%")

    def test_predictions_are_binary(self):
        """Predictions should be 0 or 1 (binary classification)."""
        df = load_data()
        X, y = separate_features_target(df)
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        predictions, _ = evaluate_model(model, X_test, y_test)
        self.assertIsNotNone(predictions)
        unique_values = set(predictions)
        self.assertTrue(unique_values.issubset({0, 1}),
                        f"Predictions should be 0 or 1, got: {unique_values}")

    # ------------------------------------------------------------------
    # 6. Overfitting check
    # ------------------------------------------------------------------

    def test_check_overfitting_returns_accuracies(self):
        """check_overfitting() should return train and test accuracies."""
        df = load_data()
        X, y = separate_features_target(df)
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        self.assertIsNotNone(model)
        train_acc, test_acc = check_overfitting(model, X_train, y_train, X_test, y_test)
        self.assertIsNotNone(train_acc, "train_accuracy is None - did you implement check_overfitting()?")
        self.assertIsNotNone(test_acc, "test_accuracy is None - did you implement check_overfitting()?")
        self.assertGreaterEqual(train_acc, 0.0)
        self.assertLessEqual(train_acc, 1.0)
        self.assertGreaterEqual(test_acc, 0.0)
        self.assertLessEqual(test_acc, 1.0)

    def test_train_accuracy_at_least_as_high(self):
        """Training accuracy should typically be >= test accuracy for a decision tree."""
        df = load_data()
        X, y = separate_features_target(df)
        X_train, X_test, y_train, y_test = split_data(X, y)
        model = train_model(X_train, y_train)
        train_acc, test_acc = check_overfitting(model, X_train, y_train, X_test, y_test)
        self.assertIsNotNone(train_acc)
        # Decision trees typically overfit (train acc near 100%)
        self.assertGreaterEqual(train_acc, test_acc,
                                "Training accuracy should be >= test accuracy for a decision tree")


if __name__ == "__main__":
    unittest.main()
