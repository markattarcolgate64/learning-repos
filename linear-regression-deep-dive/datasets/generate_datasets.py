"""
Dataset Generation for Linear Regression Practice
=================================================

This script generates various datasets for practicing linear regression.
Each dataset is designed to illustrate specific concepts or challenges.

Run this script to generate all datasets as CSV files.
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)

# Create datasets directory if it doesn't exist
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)


def save_dataset(df, name, description):
    """Save dataset and print info."""
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{name}.csv")
    df.to_csv(filepath, index=False)
    print(f"\n{'='*60}")
    print(f"Dataset: {name}")
    print(f"{'='*60}")
    print(f"Description: {description}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Saved to: {filepath}")


# =============================================================================
# DATASET 1: Simple Linear Regression (Clean)
# =============================================================================

def generate_simple_clean():
    """Perfect dataset for learning basic linear regression."""
    n = 100
    x = np.linspace(0, 10, n)
    y = 2 + 3 * x + np.random.randn(n) * 2

    df = pd.DataFrame({
        'x': x,
        'y': y
    })

    save_dataset(df, '01_simple_clean',
                 'Clean simple linear regression. True model: y = 2 + 3x + noise')
    return df


# =============================================================================
# DATASET 2: Multiple Regression
# =============================================================================

def generate_multiple():
    """Multiple regression with 3 predictors."""
    n = 200
    x1 = np.random.randn(n)
    x2 = np.random.randn(n)
    x3 = np.random.randn(n)
    y = 5 + 2*x1 - 1.5*x2 + 0.8*x3 + np.random.randn(n) * 1.5

    df = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'y': y
    })

    save_dataset(df, '02_multiple',
                 'Multiple regression. True model: y = 5 + 2*x1 - 1.5*x2 + 0.8*x3 + noise')
    return df


# =============================================================================
# DATASET 3: Multicollinearity
# =============================================================================

def generate_multicollinear():
    """Dataset with highly correlated predictors."""
    n = 150
    x1 = np.random.randn(n)
    x2 = x1 + np.random.randn(n) * 0.1  # x2 ≈ x1
    x3 = np.random.randn(n)  # Independent

    y = 3 + 2*x1 + 1*x3 + np.random.randn(n) * 0.5

    df = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'y': y
    })

    save_dataset(df, '03_multicollinear',
                 'Multicollinearity: x1 and x2 are highly correlated (r ≈ 0.99). '
                 'True model uses only x1 and x3.')
    return df


# =============================================================================
# DATASET 4: Heteroskedasticity
# =============================================================================

def generate_heteroskedastic():
    """Dataset with non-constant variance."""
    n = 200
    x = np.abs(np.random.randn(n)) + 1  # Positive values
    # Variance increases with x
    y = 2 + 3*x + np.random.randn(n) * x

    df = pd.DataFrame({
        'x': x,
        'y': y
    })

    save_dataset(df, '04_heteroskedastic',
                 'Heteroskedasticity: Variance of y increases with x. '
                 'True model: y = 2 + 3x + noise*x')
    return df


# =============================================================================
# DATASET 5: Outliers
# =============================================================================

def generate_with_outliers():
    """Clean data with a few outliers."""
    n = 100
    x = np.random.randn(n)
    y = 1 + 2*x + np.random.randn(n) * 0.5

    # Add outliers
    outlier_idx = [10, 25, 75]
    y[outlier_idx] = y[outlier_idx] + np.array([10, -8, 12])

    # Add high leverage point
    x = np.append(x, 5)
    y = np.append(y, 0)  # Doesn't follow trend

    df = pd.DataFrame({
        'x': x,
        'y': y
    })

    save_dataset(df, '05_with_outliers',
                 'Outliers: Clean data with 3 y-outliers and 1 high-leverage outlier. '
                 'True model: y = 1 + 2x + noise')
    return df


# =============================================================================
# DATASET 6: Nonlinear Relationship
# =============================================================================

def generate_nonlinear():
    """Dataset where true relationship is nonlinear."""
    n = 150
    x = np.linspace(0, 5, n)
    y = 2 + 3*x - 0.5*x**2 + np.random.randn(n) * 0.5

    df = pd.DataFrame({
        'x': x,
        'y': y
    })

    save_dataset(df, '06_nonlinear',
                 'Nonlinear relationship. True model: y = 2 + 3x - 0.5x² + noise. '
                 'Linear fit will show residual pattern.')
    return df


# =============================================================================
# DATASET 7: High-Dimensional (p > n)
# =============================================================================

def generate_high_dimensional():
    """More features than observations."""
    n = 50
    p = 100

    X = np.random.randn(n, p)
    # Only first 5 features are truly relevant
    true_beta = np.zeros(p)
    true_beta[:5] = [3, -2, 1.5, -1, 2]

    y = X @ true_beta + np.random.randn(n) * 0.5

    df = pd.DataFrame(X, columns=[f'x{i}' for i in range(p)])
    df['y'] = y

    save_dataset(df, '07_high_dimensional',
                 'High-dimensional: p=100 features, n=50 observations. '
                 'Only features x0-x4 are truly relevant. OLS will fail.')
    return df


# =============================================================================
# DATASET 8: Autocorrelated Errors (Time Series)
# =============================================================================

def generate_autocorrelated():
    """Time series data with autocorrelated errors."""
    n = 200
    t = np.arange(n)
    x = np.sin(t * 0.1) + np.random.randn(n) * 0.2

    # Generate AR(1) errors
    rho = 0.8
    errors = np.zeros(n)
    errors[0] = np.random.randn()
    for i in range(1, n):
        errors[i] = rho * errors[i-1] + np.random.randn()

    y = 5 + 2*x + errors

    df = pd.DataFrame({
        'time': t,
        'x': x,
        'y': y
    })

    save_dataset(df, '08_autocorrelated',
                 'Autocorrelated errors (AR(1) with rho=0.8). '
                 'Violates independence assumption.')
    return df


# =============================================================================
# DATASET 9: Interaction Effect
# =============================================================================

def generate_interaction():
    """Dataset with interaction between predictors."""
    n = 200
    x1 = np.random.randn(n)
    x2 = np.random.choice([0, 1], n)  # Binary variable

    # Different slopes for x1 depending on x2
    y = 3 + 2*x1 + 1*x2 + 1.5*x1*x2 + np.random.randn(n) * 0.5

    df = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'y': y
    })

    save_dataset(df, '09_interaction',
                 'Interaction effect: y = 3 + 2*x1 + 1*x2 + 1.5*x1*x2 + noise. '
                 'Effect of x1 depends on x2.')
    return df


# =============================================================================
# DATASET 10: Real-World Style (House Prices)
# =============================================================================

def generate_house_prices():
    """Simulated house price data."""
    n = 300

    # Generate features
    sqft = np.random.uniform(800, 4000, n)
    bedrooms = np.random.choice([1, 2, 3, 4, 5], n, p=[0.1, 0.2, 0.35, 0.25, 0.1])
    bathrooms = np.minimum(bedrooms, np.random.choice([1, 2, 3, 4], n, p=[0.2, 0.4, 0.3, 0.1]))
    age = np.random.uniform(0, 50, n)
    garage = np.random.choice([0, 1, 2, 3], n, p=[0.1, 0.3, 0.4, 0.2])
    pool = np.random.choice([0, 1], n, p=[0.8, 0.2])
    neighborhood_quality = np.random.choice([1, 2, 3, 4, 5], n)

    # Generate price (in thousands)
    price = (50 +
             0.1 * sqft +
             10 * bedrooms +
             15 * bathrooms -
             0.5 * age +
             20 * garage +
             30 * pool +
             25 * neighborhood_quality +
             np.random.randn(n) * 40)

    price = np.maximum(price, 50)  # Floor at 50k

    df = pd.DataFrame({
        'price': price,
        'sqft': sqft,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'age': age,
        'garage': garage,
        'pool': pool,
        'neighborhood_quality': neighborhood_quality
    })

    save_dataset(df, '10_house_prices',
                 'Simulated house prices with multiple features. '
                 'Good for practicing real-world regression.')
    return df


# =============================================================================
# DATASET 11: Sparse True Model (for Lasso)
# =============================================================================

def generate_sparse():
    """Dataset where only a few features matter."""
    n = 200
    p = 20

    X = np.random.randn(n, p)
    # Only 4 features matter
    true_beta = np.zeros(p)
    true_beta[[0, 5, 10, 15]] = [3, -2, 1.5, -1]

    y = X @ true_beta + np.random.randn(n) * 0.5

    df = pd.DataFrame(X, columns=[f'x{i}' for i in range(p)])
    df['y'] = y

    save_dataset(df, '11_sparse',
                 'Sparse model: Only x0, x5, x10, x15 are relevant. '
                 'Perfect for testing Lasso.')
    return df


# =============================================================================
# DATASET 12: Different Scales
# =============================================================================

def generate_different_scales():
    """Features with very different scales."""
    n = 150

    x1 = np.random.randn(n) * 1  # Scale ~1
    x2 = np.random.randn(n) * 1000  # Scale ~1000
    x3 = np.random.randn(n) * 0.001  # Scale ~0.001

    # True coefficients adjusted for scale
    y = 5 + 2*x1 + 0.002*x2 + 2000*x3 + np.random.randn(n) * 1

    df = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'y': y
    })

    save_dataset(df, '12_different_scales',
                 'Features with very different scales. '
                 'Demonstrates importance of standardization for regularization.')
    return df


# =============================================================================
# DATASET 13: Perfect Fit Possible
# =============================================================================

def generate_perfect_fit():
    """Small dataset where perfect fit is possible."""
    n = 5
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 5, 4, 5])

    df = pd.DataFrame({
        'x': x,
        'y': y
    })

    save_dataset(df, '13_small_dataset',
                 'Very small dataset (n=5). Good for hand calculations.')
    return df


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("GENERATING ALL DATASETS")
    print("="*60)

    generate_simple_clean()
    generate_multiple()
    generate_multicollinear()
    generate_heteroskedastic()
    generate_with_outliers()
    generate_nonlinear()
    generate_high_dimensional()
    generate_autocorrelated()
    generate_interaction()
    generate_house_prices()
    generate_sparse()
    generate_different_scales()
    generate_perfect_fit()

    print("\n" + "="*60)
    print("ALL DATASETS GENERATED SUCCESSFULLY")
    print("="*60)
    print("\nTo use these datasets in your exercises:")
    print("  import pandas as pd")
    print("  df = pd.read_csv('datasets/01_simple_clean.csv')")
    print()
