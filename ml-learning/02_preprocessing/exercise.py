"""
Data Preprocessing and Feature Engineering
===========================================
Difficulty : ** (2/5)

Real-world data is messy. Before any model can learn, you need to:
  1. Handle missing values
  2. Encode categorical variables (text -> numbers)
  3. Scale features to similar ranges
  4. Engineer useful new features from existing ones

This exercise teaches WHY each step matters and HOW to do it right.

THE CRITICAL CONCEPT: Data leakage.
When you scale or impute, you must fit on the training data ONLY, then
transform both train and test. If you fit on all the data (including test),
information from the test set "leaks" into your training process, giving
you an unrealistically optimistic estimate of model performance.

Dataset: Housing prices (predict price from house features)
Task: Regression

Run:
    python 02_preprocessing/exercise.py

Test:
    python -m unittest 02_preprocessing.test_exercise -v
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "housing_prices.csv")


# ============================================================
# PART 1: Load and Explore the Mess
# ============================================================
# Before preprocessing, you need to UNDERSTAND what's wrong with
# the data. This part is given to you - read the output carefully.

def load_data():
    """Load the housing prices dataset."""
    df = pd.read_csv(DATA_PATH)
    return df


def explore_mess(df):
    """Show what's wrong with this dataset. (GIVEN - just read the output)"""
    print("=" * 60)
    print("EXPLORING THE DATA")
    print("=" * 60)

    print(f"\nShape: {df.shape}")
    print(f"\nColumn types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDescribe (numeric only):\n{df.describe()}")
    print(f"\nCategorical columns:")
    for col in df.select_dtypes(include='object').columns:
        print(f"  {col}: {df[col].unique()}")

    print("\n--- PROBLEMS TO FIX ---")
    print(f"1. Missing values in: {list(df.columns[df.isnull().any()])}")
    print(f"2. Categorical (text) columns: {list(df.select_dtypes(include='object').columns)}")
    print(f"3. Scale differences: square_feet ranges {df['square_feet'].min()}-{df['square_feet'].max()}")
    print(f"   but num_bedrooms ranges {df['num_bedrooms'].min()}-{df['num_bedrooms'].max()}")


# ============================================================
# PART 2: Handle Missing Values
# ============================================================
# Missing values (NaN) will crash most ML models. You need to
# either remove rows with missing data or fill them in (impute).
#
# Common strategies:
#   - Fill with the median (robust to outliers)
#   - Fill with the mean (for normal distributions)
#   - Fill with the mode (for categorical data)
#   - Drop rows (only if you have LOTS of data and few missing)
#
# We'll use the median for numeric columns.

def handle_missing_values(df):
    """Fill missing values in numeric columns with the column median.

    Args:
        df: DataFrame with potential missing values.

    Returns:
        DataFrame with no missing values in numeric columns.
    """
    df = df.copy()

    # TODO: For each numeric column that has missing values, fill NaNs with the median
    # Hint: For a column like 'garage_spaces':
    #       df['garage_spaces'] = df['garage_spaces'].fillna(df['garage_spaces'].median())
    #
    # You can loop over numeric columns or do them individually.
    # The columns with missing values are 'lot_size' and 'garage_spaces'.

    # Your code here

    return df


# ============================================================
# PART 3: Encode Categorical Variables
# ============================================================
# ML models need numbers, not strings. We need to convert categorical
# columns like 'neighborhood' ("downtown", "suburbs", "rural") into numbers.
#
# The standard approach is ONE-HOT ENCODING:
#   "neighborhood" -> "neighborhood_downtown", "neighborhood_suburbs", "neighborhood_rural"
#   Each becomes a 0/1 column.
#
# Why not just use 1, 2, 3? Because that implies an ordering
# (3 > 2 > 1), which doesn't exist for categories like neighborhoods.

def encode_categoricals(df):
    """Convert categorical columns to numeric using one-hot encoding.

    Args:
        df: DataFrame with categorical columns ('neighborhood', 'condition').

    Returns:
        DataFrame where all columns are numeric.
    """
    # TODO: Use pd.get_dummies() to one-hot encode categorical columns
    # Hint: df = pd.get_dummies(df, columns=['neighborhood', 'condition'], drop_first=True)
    #
    # drop_first=True drops one category per column to avoid redundancy.
    # Example: if neighborhood has 3 values, you only need 2 dummy columns
    # (if both are 0, it must be the third category).

    df = df.copy()
    # Your code here

    return df


# ============================================================
# PART 4: Feature Engineering
# ============================================================
# Sometimes the raw features aren't the best predictors.
# You can CREATE new features that capture useful information.
#
# Example: "year_built" alone is less useful than "age" (current year - year_built).
# Example: "square_feet / num_bedrooms" tells you how spacious each bedroom is.

def engineer_features(df):
    """Create new features from existing columns.

    Args:
        df: DataFrame with the original columns.

    Returns:
        DataFrame with new engineered features added.
    """
    df = df.copy()

    # TODO: Create an 'age' feature: 2024 - year_built
    # Hint: df['age'] = 2024 - df['year_built']
    # Your code here

    # TODO: Create a 'sqft_per_bedroom' feature: square_feet / num_bedrooms
    # Hint: df['sqft_per_bedroom'] = df['square_feet'] / df['num_bedrooms']
    # Your code here

    return df


# ============================================================
# PART 5: Feature Scaling (THE DATA LEAKAGE LESSON)
# ============================================================
# Many ML algorithms work better when all features are on the same scale.
# StandardScaler transforms each feature to have mean=0 and std=1.
#
# THE CRITICAL RULE:
#   scaler.fit(X_train)       <-- learn mean/std from TRAINING data only
#   X_train = scaler.transform(X_train)  <-- transform training data
#   X_test = scaler.transform(X_test)    <-- transform test data using SAME stats
#
# WHY? If you fit on all data (including test), the scaler "sees" the test
# data's distribution. This is DATA LEAKAGE - your model indirectly has
# information about the test set, making your evaluation unrealistically good.

def scale_features(X_train, X_test):
    """Scale features using StandardScaler, fitted on training data only.

    Args:
        X_train: Training features (DataFrame or array).
        X_test: Test features (DataFrame or array).

    Returns:
        A tuple (X_train_scaled, X_test_scaled, scaler).
    """
    # TODO: Create a StandardScaler
    # Hint: scaler = StandardScaler()
    scaler = None  # Your code here

    # TODO: Fit the scaler on X_train ONLY, then transform X_train
    # Hint: X_train_scaled = scaler.fit_transform(X_train)
    X_train_scaled = None  # Your code here

    # TODO: Transform X_test using the SAME scaler (do NOT fit again!)
    # Hint: X_test_scaled = scaler.transform(X_test)
    X_test_scaled = None  # Your code here

    return X_train_scaled, X_test_scaled, scaler


# ============================================================
# PART 6: Train and Evaluate
# ============================================================
# Now we put it all together: preprocess, then train a simple linear
# regression model and evaluate it.

def train_and_evaluate(X_train, X_test, y_train, y_test):
    """Train a LinearRegression model and evaluate it.

    Args:
        X_train: Preprocessed training features.
        X_test: Preprocessed test features.
        y_train: Training target.
        y_test: Test target.

    Returns:
        A tuple (model, mse, r2) where:
        - model is the trained LinearRegression
        - mse is the mean squared error on the test set
        - r2 is the R-squared score on the test set
    """
    # TODO: Create and train a LinearRegression model
    # Hint: model = LinearRegression()
    #       model.fit(X_train, y_train)
    model = None  # Your code here

    # TODO: Make predictions on the test set
    # Hint: predictions = model.predict(X_test)
    predictions = None  # Your code here

    # TODO: Compute Mean Squared Error
    # Hint: mse = mean_squared_error(y_test, predictions)
    mse = None  # Your code here

    # TODO: Compute R-squared score
    # R-squared = 1 means perfect predictions
    # R-squared = 0 means no better than predicting the mean
    # Hint: r2 = r2_score(y_test, predictions)
    r2 = None  # Your code here

    return model, mse, r2


# ============================================================
# Run the full preprocessing pipeline
# ============================================================
if __name__ == "__main__":
    # Load and explore
    print("\n--- PART 1: Loading Data ---")
    df = load_data()
    explore_mess(df)

    # Handle missing values
    print("\n\n--- PART 2: Handling Missing Values ---")
    df = handle_missing_values(df)
    remaining_nulls = df.isnull().sum().sum()
    print(f"Missing values remaining: {remaining_nulls}")
    if remaining_nulls > 0:
        print("Still have missing values! Check your implementation.")

    # Feature engineering (before encoding, since we need year_built)
    print("\n--- PART 4: Feature Engineering ---")
    df = engineer_features(df)
    if 'age' in df.columns:
        print(f"Created 'age': range {df['age'].min()}-{df['age'].max()}")
    if 'sqft_per_bedroom' in df.columns:
        print(f"Created 'sqft_per_bedroom': mean {df['sqft_per_bedroom'].mean():.0f}")

    # Encode categoricals
    print("\n--- PART 3: Encoding Categoricals ---")
    df = encode_categoricals(df)
    object_cols = df.select_dtypes(include='object').columns
    print(f"Remaining text columns: {list(object_cols)}")
    if len(object_cols) > 0:
        print("Still have categorical columns! Check your implementation.")
    else:
        print(f"All columns now numeric: {list(df.columns)}")

    # Separate features and target, then split
    X = df.drop(columns=["price"])
    y = df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    print("\n--- PART 5: Scaling Features ---")
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    if X_train_scaled is not None:
        print(f"Training features mean (should be ~0): {np.mean(X_train_scaled, axis=0)[:3].round(2)}")
        print(f"Training features std (should be ~1): {np.std(X_train_scaled, axis=0)[:3].round(2)}")
    else:
        print("TODO: Implement scale_features()")

    # Train and evaluate
    print("\n--- PART 6: Training and Evaluating ---")
    if X_train_scaled is not None:
        model, mse, r2 = train_and_evaluate(X_train_scaled, X_test_scaled, y_train, y_test)
        if r2 is not None:
            print(f"Mean Squared Error: {mse:.2f}")
            print(f"R-squared: {r2:.4f}")
            if r2 > 0.5:
                print("Good! Model explains >50% of price variance.")
            else:
                print("Model could be better. Try different features?")
        else:
            print("TODO: Implement train_and_evaluate()")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 02_preprocessing.test_exercise -v")
    print("=" * 60)
