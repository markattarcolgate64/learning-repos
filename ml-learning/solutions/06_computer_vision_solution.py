"""
Solution for Exercise 6: Computer Vision - Image Classification
"""

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score


def load_image_data():
    digits = load_digits()
    images = digits.images
    X = digits.data
    y = digits.target
    n_samples = len(y)
    n_classes = len(np.unique(y))
    return {
        'images': images,
        'X': X,
        'y': y,
        'n_samples': n_samples,
        'n_classes': n_classes,
    }


def normalize_pixels(X_train, X_test):
    scaler = MinMaxScaler()
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.transform(X_test)
    return X_train_norm, X_test_norm, scaler


def train_classifiers(X_train, y_train):
    models = {}

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    models["KNN"] = knn

    lr = LogisticRegression(max_iter=5000, random_state=42)
    lr.fit(X_train, y_train)
    models["Logistic Regression"] = lr

    svm = SVC(kernel='rbf', random_state=42)
    svm.fit(X_train, y_train)
    models["SVM"] = svm

    return models


def evaluate_models(models, X_test, y_test):
    results = {}
    for name, model in models.items():
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        results[name] = {'accuracy': acc, 'predictions': preds}
    return results


def compute_confusion(y_true, y_pred):
    return confusion_matrix(y_true, y_pred)


def find_misclassified(y_true, y_pred):
    return np.where(y_true != y_pred)[0]


def find_most_confused_pair(cm):
    cm_copy = cm.copy()
    np.fill_diagonal(cm_copy, 0)
    idx = np.unravel_index(np.argmax(cm_copy), cm_copy.shape)
    return (idx[0], idx[1], cm_copy[idx])
