"""
SOLUTION: Implement OLS from Scratch
====================================

⚠️ SPOILER ALERT: This file contains solutions!
Only look after attempting the problems yourself.
"""

import numpy as np
from scipy import stats


class LinearRegressionFromScratch:
    """Complete solution for OLS Linear Regression."""

    def __init__(self, fit_intercept: bool = True):
        self.fit_intercept = fit_intercept
        self.coefficients = None
        self.residuals = None
        self.fitted_values = None
        self._X_with_intercept = None

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """Add a column of ones to X for the intercept term."""
        # SOLUTION: Use column_stack to prepend ones
        n = X.shape[0]
        return np.column_stack([np.ones(n), X])

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearRegressionFromScratch':
        """
        Fit using the normal equations: β̂ = (X'X)⁻¹X'y
        """
        # Step 1: Handle intercept
        if self.fit_intercept:
            X = self._add_intercept(X)
        self._X_with_intercept = X

        # SOLUTION:
        # Step 2: Compute X'X
        XtX = X.T @ X

        # Step 3: Compute X'y
        Xty = X.T @ y

        # Step 4: Solve for β̂
        # Using solve is more stable than inv(XtX) @ Xty
        self.coefficients = np.linalg.solve(XtX, Xty)

        # Step 5: Compute fitted values
        self.fitted_values = X @ self.coefficients

        # Step 6: Compute residuals
        self.residuals = y - self.fitted_values

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the fitted model."""
        if self.coefficients is None:
            raise ValueError("Model has not been fitted yet!")

        # SOLUTION: Add intercept if needed, then compute Xβ
        if self.fit_intercept:
            X = self._add_intercept(X)
        return X @ self.coefficients

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute R² = 1 - RSS/TSS."""
        # SOLUTION:
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)  # RSS
        ss_tot = np.sum((y - np.mean(y)) ** 2)  # TSS
        return 1 - ss_res / ss_tot


class LinearRegressionStatistics:
    """Solution for computing regression statistics."""

    def __init__(self, model: LinearRegressionFromScratch, X: np.ndarray, y: np.ndarray):
        self.model = model
        self.X = X
        self.y = y
        self.n = len(y)
        self.X_design = model._X_with_intercept
        self.p = self.X_design.shape[1]

    def compute_rss(self) -> float:
        """RSS = Σeᵢ²"""
        # SOLUTION:
        return np.sum(self.model.residuals ** 2)

    def compute_tss(self) -> float:
        """TSS = Σ(yᵢ - ȳ)²"""
        # SOLUTION:
        return np.sum((self.y - np.mean(self.y)) ** 2)

    def compute_mse(self) -> float:
        """MSE = RSS / (n - p)"""
        # SOLUTION:
        return self.compute_rss() / (self.n - self.p)

    def compute_standard_errors(self) -> np.ndarray:
        """SE(β̂ⱼ) = s * sqrt([(X'X)^(-1)]ⱼⱼ)"""
        # SOLUTION:
        mse = self.compute_mse()
        XtX_inv = np.linalg.inv(self.X_design.T @ self.X_design)
        var_beta = mse * np.diag(XtX_inv)
        return np.sqrt(var_beta)

    def compute_t_statistics(self) -> np.ndarray:
        """t = β̂ⱼ / SE(β̂ⱼ)"""
        # SOLUTION:
        return self.model.coefficients / self.compute_standard_errors()

    def compute_p_values(self) -> np.ndarray:
        """Two-sided p-values for t-statistics."""
        # SOLUTION:
        t_stats = self.compute_t_statistics()
        df = self.n - self.p
        # Two-sided: 2 * P(T > |t|)
        return 2 * stats.t.sf(np.abs(t_stats), df)

    def compute_f_statistic(self) -> tuple:
        """F-statistic for overall model significance."""
        # SOLUTION:
        r2 = self.model.score(self.X, self.y)
        df1 = self.p - 1  # Number of predictors (excluding intercept)
        df2 = self.n - self.p

        f_stat = (r2 / df1) / ((1 - r2) / df2)
        p_value = stats.f.sf(f_stat, df1, df2)

        return f_stat, p_value

    def compute_confidence_intervals(self, alpha: float = 0.05) -> np.ndarray:
        """CI = β̂ⱼ ± t_{α/2, n-p} * SE(β̂ⱼ)"""
        # SOLUTION:
        se = self.compute_standard_errors()
        df = self.n - self.p
        t_crit = stats.t.ppf(1 - alpha/2, df)

        lower = self.model.coefficients - t_crit * se
        upper = self.model.coefficients + t_crit * se

        return np.column_stack([lower, upper])

    def summary(self) -> str:
        """Generate summary table."""
        lines = []
        lines.append("=" * 70)
        lines.append("OLS Regression Results")
        lines.append("=" * 70)
        lines.append(f"Observations: {self.n}")
        lines.append(f"Parameters:   {self.p}")
        lines.append(f"R-squared:    {self.model.score(self.X, self.y):.4f}")

        f_stat, f_pval = self.compute_f_statistic()
        lines.append(f"F-statistic:  {f_stat:.4f} (p = {f_pval:.4e})")
        lines.append("-" * 70)
        lines.append(f"{'Variable':>12} {'Coef':>10} {'Std Err':>10} {'t':>10} {'P>|t|':>10}")
        lines.append("-" * 70)

        se = self.compute_standard_errors()
        t_stats = self.compute_t_statistics()
        p_vals = self.compute_p_values()

        var_names = ['Intercept'] + [f'X{i}' for i in range(1, self.p)]

        for i in range(self.p):
            lines.append(f"{var_names[i]:>12} {self.model.coefficients[i]:>10.4f} "
                        f"{se[i]:>10.4f} {t_stats[i]:>10.4f} {p_vals[i]:>10.4f}")

        lines.append("=" * 70)
        return "\n".join(lines)


# =============================================================================
# TEST THE SOLUTION
# =============================================================================

if __name__ == "__main__":
    print("Testing OLS Solution...")

    # Generate test data
    np.random.seed(42)
    n = 100
    X = np.random.randn(n, 2)
    y = 1 + 2*X[:, 0] + 3*X[:, 1] + np.random.randn(n) * 0.5

    # Fit model
    model = LinearRegressionFromScratch()
    model.fit(X, y)

    print(f"\nCoefficients: {model.coefficients}")
    print(f"True values: [1, 2, 3]")
    print(f"R²: {model.score(X, y):.4f}")

    # Statistics
    stats_obj = LinearRegressionStatistics(model, X, y)
    print("\n" + stats_obj.summary())

    # Compare with sklearn
    try:
        from sklearn.linear_model import LinearRegression
        sk_model = LinearRegression()
        sk_model.fit(X, y)
        print(f"\nsklearn intercept: {sk_model.intercept_:.4f}")
        print(f"sklearn coefs: {sk_model.coef_}")
    except ImportError:
        pass
