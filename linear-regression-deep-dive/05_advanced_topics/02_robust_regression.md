# Robust Regression

## Why Robustness Matters

OLS is sensitive to outliers. A single bad data point can completely ruin your estimates. Robust methods resist the influence of outliers.

---

## Part 1: The Problem with OLS

### Exercise 1.1 ⭐⭐
**Question:** Consider fitting y = βx through the origin to data:
```
x: 1, 2, 3, 4, 5
y: 1, 2, 3, 4, 100
```

a) What is the OLS estimate β̂?
b) What would β̂ be without the outlier (100)?
c) What is the "sensible" estimate looking at the data?

*Your calculations:*
```
a) β̂_OLS = Σxᵢyᵢ / Σxᵢ² =




b) Without outlier:




c) The outlier has completely skewed the estimate from ~1 to ~

```

### Exercise 1.2 ⭐⭐
**Question:** The influence function measures how much an estimator changes when we add a point at location z. For OLS:

IF(z) ∝ z (unbounded!)

What does this tell us about OLS robustness?

*Your answer:*
```




```

---

## Part 2: M-Estimators

### Key Concept

Instead of minimizing Σ(yᵢ - xᵢᵀβ)² (squared errors), minimize:

Σρ(yᵢ - xᵢᵀβ)

Where ρ is a loss function less sensitive to outliers.

### Common Loss Functions

| Name | ρ(r) | ψ(r) = ρ'(r) |
|------|------|--------------|
| OLS | r²/2 | r |
| Huber | r²/2 if |r|≤k, else k|r|-k²/2 | r if |r|≤k, else k·sign(r) |
| Tukey bisquare | (k²/6)[1-(1-(r/k)²)³] if |r|≤k, else k²/6 | r(1-(r/k)²)² if |r|≤k, else 0 |

### Exercise 2.1 ⭐⭐
**Question:** Sketch the Huber loss function and compare to squared loss. At what point does it transition from quadratic to linear?

*Your sketch/description:*
```




```

### Exercise 2.2 ⭐⭐
**Question:** The Tukey bisquare completely ignores residuals beyond a threshold (ψ(r) = 0 for |r| > k). Why might this be desirable? What are the risks?

*Your answer:*
```
Why desirable:




Risks:



```

### Exercise 2.3 ⭐⭐⭐
**Question:** M-estimators solve: Σψ(yᵢ - xᵢᵀβ) · xᵢ = 0

For OLS, ψ(r) = r, giving the normal equations.

Write the estimating equation for Huber's M-estimator.

*Your equation:*
```




```

---

## Part 3: Iteratively Reweighted Least Squares (IRLS)

### The Algorithm

M-estimators can be computed by repeatedly solving weighted least squares:

1. Start with initial β̂
2. Compute residuals rᵢ = yᵢ - xᵢᵀβ̂
3. Compute weights wᵢ = ψ(rᵢ)/rᵢ
4. Solve weighted least squares: β̂ = (XᵀWX)⁻¹XᵀWy
5. Repeat until convergence

### Exercise 3.1 ⭐⭐⭐
**Question:** For Huber's ψ function, what are the weights wᵢ?

*Your derivation:*
```
ψ(r) = r if |r| ≤ k, else k·sign(r)

wᵢ = ψ(rᵢ)/rᵢ =

    = 1 if |rᵢ| ≤ k

    = ??? if |rᵢ| > k

```

### Exercise 3.2 ⭐⭐
**Question:** What do the weights do to outliers?

*Your explanation:*
```




```

### Coding Exercise 3.3 ⭐⭐⭐
Implement IRLS for Huber regression:

```python
def huber_weights(residuals, k=1.345):
    """
    Compute Huber weights for IRLS.

    Args:
        residuals: Array of residuals
        k: Huber threshold (default 1.345 gives 95% efficiency)

    Returns:
        weights: Array of weights
    """
    # TODO: Implement Huber weights
    # w_i = 1 if |r_i| <= k
    # w_i = k / |r_i| if |r_i| > k

    pass


def irls_huber(X, y, k=1.345, max_iter=100, tol=1e-6):
    """
    Iteratively Reweighted Least Squares for Huber regression.

    Args:
        X: Design matrix
        y: Response vector
        k: Huber threshold
        max_iter: Maximum iterations
        tol: Convergence tolerance

    Returns:
        beta: Estimated coefficients
    """
    # TODO: Implement IRLS
    # 1. Initialize with OLS
    # 2. Compute residuals
    # 3. Compute weights
    # 4. Solve weighted least squares
    # 5. Repeat until convergence

    pass
```

---

## Part 4: Least Median of Squares (LMS)

### A Highly Robust Method

Instead of minimizing sum of squared residuals, minimize the MEDIAN of squared residuals:

β̂_LMS = argmin median(r₁², r₂², ..., rₙ²)

### Exercise 4.1 ⭐⭐
**Question:** LMS has a breakdown point of 50%. What does this mean?

*Your answer:*
```




```

### Exercise 4.2 ⭐⭐
**Question:** OLS has a breakdown point of 1/n (one outlier can destroy it). Why is a high breakdown point desirable?

*Your answer:*
```




```

### Exercise 4.3 ⭐⭐⭐
**Question:** LMS is computationally harder than M-estimation. Why can't we simply take derivatives?

*Your answer:*
```




```

---

## Part 5: MM-Estimators

### Combining High Breakdown and Efficiency

MM-estimators are a two-stage procedure:
1. First, use a high-breakdown method (like LMS or S-estimator) to get a robust scale estimate
2. Then, use M-estimation with a bounded ψ function, using the robust scale from step 1

### Exercise 5.1 ⭐⭐⭐
**Question:** Why do we need a robust scale estimate in step 1? What goes wrong if we use the usual MAD or standard deviation?

*Your answer:*
```




```

### Exercise 5.2 ⭐⭐⭐
**Question:** MM-estimators can achieve 95% efficiency while maintaining 50% breakdown. What trade-off are we making?

*Your answer:*
```




```

---

## Part 6: Quantile Regression

### Beyond the Mean

OLS estimates E[y | x]. Quantile regression estimates quantiles of y | x.

For the τ-th quantile, minimize:

Σρ_τ(yᵢ - xᵢᵀβ)

where ρ_τ(r) = r(τ - I(r < 0)) = |τ - I(r < 0)| · |r|

### Exercise 6.1 ⭐⭐
**Question:** For τ = 0.5 (median regression), what is ρ₀.₅(r)?

*Your derivation:*
```
ρ₀.₅(r) = r(0.5 - I(r < 0))

If r > 0: ρ = r(0.5 - 0) = 0.5r
If r < 0: ρ = r(0.5 - 1) = -0.5r = 0.5|r|

So ρ₀.₅(r) = 0.5|r|

This is Least Absolute Deviations (LAD)!

```

### Exercise 6.2 ⭐⭐
**Question:** Why is median regression more robust than mean regression?

*Your answer:*
```




```

### Exercise 6.3 ⭐⭐⭐
**Question:** You fit quantile regression at τ = 0.1, 0.5, 0.9. The slopes are:
- τ = 0.1: β̂₁ = 1.2
- τ = 0.5: β̂₁ = 2.0
- τ = 0.9: β̂₁ = 3.5

What does this tell you about the relationship between x and y?

*Your interpretation:*
```




```

---

## Part 7: Detecting Outliers

### Methods

1. **Studentized residuals**: |tᵢ| > 2 or 3
2. **Cook's distance**: Dᵢ > 4/n or Dᵢ > 1
3. **DFFITS**: |DFFITSᵢ| > 2√(p/n)
4. **Robust Mahalanobis distance**: For multivariate outliers

### Exercise 7.1 ⭐⭐
**Question:** You've detected potential outliers. What should you do next?

*Your answer:*
```
1.


2.


3.


4.

```

### Exercise 7.2 ⭐⭐
**Question:** "Never delete outliers" vs "Always investigate outliers." Discuss.

*Your discussion:*
```




```

---

## Part 8: Comparison and Selection

### When to Use What

| Method | Breakdown | Efficiency | Computation | When to Use |
|--------|-----------|------------|-------------|-------------|
| OLS | 0% | 100% | Fast | No outliers |
| Huber | ~0% | ~95% | Medium | Mild outliers |
| Tukey | ~0% | ~95% | Medium | Moderate outliers |
| LMS | 50% | Low | Slow | Severe outliers |
| MM | 50% | ~95% | Medium | General robust |
| LAD | 50% | ~64% | Medium | Heavy tails |

### Exercise 8.1 ⭐⭐
**Question:** You have a dataset where you expect about 10% of observations might be outliers. Which method would you choose and why?

*Your answer:*
```




```

### Exercise 8.2 ⭐⭐⭐
**Question:** Design a workflow for robust regression analysis:

1. Start with...
2. Check for...
3. If outliers detected...
4. Final model...

*Your workflow:*
```
1.



2.



3.



4.


```

---

## Coding Challenges

### Challenge 1 ⭐⭐⭐
Implement Least Absolute Deviations (LAD) regression using linear programming:

```python
def lad_regression(X, y):
    """
    Least Absolute Deviations regression.

    Minimizes: Σ|yᵢ - xᵢᵀβ|

    This can be formulated as a linear program.

    Args:
        X: Design matrix
        y: Response vector

    Returns:
        beta: Estimated coefficients
    """
    # TODO: Implement LAD regression
    # Hint: Introduce slack variables u, v >= 0
    # Minimize: Σ(uᵢ + vᵢ)
    # Subject to: y - Xβ = u - v, u >= 0, v >= 0

    pass
```

### Challenge 2 ⭐⭐⭐⭐
Implement MM-estimation:

```python
def mm_estimator(X, y, k_initial=1.548, k_final=4.685):
    """
    MM-estimator for robust regression.

    Step 1: Get initial estimate using S-estimator (or similar)
    Step 2: Compute robust scale from step 1 residuals
    Step 3: Run M-estimation with Tukey bisquare, using robust scale

    Args:
        X: Design matrix
        y: Response vector
        k_initial: Tukey constant for initial estimate
        k_final: Tukey constant for final M-estimate

    Returns:
        beta: Robust coefficient estimates
    """
    # TODO: Implement MM-estimation

    pass
```

---

## Summary

Robust regression protects against:
1. **Vertical outliers**: Unusual y values
2. **Leverage points**: Unusual x values
3. **Influential points**: Points that strongly affect the fit

Key methods:
- **M-estimators**: Downweight outliers (Huber, Tukey)
- **LMS/LTS**: Highly robust but less efficient
- **MM-estimators**: Best of both worlds
- **Quantile regression**: Estimate quantiles, not just mean

## Further Reading

- Huber & Ronchetti - "Robust Statistics"
- Maronna, Martin & Yohai - "Robust Statistics: Theory and Methods"
- Rousseeuw & Leroy - "Robust Regression and Outlier Detection"
