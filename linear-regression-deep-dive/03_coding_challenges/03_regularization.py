"""
CODING CHALLENGE 3: Implement Regularized Regression
====================================================

Your mission: Implement Ridge, Lasso, and Elastic Net regression from scratch.

Difficulty: ⭐⭐⭐

Instructions:
1. Implement Ridge regression (L2 penalty) - closed form
2. Implement Lasso regression (L1 penalty) - coordinate descent
3. Implement Elastic Net (L1 + L2) - coordinate descent
4. Implement cross-validation for hyperparameter selection

Learning objectives:
- Understand how regularization prevents overfitting
- See the difference between L1 and L2 penalties
- Learn coordinate descent optimization
- Practice cross-validation
"""

import numpy as np
from typing import Tuple, List, Optional
import matplotlib.pyplot as plt

np.random.seed(42)


# =============================================================================
# PART 1: RIDGE REGRESSION (L2 Regularization)
# =============================================================================

class RidgeRegression:
    """
    Ridge Regression: minimize ||y - Xβ||² + λ||β||²

    Has a closed-form solution: β̂ = (X'X + λI)⁻¹X'y

    Note: We typically don't penalize the intercept.
    """

    def __init__(self, alpha: float = 1.0, fit_intercept: bool = True):
        """
        Args:
            alpha: Regularization strength (λ in the formula)
            fit_intercept: Whether to fit an intercept term
        """
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.coefficients = None
        self.intercept = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RidgeRegression':
        """
        Fit the Ridge regression model.

        The closed-form solution (not penalizing intercept):
        1. Center X and y
        2. Solve β̂ = (X'X + λI)⁻¹X'y on centered data
        3. Recover intercept from means

        Args:
            X: Feature matrix (n, p)
            y: Target vector (n,)

        Returns:
            self
        """
        n, p = X.shape

        # TODO: Implement Ridge regression
        # Step 1: If fitting intercept, center the data
        if self.fit_intercept:
            X_mean = None  # Your code
            y_mean = None  # Your code
            X_centered = None  # Your code
            y_centered = None  # Your code
        else:
            X_centered = X
            y_centered = y

        # Step 2: Compute (X'X + λI)⁻¹X'y
        # Hint: Use np.linalg.solve for numerical stability

        XtX = None  # Your code
        penalty_matrix = None  # λI
        Xty = None  # Your code

        self.coefficients = None  # Solve the system

        # Step 3: Recover intercept
        if self.fit_intercept:
            self.intercept = None  # ȳ - x̄'β̂
        else:
            self.intercept = 0.0

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the fitted model."""
        # TODO: Implement prediction

        pass

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute R² score."""
        # TODO: Implement R² calculation

        pass


# =============================================================================
# PART 2: SOFT THRESHOLDING (for Lasso)
# =============================================================================

def soft_threshold(x: float, threshold: float) -> float:
    """
    Soft thresholding operator (proximal operator for L1 norm).

    S(x, λ) = sign(x) * max(|x| - λ, 0)

    This is the key operation in Lasso optimization.

    Args:
        x: Input value
        threshold: Threshold value (λ)

    Returns:
        Soft-thresholded value
    """
    # TODO: Implement soft thresholding
    # Hint: Consider three cases: x > threshold, x < -threshold, |x| <= threshold

    pass


# =============================================================================
# PART 3: LASSO REGRESSION (L1 Regularization)
# =============================================================================

class LassoRegression:
    """
    Lasso Regression: minimize (1/2n)||y - Xβ||² + λ||β||₁

    No closed-form solution! We use coordinate descent.

    Coordinate descent updates one coefficient at a time while holding
    others fixed. For Lasso, each update has a closed form using
    soft thresholding.
    """

    def __init__(
        self,
        alpha: float = 1.0,
        fit_intercept: bool = True,
        max_iter: int = 1000,
        tol: float = 1e-4
    ):
        """
        Args:
            alpha: Regularization strength (λ)
            fit_intercept: Whether to fit an intercept
            max_iter: Maximum coordinate descent iterations
            tol: Convergence tolerance
        """
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.coefficients = None
        self.intercept = None
        self.n_iter_ = 0

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LassoRegression':
        """
        Fit Lasso using coordinate descent.

        The coordinate descent update for coefficient j is:

        ρⱼ = Σᵢ xᵢⱼ(yᵢ - Σₖ≠ⱼ xᵢₖβₖ)  [partial residual]
        zⱼ = Σᵢ xᵢⱼ²                    [squared norm of feature j]
        βⱼ = S(ρⱼ, nλ) / zⱼ            [soft threshold and normalize]

        Args:
            X: Feature matrix (n, p)
            y: Target vector (n,)

        Returns:
            self
        """
        n, p = X.shape

        # TODO: Implement Lasso coordinate descent

        # Step 1: Standardize features (important for Lasso!)
        if self.fit_intercept:
            X_mean = None  # Your code
            y_mean = None  # Your code
            X_std = None  # Standard deviation of each feature
            # Standardize: X_scaled = (X - X_mean) / X_std
            X_scaled = None  # Your code
            y_centered = None  # Your code
        else:
            X_scaled = X
            y_centered = y
            X_std = np.ones(p)

        # Step 2: Initialize coefficients
        beta = np.zeros(p)

        # Step 3: Precompute z values (squared column norms)
        z = None  # Your code: z[j] = sum of x_ij^2 for each j

        # Step 4: Coordinate descent loop
        for iteration in range(self.max_iter):
            beta_old = beta.copy()

            for j in range(p):
                # TODO: Implement the coordinate descent update for β_j

                # Compute partial residual (residual without feature j's contribution)
                # r_j = y - X @ beta + X[:, j] * beta[j]

                # Compute ρ_j = X[:, j]' @ r_j

                # Apply soft thresholding
                # beta[j] = soft_threshold(rho_j, n * self.alpha) / z[j]

                pass  # Your implementation

            # Check for convergence
            if np.max(np.abs(beta - beta_old)) < self.tol:
                break

        self.n_iter_ = iteration + 1

        # Step 5: Transform coefficients back to original scale
        self.coefficients = None  # beta / X_std

        # Step 6: Compute intercept
        if self.fit_intercept:
            self.intercept = None  # ȳ - x̄'β̂
        else:
            self.intercept = 0.0

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the fitted model."""
        # TODO: Implement prediction

        pass

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute R² score."""
        # TODO: Implement R² calculation

        pass


# =============================================================================
# PART 4: ELASTIC NET (L1 + L2 Regularization)
# =============================================================================

class ElasticNet:
    """
    Elastic Net: minimize (1/2n)||y - Xβ||² + λ₁||β||₁ + λ₂||β||²

    Often parameterized as:
    minimize (1/2n)||y - Xβ||² + α * [ρ||β||₁ + (1-ρ)/2 ||β||²]

    where α is total regularization and ρ ∈ [0,1] is the L1 ratio.

    Uses coordinate descent like Lasso, but the update formula changes.
    """

    def __init__(
        self,
        alpha: float = 1.0,
        l1_ratio: float = 0.5,
        fit_intercept: bool = True,
        max_iter: int = 1000,
        tol: float = 1e-4
    ):
        """
        Args:
            alpha: Total regularization strength
            l1_ratio: Ratio of L1 penalty (0 = Ridge, 1 = Lasso)
            fit_intercept: Whether to fit an intercept
            max_iter: Maximum iterations
            tol: Convergence tolerance
        """
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.coefficients = None
        self.intercept = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ElasticNet':
        """
        Fit Elastic Net using coordinate descent.

        The update for coefficient j is:
        βⱼ = S(ρⱼ, nλ₁) / (zⱼ + nλ₂)

        where λ₁ = α * l1_ratio and λ₂ = α * (1 - l1_ratio)

        Args:
            X: Feature matrix (n, p)
            y: Target vector (n,)

        Returns:
            self
        """
        # TODO: Implement Elastic Net
        # This is very similar to Lasso, but with a modified update formula

        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the fitted model."""
        # TODO: Implement prediction

        pass


# =============================================================================
# PART 5: CROSS-VALIDATION
# =============================================================================

def cross_validation_score(
    model_class,
    X: np.ndarray,
    y: np.ndarray,
    alpha: float,
    n_folds: int = 5,
    **model_kwargs
) -> float:
    """
    Compute cross-validated MSE for a given alpha.

    Args:
        model_class: The model class (RidgeRegression, LassoRegression, etc.)
        X: Feature matrix
        y: Target vector
        alpha: Regularization parameter to test
        n_folds: Number of CV folds
        **model_kwargs: Additional arguments for the model

    Returns:
        Mean cross-validated MSE
    """
    n = len(y)
    indices = np.arange(n)
    np.random.shuffle(indices)
    fold_size = n // n_folds

    mse_scores = []

    # TODO: Implement k-fold cross-validation
    for fold in range(n_folds):
        # Create train/test split for this fold
        # test_idx = indices in this fold
        # train_idx = all other indices

        # Fit model on training data

        # Predict on test data

        # Compute MSE

        pass

    return np.mean(mse_scores)


def find_best_alpha(
    model_class,
    X: np.ndarray,
    y: np.ndarray,
    alphas: np.ndarray,
    n_folds: int = 5,
    **model_kwargs
) -> Tuple[float, List[float]]:
    """
    Find the best alpha using cross-validation.

    Args:
        model_class: The model class
        X: Feature matrix
        y: Target vector
        alphas: Array of alpha values to try
        n_folds: Number of CV folds
        **model_kwargs: Additional model arguments

    Returns:
        Tuple of (best_alpha, list of cv_scores for each alpha)
    """
    # TODO: Implement alpha selection via cross-validation

    cv_scores = []
    for alpha in alphas:
        pass  # Compute CV score for this alpha

    best_alpha = None  # Alpha with lowest CV score
    return best_alpha, cv_scores


# =============================================================================
# PART 6: REGULARIZATION PATH
# =============================================================================

def compute_regularization_path(
    model_class,
    X: np.ndarray,
    y: np.ndarray,
    alphas: np.ndarray,
    **model_kwargs
) -> np.ndarray:
    """
    Compute coefficients for a sequence of regularization parameters.

    This creates the classic "regularization path" plot.

    Args:
        model_class: The model class
        X: Feature matrix
        y: Target vector
        alphas: Array of alpha values (typically log-spaced)
        **model_kwargs: Additional model arguments

    Returns:
        Array of shape (len(alphas), n_features) containing coefficients
    """
    n, p = X.shape
    coef_path = np.zeros((len(alphas), p))

    # TODO: Fit model for each alpha and store coefficients
    for i, alpha in enumerate(alphas):
        pass  # Fit model and store coefficients

    return coef_path


def plot_regularization_path(
    alphas: np.ndarray,
    coef_path: np.ndarray,
    feature_names: Optional[List[str]] = None
):
    """
    Plot the regularization path.

    Args:
        alphas: Array of alpha values
        coef_path: Array of shape (len(alphas), n_features)
        feature_names: Optional names for features
    """
    # TODO: Create a plot showing how coefficients change with alpha
    # X-axis: log(alpha)
    # Y-axis: coefficient values
    # Each feature is a different line

    pass


# =============================================================================
# EXPERIMENTS
# =============================================================================

def experiment_ridge_vs_ols():
    """Compare Ridge to OLS when p > n (more features than samples)."""
    print("=" * 60)
    print("EXPERIMENT: Ridge vs OLS (High-dimensional)")
    print("=" * 60)

    # Create high-dimensional data where OLS fails
    n, p = 50, 100  # More features than samples!
    X = np.random.randn(n, p)
    true_beta = np.zeros(p)
    true_beta[:5] = [1, -2, 3, -4, 5]  # Only 5 features matter
    y = X @ true_beta + np.random.randn(n) * 0.5

    # TODO: Show that OLS fails (singular matrix)
    # Show that Ridge works

    pass


def experiment_lasso_sparsity():
    """Show that Lasso produces sparse solutions."""
    print("=" * 60)
    print("EXPERIMENT: Lasso Sparsity")
    print("=" * 60)

    # Create data with only a few relevant features
    n, p = 200, 20
    X = np.random.randn(n, p)
    true_beta = np.zeros(p)
    true_beta[[0, 5, 10]] = [3, -2, 4]  # Only 3 features matter
    y = X @ true_beta + np.random.randn(n) * 0.5

    # TODO: Fit Lasso and show it correctly identifies sparse structure
    # Compare to Ridge which keeps all coefficients non-zero

    pass


def experiment_elastic_net():
    """Show Elastic Net behavior with correlated features."""
    print("=" * 60)
    print("EXPERIMENT: Elastic Net with Correlated Features")
    print("=" * 60)

    # Create correlated features
    n = 200
    X1 = np.random.randn(n)
    X2 = X1 + np.random.randn(n) * 0.1  # X2 ≈ X1
    X3 = np.random.randn(n)
    X = np.column_stack([X1, X2, X3])
    y = 3 * X1 + 2 * X3 + np.random.randn(n) * 0.5

    # TODO: Compare Lasso vs Elastic Net
    # Lasso tends to select one of correlated features arbitrarily
    # Elastic Net tends to select both

    pass


# =============================================================================
# TESTS
# =============================================================================

def test_soft_threshold():
    """Test soft thresholding function."""
    print("TEST: Soft Thresholding")

    test_cases = [
        (5, 2, 3),    # 5 - 2 = 3
        (-5, 2, -3),  # -(-5 - 2) = -3
        (1, 2, 0),    # |1| < 2, so 0
        (-1, 2, 0),   # |-1| < 2, so 0
    ]

    all_passed = True
    for x, thresh, expected in test_cases:
        result = soft_threshold(x, thresh)
        if result is not None:
            passed = np.isclose(result, expected)
            print(f"  S({x}, {thresh}) = {result} (expected {expected}) {'✓' if passed else '✗'}")
            all_passed = all_passed and passed
        else:
            print(f"  Not implemented")
            all_passed = False

    print(f"Test {'PASSED' if all_passed else 'FAILED'}\n")


def test_ridge_regression():
    """Test Ridge regression implementation."""
    print("TEST: Ridge Regression")

    n = 100
    X = np.random.randn(n, 3)
    y = 1 + 2*X[:, 0] - X[:, 1] + 0.5*X[:, 2] + np.random.randn(n) * 0.3

    model = RidgeRegression(alpha=1.0)
    model.fit(X, y)

    if model.coefficients is not None:
        print(f"  Coefficients: {model.coefficients}")
        print(f"  Intercept: {model.intercept}")

        # Compare with sklearn if available
        try:
            from sklearn.linear_model import Ridge
            sklearn_ridge = Ridge(alpha=1.0)
            sklearn_ridge.fit(X, y)
            print(f"  sklearn coef: {sklearn_ridge.coef_}")
            print(f"  sklearn intercept: {sklearn_ridge.intercept_}")
        except ImportError:
            pass
    else:
        print("  Not implemented")

    print()


def test_lasso_regression():
    """Test Lasso regression implementation."""
    print("TEST: Lasso Regression")

    n = 200
    X = np.random.randn(n, 10)
    true_beta = np.array([3, -2, 0, 0, 1.5, 0, 0, 0, 0, 0])
    y = X @ true_beta + np.random.randn(n) * 0.5

    model = LassoRegression(alpha=0.1, max_iter=1000)
    model.fit(X, y)

    if model.coefficients is not None:
        print(f"  True beta:    {true_beta}")
        print(f"  Fitted beta:  {np.round(model.coefficients, 2)}")
        print(f"  Intercept:    {model.intercept:.4f}")
        print(f"  Iterations:   {model.n_iter_}")

        # Count near-zero coefficients
        n_zero = np.sum(np.abs(model.coefficients) < 0.01)
        print(f"  Near-zero coefficients: {n_zero}/10")
    else:
        print("  Not implemented")

    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("REGULARIZED REGRESSION")
    print("=" * 60 + "\n")

    test_soft_threshold()
    test_ridge_regression()
    test_lasso_regression()

    # Uncomment to run experiments when implementations are ready
    # experiment_ridge_vs_ols()
    # experiment_lasso_sparsity()
    # experiment_elastic_net()

    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
