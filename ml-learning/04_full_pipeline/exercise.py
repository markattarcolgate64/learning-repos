"""
The Full ML Pipeline
====================
Difficulty : *** (3/5)

This is the capstone for the sklearn exercises. You'll do everything
end-to-end on a new dataset:
  EDA -> Preprocess -> Feature Engineer -> Model -> Evaluate -> Iterate

Less hand-holding this time. You've learned the tools in exercises 1-3.
Now you'll make DECISIONS about what to do, not just how to do it.

New concept: sklearn's Pipeline, which chains preprocessing and modeling
into a single, clean, reproducible object.

Dataset: Daily bike rental counts with weather and calendar features.
Task: Predict how many bikes will be rented on a given day (regression).

Run:
    python 04_full_pipeline/exercise.py

Test:
    python -m unittest 04_full_pipeline.test_exercise -v
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "bike_rentals.csv")


# ============================================================
# PART 1: Exploratory Data Analysis (EDA)
# ============================================================
# ALWAYS look at your data before modeling. EDA helps you:
#   - Spot problems (missing values, outliers, wrong types)
#   - Understand feature distributions
#   - Find relationships between features and target
#   - Decide what preprocessing to do

def load_data():
    """Load the bike rentals dataset."""
    return pd.read_csv(DATA_PATH)


def eda(df):
    """Perform exploratory data analysis and return a summary dict.

    Look at the data. Understand it. Then fill in the summary.

    Args:
        df: The bike rentals DataFrame.

    Returns:
        A dict with keys:
        - 'n_rows': number of rows
        - 'n_cols': number of columns
        - 'missing_cols': list of column names that have missing values
        - 'categorical_cols': list of column names with string/object dtype
        - 'target_mean': mean value of the 'rentals' column
    """
    summary = {}

    # TODO: Fill in the summary dict
    # Hint: summary['n_rows'] = len(df)  or  df.shape[0]
    # Hint: summary['n_cols'] = df.shape[1]
    # Hint: summary['missing_cols'] = list(df.columns[df.isnull().any()])
    # Hint: summary['categorical_cols'] = list(df.select_dtypes(include='object').columns)
    # Hint: summary['target_mean'] = df['rentals'].mean()

    summary['n_rows'] = None  # Your code here
    summary['n_cols'] = None  # Your code here
    summary['missing_cols'] = None  # Your code here
    summary['categorical_cols'] = None  # Your code here
    summary['target_mean'] = None  # Your code here

    return summary


# ============================================================
# PART 2: Preprocessing
# ============================================================
# Based on your EDA, you need to:
#   1. Handle missing values
#   2. Encode categorical variables
#   3. Separate features and target
#
# This time, do all preprocessing in one function.

def preprocess(df):
    """Clean the data: handle missing values and encode categoricals.

    Args:
        df: Raw DataFrame.

    Returns:
        A tuple (X, y) where X is a fully numeric DataFrame and
        y is the target Series.
    """
    df = df.copy()

    # TODO: Fill missing values in numeric columns with the median
    # Hint: Look at your EDA results to know which columns have NaN
    #       For each such column: df[col] = df[col].fillna(df[col].median())
    # Your code here

    # TODO: One-hot encode categorical columns
    # Hint: df = pd.get_dummies(df, columns=['season', 'weather'], drop_first=True)
    # Your code here

    # TODO: Separate features (X) and target (y)
    # Hint: y = df['rentals']
    #       X = df.drop(columns=['rentals'])
    X = None  # Your code here
    y = None  # Your code here

    return X, y


# ============================================================
# PART 3: Build a Pipeline
# ============================================================
# An sklearn Pipeline chains preprocessing steps and a model together.
# Why use a Pipeline?
#   1. Cleaner code (one object does everything)
#   2. No data leakage (scaling is handled correctly in CV)
#   3. Easy to swap models or preprocessors
#
# Pipeline([
#     ('scaler', StandardScaler()),     # Step 1: scale features
#     ('model', LinearRegression()),    # Step 2: train model
# ])
#
# When you call pipeline.fit(X, y), it fits the scaler on X,
# transforms X, then fits the model. When you call pipeline.predict(X),
# it transforms X with the fitted scaler, then predicts.

def build_pipeline(model):
    """Build a Pipeline with StandardScaler and the given model.

    Args:
        model: An sklearn regressor (e.g., LinearRegression()).

    Returns:
        An sklearn Pipeline with two steps: 'scaler' and 'model'.
    """
    # TODO: Create a Pipeline with a StandardScaler and the model
    # Hint: pipe = Pipeline([
    #           ('scaler', StandardScaler()),
    #           ('model', model),
    #       ])
    pipe = None  # Your code here

    return pipe


# ============================================================
# PART 4: Train and Evaluate with Cross-Validation
# ============================================================
# Use cross-validation to get a reliable estimate of performance.
# For regression, we'll use R-squared as our metric.

def evaluate_pipeline(pipeline, X, y, cv=5):
    """Evaluate a pipeline using cross-validation.

    Args:
        pipeline: An sklearn Pipeline.
        X: Feature DataFrame/array.
        y: Target Series/array.
        cv: Number of cross-validation folds.

    Returns:
        A dict with keys:
        - 'cv_scores': array of per-fold R-squared scores
        - 'mean_score': mean R-squared across folds
        - 'std_score': std of R-squared across folds
    """
    # TODO: Run cross-validation with scoring='r2'
    # Hint: scores = cross_val_score(pipeline, X, y, cv=cv, scoring='r2')
    scores = None  # Your code here

    if scores is not None:
        return {
            'cv_scores': scores,
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
        }
    return {'cv_scores': None, 'mean_score': None, 'std_score': None}


# ============================================================
# PART 5: Iterate - Try Multiple Configurations
# ============================================================
# The power of ML is iteration. Try different models, compare results,
# pick the best one. A Pipeline makes this easy to swap.

def run_experiment(X, y):
    """Try multiple model configurations and return results.

    Args:
        X: Feature DataFrame/array.
        y: Target Series/array.

    Returns:
        A list of dicts, each with keys:
        - 'name': descriptive name of the configuration
        - 'mean_score': mean CV R-squared
        - 'std_score': std of CV R-squared
        The list should have at least 2 entries.
    """
    results = []

    # TODO: Try at least 2 different models. For each one:
    #   1. Build a pipeline with build_pipeline(model)
    #   2. Evaluate it with evaluate_pipeline(pipeline, X, y)
    #   3. Append a result dict to the results list
    #
    # Example configuration 1: LinearRegression
    # Example configuration 2: Ridge regression (Ridge(alpha=1.0))
    # Example configuration 3: DecisionTreeRegressor(random_state=42)
    # Example configuration 4: RandomForestRegressor(n_estimators=50, random_state=42)
    #
    # Hint:
    #   pipe = build_pipeline(LinearRegression())
    #   eval_result = evaluate_pipeline(pipe, X, y)
    #   results.append({
    #       'name': 'Linear Regression',
    #       'mean_score': eval_result['mean_score'],
    #       'std_score': eval_result['std_score'],
    #   })

    # Your code here

    return results


# ============================================================
# PART 6: Document Your Findings
# ============================================================
# A good ML practitioner documents what they tried and what they learned.

def summarize_findings(results):
    """Write a brief summary of your experiment.

    Args:
        results: The list of result dicts from run_experiment.

    Returns:
        A non-empty string summarizing which model worked best and why
        you think that is.
    """
    # TODO: Return a string summarizing your findings
    # Example: "Linear Regression achieved R2=0.75, while Ridge got R2=0.74.
    #           The best model was Linear Regression. The models performed
    #           similarly because the dataset is small and features are informative."
    #
    # There is no wrong answer here - just write what you observed!

    summary = ""  # Your summary here

    return summary


# ============================================================
# Run the full pipeline
# ============================================================
if __name__ == "__main__":
    # Part 1: EDA
    print("=" * 60)
    print("PART 1: Exploratory Data Analysis")
    print("=" * 60)
    df = load_data()
    summary = eda(df)
    if summary.get('n_rows') is not None:
        print(f"Rows: {summary['n_rows']}, Columns: {summary['n_cols']}")
        print(f"Missing value columns: {summary['missing_cols']}")
        print(f"Categorical columns: {summary['categorical_cols']}")
        print(f"Target mean: {summary['target_mean']:.1f} rentals/day")
    else:
        print("TODO: Implement eda()")

    # Part 2: Preprocess
    print("\n" + "=" * 60)
    print("PART 2: Preprocessing")
    print("=" * 60)
    X, y = preprocess(df)
    if X is not None:
        print(f"Features shape: {X.shape}")
        print(f"All numeric: {all(X.dtypes != 'object')}")
        print(f"Any NaN: {X.isnull().any().any()}")
    else:
        print("TODO: Implement preprocess()")

    # Parts 3-5: Pipeline, evaluate, iterate
    print("\n" + "=" * 60)
    print("PARTS 3-5: Build, Evaluate, Iterate")
    print("=" * 60)
    if X is not None:
        results = run_experiment(X, y)
        if results:
            print("\nExperiment Results:")
            print("-" * 50)
            for r in sorted(results, key=lambda x: x.get('mean_score', 0) or 0, reverse=True):
                score = r.get('mean_score')
                std = r.get('std_score')
                if score is not None:
                    print(f"  {r['name']:30s} R2 = {score:.3f} (+/- {std:.3f})")
        else:
            print("TODO: Implement run_experiment()")

        # Part 6: Summary
        print("\n" + "=" * 60)
        print("PART 6: Your Findings")
        print("=" * 60)
        findings = summarize_findings(results)
        if findings:
            print(f"\n{findings}")
        else:
            print("TODO: Write your findings in summarize_findings()")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 04_full_pipeline.test_exercise -v")
    print("=" * 60)
