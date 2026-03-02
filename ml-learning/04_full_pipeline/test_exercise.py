"""
Tests for Exercise 4: The Full ML Pipeline.

Run with:
    python -m unittest 04_full_pipeline.test_exercise -v
"""

import unittest
import numpy as np
from sklearn.pipeline import Pipeline
from .exercise import (
    load_data,
    eda,
    preprocess,
    build_pipeline,
    evaluate_pipeline,
    run_experiment,
    summarize_findings,
)
from sklearn.linear_model import LinearRegression


class TestFullPipeline(unittest.TestCase):
    """Tests for the full pipeline exercise."""

    @classmethod
    def setUpClass(cls):
        cls.df = load_data()

    # ------------------------------------------------------------------
    # 1. EDA
    # ------------------------------------------------------------------

    def test_eda_summary_complete(self):
        """EDA summary should have all required keys filled in."""
        summary = eda(self.df)
        for key in ['n_rows', 'n_cols', 'missing_cols', 'categorical_cols', 'target_mean']:
            self.assertIn(key, summary, f"Missing key: {key}")
            self.assertIsNotNone(summary[key], f"'{key}' is None")

    def test_eda_correct_shape(self):
        """EDA should report correct row and column counts."""
        summary = eda(self.df)
        self.assertEqual(summary['n_rows'], 200)
        self.assertEqual(summary['n_cols'], 8)

    def test_eda_finds_missing_cols(self):
        """EDA should identify columns with missing values."""
        summary = eda(self.df)
        self.assertIsNotNone(summary['missing_cols'])
        self.assertGreater(len(summary['missing_cols']), 0,
                           "Should find at least one column with missing values")

    def test_eda_finds_categorical_cols(self):
        """EDA should identify categorical columns."""
        summary = eda(self.df)
        self.assertIsNotNone(summary['categorical_cols'])
        self.assertGreater(len(summary['categorical_cols']), 0,
                           "Should find at least one categorical column")

    # ------------------------------------------------------------------
    # 2. Preprocessing
    # ------------------------------------------------------------------

    def test_preprocess_returns_X_and_y(self):
        """preprocess() should return (X, y) tuple."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X, "X is None")
        self.assertIsNotNone(y, "y is None")

    def test_preprocess_no_missing(self):
        """Preprocessed features should have no missing values."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        self.assertFalse(X.isnull().any().any(),
                         "X still has missing values after preprocessing")

    def test_preprocess_all_numeric(self):
        """Preprocessed features should be all numeric."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        object_cols = X.select_dtypes(include='object').columns
        self.assertEqual(len(object_cols), 0,
                         f"Non-numeric columns remain: {list(object_cols)}")

    def test_preprocess_target_not_in_features(self):
        """Target 'rentals' should not be in the feature set."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        self.assertNotIn('rentals', X.columns,
                         "'rentals' should be the target, not a feature")

    # ------------------------------------------------------------------
    # 3. Pipeline
    # ------------------------------------------------------------------

    def test_build_pipeline_is_pipeline(self):
        """build_pipeline() should return an sklearn Pipeline."""
        pipe = build_pipeline(LinearRegression())
        self.assertIsNotNone(pipe, "build_pipeline returned None")
        self.assertIsInstance(pipe, Pipeline)

    def test_build_pipeline_has_scaler_and_model(self):
        """Pipeline should have a scaler step and a model step."""
        pipe = build_pipeline(LinearRegression())
        self.assertIsNotNone(pipe)
        step_names = [name for name, _ in pipe.steps]
        self.assertIn('scaler', step_names, "Pipeline should have a 'scaler' step")
        self.assertIn('model', step_names, "Pipeline should have a 'model' step")

    # ------------------------------------------------------------------
    # 4. Evaluation
    # ------------------------------------------------------------------

    def test_evaluate_pipeline_returns_scores(self):
        """evaluate_pipeline should return CV scores."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        pipe = build_pipeline(LinearRegression())
        self.assertIsNotNone(pipe)
        result = evaluate_pipeline(pipe, X, y)
        self.assertIsNotNone(result['cv_scores'], "cv_scores is None")
        self.assertEqual(len(result['cv_scores']), 5, "Should have 5 CV fold scores")
        self.assertIsNotNone(result['mean_score'])

    # ------------------------------------------------------------------
    # 5. Experimentation
    # ------------------------------------------------------------------

    def test_run_experiment_multiple_configs(self):
        """Should try at least 2 different configurations."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        results = run_experiment(X, y)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 2,
                                "Should try at least 2 model configurations")

    def test_run_experiment_has_required_keys(self):
        """Each result should have name, mean_score, and std_score."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        results = run_experiment(X, y)
        for r in results:
            self.assertIn('name', r)
            self.assertIn('mean_score', r)
            self.assertIn('std_score', r)
            self.assertIsNotNone(r['mean_score'],
                                 f"mean_score is None for '{r.get('name')}'")

    def test_run_experiment_reasonable_performance(self):
        """At least one model should achieve R2 > 0.3."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        results = run_experiment(X, y)
        best_score = max(r['mean_score'] for r in results if r['mean_score'] is not None)
        self.assertGreater(best_score, 0.3,
                           f"Best R2 was {best_score:.3f} - expected > 0.3")

    # ------------------------------------------------------------------
    # 6. Summary
    # ------------------------------------------------------------------

    def test_summarize_findings_non_empty(self):
        """Summary should be a non-empty string."""
        X, y = preprocess(self.df)
        self.assertIsNotNone(X)
        results = run_experiment(X, y)
        summary = summarize_findings(results)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 10,
                           "Summary should describe your findings (not just a few characters)")


if __name__ == "__main__":
    unittest.main()
