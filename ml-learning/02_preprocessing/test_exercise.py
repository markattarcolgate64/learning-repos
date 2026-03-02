"""
Tests for Exercise 2: Data Preprocessing and Feature Engineering.

Run with:
    python -m unittest 02_preprocessing.test_exercise -v
"""

import unittest
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from .exercise import (
    load_data,
    handle_missing_values,
    encode_categoricals,
    engineer_features,
    scale_features,
    train_and_evaluate,
)


class TestPreprocessing(unittest.TestCase):
    """Tests for the preprocessing exercise."""

    @classmethod
    def setUpClass(cls):
        """Load data once for all tests."""
        cls.df = load_data()

    # ------------------------------------------------------------------
    # 1. Missing values
    # ------------------------------------------------------------------

    def test_handle_missing_values_no_nans(self):
        """After handling missing values, no NaN should remain in numeric columns."""
        df_clean = handle_missing_values(self.df)
        numeric_nulls = df_clean.select_dtypes(include=np.number).isnull().sum().sum()
        self.assertEqual(numeric_nulls, 0,
                         "There are still NaN values in numeric columns")

    def test_handle_missing_values_preserves_shape(self):
        """Handling missing values should not change the number of rows."""
        df_clean = handle_missing_values(self.df)
        self.assertEqual(len(df_clean), len(self.df),
                         "Row count changed - you should fill values, not drop rows")

    def test_handle_missing_values_does_not_modify_original(self):
        """Original DataFrame should not be modified."""
        original_nulls = self.df.isnull().sum().sum()
        handle_missing_values(self.df)
        self.assertEqual(self.df.isnull().sum().sum(), original_nulls,
                         "Original DataFrame was modified - make sure to use df.copy()")

    # ------------------------------------------------------------------
    # 2. Categorical encoding
    # ------------------------------------------------------------------

    def test_encode_categoricals_all_numeric(self):
        """After encoding, all columns should be numeric."""
        df_clean = handle_missing_values(self.df)
        df_encoded = encode_categoricals(df_clean)
        object_cols = df_encoded.select_dtypes(include='object').columns
        self.assertEqual(len(object_cols), 0,
                         f"Still have non-numeric columns: {list(object_cols)}")

    def test_encode_categoricals_has_dummy_columns(self):
        """One-hot encoding should create new columns for categories."""
        df_clean = handle_missing_values(self.df)
        df_encoded = encode_categoricals(df_clean)
        # Should have more columns than original (dummies replace text columns)
        self.assertGreater(len(df_encoded.columns), 7,
                           "Expected new dummy columns after encoding")

    def test_encode_categoricals_does_not_modify_original(self):
        """Original DataFrame should not be modified."""
        df_clean = handle_missing_values(self.df)
        orig_cols = list(df_clean.columns)
        encode_categoricals(df_clean)
        self.assertEqual(list(df_clean.columns), orig_cols)

    # ------------------------------------------------------------------
    # 3. Feature engineering
    # ------------------------------------------------------------------

    def test_engineer_features_age(self):
        """Should create an 'age' column = 2024 - year_built."""
        df_eng = engineer_features(self.df)
        self.assertIn('age', df_eng.columns, "Missing 'age' column")
        # Check a value: if year_built=2000, age should be 24
        sample = df_eng[df_eng['year_built'] == df_eng['year_built'].iloc[0]]
        expected_age = 2024 - sample['year_built'].iloc[0]
        self.assertEqual(sample['age'].iloc[0], expected_age)

    def test_engineer_features_sqft_per_bedroom(self):
        """Should create 'sqft_per_bedroom' = square_feet / num_bedrooms."""
        df_eng = engineer_features(self.df)
        self.assertIn('sqft_per_bedroom', df_eng.columns,
                       "Missing 'sqft_per_bedroom' column")
        # Verify calculation
        sample = df_eng.iloc[0]
        expected = sample['square_feet'] / sample['num_bedrooms']
        self.assertAlmostEqual(sample['sqft_per_bedroom'], expected, places=2)

    # ------------------------------------------------------------------
    # 4. Feature scaling
    # ------------------------------------------------------------------

    def test_scale_features_train_centered(self):
        """Scaled training features should have mean ~0."""
        df_clean = handle_missing_values(self.df)
        df_eng = engineer_features(df_clean)
        df_encoded = encode_categoricals(df_eng)
        X = df_encoded.drop(columns=['price'])
        y = df_encoded['price']
        X_train, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_s, X_test_s, scaler = scale_features(X_train, X_test)
        self.assertIsNotNone(X_train_s, "X_train_scaled is None")
        self.assertIsNotNone(scaler, "scaler is None")
        means = np.mean(X_train_s, axis=0)
        np.testing.assert_allclose(means, 0, atol=0.1,
                                   err_msg="Scaled training data mean should be ~0")

    def test_scale_features_train_unit_std(self):
        """Scaled training features should have std ~1."""
        df_clean = handle_missing_values(self.df)
        df_eng = engineer_features(df_clean)
        df_encoded = encode_categoricals(df_eng)
        X = df_encoded.drop(columns=['price'])
        y = df_encoded['price']
        X_train, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_s, _, _ = scale_features(X_train, X_test)
        stds = np.std(X_train_s, axis=0)
        # Some binary columns will have std != 1, that's fine. Check most columns.
        close_to_one = np.sum(np.abs(stds - 1.0) < 0.15)
        self.assertGreater(close_to_one, 3,
                           "At least some scaled features should have std ~1")

    def test_scale_features_no_data_leakage(self):
        """Scaler should be fitted on training data only (not test data)."""
        df_clean = handle_missing_values(self.df)
        df_eng = engineer_features(df_clean)
        df_encoded = encode_categoricals(df_eng)
        X = df_encoded.drop(columns=['price'])
        y = df_encoded['price']
        X_train, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        _, _, scaler = scale_features(X_train, X_test)
        self.assertIsNotNone(scaler)
        # The scaler's mean_ should match the training data's mean
        np.testing.assert_allclose(scaler.mean_, X_train.mean().values, atol=0.01,
                                   err_msg="Scaler appears fitted on wrong data (data leakage?)")

    # ------------------------------------------------------------------
    # 5. Training and evaluation
    # ------------------------------------------------------------------

    def test_train_and_evaluate_r2(self):
        """Model should achieve reasonable R-squared on test data."""
        df_clean = handle_missing_values(self.df)
        df_eng = engineer_features(df_clean)
        df_encoded = encode_categoricals(df_eng)
        X = df_encoded.drop(columns=['price'])
        y = df_encoded['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_s, X_test_s, _ = scale_features(X_train, X_test)

        model, mse, r2 = train_and_evaluate(X_train_s, X_test_s, y_train, y_test)
        self.assertIsNotNone(model, "model is None")
        self.assertIsNotNone(r2, "r2 is None")
        self.assertGreater(r2, 0.5, f"R-squared ({r2:.3f}) should be > 0.5")

    def test_train_and_evaluate_model_type(self):
        """Should use LinearRegression."""
        df_clean = handle_missing_values(self.df)
        df_eng = engineer_features(df_clean)
        df_encoded = encode_categoricals(df_eng)
        X = df_encoded.drop(columns=['price'])
        y = df_encoded['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_s, X_test_s, _ = scale_features(X_train, X_test)

        model, _, _ = train_and_evaluate(X_train_s, X_test_s, y_train, y_test)
        self.assertEqual(type(model).__name__, "LinearRegression")


if __name__ == "__main__":
    unittest.main()
