"""
Model Evaluation and Comparison
================================
Difficulty : ** (2/5)

Training a model is easy. Knowing if it's GOOD is the hard part.

This exercise teaches you to:
  1. Evaluate models with multiple metrics (not just accuracy)
  2. Use cross-validation for reliable estimates
  3. Compare multiple models fairly
  4. Select the best one WITHOUT data leakage

Accuracy alone can be misleading. Imagine a cancer detection model on
data where 99% of patients are healthy. A model that always predicts
"healthy" gets 99% accuracy but is completely useless. You need
metrics that capture different aspects of model quality.

Dataset: Student performance (same as Exercise 1 - already clean)
Task: Binary classification

Run:
    python 03_model_evaluation/exercise.py

Test:
    python -m unittest 03_model_evaluation.test_exercise -v
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "student_performance.csv")


def load_and_split():
    """Load data and perform train/test split. (GIVEN)"""
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["passed"])
    y = df["passed"]
    return train_test_split(X, y, test_size=0.2, random_state=42)


# ============================================================
# PART 1: The Confusion Matrix
# ============================================================
# A confusion matrix shows you exactly WHERE your model goes wrong.
#
#                    Predicted
#                  Neg    Pos
#  Actual  Neg  [  TN  |  FP  ]    TN = True Negative (correctly said no)
#          Pos  [  FN  |  TP  ]    FP = False Positive (wrongly said yes)
#                                  FN = False Negative (wrongly said no)
#                                  TP = True Positive (correctly said yes)
#
# This is WAY more informative than a single accuracy number.
# In medical diagnosis: FN (missing a disease) might be worse than FP (false alarm).
# In spam detection: FP (marking real email as spam) might be worse than FN.

def compute_confusion_matrix(y_true, y_pred):
    """Compute the confusion matrix for binary classification.

    Args:
        y_true: True labels (0 or 1).
        y_pred: Predicted labels (0 or 1).

    Returns:
        A 2x2 numpy array: the confusion matrix.
    """
    # TODO: Use sklearn's confusion_matrix function
    # Hint: cm = confusion_matrix(y_true, y_pred)
    cm = None  # Your code here

    return cm


# ============================================================
# PART 2: Precision, Recall, and F1
# ============================================================
# These three metrics give you different views of model quality:
#
# PRECISION: Of all the times the model said "pass", how many actually passed?
#   Precision = TP / (TP + FP)
#   High precision = few false alarms
#
# RECALL: Of all students who actually passed, how many did the model catch?
#   Recall = TP / (TP + FN)
#   High recall = few missed cases
#
# F1 SCORE: The harmonic mean of precision and recall.
#   F1 = 2 * (precision * recall) / (precision + recall)
#   Balances both concerns into a single number.

def compute_metrics(y_true, y_pred):
    """Compute precision, recall, and F1 score.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.

    Returns:
        A tuple (precision, recall, f1) of floats.
    """
    # TODO: Compute precision
    # Hint: prec = precision_score(y_true, y_pred)
    prec = None  # Your code here

    # TODO: Compute recall
    # Hint: rec = recall_score(y_true, y_pred)
    rec = None  # Your code here

    # TODO: Compute F1 score
    # Hint: f1 = f1_score(y_true, y_pred)
    f1 = None  # Your code here

    return prec, rec, f1


# ============================================================
# PART 3: Cross-Validation
# ============================================================
# A single train/test split is unreliable. You might get lucky (or unlucky)
# with which data ends up in which set.
#
# CROSS-VALIDATION solves this:
#   1. Split data into K folds (e.g., 5)
#   2. Train on K-1 folds, test on the remaining 1
#   3. Repeat K times, each fold gets a turn as the test set
#   4. Average the K scores
#
# This gives you a much more reliable estimate of model performance.
# Standard choice: 5-fold or 10-fold CV.

def cross_validate_model(model, X, y, cv=5):
    """Run k-fold cross-validation and return the scores.

    Args:
        model: An sklearn model (unfitted).
        X: All features (the function will handle splitting).
        y: All targets.
        cv: Number of folds (default 5).

    Returns:
        A numpy array of accuracy scores, one per fold.
    """
    # TODO: Use cross_val_score to run cross-validation
    # Hint: scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    scores = None  # Your code here

    return scores


# ============================================================
# PART 4: Train Multiple Models
# ============================================================
# Different algorithms have different strengths. You should always
# try a few and compare them. Here we'll compare:
#
# 1. Decision Tree: simple, interpretable, but prone to overfitting
# 2. K-Nearest Neighbors (KNN): finds similar examples, simple but slow
# 3. Logistic Regression: linear model for classification, fast and reliable

def create_models():
    """Create a dictionary of models to compare.

    Returns:
        A dict mapping model names to unfitted sklearn models.
    """
    # TODO: Create a dictionary with three models:
    #   "Decision Tree": DecisionTreeClassifier(random_state=42)
    #   "KNN": KNeighborsClassifier(n_neighbors=5)
    #   "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000)
    #
    # Hint: models = {"Decision Tree": DecisionTreeClassifier(random_state=42), ...}
    models = None  # Your code here

    return models


# ============================================================
# PART 5: Compare and Select the Best Model
# ============================================================
# The right way to compare models:
#   1. Use cross-validation on the TRAINING data to compare models
#   2. Select the best model based on CV scores
#   3. Evaluate the winner on the TEST set ONLY ONCE at the end
#
# DO NOT use test set scores to choose between models!
# That's data leakage - you're making decisions based on test data.

def compare_models(models, X_train, y_train):
    """Compare multiple models using cross-validation.

    Args:
        models: Dict mapping model names to unfitted sklearn models.
        X_train: Training features.
        y_train: Training target.

    Returns:
        A dict mapping model names to their mean CV accuracy scores.
    """
    results = {}

    # TODO: For each model, run 5-fold cross-validation and store the mean score
    # Hint:
    #   for name, model in models.items():
    #       scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    #       results[name] = np.mean(scores)

    # Your code here

    return results


def select_best_model(results):
    """Select the model with the highest mean CV score.

    Args:
        results: Dict mapping model names to mean CV scores.

    Returns:
        The name (string) of the best model.
    """
    # TODO: Find the model name with the highest score
    # Hint: best_name = max(results, key=results.get)
    best_name = None  # Your code here

    return best_name


# ============================================================
# Run the full evaluation pipeline
# ============================================================
if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_and_split()

    # Train a baseline model for Parts 1-2
    baseline = DecisionTreeClassifier(random_state=42)
    baseline.fit(X_train, y_train)
    y_pred = baseline.predict(X_test)

    # Part 1: Confusion Matrix
    print("=" * 60)
    print("PART 1: Confusion Matrix")
    print("=" * 60)
    cm = compute_confusion_matrix(y_test, y_pred)
    if cm is not None:
        print(f"\n{cm}")
        tn, fp, fn, tp = cm.ravel()
        print(f"\nTrue Negatives:  {tn} (correctly predicted fail)")
        print(f"False Positives: {fp} (predicted pass, actually failed)")
        print(f"False Negatives: {fn} (predicted fail, actually passed)")
        print(f"True Positives:  {tp} (correctly predicted pass)")
    else:
        print("TODO: Implement compute_confusion_matrix()")

    # Part 2: Precision, Recall, F1
    print("\n" + "=" * 60)
    print("PART 2: Precision, Recall, F1")
    print("=" * 60)
    prec, rec, f1 = compute_metrics(y_test, y_pred)
    if prec is not None:
        print(f"\nPrecision: {prec:.3f} (of predicted passes, {prec:.0%} actually passed)")
        print(f"Recall:    {rec:.3f} (of actual passes, model caught {rec:.0%})")
        print(f"F1 Score:  {f1:.3f} (balance of precision and recall)")
    else:
        print("TODO: Implement compute_metrics()")

    # Part 3: Cross-Validation
    print("\n" + "=" * 60)
    print("PART 3: Cross-Validation")
    print("=" * 60)
    cv_scores = cross_validate_model(DecisionTreeClassifier(random_state=42), X_train, y_train)
    if cv_scores is not None:
        print(f"\n5-Fold CV scores: {cv_scores.round(3)}")
        print(f"Mean: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        print("Notice the variance - that's why a single split isn't reliable!")
    else:
        print("TODO: Implement cross_validate_model()")

    # Part 4 & 5: Compare models
    print("\n" + "=" * 60)
    print("PARTS 4 & 5: Model Comparison")
    print("=" * 60)
    models = create_models()
    if models is not None:
        results = compare_models(models, X_train, y_train)
        if results:
            print("\nCross-Validation Results:")
            print("-" * 40)
            for name, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
                print(f"  {name:25s} {score:.3f}")

            best = select_best_model(results)
            if best is not None:
                print(f"\nBest model: {best}")

                # Final evaluation on test set
                final_model = models[best]
                final_model.fit(X_train, y_train)
                final_pred = final_model.predict(X_test)
                final_acc = accuracy_score(y_test, final_pred)
                print(f"Final test accuracy: {final_acc:.3f}")
            else:
                print("TODO: Implement select_best_model()")
        else:
            print("TODO: Implement compare_models()")
    else:
        print("TODO: Implement create_models()")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 03_model_evaluation.test_exercise -v")
    print("=" * 60)
