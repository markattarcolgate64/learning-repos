"""
CODING CHALLENGE 1: Implement OLS from Scratch
==============================================

Your mission: Implement linear regression using only NumPy.
NO sklearn, NO statsmodels - just pure linear algebra.

Difficulty: ⭐⭐

Instructions:
1. Complete all the TODO sections
2. Run the tests at the bottom to verify your implementation
3. Compare your results with sklearn to validate

Learning objectives:
- Translate the normal equations into code
- Understand matrix operations in practice
- Build intuition by implementing each piece
"""

import numpy as np

# Set random seed for reproducibility
np.random.seed(42)


class LinearRegressionFromScratch:
    """
    Ordinary Least Squares Linear Regression.

    Implements: β̂ = (X'X)^(-1) X'y

    Attributes:
        coefficients (np.ndarray): The fitted β values (including intercept)
        residuals (np.ndarray): y - ŷ after fitting
        fitted_values (np.ndarray): ŷ = Xβ̂ after fitting
    """

    def __init__(self, fit_intercept: bool = True):
        """
        Initialize the model.

        Args:
            fit_intercept: If True, add a column of ones for the intercept term
        """
        self.fit_intercept = fit_intercept
        self.coefficients = None
        self.residuals = None
        self.fitted_values = None
        self._X_with_intercept = None

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """
        Add a column of ones to X for the intercept term.

        Args:
            X: Feature matrix of shape (n_samples, n_features)

        Returns:
            X with intercept column prepended, shape (n_samples, n_features + 1)
        """
        # TODO: Add a column of ones to the LEFT of X
        # Hint: Use np.column_stack or np.hstack with np.ones

        pass  # Replace with your implementation

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearRegressionFromScratch':
        """
        Fit the linear regression model using the normal equations.

        The normal equations: β̂ = (X'X)^(-1) X'y

        Args:
            X: Feature matrix of shape (n_samples, n_features)
            y: Target vector of shape (n_samples,)

        Returns:
            self (for method chaining)
        """
        # Step 1: Handle intercept
        if self.fit_intercept:
            X = self._add_intercept(X)

        self._X_with_intercept = X

        # TODO: Implement the normal equations
        # Step 2: Compute X'X (X transpose times X)
        XtX = None  # Your code here

        # Step 3: Compute X'y (X transpose times y)
        Xty = None  # Your code here

        # Step 4: Solve for β̂ = (X'X)^(-1) X'y
        # Hint: Use np.linalg.solve(A, b) instead of np.linalg.inv(A) @ b
        # (It's more numerically stable)
        self.coefficients = None  # Your code here

        # Step 5: Compute fitted values ŷ = Xβ̂
        self.fitted_values = None  # Your code here

        # Step 6: Compute residuals e = y - ŷ
        self.residuals = None  # Your code here

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using the fitted model.

        Args:
            X: Feature matrix of shape (n_samples, n_features)

        Returns:
            Predicted values of shape (n_samples,)
        """
        if self.coefficients is None:
            raise ValueError("Model has not been fitted yet!")

        # TODO: Add intercept if needed and compute predictions

        pass  # Replace with your implementation

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Compute R² (coefficient of determination).

        R² = 1 - RSS/TSS = 1 - Σ(yᵢ - ŷᵢ)² / Σ(yᵢ - ȳ)²

        Args:
            X: Feature matrix
            y: True target values

        Returns:
            R² score
        """
        # TODO: Implement R² calculation

        pass  # Replace with your implementation


class LinearRegressionStatistics:
    """
    Compute statistical measures for a fitted linear regression.

    This class takes a fitted LinearRegressionFromScratch object
    and computes various statistics.
    """

    def __init__(self, model: LinearRegressionFromScratch, X: np.ndarray, y: np.ndarray):
        """
        Initialize with a fitted model and data.
        """
        self.model = model
        self.X = X
        self.y = y
        self.n = len(y)

        # Get the design matrix (with intercept if applicable)
        self.X_design = model._X_with_intercept
        self.p = self.X_design.shape[1]  # Number of parameters including intercept

    def compute_rss(self) -> float:
        """
        Compute Residual Sum of Squares: RSS = Σeᵢ²

        Returns:
            RSS value
        """
        # TODO: Implement RSS calculation

        pass

    def compute_tss(self) -> float:
        """
        Compute Total Sum of Squares: TSS = Σ(yᵢ - ȳ)²

        Returns:
            TSS value
        """
        # TODO: Implement TSS calculation

        pass

    def compute_mse(self) -> float:
        """
        Compute Mean Squared Error (unbiased): s² = RSS / (n - p)

        This is the unbiased estimator of σ².

        Returns:
            MSE value
        """
        # TODO: Implement MSE calculation

        pass

    def compute_standard_errors(self) -> np.ndarray:
        """
        Compute standard errors for each coefficient.

        SE(β̂ⱼ) = s * sqrt([(X'X)^(-1)]ⱼⱼ)

        Returns:
            Array of standard errors for each coefficient
        """
        # TODO: Implement standard error calculation
        # Hint:
        # 1. Compute (X'X)^(-1)
        # 2. Extract the diagonal
        # 3. Take sqrt and multiply by s (the standard error of the regression)

        pass

    def compute_t_statistics(self) -> np.ndarray:
        """
        Compute t-statistics for testing H₀: βⱼ = 0

        t = β̂ⱼ / SE(β̂ⱼ)

        Returns:
            Array of t-statistics
        """
        # TODO: Implement t-statistic calculation

        pass

    def compute_p_values(self) -> np.ndarray:
        """
        Compute two-sided p-values for the t-statistics.

        p = 2 * P(T > |t|) where T ~ t_{n-p}

        Returns:
            Array of p-values
        """
        from scipy import stats

        # TODO: Implement p-value calculation
        # Hint: Use stats.t.sf() for survival function (1 - CDF)

        pass

    def compute_f_statistic(self) -> tuple:
        """
        Compute the F-statistic for overall model significance.

        H₀: All slope coefficients = 0

        F = [R² / (p-1)] / [(1-R²) / (n-p)]

        Returns:
            Tuple of (F-statistic, p-value)
        """
        from scipy import stats

        # TODO: Implement F-statistic calculation

        pass

    def compute_confidence_intervals(self, alpha: float = 0.05) -> np.ndarray:
        """
        Compute confidence intervals for each coefficient.

        CI = β̂ⱼ ± t_{α/2, n-p} * SE(β̂ⱼ)

        Args:
            alpha: Significance level (default 0.05 for 95% CI)

        Returns:
            Array of shape (p, 2) with lower and upper bounds
        """
        from scipy import stats

        # TODO: Implement confidence interval calculation

        pass

    def summary(self) -> str:
        """
        Generate a summary table similar to statsmodels.

        Returns:
            Formatted string with regression results
        """
        # TODO: Create a nice summary output
        # This is optional but good practice!

        pass


# =============================================================================
# TEST YOUR IMPLEMENTATION
# =============================================================================

def test_simple_regression():
    """Test with simple linear regression (one predictor)."""
    print("=" * 60)
    print("TEST 1: Simple Linear Regression")
    print("=" * 60)

    # Generate data: y = 2 + 3*x + noise
    n = 100
    X = np.random.randn(n, 1)
    y = 2 + 3 * X.squeeze() + np.random.randn(n) * 0.5

    # Fit your model
    model = LinearRegressionFromScratch()
    model.fit(X, y)

    print(f"\nYour coefficients: {model.coefficients}")
    print(f"Expected (approximately): [2, 3]")

    # Compare with sklearn
    try:
        from sklearn.linear_model import LinearRegression
        sklearn_model = LinearRegression()
        sklearn_model.fit(X, y)
        print(f"\nsklearn intercept: {sklearn_model.intercept_:.4f}")
        print(f"sklearn coefficient: {sklearn_model.coef_[0]:.4f}")

        if model.coefficients is not None:
            print(f"\nDifference from sklearn:")
            print(f"  Intercept diff: {abs(model.coefficients[0] - sklearn_model.intercept_):.6f}")
            print(f"  Slope diff: {abs(model.coefficients[1] - sklearn_model.coef_[0]):.6f}")
    except ImportError:
        print("\n(sklearn not available for comparison)")

    print()


def test_multiple_regression():
    """Test with multiple predictors."""
    print("=" * 60)
    print("TEST 2: Multiple Linear Regression")
    print("=" * 60)

    # Generate data: y = 1 + 2*x1 - 0.5*x2 + 3*x3 + noise
    n = 200
    X = np.random.randn(n, 3)
    true_beta = np.array([1, 2, -0.5, 3])  # intercept, x1, x2, x3
    y = true_beta[0] + X @ true_beta[1:] + np.random.randn(n) * 0.5

    # Fit your model
    model = LinearRegressionFromScratch()
    model.fit(X, y)

    print(f"\nYour coefficients: {model.coefficients}")
    print(f"True coefficients: {true_beta}")

    # Test R² score
    r2 = model.score(X, y)
    print(f"\nYour R² score: {r2}")

    print()


def test_statistics():
    """Test statistical computations."""
    print("=" * 60)
    print("TEST 3: Statistical Measures")
    print("=" * 60)

    # Generate data
    n = 100
    X = np.random.randn(n, 2)
    y = 1 + 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(n)

    # Fit model
    model = LinearRegressionFromScratch()
    model.fit(X, y)

    # Compute statistics
    stats_obj = LinearRegressionStatistics(model, X, y)

    print("\nYour computed statistics:")
    print(f"  RSS: {stats_obj.compute_rss()}")
    print(f"  TSS: {stats_obj.compute_tss()}")
    print(f"  MSE: {stats_obj.compute_mse()}")
    print(f"  Standard errors: {stats_obj.compute_standard_errors()}")
    print(f"  t-statistics: {stats_obj.compute_t_statistics()}")
    print(f"  p-values: {stats_obj.compute_p_values()}")
    print(f"  F-statistic: {stats_obj.compute_f_statistic()}")
    print(f"  95% CIs:\n{stats_obj.compute_confidence_intervals()}")

    # Compare with statsmodels if available
    try:
        import statsmodels.api as sm
        X_sm = sm.add_constant(X)
        sm_model = sm.OLS(y, X_sm).fit()
        print("\n\nstatsmodels summary for comparison:")
        print(sm_model.summary())
    except ImportError:
        print("\n(statsmodels not available for comparison)")

    print()


def test_prediction():
    """Test prediction functionality."""
    print("=" * 60)
    print("TEST 4: Prediction")
    print("=" * 60)

    # Training data
    X_train = np.array([[1], [2], [3], [4], [5]])
    y_train = np.array([2.1, 4.0, 5.9, 8.1, 9.8])

    # Test data
    X_test = np.array([[6], [7], [8]])

    # Fit and predict
    model = LinearRegressionFromScratch()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"\nYour predictions for x = [6, 7, 8]: {predictions}")
    print(f"If y ≈ 2x, expected around: [12, 14, 16]")

    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60 + "\n")

    test_simple_regression()
    test_multiple_regression()
    test_statistics()
    test_prediction()

    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60)
    print("\nNote: If you see 'None' for any values, that means")
    print("you still need to implement that part!")
