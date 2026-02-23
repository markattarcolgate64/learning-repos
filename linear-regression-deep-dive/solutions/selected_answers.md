# Selected Answers and Key Solutions

## ⚠️ SPOILER ALERT!

Only consult after seriously attempting the problems.

---

## Section 1: Linear Algebra (01_linear_algebra_essentials.md)

### Exercise 1.1
**Given a = [1, 2, 3]ᵀ, b = [4, 5, 6]ᵀ:**

a) **a + b** = [5, 7, 9]ᵀ

b) **3a** = [3, 6, 9]ᵀ

c) **a · b** = 1×4 + 2×5 + 3×6 = 4 + 10 + 18 = **32**

d) **||a||** = √(1² + 2² + 3²) = √14 ≈ **3.74**

### Exercise 4.1 (Projection Matrix Properties)

**Prove P = Pᵀ (symmetric):**
```
P = X(X'X)⁻¹X'
Pᵀ = [X(X'X)⁻¹X']ᵀ
   = X[(X'X)⁻¹]ᵀX'    (using (AB)ᵀ = BᵀAᵀ)
   = X[(X'X)ᵀ]⁻¹X'    (using (A⁻¹)ᵀ = (Aᵀ)⁻¹)
   = X(X'X)⁻¹X'       (since X'X is symmetric, (X'X)ᵀ = X'X)
   = P ✓
```

**Prove P² = P (idempotent):**
```
P² = [X(X'X)⁻¹X'][X(X'X)⁻¹X']
   = X(X'X)⁻¹[X'X](X'X)⁻¹X'
   = X(X'X)⁻¹X'
   = P ✓
```

---

## Section 2: Calculus (02_calculus_for_optimization.md)

### Exercise 5.3 (Gradient of Least Squares)

**L(β) = (y - Xβ)ᵀ(y - Xβ)**

Expanding:
```
L(β) = yᵀy - 2yᵀXβ + βᵀXᵀXβ
```

Taking gradient:
```
∇L = -2Xᵀy + 2XᵀXβ
   = 2Xᵀ(Xβ - y)
```

Setting to zero:
```
Xᵀ(Xβ - y) = 0
XᵀXβ = Xᵀy
β = (XᵀX)⁻¹Xᵀy ✓
```

---

## Section 3: Deriving Normal Equations

### Method 1: Calculus Approach

**Step 1: Expand**
```
L(β) = (y - Xβ)ᵀ(y - Xβ)
     = yᵀy - yᵀXβ - βᵀXᵀy + βᵀXᵀXβ
     = yᵀy - 2βᵀXᵀy + βᵀXᵀXβ   (since yᵀXβ is scalar = βᵀXᵀy)
```

**Step 2: Differentiate**
```
∂L/∂β = -2Xᵀy + 2XᵀXβ
```

**Step 3: Set to zero**
```
-2Xᵀy + 2XᵀXβ = 0
XᵀXβ = Xᵀy
β = (XᵀX)⁻¹Xᵀy
```

**Step 4: Verify minimum**
```
Hessian = 2XᵀX
This is positive semi-definite (zᵀXᵀXz = ||Xz||² ≥ 0)
So we have a minimum ✓
```

---

## Section 4: OLS Properties

### Unbiasedness Proof

Starting with β̂ = (XᵀX)⁻¹Xᵀy and y = Xβ + ε:

```
β̂ = (XᵀX)⁻¹Xᵀ(Xβ + ε)
   = (XᵀX)⁻¹XᵀXβ + (XᵀX)⁻¹Xᵀε
   = Iβ + (XᵀX)⁻¹Xᵀε
   = β + (XᵀX)⁻¹Xᵀε

E[β̂ | X] = β + (XᵀX)⁻¹XᵀE[ε | X]
         = β + (XᵀX)⁻¹Xᵀ · 0
         = β ✓
```

### Variance of β̂

```
Var(β̂ | X) = Var[(XᵀX)⁻¹Xᵀε | X]

Let A = (XᵀX)⁻¹Xᵀ

Var(Aε | X) = A · Var(ε | X) · Aᵀ
            = A · σ²I · Aᵀ
            = σ² · (XᵀX)⁻¹Xᵀ · X(XᵀX)⁻¹
            = σ² · (XᵀX)⁻¹ · XᵀX · (XᵀX)⁻¹
            = σ² · (XᵀX)⁻¹ ✓
```

---

## Section 5: Simple Linear Regression Formulas

For y = β₀ + β₁x + ε:

```
β̂₁ = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)² = Sxy/Sxx

β̂₀ = ȳ - β̂₁x̄

Var(β̂₁) = σ² / Σ(xᵢ - x̄)²

SE(β̂₁) = s / √Sxx  where s² = RSS/(n-2)
```

---

## Section 6: Key Conceptual Answers

### True/False A.2
**"Adding more predictors can never decrease R²"** - **TRUE**

R² = 1 - RSS/TSS. Adding a predictor can only decrease RSS (the best new model at worst ignores the new variable). Since TSS is fixed, R² can only increase.

This is why we use Adjusted R² = 1 - (n-1)/(n-p)·(1-R²)

### True/False A.5
**"If all t-statistics are insignificant, F-test must also be insignificant"** - **FALSE**

Counterexample: With highly correlated predictors, each individual coefficient may be poorly estimated (large SE → small t), but together they may explain significant variance.

### True/False A.6
**"Heteroskedasticity causes OLS to be biased"** - **FALSE**

Heteroskedasticity does NOT cause bias. OLS is still unbiased under heteroskedasticity. However:
1. Standard errors are wrong
2. OLS is no longer BLUE (efficient)

---

## Section 7: Computational Problem B.1

**Data: x = [1,2,3,4,5], y = [2.1, 3.9, 6.2, 7.8, 10.1]**

```
x̄ = 15/5 = 3
ȳ = 30.1/5 = 6.02

Sxy = Σ(xᵢ - 3)(yᵢ - 6.02)
    = (-2)(-3.92) + (-1)(-2.12) + (0)(0.18) + (1)(1.78) + (2)(4.08)
    = 7.84 + 2.12 + 0 + 1.78 + 8.16
    = 19.9

Sxx = Σ(xᵢ - 3)²
    = 4 + 1 + 0 + 1 + 4 = 10

β̂₁ = 19.9/10 = 1.99

β̂₀ = 6.02 - 1.99(3) = 0.05
```

---

## Section 8: Ridge as Bayesian MAP

**Likelihood:** y | β ~ N(Xβ, σ²I)
**Prior:** β ~ N(0, τ²I)

Log posterior:
```
log P(β|y) ∝ -1/(2σ²)||y - Xβ||² - 1/(2τ²)||β||²
```

Maximizing is equivalent to minimizing:
```
||y - Xβ||² + (σ²/τ²)||β||²
```

This is Ridge regression with λ = σ²/τ² ✓

---

## Gauss-Markov Theorem Summary

**Statement:** Under assumptions:
1. Linearity: y = Xβ + ε
2. E[ε | X] = 0
3. Var(ε | X) = σ²I
4. rank(X) = p

OLS is **BLUE**: Best Linear Unbiased Estimator

**Key insight:** Any other linear unbiased estimator β̃ = Cy has:
```
Var(β̃) = Var(β̂_OLS) + positive semi-definite matrix
```

Therefore OLS has minimum variance among all linear unbiased estimators.

---

## Quick Formula Reference

| Quantity | Formula |
|----------|---------|
| β̂ (matrix) | (XᵀX)⁻¹Xᵀy |
| β̂₁ (simple) | Sxy/Sxx |
| R² | 1 - RSS/TSS |
| Adjusted R² | 1 - (n-1)/(n-p)(1-R²) |
| SE(β̂ⱼ) | s√[(XᵀX)⁻¹]ⱼⱼ |
| t-statistic | β̂ⱼ / SE(β̂ⱼ) |
| F-statistic | [R²/(p-1)] / [(1-R²)/(n-p)] |
| Ridge | (XᵀX + λI)⁻¹Xᵀy |

---

*For complete solutions to all problems, work through them first and then compare with the approaches shown here.*
