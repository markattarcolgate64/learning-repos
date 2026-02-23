"""
CODING CHALLENGE 2: Implement Gradient Descent for Linear Regression
====================================================================

Your mission: Implement various gradient descent algorithms to solve
linear regression. This builds intuition for optimization that carries
over to deep learning.

Difficulty: ⭐⭐⭐

Instructions:
1. Implement batch gradient descent
2. Implement stochastic gradient descent (SGD)
3. Implement mini-batch gradient descent
4. Experiment with learning rates
5. Visualize the convergence

Learning objectives:
- Understand gradient-based optimization
- See how different variants trade off speed vs. stability
- Build intuition for hyperparameter tuning (learning rate, batch size)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional, Callable

np.random.seed(42)


# =============================================================================
# PART 1: COMPUTE THE GRADIENT
# =============================================================================

def compute_loss(X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> float:
    """
    Compute the Mean Squared Error loss.

    L(β) = (1/2n) * ||y - Xβ||² = (1/2n) * Σᵢ(yᵢ - xᵢᵀβ)²

    We use 1/2n instead of 1/n to make the gradient cleaner.

    Args:
        X: Design matrix (n, p) - should include intercept column if needed
        y: Target vector (n,)
        beta: Parameter vector (p,)

    Returns:
        The MSE loss
    """
    # TODO: Implement the loss function

    pass


def compute_gradient(X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    Compute the gradient of the MSE loss with respect to beta.

    ∇L(β) = (1/n) * Xᵀ(Xβ - y)

    Args:
        X: Design matrix (n, p)
        y: Target vector (n,)
        beta: Parameter vector (p,)

    Returns:
        The gradient vector (p,)
    """
    # TODO: Implement the gradient computation
    # Hint: This is the derivative of L(β) = (1/2n) * ||y - Xβ||²

    pass


# =============================================================================
# PART 2: BATCH GRADIENT DESCENT
# =============================================================================

def batch_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    n_iterations: int = 1000,
    tolerance: float = 1e-6,
    verbose: bool = False
) -> Tuple[np.ndarray, List[float]]:
    """
    Perform batch gradient descent.

    Update rule: β_{t+1} = β_t - α * ∇L(β_t)

    Args:
        X: Design matrix (n, p)
        y: Target vector (n,)
        learning_rate: Step size α
        n_iterations: Maximum number of iterations
        tolerance: Stop if gradient norm < tolerance
        verbose: Print progress every 100 iterations

    Returns:
        Tuple of (final_beta, loss_history)
    """
    n, p = X.shape
    beta = np.zeros(p)  # Initialize at zero
    loss_history = []

    # TODO: Implement the gradient descent loop
    # For each iteration:
    # 1. Compute the loss (for tracking)
    # 2. Compute the gradient
    # 3. Update beta
    # 4. Check for convergence

    for i in range(n_iterations):
        pass  # Your implementation here

    return beta, loss_history


# =============================================================================
# PART 3: STOCHASTIC GRADIENT DESCENT
# =============================================================================

def stochastic_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    n_epochs: int = 100,
    verbose: bool = False
) -> Tuple[np.ndarray, List[float]]:
    """
    Perform stochastic gradient descent (SGD).

    Instead of using all data points, use ONE random sample per update.

    Args:
        X: Design matrix (n, p)
        y: Target vector (n,)
        learning_rate: Step size
        n_epochs: Number of passes through the data
        verbose: Print progress

    Returns:
        Tuple of (final_beta, loss_history)
    """
    n, p = X.shape
    beta = np.zeros(p)
    loss_history = []

    # TODO: Implement SGD
    # For each epoch:
    #   Shuffle the data
    #   For each sample (xᵢ, yᵢ):
    #     Compute gradient using just this one sample
    #     Update beta
    #   Record the full loss at end of epoch

    for epoch in range(n_epochs):
        pass  # Your implementation here

    return beta, loss_history


# =============================================================================
# PART 4: MINI-BATCH GRADIENT DESCENT
# =============================================================================

def minibatch_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    batch_size: int = 32,
    learning_rate: float = 0.01,
    n_epochs: int = 100,
    verbose: bool = False
) -> Tuple[np.ndarray, List[float]]:
    """
    Perform mini-batch gradient descent.

    A compromise between batch GD and SGD: use small batches.

    Args:
        X: Design matrix (n, p)
        y: Target vector (n,)
        batch_size: Number of samples per batch
        learning_rate: Step size
        n_epochs: Number of passes through the data
        verbose: Print progress

    Returns:
        Tuple of (final_beta, loss_history)
    """
    n, p = X.shape
    beta = np.zeros(p)
    loss_history = []

    # TODO: Implement mini-batch GD
    # For each epoch:
    #   Shuffle the data
    #   For each batch:
    #     Compute gradient using the batch
    #     Update beta
    #   Record the full loss at end of epoch

    for epoch in range(n_epochs):
        pass  # Your implementation here

    return beta, loss_history


# =============================================================================
# PART 5: GRADIENT DESCENT WITH MOMENTUM
# =============================================================================

def gradient_descent_with_momentum(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    momentum: float = 0.9,
    n_iterations: int = 1000,
    tolerance: float = 1e-6
) -> Tuple[np.ndarray, List[float]]:
    """
    Gradient descent with momentum.

    Momentum helps accelerate convergence and escape local minima.

    Update rules:
        v_{t+1} = γ * v_t + α * ∇L(β_t)
        β_{t+1} = β_t - v_{t+1}

    where γ is the momentum coefficient.

    Args:
        X: Design matrix (n, p)
        y: Target vector (n,)
        learning_rate: Step size α
        momentum: Momentum coefficient γ (typically 0.9)
        n_iterations: Maximum iterations
        tolerance: Convergence threshold

    Returns:
        Tuple of (final_beta, loss_history)
    """
    n, p = X.shape
    beta = np.zeros(p)
    velocity = np.zeros(p)
    loss_history = []

    # TODO: Implement gradient descent with momentum

    for i in range(n_iterations):
        pass  # Your implementation here

    return beta, loss_history


# =============================================================================
# PART 6: LEARNING RATE SCHEDULES
# =============================================================================

def gradient_descent_with_schedule(
    X: np.ndarray,
    y: np.ndarray,
    initial_lr: float = 0.1,
    schedule: str = 'constant',  # 'constant', 'decay', 'step'
    n_iterations: int = 1000
) -> Tuple[np.ndarray, List[float], List[float]]:
    """
    Gradient descent with learning rate schedules.

    Schedules:
    - 'constant': α_t = initial_lr
    - 'decay': α_t = initial_lr / (1 + decay_rate * t)
    - 'step': α_t = initial_lr * 0.5^(t // step_size)

    Args:
        X, y: Data
        initial_lr: Starting learning rate
        schedule: Type of schedule
        n_iterations: Number of iterations

    Returns:
        Tuple of (final_beta, loss_history, lr_history)
    """
    n, p = X.shape
    beta = np.zeros(p)
    loss_history = []
    lr_history = []

    # TODO: Implement different learning rate schedules

    for t in range(n_iterations):
        # Determine learning rate based on schedule
        if schedule == 'constant':
            lr = initial_lr
        elif schedule == 'decay':
            # TODO: Implement decay schedule
            lr = None
        elif schedule == 'step':
            # TODO: Implement step schedule (halve every 100 iterations)
            lr = None
        else:
            lr = initial_lr

        pass  # Your gradient descent step here

    return beta, loss_history, lr_history


# =============================================================================
# PART 7: VISUALIZATIONS
# =============================================================================

def plot_convergence(loss_histories: dict, title: str = "Convergence Comparison"):
    """
    Plot loss curves for different methods.

    Args:
        loss_histories: Dict mapping method name to loss history list
        title: Plot title
    """
    # TODO: Create a plot comparing convergence of different methods
    # - X-axis: iteration/epoch
    # - Y-axis: loss (consider log scale)
    # - Different colored lines for each method

    pass


def plot_2d_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    beta_history: List[np.ndarray],
    title: str = "Gradient Descent Path"
):
    """
    Visualize gradient descent on the loss surface for 2D case.

    Only works when we have exactly 2 parameters (intercept + 1 feature).

    Args:
        X: Design matrix (n, 2) - with intercept
        y: Target vector
        beta_history: List of beta values at each iteration
        title: Plot title
    """
    # TODO: Create a contour plot of the loss surface
    # and overlay the path taken by gradient descent
    # This is a great visualization exercise!

    pass


# =============================================================================
# EXPERIMENTS
# =============================================================================

def experiment_learning_rates():
    """
    Experiment with different learning rates.

    Observe:
    - Too small: slow convergence
    - Too large: divergence or oscillation
    - Just right: fast, stable convergence
    """
    print("=" * 60)
    print("EXPERIMENT: Learning Rate Sensitivity")
    print("=" * 60)

    # Generate data
    n = 1000
    X = np.random.randn(n, 1)
    X = np.column_stack([np.ones(n), X])  # Add intercept
    true_beta = np.array([2, 3])
    y = X @ true_beta + np.random.randn(n) * 0.5

    # TODO: Try different learning rates and compare convergence
    learning_rates = [0.001, 0.01, 0.1, 0.5, 1.0]

    for lr in learning_rates:
        pass  # Run gradient descent and record results

    # TODO: Plot the results


def experiment_batch_sizes():
    """
    Experiment with different batch sizes.

    Observe the tradeoff:
    - Larger batches: more stable but slower updates
    - Smaller batches: noisier but faster updates
    """
    print("=" * 60)
    print("EXPERIMENT: Batch Size Comparison")
    print("=" * 60)

    # Generate data
    n = 1000
    X = np.random.randn(n, 3)
    X = np.column_stack([np.ones(n), X])
    true_beta = np.array([1, 2, -1, 0.5])
    y = X @ true_beta + np.random.randn(n) * 0.5

    # TODO: Compare batch sizes: 1 (SGD), 32, 128, 1000 (full batch)
    batch_sizes = [1, 32, 128, n]

    for bs in batch_sizes:
        pass  # Run mini-batch GD and record results

    # TODO: Plot the results


def experiment_momentum():
    """
    Experiment with momentum.

    Observe how momentum helps with:
    - Faster convergence
    - Less oscillation in narrow valleys
    """
    print("=" * 60)
    print("EXPERIMENT: Effect of Momentum")
    print("=" * 60)

    # Generate data with correlated features (creates elongated loss surface)
    n = 1000
    X1 = np.random.randn(n)
    X2 = 0.9 * X1 + 0.1 * np.random.randn(n)  # Correlated with X1
    X = np.column_stack([np.ones(n), X1, X2])
    true_beta = np.array([1, 2, 3])
    y = X @ true_beta + np.random.randn(n) * 0.5

    # TODO: Compare momentum values: 0, 0.5, 0.9, 0.99
    momentum_values = [0, 0.5, 0.9, 0.99]

    for mom in momentum_values:
        pass  # Run GD with momentum and record results

    # TODO: Plot the results


# =============================================================================
# TESTS
# =============================================================================

def test_gradient_computation():
    """Test that your gradient is correct using numerical differentiation."""
    print("=" * 60)
    print("TEST: Gradient Computation")
    print("=" * 60)

    n, p = 100, 3
    X = np.random.randn(n, p)
    y = np.random.randn(n)
    beta = np.random.randn(p)

    # Your analytical gradient
    analytical_grad = compute_gradient(X, y, beta)

    # Numerical gradient (finite differences)
    eps = 1e-5
    numerical_grad = np.zeros(p)
    for j in range(p):
        beta_plus = beta.copy()
        beta_plus[j] += eps
        beta_minus = beta.copy()
        beta_minus[j] -= eps
        numerical_grad[j] = (compute_loss(X, y, beta_plus) - compute_loss(X, y, beta_minus)) / (2 * eps)

    if analytical_grad is not None:
        diff = np.max(np.abs(analytical_grad - numerical_grad))
        print(f"Max difference between analytical and numerical gradient: {diff:.2e}")
        print(f"Test {'PASSED' if diff < 1e-5 else 'FAILED'}")
    else:
        print("Gradient function not implemented yet")

    print()


def test_convergence_to_ols():
    """Test that gradient descent converges to the OLS solution."""
    print("=" * 60)
    print("TEST: Convergence to OLS Solution")
    print("=" * 60)

    n = 200
    X = np.random.randn(n, 2)
    X = np.column_stack([np.ones(n), X])  # Add intercept
    true_beta = np.array([1, 2, 3])
    y = X @ true_beta + np.random.randn(n) * 0.5

    # OLS solution
    ols_beta = np.linalg.solve(X.T @ X, X.T @ y)

    # Gradient descent solution
    gd_beta, _ = batch_gradient_descent(X, y, learning_rate=0.1, n_iterations=5000)

    if gd_beta is not None:
        diff = np.max(np.abs(gd_beta - ols_beta))
        print(f"OLS solution: {ols_beta}")
        print(f"GD solution:  {gd_beta}")
        print(f"Max difference: {diff:.6f}")
        print(f"Test {'PASSED' if diff < 0.01 else 'FAILED'}")
    else:
        print("Gradient descent not implemented yet")

    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GRADIENT DESCENT FOR LINEAR REGRESSION")
    print("=" * 60 + "\n")

    # Run tests
    test_gradient_computation()
    test_convergence_to_ols()

    # Run experiments (uncomment when implementations are ready)
    # experiment_learning_rates()
    # experiment_batch_sizes()
    # experiment_momentum()

    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
