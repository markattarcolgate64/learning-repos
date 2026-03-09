"""
Solution for Exercise 3: Model Evaluation and Comparison
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
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["passed"])
    y = df["passed"]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def compute_confusion_matrix(y_true, y_pred):
    return confusion_matrix(y_true, y_pred)


def compute_metrics(y_true, y_pred):
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return prec, rec, f1


def cross_validate_model(model, X, y, cv=5):
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    return scores


def create_models():
    return {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
    }


def compare_models(models, X_train, y_train):
    results = {}
    for name, model in models.items():
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        results[name] = np.mean(scores)
    return results


def select_best_model(results):
    return max(results, key=results.get)
