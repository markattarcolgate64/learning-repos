"""
Solution for Exercise 5: Neural Network from Scratch
"""

import numpy as np


def make_circles(n_samples=300, noise=0.1, seed=42):
    rng = np.random.RandomState(seed)
    n_each = n_samples // 2

    theta_inner = rng.uniform(0, 2 * np.pi, n_each)
    r_inner = 0.5 + rng.normal(0, noise, n_each)
    x_inner = np.column_stack([r_inner * np.cos(theta_inner),
                                r_inner * np.sin(theta_inner)])

    theta_outer = rng.uniform(0, 2 * np.pi, n_each)
    r_outer = 1.5 + rng.normal(0, noise, n_each)
    x_outer = np.column_stack([r_outer * np.cos(theta_outer),
                                r_outer * np.sin(theta_outer)])

    X = np.vstack([x_inner, x_outer])
    y = np.concatenate([np.zeros(n_each), np.ones(n_each)]).reshape(-1, 1)

    idx = rng.permutation(n_samples)
    return X[idx], y[idx]


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def sigmoid_derivative(a):
    return a * (1 - a)


def initialize_weights(input_size, hidden_size, output_size, seed=42):
    rng = np.random.RandomState(seed)
    W1 = rng.randn(input_size, hidden_size) * 0.5
    b1 = np.zeros((1, hidden_size))
    W2 = rng.randn(hidden_size, output_size) * 0.5
    b2 = np.zeros((1, output_size))
    return {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}


def forward(X, params):
    W1, b1 = params['W1'], params['b1']
    W2, b2 = params['W2'], params['b2']

    z1 = X @ W1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ W2 + b2
    a2 = sigmoid(z2)

    return {'z1': z1, 'a1': a1, 'z2': z2, 'a2': a2}


def compute_loss(y, a2):
    m = len(y)
    epsilon = 1e-8
    loss = -(1 / m) * np.sum(
        y * np.log(a2 + epsilon) + (1 - y) * np.log(1 - a2 + epsilon)
    )
    return loss


def backward(X, y, params, cache):
    m = len(y)
    W2 = params['W2']
    a1, a2 = cache['a1'], cache['a2']

    # Output layer gradients
    dz2 = a2 - y
    dW2 = (1 / m) * (a1.T @ dz2)
    db2 = (1 / m) * np.sum(dz2, axis=0, keepdims=True)

    # Hidden layer gradients (chain rule)
    dz1 = (dz2 @ W2.T) * sigmoid_derivative(a1)
    dW1 = (1 / m) * (X.T @ dz1)
    db1 = (1 / m) * np.sum(dz1, axis=0, keepdims=True)

    return {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}


def train(X, y, hidden_size=8, learning_rate=1.0, epochs=1000, seed=42):
    input_size = X.shape[1]
    output_size = 1

    params = initialize_weights(input_size, hidden_size, output_size, seed)
    loss_history = []

    for epoch in range(epochs):
        cache = forward(X, params)
        loss = compute_loss(y, cache['a2'])
        grads = backward(X, y, params, cache)

        params['W1'] -= learning_rate * grads['dW1']
        params['b1'] -= learning_rate * grads['db1']
        params['W2'] -= learning_rate * grads['dW2']
        params['b2'] -= learning_rate * grads['db2']

        loss_history.append(loss)

    return params, loss_history


def predict(X, params):
    cache = forward(X, params)
    predictions = (cache['a2'] >= 0.5).astype(int)
    return predictions
