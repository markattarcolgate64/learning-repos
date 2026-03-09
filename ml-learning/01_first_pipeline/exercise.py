"""
Your First ML Pipeline
======================
Difficulty : * (1/5)

You know the math behind ML. Now let's learn the WORKFLOW.

This exercise teaches the most fundamental ML pattern:
  Load data -> Split -> Train -> Predict -> Evaluate

We'll use scikit-learn (sklearn), the standard ML library that every
data scientist uses daily. The goal is NOT to understand the algorithm's
internals (you already did that with linear regression). The goal is to
learn the practical workflow of training a model end-to-end.

Dataset: Student performance (predict pass/fail from study habits)
Task: Binary classification

Run:
    python 01_first_pipeline/exercise.py

Test:
    python -m unittest 01_first_pipeline.test_exercise -v
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Path to our dataset (relative to ml-learning/)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "student_performance.csv")


# ============================================================
# PART 1: Load and Explore the Data
# ============================================================
# The first thing you ALWAYS do with a new dataset: load it and look at it.
# Don't jump straight to modeling. Get a feel for what you're working with.

def load_data():
    """Load the student performance dataset.

    Returns:
        A pandas DataFrame with the student performance data.
    """
    # TODO: Load the CSV file at DATA_PATH using pd.read_csv()
    # Hint: df = pd.read_csv(DATA_PATH)
    df = None  # Your code here

    return df


def explore_data(df):
    """Print basic info about the dataset so you understand what you're working with.

    This function is GIVEN to you. Read the output carefully when you run it.
    Understanding your data is the most important step in ML.
    """
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nBasic statistics:\n{df.describe()}")
    print(f"\nTarget distribution (how many passed vs failed):")
    print(df["passed"].value_counts())
    print(f"\nMissing values:\n{df.isnull().sum()}")


# ============================================================
# PART 2: Separate Features and Target
# ============================================================
# In ML, we split our data into:
#   X = features (the inputs the model learns from)
#   y = target (what we're trying to predict)
#
# Think of it like a function: y = f(X)
# The model learns f, and X are the inputs to that function.

def separate_features_target(df):
    """Separate the DataFrame into features (X) and target (y).

    The target column is 'passed' (0 = failed, 1 = passed).
    The features are everything else (study_hours, attendance_rate, etc.)

    Args:
        df: The full DataFrame.

    Returns:
        A tuple (X, y) where:
        - X is a DataFrame of features (all columns except 'passed')
        - y is a Series of the target variable ('passed')
    """
    # TODO: Create X by dropping the 'passed' column from df
    # Hint: X = df.drop(columns=['passed'])
    X = None  # Your code here

    # TODO: Create y by selecting just the 'passed' column
    # Hint: y = df['passed']
    y = None  # Your code here

    return X, y


# ============================================================
# PART 3: Split into Training and Test Sets
# ============================================================
# WHY DO WE SPLIT?
# If we train a model on ALL our data and then test it on the SAME data,
# we're just testing whether it memorized the answers. That tells us
# nothing about how it'll perform on NEW data it's never seen.
#
# Think of it like studying for a test: if you study the answer key,
# you'll ace that exact test, but you haven't actually learned the
# material. You want to test on UNSEEN questions.
#
# Convention: 80% train, 20% test is a common split.
# random_state=42 makes the split reproducible (same split every time).

def split_data(X, y):
    """Split features and target into training and test sets.

    Args:
        X: Feature DataFrame.
        y: Target Series.

    Returns:
        A tuple (X_train, X_test, y_train, y_test).
    """
    # TODO: Use train_test_split to split X and y
    # Use test_size=0.2 (20% for testing) and random_state=42
    # Hint: X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_test, y_train, y_test = None, None, None, None  # Replace this line

    return X_train, X_test, y_train, y_test


# ============================================================
# PART 4: Train a Model
# ============================================================
# In sklearn, every model follows the same pattern:
#   1. Create the model:     model = SomeModel()
#   2. Train it:             model.fit(X_train, y_train)
#   3. Make predictions:     predictions = model.predict(X_test)
#
# That's it. Three lines. The magic of sklearn is this consistent API.
# We'll use a Decision Tree - it's simple, interpretable, and works
# well on small datasets.

def train_model(X_train, y_train):
    """Create and train a Decision Tree classifier.

    Args:
        X_train: Training features.
        y_train: Training target.

    Returns:
        The trained model.
    """
    # TODO: Create a DecisionTreeClassifier with random_state=42
    # Hint: model = DecisionTreeClassifier(random_state=42)
    model = None  # Your code here

    # TODO: Train (fit) the model on the training data
    # Hint: model.fit(X_train, y_train)
    # Your code here

    return model


# ============================================================
# PART 5: Make Predictions and Evaluate
# ============================================================
# Now we use our trained model to predict on the TEST set (data it
# has never seen) and measure how well it did.
#
# Accuracy = (correct predictions) / (total predictions)
# It's the simplest metric. We'll learn better ones in Exercise 3.

def evaluate_model(model, X_test, y_test):
    """Make predictions on the test set and compute accuracy.

    Args:
        model: A trained model.
        X_test: Test features.
        y_test: Test target.

    Returns:
        A tuple (predictions, accuracy) where predictions is a numpy array
        and accuracy is a float between 0 and 1.
    """
    # TODO: Use the model to predict on X_test
    # Hint: predictions = model.predict(X_test)
    predictions = None  # Your code here

    # TODO: Compute accuracy by comparing predictions to y_test
    # Hint: accuracy = accuracy_score(y_test, predictions)
    accuracy = None  # Your code here

    return predictions, accuracy


# ============================================================
# PART 6: Check for Overfitting
# ============================================================
# OVERFITTING is the #1 problem in ML. It means your model memorized
# the training data instead of learning general patterns.
#
# How to detect it: compare training accuracy vs test accuracy.
# - If train accuracy >> test accuracy: overfitting!
# - If both are similar: good generalization
# - If both are low: underfitting (model too simple)
#
# Decision trees are VERY prone to overfitting because they can
# memorize every single training example perfectly.

def check_overfitting(model, X_train, y_train, X_test, y_test):
    """Compare training vs test accuracy to check for overfitting.

    Args:
        model: A trained model.
        X_train: Training features.
        y_train: Training target.
        X_test: Test features.
        y_test: Test target.

    Returns:
        A tuple (train_accuracy, test_accuracy).
    """
    # TODO: Compute accuracy on the TRAINING set
    # Hint: train_predictions = model.predict(X_train)
    #       train_accuracy = accuracy_score(y_train, train_predictions)
    train_accuracy = None  # Your code here

    # TODO: Compute accuracy on the TEST set
    # (You already did this in Part 5, same idea)
    test_accuracy = None  # Your code here

    return train_accuracy, test_accuracy


# ============================================================
# Run the full pipeline
# ============================================================
if __name__ == "__main__":
    # Part 1: Load and explore
    print("\n--- PART 1: Loading Data ---")
    df = load_data()
    if df is not None:
        explore_data(df)
    else:
        print("TODO: Implement load_data()")

    # Part 2: Separate features and target
    print("\n--- PART 2: Separating Features and Target ---")
    if df is not None:
        X, y = separate_features_target(df)
        if X is not None:
            print(f"Features (X) shape: {X.shape}")
            print(f"Target (y) shape: {y.shape}")
            print(f"Feature columns: {list(X.columns)}")
        else:
            print("TODO: Implement separate_features_target()")
    else:
        X, y = None, None

    # Part 3: Split data
    print("\n--- PART 3: Splitting Data ---")
    if X is not None:
        X_train, X_test, y_train, y_test = split_data(X, y)
        if X_train is not None:
            print(f"Training set: {X_train.shape[0]} samples")
            print(f"Test set: {X_test.shape[0]} samples")
        else:
            print("TODO: Implement split_data()")
    else:
        X_train, X_test, y_train, y_test = None, None, None, None

    # Part 4: Train
    print("\n--- PART 4: Training Model ---")
    if X_train is not None:
        model = train_model(X_train, y_train)
        if model is not None:
            print("Model trained successfully!")
            print(f"Model type: {type(model).__name__}")
        else:
            print("TODO: Implement train_model()")
    else:
        model = None

    # Part 5: Evaluate
    print("\n--- PART 5: Evaluating ---")
    if model is not None:
        predictions, accuracy = evaluate_model(model, X_test, y_test)
        if accuracy is not None:
            print(f"Test accuracy: {accuracy:.2%}")
        else:
            print("TODO: Implement evaluate_model()")
    else:
        predictions, accuracy = None, None

    # Part 6: Overfitting check
    print("\n--- PART 6: Overfitting Check ---")
    if model is not None:
        train_acc, test_acc = check_overfitting(model, X_train, y_train, X_test, y_test)
        if train_acc is not None:
            print(f"Training accuracy: {train_acc:.2%}")
            print(f"Test accuracy:     {test_acc:.2%}")
            gap = train_acc - test_acc
            if gap > 0.1:
                print(f"WARNING: {gap:.2%} gap - your model is overfitting!")
                print("The model memorized training data rather than learning patterns.")
            else:
                print(f"Gap: {gap:.2%} - looks like good generalization!")
        else:
            print("TODO: Implement check_overfitting()")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 01_first_pipeline.test_exercise -v")
    print("=" * 60)
