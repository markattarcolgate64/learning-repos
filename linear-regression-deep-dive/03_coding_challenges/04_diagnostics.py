"""
CODING CHALLENGE 4: Regression Diagnostics
==========================================

Your mission: Implement tools to diagnose and validate linear regression models.

Difficulty: ⭐⭐⭐

A model is only as good as its assumptions. This challenge focuses on:
1. Checking assumptions (linearity, homoskedasticity, normality)
2. Detecting influential points
3. Identifying multicollinearity
4. Assessing model fit

Learning objectives:
- Understand what can go wrong with regression
- Build diagnostic tools used by practicing statisticians
- Learn to interpret diagnostic plots
"""

import numpy as np
from typing import Tuple, Dict, Optional, List
import matplotlib.pyplot as plt

np.random.seed(42)


# =============================================================================
# PART 1: RESIDUAL ANALYSIS
# =============================================================================

class RegressionDiagnostics:
    """
    Comprehensive diagnostics for a fitted linear regression model.
    """

    def __init__(self, X: np.ndarray, y: np.ndarray, beta: np.ndarray, fit_intercept: bool = True):
        """
        Initialize with fitted model.

        Args:
            X: Original feature matrix (n, p) - WITHOUT intercept column
            y: Target vector (n,)
            beta: Fitted coefficients (including intercept if fit_intercept=True)
            fit_intercept: Whether the model included an intercept
        """
        self.X_original = X
        self.y = y
        self.beta = beta
        self.fit_intercept = fit_intercept

        # Build design matrix
        if fit_intercept:
            self.X = np.column_stack([np.ones(len(y)), X])
        else:
            self.X = X

        self.n, self.p = self.X.shape

        # Compute basic quantities
        self.fitted_values = self.X @ self.beta
        self.residuals = self.y - self.fitted_values

    def compute_hat_matrix(self) -> np.ndarray:
        """
        Compute the hat matrix H = X(X'X)^(-1)X'.

        The diagonal elements hᵢᵢ are called "leverage" values.
        They measure how much yᵢ influences ŷᵢ.

        Returns:
            Hat matrix of shape (n, n)
        """
        # TODO: Implement hat matrix computation
        # H = X @ (X'X)^(-1) @ X'

        pass

    def compute_leverage(self) -> np.ndarray:
        """
        Compute leverage values (diagonal of hat matrix).

        High leverage points have unusual X values.
        Rule of thumb: leverage > 2p/n is high.

        Returns:
            Leverage values of shape (n,)
        """
        # TODO: Compute leverage values
        # Hint: You can compute just the diagonal more efficiently:
        # h_ii = x_i' (X'X)^(-1) x_i

        pass

    def compute_standardized_residuals(self) -> np.ndarray:
        """
        Compute internally studentized (standardized) residuals.

        rᵢ = eᵢ / (s * sqrt(1 - hᵢᵢ))

        where s² = RSS / (n - p)

        Returns:
            Standardized residuals of shape (n,)
        """
        # TODO: Implement standardized residuals

        pass

    def compute_studentized_residuals(self) -> np.ndarray:
        """
        Compute externally studentized (deleted) residuals.

        tᵢ = eᵢ / (s₍₋ᵢ₎ * sqrt(1 - hᵢᵢ))

        where s₍₋ᵢ₎ is the residual standard error computed WITHOUT observation i.

        These follow a t-distribution under the null hypothesis.

        Returns:
            Studentized residuals of shape (n,)
        """
        # TODO: Implement studentized residuals
        # Hint: There's a formula that avoids refitting n times:
        # t_i = r_i * sqrt((n - p - 1) / (n - p - r_i²))
        # where r_i is the internally studentized residual

        pass


# =============================================================================
# PART 2: INFLUENCE MEASURES
# =============================================================================

class InfluenceMeasures:
    """
    Measures of how much each observation influences the regression.
    """

    def __init__(self, diagnostics: RegressionDiagnostics):
        self.diag = diagnostics

    def compute_cooks_distance(self) -> np.ndarray:
        """
        Compute Cook's distance for each observation.

        Cook's D measures the change in all fitted values when
        observation i is removed:

        Dᵢ = Σⱼ(ŷⱼ - ŷⱼ₍₋ᵢ₎)² / (p * MSE)

        Can be computed as:
        Dᵢ = rᵢ² * hᵢᵢ / (p * (1 - hᵢᵢ))

        where rᵢ is the standardized residual.

        Rule of thumb: D > 4/n or D > 1 indicates influential point.

        Returns:
            Cook's distance values of shape (n,)
        """
        # TODO: Implement Cook's distance

        pass

    def compute_dffits(self) -> np.ndarray:
        """
        Compute DFFITS (Difference in Fits).

        DFFITS measures how much ŷᵢ changes when observation i is removed:

        DFFITSᵢ = (ŷᵢ - ŷᵢ₍₋ᵢ₎) / (s₍₋ᵢ₎ * sqrt(hᵢᵢ))

        Can be computed as:
        DFFITSᵢ = tᵢ * sqrt(hᵢᵢ / (1 - hᵢᵢ))

        where tᵢ is the externally studentized residual.

        Rule of thumb: |DFFITS| > 2*sqrt(p/n) indicates influential point.

        Returns:
            DFFITS values of shape (n,)
        """
        # TODO: Implement DFFITS

        pass

    def compute_dfbetas(self) -> np.ndarray:
        """
        Compute DFBETAS for each coefficient and observation.

        DFBETASᵢⱼ measures how much β̂ⱼ changes when observation i is removed:

        DFBETASᵢⱼ = (β̂ⱼ - β̂ⱼ₍₋ᵢ₎) / (s₍₋ᵢ₎ * sqrt[(X'X)⁻¹]ⱼⱼ)

        Rule of thumb: |DFBETAS| > 2/sqrt(n) indicates influential point.

        Returns:
            DFBETAS matrix of shape (n, p)
        """
        # TODO: Implement DFBETAS
        # This one is more complex - you'll need (X'X)^(-1)

        pass


# =============================================================================
# PART 3: MULTICOLLINEARITY DIAGNOSTICS
# =============================================================================

class MulticollinearityDiagnostics:
    """
    Diagnose multicollinearity issues in the design matrix.
    """

    def __init__(self, X: np.ndarray, feature_names: Optional[List[str]] = None):
        """
        Args:
            X: Feature matrix (n, p) - WITHOUT intercept
            feature_names: Optional names for features
        """
        self.X = X
        self.n, self.p = X.shape
        self.feature_names = feature_names or [f"X{i}" for i in range(self.p)]

    def compute_correlation_matrix(self) -> np.ndarray:
        """
        Compute pairwise correlations between features.

        Returns:
            Correlation matrix of shape (p, p)
        """
        # TODO: Implement correlation matrix
        # Hint: Use np.corrcoef or compute manually

        pass

    def compute_vif(self) -> np.ndarray:
        """
        Compute Variance Inflation Factor for each feature.

        VIF measures how much the variance of β̂ⱼ is inflated due to
        correlation with other predictors.

        VIFⱼ = 1 / (1 - Rⱼ²)

        where Rⱼ² is the R² from regressing Xⱼ on all other features.

        Rule of thumb: VIF > 5 or 10 indicates multicollinearity.

        Returns:
            VIF values of shape (p,)
        """
        # TODO: Implement VIF computation
        # For each feature j:
        # 1. Regress X_j on all other features
        # 2. Compute R²
        # 3. VIF_j = 1 / (1 - R²)

        pass

    def compute_condition_number(self) -> float:
        """
        Compute the condition number of X'X.

        condition_number = sqrt(λ_max / λ_min)

        where λ are eigenvalues of X'X.

        Rule of thumb: condition number > 30 indicates multicollinearity.

        Returns:
            Condition number
        """
        # TODO: Implement condition number computation

        pass

    def compute_eigenvalue_decomposition(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenvalues and condition indices of X'X.

        Condition indices: sqrt(λ_max / λ_k) for each eigenvalue λ_k.

        Returns:
            Tuple of (eigenvalues, condition_indices)
        """
        # TODO: Implement eigenvalue analysis

        pass


# =============================================================================
# PART 4: DIAGNOSTIC PLOTS
# =============================================================================

class DiagnosticPlots:
    """
    Create standard diagnostic plots for regression.
    """

    def __init__(self, diagnostics: RegressionDiagnostics):
        self.diag = diagnostics

    def residuals_vs_fitted(self, ax=None):
        """
        Plot residuals vs fitted values.

        What to look for:
        - Random scatter around 0: good
        - Curved pattern: nonlinearity
        - Funnel shape: heteroskedasticity

        Args:
            ax: Matplotlib axis (creates new figure if None)
        """
        # TODO: Create residuals vs fitted plot

        pass

    def qq_plot(self, ax=None):
        """
        Normal Q-Q plot of residuals.

        What to look for:
        - Points on diagonal line: normality
        - S-curve: heavy/light tails
        - Deviations at ends: outliers

        Args:
            ax: Matplotlib axis
        """
        # TODO: Create Q-Q plot
        # Hint: Sort residuals, compute theoretical quantiles using
        # scipy.stats.norm.ppf((i - 0.5) / n)

        pass

    def scale_location(self, ax=None):
        """
        Scale-Location plot (sqrt of standardized residuals vs fitted).

        Good for detecting heteroskedasticity.
        Should show random scatter with no trend.

        Args:
            ax: Matplotlib axis
        """
        # TODO: Create scale-location plot

        pass

    def residuals_vs_leverage(self, ax=None):
        """
        Residuals vs leverage plot with Cook's distance contours.

        Identifies influential points that are both outliers AND
        have high leverage.

        Args:
            ax: Matplotlib axis
        """
        # TODO: Create residuals vs leverage plot
        # Include Cook's distance contours at D = 0.5 and D = 1

        pass

    def component_plus_residual(self, feature_idx: int, ax=None):
        """
        Component + Residual plot (partial residual plot).

        For feature Xⱼ, plot:
        - X-axis: Xⱼ
        - Y-axis: e + β̂ⱼ * Xⱼ (partial residual)

        Helps detect nonlinear relationships.

        Args:
            feature_idx: Index of feature to plot
            ax: Matplotlib axis
        """
        # TODO: Create component + residual plot

        pass

    def four_panel_diagnostic(self):
        """
        Create the classic 4-panel diagnostic plot.

        1. Residuals vs Fitted
        2. Q-Q Plot
        3. Scale-Location
        4. Residuals vs Leverage
        """
        # TODO: Create 2x2 figure with all four diagnostic plots

        pass


# =============================================================================
# PART 5: ASSUMPTION TESTS
# =============================================================================

class AssumptionTests:
    """
    Statistical tests for regression assumptions.
    """

    def __init__(self, diagnostics: RegressionDiagnostics):
        self.diag = diagnostics

    def breusch_pagan_test(self) -> Tuple[float, float]:
        """
        Breusch-Pagan test for heteroskedasticity.

        H₀: Constant variance (homoskedasticity)
        H₁: Variance depends on X

        Procedure:
        1. Fit the original regression, get residuals e
        2. Regress e² on X
        3. Test statistic = n * R² from step 2
        4. Under H₀, statistic ~ χ²(p-1)

        Returns:
            Tuple of (test_statistic, p_value)
        """
        from scipy import stats

        # TODO: Implement Breusch-Pagan test

        pass

    def durbin_watson_test(self) -> float:
        """
        Durbin-Watson test for autocorrelation in residuals.

        DW = Σᵢ(eᵢ - eᵢ₋₁)² / Σᵢeᵢ²

        DW ≈ 2: No autocorrelation
        DW < 2: Positive autocorrelation
        DW > 2: Negative autocorrelation

        Returns:
            Durbin-Watson statistic
        """
        # TODO: Implement Durbin-Watson statistic

        pass

    def shapiro_wilk_test(self) -> Tuple[float, float]:
        """
        Shapiro-Wilk test for normality of residuals.

        H₀: Residuals are normally distributed

        Returns:
            Tuple of (test_statistic, p_value)
        """
        from scipy import stats

        # TODO: Implement (or use scipy's shapiro)

        pass

    def reset_test(self, powers: List[int] = [2, 3]) -> Tuple[float, float]:
        """
        Ramsey RESET test for functional form misspecification.

        Tests whether adding powers of fitted values improves the model.

        H₀: Model is correctly specified
        H₁: Nonlinearity exists

        Args:
            powers: Powers of ŷ to add (default [2, 3])

        Returns:
            Tuple of (F_statistic, p_value)
        """
        from scipy import stats

        # TODO: Implement RESET test
        # 1. Fit original model, get ŷ
        # 2. Fit augmented model with ŷ², ŷ³, etc.
        # 3. F-test comparing the two models

        pass


# =============================================================================
# TESTS AND EXAMPLES
# =============================================================================

def example_good_model():
    """Example with a well-behaved model."""
    print("=" * 60)
    print("EXAMPLE: Well-behaved Model")
    print("=" * 60)

    # Generate clean data
    n = 200
    X = np.random.randn(n, 2)
    beta_true = np.array([1, 2, -1])  # intercept, x1, x2
    y = beta_true[0] + X @ beta_true[1:] + np.random.randn(n) * 0.5

    # Fit model (using normal equations)
    X_design = np.column_stack([np.ones(n), X])
    beta_hat = np.linalg.solve(X_design.T @ X_design, X_design.T @ y)

    # Create diagnostics
    diag = RegressionDiagnostics(X, y, beta_hat, fit_intercept=True)

    # TODO: Compute and print diagnostic measures

    print()


def example_heteroskedasticity():
    """Example with heteroskedasticity."""
    print("=" * 60)
    print("EXAMPLE: Heteroskedasticity")
    print("=" * 60)

    # Generate data with non-constant variance
    n = 200
    X = np.abs(np.random.randn(n, 1)) + 0.5  # Positive values
    y = 1 + 2*X.squeeze() + np.random.randn(n) * X.squeeze()  # Variance increases with X

    # Fit model
    X_design = np.column_stack([np.ones(n), X])
    beta_hat = np.linalg.solve(X_design.T @ X_design, X_design.T @ y)

    # TODO: Show that diagnostics detect heteroskedasticity

    print()


def example_outlier_and_leverage():
    """Example with outliers and high leverage points."""
    print("=" * 60)
    print("EXAMPLE: Outliers and Leverage Points")
    print("=" * 60)

    # Generate clean data
    n = 50
    X = np.random.randn(n, 1)
    y = 1 + 2*X.squeeze() + np.random.randn(n) * 0.3

    # Add an outlier (unusual y, normal x)
    X = np.vstack([X, [[0]]])
    y = np.append(y, 10)  # Outlier in y

    # Add a high leverage point (unusual x, follows trend)
    X = np.vstack([X, [[5]]])
    y = np.append(y, 11)  # Follows the trend

    # Add an influential point (unusual x AND unusual y)
    X = np.vstack([X, [[-5]]])
    y = np.append(y, 10)  # Doesn't follow trend

    # Fit model
    X_design = np.column_stack([np.ones(len(y)), X])
    beta_hat = np.linalg.solve(X_design.T @ X_design, X_design.T @ y)

    # TODO: Identify the different types of problematic points

    print()


def example_multicollinearity():
    """Example with multicollinear features."""
    print("=" * 60)
    print("EXAMPLE: Multicollinearity")
    print("=" * 60)

    n = 100

    # Create correlated features
    X1 = np.random.randn(n)
    X2 = X1 + np.random.randn(n) * 0.1  # Almost identical to X1
    X3 = np.random.randn(n)  # Independent
    X = np.column_stack([X1, X2, X3])

    # True model (note: X1 and X2 effects can't be distinguished)
    y = 1 + 3*X1 + 2*X3 + np.random.randn(n) * 0.5

    # Create multicollinearity diagnostics
    mc_diag = MulticollinearityDiagnostics(X, ['X1', 'X2', 'X3'])

    # TODO: Compute VIFs and condition number

    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("REGRESSION DIAGNOSTICS")
    print("=" * 60 + "\n")

    example_good_model()
    example_heteroskedasticity()
    example_outlier_and_leverage()
    example_multicollinearity()

    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
