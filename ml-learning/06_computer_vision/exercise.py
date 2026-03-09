"""
Computer Vision: Image Classification
=======================================
Difficulty : ** (2/5)

The fundamental insight of computer vision:
  AN IMAGE IS JUST A GRID OF NUMBERS.

An 8x8 grayscale image is a matrix of 64 pixel values.
A 1080p color photo is a 1920x1080x3 array of numbers.
That's it. Once you see images as numbers, you can feed
them to any ML model.

This exercise teaches you to:
  1. Understand how images are represented as numpy arrays
  2. Flatten images into feature vectors for ML
  3. Normalize pixel values (preprocessing for images)
  4. Train classifiers on image data
  5. Analyze which images get confused (where CV is hard)

Dataset: sklearn's built-in digits dataset
  - 1,797 images of handwritten digits (0-9)
  - Each image is 8x8 pixels, grayscale (values 0-16)
  - No downloads needed — it ships with sklearn

This is the same TYPE of problem as the famous MNIST dataset
that every ML course uses, just smaller (8x8 instead of 28x28).

Run:
    python 06_computer_vision/exercise.py

Test:
    python -m unittest 06_computer_vision.test_exercise -v
"""

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


# ============================================================
# PART 1: Load and Understand Image Data
# ============================================================
# The key insight: a grayscale image is a 2D array of pixel intensities.
#
#   [ 0  0  5 13  9  1  0  0 ]
#   [ 0  0 13 15 10 15  5  0 ]    <- This IS the image.
#   [ 0  3 15  2  0 11  8  0 ]       Each number is a pixel brightness
#   [ 0  4 12  0  0  8  8  0 ]       (0 = black, 16 = white).
#   [ 0  5  8  0  0  9  8  0 ]
#   [ 0  4 11  0  1 12  7  0 ]    When your brain "sees" a digit,
#   [ 0  2 14  5 10 12  0  0 ]    it's really just recognizing patterns
#   [ 0  0  6 13 10  0  0  0 ]    in a grid of numbers.
#
# For ML, we FLATTEN this 8x8 grid into a single row of 64 numbers.
# Each pixel becomes a feature. The model learns which pixel patterns
# correspond to which digits.

def load_image_data():
    """Load the digits dataset and return images, flat features, and labels.

    Returns:
        A dict with keys:
        - 'images': array of shape (n_samples, 8, 8) — the raw 2D images
        - 'X': array of shape (n_samples, 64) — flattened feature vectors
        - 'y': array of shape (n_samples,) — digit labels (0-9)
        - 'n_samples': total number of images
        - 'n_classes': number of unique digit classes
    """
    digits = load_digits()

    # TODO: Extract the data from the digits object
    # Hint: digits.images gives you the 8x8 arrays
    #       digits.data gives you the pre-flattened 64-feature vectors
    #       digits.target gives you the labels (0-9)
    images = None  # Your code here (shape: n_samples x 8 x 8)
    X = None       # Your code here (shape: n_samples x 64)
    y = None       # Your code here (shape: n_samples,)

    # TODO: Count samples and classes
    # Hint: n_samples = len(y)
    #       n_classes = len(np.unique(y))
    n_samples = None  # Your code here
    n_classes = None  # Your code here

    return {
        'images': images,
        'X': X,
        'y': y,
        'n_samples': n_samples,
        'n_classes': n_classes,
    }


def display_digit_text(image):
    """Display an 8x8 digit image as text art. (GIVEN)

    This shows you what the model 'sees' — just a grid of numbers.
    """
    symbols = " .:-=+*#%@"
    for row in image:
        line = ""
        for pixel in row:
            idx = int(pixel / 16 * (len(symbols) - 1))
            idx = min(idx, len(symbols) - 1)
            line += symbols[idx] * 2
        print(line)


# ============================================================
# PART 2: Pixel Normalization
# ============================================================
# Image pixel values range from 0-16 in this dataset (or 0-255
# in standard images). We normalize them to 0-1 because:
#   1. Many algorithms work better with small, uniform scales
#   2. It's a standard practice in computer vision
#   3. It makes the model less sensitive to brightness differences
#
# We use MinMaxScaler which maps values to [0, 1]:
#   normalized = (value - min) / (max - min)

def normalize_pixels(X_train, X_test):
    """Normalize pixel values to [0, 1] range.

    Args:
        X_train: Training feature array.
        X_test: Test feature array.

    Returns:
        A tuple (X_train_norm, X_test_norm, scaler).
    """
    # TODO: Create a MinMaxScaler, fit on training data, transform both
    # Hint: scaler = MinMaxScaler()
    #       X_train_norm = scaler.fit_transform(X_train)
    #       X_test_norm = scaler.transform(X_test)
    # Remember: fit on train only! (same data leakage rule as Exercise 2)
    scaler = None       # Your code here
    X_train_norm = None  # Your code here
    X_test_norm = None   # Your code here

    return X_train_norm, X_test_norm, scaler


# ============================================================
# PART 3: Train an Image Classifier
# ============================================================
# KNN works surprisingly well on digit images. Why?
# Because similar digits have similar pixel patterns.
# A handwritten "3" looks more like other "3"s than like "7"s
# in pixel space.
#
# But we'll try multiple models to see which works best.

def train_classifiers(X_train, y_train):
    """Train multiple classifiers on the image data.

    Args:
        X_train: Normalized training features.
        y_train: Training labels.

    Returns:
        A dict mapping model names to fitted models.
    """
    models = {}

    # TODO: Create and train at least 3 different classifiers
    # Suggested models:
    #   "KNN": KNeighborsClassifier(n_neighbors=3)
    #   "Logistic Regression": LogisticRegression(max_iter=5000, random_state=42)
    #   "SVM": SVC(kernel='rbf', random_state=42)
    #
    # For each: create the model, call .fit(X_train, y_train), store in dict
    #
    # Hint:
    #   knn = KNeighborsClassifier(n_neighbors=3)
    #   knn.fit(X_train, y_train)
    #   models["KNN"] = knn

    # Your code here

    return models


# ============================================================
# PART 4: Evaluate and Compare
# ============================================================
# For multi-class classification (10 digits), the confusion matrix
# is 10x10. Each cell (i, j) tells you how many times digit i
# was predicted as digit j.
#
# This reveals which digits the model confuses — for example,
# 3 and 8 often get mixed up because they look similar.

def evaluate_models(models, X_test, y_test):
    """Evaluate each model and return results.

    Args:
        models: Dict of {name: fitted_model}.
        X_test: Normalized test features.
        y_test: Test labels.

    Returns:
        A dict mapping model names to dicts with:
        - 'accuracy': overall accuracy on test set
        - 'predictions': the predicted labels
    """
    results = {}

    # TODO: For each model, compute predictions and accuracy
    # Hint:
    #   for name, model in models.items():
    #       preds = model.predict(X_test)
    #       acc = accuracy_score(y_test, preds)
    #       results[name] = {'accuracy': acc, 'predictions': preds}

    # Your code here

    return results


def compute_confusion(y_true, y_pred):
    """Compute the confusion matrix for multi-class classification.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.

    Returns:
        A 10x10 confusion matrix (numpy array).
    """
    # TODO: Compute the confusion matrix
    # Hint: cm = confusion_matrix(y_true, y_pred)
    cm = None  # Your code here

    return cm


# ============================================================
# PART 5: Analyze Misclassifications
# ============================================================
# The most informative thing in CV is looking at what the model
# gets WRONG. This tells you where the problem is hard and often
# reveals patterns (e.g., "my model always confuses 4 and 9").

def find_misclassified(y_true, y_pred):
    """Find indices where the model made mistakes.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.

    Returns:
        A numpy array of indices where y_true != y_pred.
    """
    # TODO: Find indices where predictions don't match true labels
    # Hint: indices = np.where(y_true != y_pred)[0]
    indices = None  # Your code here

    return indices


def find_most_confused_pair(cm):
    """Find the pair of digits most often confused with each other.

    Looks at off-diagonal elements of the confusion matrix to find
    the most common mistake.

    Args:
        cm: A 10x10 confusion matrix.

    Returns:
        A tuple (true_digit, predicted_digit, count) for the most
        common confusion.
    """
    # TODO: Find the largest off-diagonal element in the confusion matrix
    # Hint: Set diagonal to 0 (we don't care about correct predictions)
    #       then find the position of the maximum value
    #
    #   cm_copy = cm.copy()
    #   np.fill_diagonal(cm_copy, 0)
    #   idx = np.unravel_index(np.argmax(cm_copy), cm_copy.shape)
    #   return (idx[0], idx[1], cm_copy[idx])

    # Your code here
    return None, None, None


# ============================================================
# Run the full CV pipeline
# ============================================================
if __name__ == "__main__":
    # Part 1: Load data
    print("=" * 60)
    print("PART 1: Understanding Image Data")
    print("=" * 60)
    data = load_image_data()
    if data['X'] is not None:
        print(f"Total images: {data['n_samples']}")
        print(f"Image shape: {data['images'].shape[1:]} (8x8 pixels)")
        print(f"Flattened features: {data['X'].shape[1]} (one per pixel)")
        print(f"Classes: {data['n_classes']} digits (0-9)")
        print(f"Pixel value range: [{data['X'].min():.0f}, {data['X'].max():.0f}]")

        print("\nHere's what a digit looks like as numbers vs text art:")
        print(f"\nDigit label: {data['y'][0]}")
        print(f"Raw pixel values:\n{data['images'][0].astype(int)}")
        print(f"\nAs text art:")
        display_digit_text(data['images'][0])
    else:
        print("TODO: Implement load_image_data()")

    # Split data
    if data['X'] is not None:
        X_train, X_test, y_train, y_test = train_test_split(
            data['X'], data['y'], test_size=0.2, random_state=42
        )
    else:
        X_train = X_test = y_train = y_test = None

    # Part 2: Normalize
    print("\n" + "=" * 60)
    print("PART 2: Pixel Normalization")
    print("=" * 60)
    if X_train is not None:
        X_train_n, X_test_n, scaler = normalize_pixels(X_train, X_test)
        if X_train_n is not None:
            print(f"Before normalization: pixels in [{X_train.min():.0f}, {X_train.max():.0f}]")
            print(f"After normalization:  pixels in [{X_train_n.min():.2f}, {X_train_n.max():.2f}]")
        else:
            print("TODO: Implement normalize_pixels()")
            X_train_n = X_test_n = None
    else:
        X_train_n = X_test_n = None

    # Part 3: Train classifiers
    print("\n" + "=" * 60)
    print("PART 3: Training Image Classifiers")
    print("=" * 60)
    if X_train_n is not None:
        models = train_classifiers(X_train_n, y_train)
        if models:
            print(f"Trained {len(models)} models: {list(models.keys())}")
        else:
            print("TODO: Implement train_classifiers()")
    else:
        models = {}

    # Part 4: Evaluate
    print("\n" + "=" * 60)
    print("PART 4: Model Comparison")
    print("=" * 60)
    if models:
        results = evaluate_models(models, X_test_n, y_test)
        if results:
            print("\nAccuracy by model:")
            print("-" * 40)
            for name in sorted(results, key=lambda n: results[n]['accuracy'], reverse=True):
                print(f"  {name:25s} {results[name]['accuracy']:.2%}")

            # Use best model for confusion matrix
            best_name = max(results, key=lambda n: results[n]['accuracy'])
            best_preds = results[best_name]['predictions']
            cm = compute_confusion(y_test, best_preds)
            if cm is not None:
                print(f"\nConfusion matrix for {best_name}:")
                print(cm)
        else:
            print("TODO: Implement evaluate_models()")
    else:
        best_preds = None
        cm = None

    # Part 5: Misclassification analysis
    print("\n" + "=" * 60)
    print("PART 5: Misclassification Analysis")
    print("=" * 60)
    if best_preds is not None:
        wrong = find_misclassified(y_test, best_preds)
        if wrong is not None:
            print(f"\nMisclassified: {len(wrong)} out of {len(y_test)} ({len(wrong)/len(y_test):.1%})")

            if cm is not None:
                true_d, pred_d, count = find_most_confused_pair(cm)
                if true_d is not None:
                    print(f"Most confused pair: digit {true_d} misclassified as {pred_d} ({count} times)")

            if len(wrong) > 0:
                print(f"\nFirst few mistakes:")
                for i in wrong[:3]:
                    print(f"\n  Predicted: {best_preds[i]}, Actual: {y_test.iloc[i] if hasattr(y_test, 'iloc') else y_test[i]}")
                    # Show the image as text
                    img_idx = X_test[i].reshape(8, 8)
                    display_digit_text(img_idx)
        else:
            print("TODO: Implement find_misclassified()")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 06_computer_vision.test_exercise -v")
    print("=" * 60)
