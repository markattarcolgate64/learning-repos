"""
Neural Network from Scratch
============================
Difficulty : *** (3/5)

You implemented gradient descent for linear regression.
Now extend it to a neural network.

A neural network is just:
  1. Matrix multiplications + nonlinear activations (forward pass)
  2. A loss function to measure how wrong we are
  3. Calculus to compute how to adjust weights (backpropagation)
  4. Gradient descent to update the weights

Architecture:
  Input (2) -> Hidden (8, sigmoid) -> Output (1, sigmoid)

This is the simplest possible neural network that can learn
NONLINEAR patterns. A linear model (like logistic regression) can
only draw a straight line to separate classes. This network can
draw curves.

Dataset: Synthetic concentric circles (generated with numpy)
Task: Binary classification on non-linearly-separable data

Run:
    python 05_neural_network/exercise.py

Test:
    python -m unittest 05_neural_network.test_exercise -v
"""

import numpy as np


# ============================================================
# PART 1: Generate a Non-Linearly-Separable Dataset
# ============================================================
# We create two concentric circles of points. The inner circle is
# class 0, the outer circle is class 1. A straight line CANNOT
# separate these - you NEED a nonlinear model.

def make_circles(n_samples=300, noise=0.1, seed=42):
    """Generate concentric circles dataset. (GIVEN)

    Returns:
        X: array of shape (n_samples, 2) - the 2D points
        y: array of shape (n_samples, 1) - labels (0 or 1)
    """
    rng = np.random.RandomState(seed)
    n_each = n_samples // 2

    # Inner circle (class 0)
    theta_inner = rng.uniform(0, 2 * np.pi, n_each)
    r_inner = 0.5 + rng.normal(0, noise, n_each)
    x_inner = np.column_stack([r_inner * np.cos(theta_inner),
                                r_inner * np.sin(theta_inner)])

    # Outer circle (class 1)
    theta_outer = rng.uniform(0, 2 * np.pi, n_each)
    r_outer = 1.5 + rng.normal(0, noise, n_each)
    x_outer = np.column_stack([r_outer * np.cos(theta_outer),
                                r_outer * np.sin(theta_outer)])

    X = np.vstack([x_inner, x_outer])
    y = np.concatenate([np.zeros(n_each), np.ones(n_each)]).reshape(-1, 1)

    # Shuffle
    idx = rng.permutation(n_samples)
    return X[idx], y[idx]


# ============================================================
# Activation Functions (GIVEN)
# ============================================================
# Sigmoid squashes any number into (0, 1) - perfect for probabilities.
# Its derivative is needed for backpropagation.

def sigmoid(z):
    """Sigmoid activation: 1 / (1 + exp(-z)). (GIVEN)"""
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def sigmoid_derivative(a):
    """Derivative of sigmoid, given the ACTIVATED output a. (GIVEN)

    If a = sigmoid(z), then d_sigmoid/dz = a * (1 - a).
    """
    return a * (1 - a)


# ============================================================
# PART 2: Initialize the Network
# ============================================================
# A neural network's "knowledge" lives in its weights and biases.
# We start with random weights (small values) and zero biases.
#
# Our architecture:
#   Layer 1 (hidden):  2 inputs -> 8 hidden neurons
#     W1 shape: (2, 8)    b1 shape: (1, 8)
#
#   Layer 2 (output):  8 hidden -> 1 output
#     W2 shape: (8, 1)    b2 shape: (1, 1)
#
# WHY small random weights? If all weights start at 0 or the same
# value, all neurons learn the same thing (symmetry breaking).

def initialize_weights(input_size, hidden_size, output_size, seed=42):
    """Initialize network weights and biases.

    Args:
        input_size: Number of input features (2).
        hidden_size: Number of hidden neurons (8).
        output_size: Number of output neurons (1).
        seed: Random seed.

    Returns:
        A dict with keys 'W1', 'b1', 'W2', 'b2'.
    """
    rng = np.random.RandomState(seed)

    # TODO: Initialize weights with small random values and biases with zeros
    # Hint:
    #   W1 = rng.randn(input_size, hidden_size) * 0.5
    #   b1 = np.zeros((1, hidden_size))
    #   W2 = rng.randn(hidden_size, output_size) * 0.5
    #   b2 = np.zeros((1, output_size))

    W1 = None  # Your code here  (shape: input_size x hidden_size)
    b1 = None  # Your code here  (shape: 1 x hidden_size)
    W2 = None  # Your code here  (shape: hidden_size x output_size)
    b2 = None  # Your code here  (shape: 1 x output_size)

    return {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}


# ============================================================
# PART 3: Forward Propagation
# ============================================================
# Forward propagation pushes data through the network:
#
#   Layer 1:  z1 = X @ W1 + b1      (linear transformation)
#             a1 = sigmoid(z1)       (nonlinear activation)
#
#   Layer 2:  z2 = a1 @ W2 + b2     (linear transformation)
#             a2 = sigmoid(z2)       (output probability)
#
# a2 is our prediction: a probability between 0 and 1.
# We also return the intermediate values (z1, a1) because
# backpropagation needs them to compute gradients.

def forward(X, params):
    """Compute the forward pass through the network.

    Args:
        X: Input data of shape (n_samples, 2).
        params: Dict with 'W1', 'b1', 'W2', 'b2'.

    Returns:
        A dict with keys 'z1', 'a1', 'z2', 'a2' (the intermediate
        and final values). a2 is the output prediction.
    """
    W1, b1 = params['W1'], params['b1']
    W2, b2 = params['W2'], params['b2']

    # TODO: Compute the forward pass
    # Layer 1: hidden layer
    # Hint: z1 = X @ W1 + b1
    #       a1 = sigmoid(z1)
    z1 = None  # Your code here
    a1 = None  # Your code here

    # Layer 2: output layer
    # Hint: z2 = a1 @ W2 + b2
    #       a2 = sigmoid(z2)
    z2 = None  # Your code here
    a2 = None  # Your code here

    return {'z1': z1, 'a1': a1, 'z2': z2, 'a2': a2}


# ============================================================
# PART 4: Compute Loss
# ============================================================
# Binary Cross-Entropy Loss measures how wrong our predictions are:
#
#   L = -(1/m) * sum( y*log(a2) + (1-y)*log(1-a2) )
#
# When the prediction is close to the true label, loss is LOW.
# When the prediction is far from the true label, loss is HIGH.
# This is the standard loss function for binary classification.

def compute_loss(y, a2):
    """Compute binary cross-entropy loss.

    Args:
        y: True labels, shape (m, 1).
        a2: Predicted probabilities, shape (m, 1).

    Returns:
        A float: the mean binary cross-entropy loss.
    """
    m = len(y)

    # TODO: Compute binary cross-entropy loss
    # Add a tiny epsilon to prevent log(0)
    # Hint:
    #   epsilon = 1e-8
    #   loss = -(1/m) * np.sum(y * np.log(a2 + epsilon) + (1 - y) * np.log(1 - a2 + epsilon))
    loss = None  # Your code here

    return loss


# ============================================================
# PART 5: Backpropagation
# ============================================================
# THIS IS THE KEY ALGORITHM.
#
# Backpropagation uses the chain rule to compute how much each
# weight contributed to the error, working backwards from the output.
#
# The math (don't panic, we'll walk through it):
#
#   Output layer gradients:
#     dz2 = a2 - y                          (error at output)
#     dW2 = (1/m) * a1.T @ dz2             (how much W2 caused the error)
#     db2 = (1/m) * sum(dz2)               (how much b2 caused the error)
#
#   Hidden layer gradients (chain rule!):
#     dz1 = (dz2 @ W2.T) * sigmoid_derivative(a1)   (error propagated back)
#     dW1 = (1/m) * X.T @ dz1              (how much W1 caused the error)
#     db1 = (1/m) * sum(dz1)               (how much b1 caused the error)
#
# Each gradient tells us: "if I nudge this weight a tiny bit,
# how much does the loss change?" We then nudge in the OPPOSITE
# direction to reduce the loss. That's gradient descent!

def backward(X, y, params, cache):
    """Compute gradients via backpropagation.

    Args:
        X: Input data, shape (m, 2).
        y: True labels, shape (m, 1).
        params: Dict with 'W1', 'b1', 'W2', 'b2'.
        cache: Dict from forward() with 'z1', 'a1', 'z2', 'a2'.

    Returns:
        A dict with keys 'dW1', 'db1', 'dW2', 'db2' (the gradients).
    """
    m = len(y)
    W2 = params['W2']
    a1, a2 = cache['a1'], cache['a2']

    # TODO: Compute output layer gradients
    # Hint: dz2 = a2 - y
    #       dW2 = (1/m) * (a1.T @ dz2)
    #       db2 = (1/m) * np.sum(dz2, axis=0, keepdims=True)
    dz2 = None  # Your code here
    dW2 = None  # Your code here
    db2 = None  # Your code here

    # TODO: Compute hidden layer gradients (chain rule)
    # Hint: dz1 = (dz2 @ W2.T) * sigmoid_derivative(a1)
    #       dW1 = (1/m) * (X.T @ dz1)
    #       db1 = (1/m) * np.sum(dz1, axis=0, keepdims=True)
    dz1 = None  # Your code here
    dW1 = None  # Your code here
    db1 = None  # Your code here

    return {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}


# ============================================================
# PART 6: Training Loop
# ============================================================
# Put it all together: forward -> loss -> backward -> update.
# Repeat for many epochs until the network learns.

def train(X, y, hidden_size=8, learning_rate=1.0, epochs=1000, seed=42):
    """Train the neural network.

    Args:
        X: Training data, shape (m, 2).
        y: Labels, shape (m, 1).
        hidden_size: Number of hidden neurons.
        learning_rate: Step size for gradient descent.
        epochs: Number of training iterations.
        seed: Random seed.

    Returns:
        A tuple (params, loss_history) where params is the trained
        weights dict and loss_history is a list of loss values.
    """
    input_size = X.shape[1]
    output_size = 1

    # TODO: Initialize weights
    # Hint: params = initialize_weights(input_size, hidden_size, output_size, seed)
    params = None  # Your code here

    loss_history = []

    for epoch in range(epochs):
        # TODO: Forward pass
        # Hint: cache = forward(X, params)
        cache = None  # Your code here

        # TODO: Compute loss
        # Hint: loss = compute_loss(y, cache['a2'])
        loss = None  # Your code here

        # TODO: Backward pass
        # Hint: grads = backward(X, y, params, cache)
        grads = None  # Your code here

        # TODO: Update weights using gradient descent
        # Hint: params['W1'] -= learning_rate * grads['dW1']
        #       params['b1'] -= learning_rate * grads['db1']
        #       params['W2'] -= learning_rate * grads['dW2']
        #       params['b2'] -= learning_rate * grads['db2']
        # Your code here

        if loss is not None:
            loss_history.append(loss)

        if epoch % 100 == 0 and loss is not None:
            print(f"Epoch {epoch:4d}  Loss: {loss:.4f}")

    return params, loss_history


# ============================================================
# PART 7: Predict
# ============================================================

def predict(X, params):
    """Make binary predictions using the trained network.

    Args:
        X: Input data, shape (m, 2).
        params: Trained weights dict.

    Returns:
        Binary predictions as a numpy array of shape (m, 1),
        containing 0s and 1s.
    """
    # TODO: Run forward pass and threshold at 0.5
    # Hint: cache = forward(X, params)
    #       predictions = (cache['a2'] >= 0.5).astype(int)
    predictions = None  # Your code here

    return predictions


# ============================================================
# Run the neural network
# ============================================================
if __name__ == "__main__":
    # Generate data
    print("=" * 60)
    print("PART 1: Generating Non-Linearly-Separable Data")
    print("=" * 60)
    X, y = make_circles(n_samples=300, noise=0.1, seed=42)
    print(f"Data shape: X={X.shape}, y={y.shape}")
    print(f"Class balance: {np.mean(y):.0%} positive")

    # Train
    print("\n" + "=" * 60)
    print("PARTS 2-6: Training the Network")
    print("=" * 60)
    params, loss_history = train(X, y, hidden_size=8, learning_rate=1.0, epochs=1000)

    if loss_history:
        print(f"\nFinal loss: {loss_history[-1]:.4f}")
        print(f"Loss decreased: {loss_history[-1] < loss_history[0]}")

    # Evaluate
    print("\n" + "=" * 60)
    print("PART 7: Evaluation")
    print("=" * 60)
    preds = predict(X, params)
    if preds is not None:
        accuracy = np.mean(preds == y)
        print(f"Training accuracy: {accuracy:.2%}")
        if accuracy > 0.9:
            print("Excellent! Your neural network learned the nonlinear pattern!")
        elif accuracy > 0.7:
            print("Good! Try more epochs or adjust the learning rate.")
        else:
            print("The network is still learning. Check your implementation.")
    else:
        print("TODO: Implement predict()")

    # Compare with a linear model
    print("\n--- For comparison: a linear model on this data ---")
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression()
    lr.fit(X, y.ravel())
    lr_acc = lr.score(X, y.ravel())
    print(f"Logistic Regression accuracy: {lr_acc:.2%}")
    print("(A linear model can't solve this because the data is not linearly separable!)")

    print("\n" + "=" * 60)
    print("Done! Run the tests to verify:")
    print("  python -m unittest 05_neural_network.test_exercise -v")
    print("=" * 60)
