# Problem Set 2: Computational Problems

## Instructions
These problems require calculations. Show all your work.
Use a calculator or Python/R for numerical computations, but understand each step.

---

## Section A: Matrix Calculations ⭐

### Problem A.1
Given:
```
X = [1  2]      y = [5]
    [1  3]          [7]
    [1  5]          [10]
```

Compute:
a) X'X
b) X'y
c) (X'X)⁻¹
d) β̂ = (X'X)⁻¹X'y

**Your calculations:**
```
a) X'X =




b) X'y =



c) (X'X)⁻¹ =




d) β̂ =


```

---

### Problem A.2
For the same data as A.1, compute:
a) Fitted values ŷ = Xβ̂
b) Residuals e = y - ŷ
c) RSS = e'e
d) TSS = Σ(yᵢ - ȳ)²
e) R²

**Your calculations:**
```
a) ŷ =



b) e =



c) RSS =


d) TSS =


e) R² =

```

---

### Problem A.3
Verify that X'e = 0 for the residuals computed in A.2.

**Your verification:**
```


```

---

## Section B: Simple Linear Regression ⭐⭐

### Problem B.1
Data:
| x | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| y | 2.1 | 3.9 | 6.2 | 7.8 | 10.1 |

Fit y = β₀ + β₁x + ε by computing:

a) x̄, ȳ
b) Sxy = Σ(xᵢ - x̄)(yᵢ - ȳ)
c) Sxx = Σ(xᵢ - x̄)²
d) β̂₁ = Sxy/Sxx
e) β̂₀ = ȳ - β̂₁x̄

**Your calculations:**
```
a) x̄ =         ȳ =


b) Sxy =


c) Sxx =


d) β̂₁ =


e) β̂₀ =

```

---

### Problem B.2
Continuing from B.1:

a) Calculate s² = RSS/(n-2)
b) Calculate SE(β̂₁) = s/√Sxx
c) Calculate the t-statistic for testing H₀: β₁ = 0
d) What is the 95% CI for β₁? (Use t₀.₀₂₅,₃ = 3.182)

**Your calculations:**
```
a) First find RSS:
   Fitted values:

   Residuals:

   RSS =

   s² =


b) SE(β̂₁) =


c) t =


d) 95% CI =

```

---

### Problem B.3
For the model in B.1, predict y when x = 6 and compute a 95% prediction interval.

Formula: ŷ₀ ± t_{α/2} · s · √(1 + 1/n + (x₀ - x̄)²/Sxx)

**Your calculations:**
```
Point prediction:


Prediction interval:


```

---

## Section C: Multiple Regression ⭐⭐

### Problem C.1
You're given the following summary statistics (n = 50):

| Variable | Mean | Std Dev |
|----------|------|---------|
| y | 100 | 15 |
| x₁ | 50 | 10 |
| x₂ | 25 | 5 |

Correlations:
- r(y, x₁) = 0.6
- r(y, x₂) = 0.4
- r(x₁, x₂) = 0.3

For the standardized regression zy = β₁*zx₁ + β₂*zx₂:

The standardized coefficients are:
β₁* = [r(y,x₁) - r(y,x₂)·r(x₁,x₂)] / [1 - r(x₁,x₂)²]
β₂* = [r(y,x₂) - r(y,x₁)·r(x₁,x₂)] / [1 - r(x₁,x₂)²]

a) Calculate β₁* and β₂*
b) Calculate R² = β₁*·r(y,x₁) + β₂*·r(y,x₂)
c) Convert to unstandardized: β̂₁ = β₁*·(sy/sx₁)

**Your calculations:**
```
a) β₁* =




   β₂* =



b) R² =



c) Unstandardized:
   β̂₁ =

   β̂₂ =

```

---

### Problem C.2
Given this ANOVA table:

| Source | SS | df | MS | F |
|--------|-----|-----|-----|-----|
| Regression | 450 | 3 | ? | ? |
| Residual | 150 | 46 | ? | |
| Total | 600 | 49 | | |

a) Fill in the missing values
b) Calculate R²
c) Calculate Adjusted R²
d) Test whether the regression is significant at α = 0.05

**Your calculations:**
```
a) MS_regression =
   MS_residual =
   F =


b) R² =


c) R̄² = 1 - (n-1)/(n-p) · (1 - R²) =


d) F_crit(3, 46, 0.05) ≈ 2.81
   Decision:

```

---

## Section D: Hypothesis Testing ⭐⭐

### Problem D.1
A researcher reports these results (n = 100):

ŷ = 5.2 + 2.3x₁ - 1.1x₂ + 0.8x₃
      (1.0)  (0.5)   (0.4)   (0.6)

(Standard errors in parentheses)

a) Test each coefficient for significance at α = 0.05 (use z ≈ 1.96)
b) Which coefficients are significant?
c) Construct 95% CIs for each coefficient

**Your calculations:**
```
a) t-statistics:
   β₁: t =
   β₂: t =
   β₃: t =


b) Significant at α = 0.05:



c) 95% CIs:
   β₁:
   β₂:
   β₃:

```

---

### Problem D.2
You want to test H₀: β₂ = β₃ (the effects of x₂ and x₃ are equal).

Given:
- β̂₂ = -1.1, SE(β̂₂) = 0.4
- β̂₃ = 0.8, SE(β̂₃) = 0.6
- Cov(β̂₂, β̂₃) = 0.05

The test statistic is: t = (β̂₂ - β̂₃) / SE(β̂₂ - β̂₃)

Where: Var(β̂₂ - β̂₃) = Var(β̂₂) + Var(β̂₃) - 2Cov(β̂₂, β̂₃)

Calculate the test statistic and make a decision at α = 0.05.

**Your calculations:**
```
Var(β̂₂ - β̂₃) =



SE(β̂₂ - β̂₃) =


t =


Decision:

```

---

### Problem D.3
For testing whether x₃ and x₄ are jointly significant:

Full model: RSS = 200, p = 5
Reduced model (without x₃, x₄): RSS = 280, p = 3
n = 100

Calculate the F-statistic and test at α = 0.05.

**Your calculations:**
```
F = [(RSS_R - RSS_F) / (p_F - p_R)] / [RSS_F / (n - p_F)]

  =



F_crit(2, 95, 0.05) ≈ 3.09

Decision:

```

---

## Section E: Diagnostics ⭐⭐⭐

### Problem E.1
From a regression with n = 20 and p = 4, you get:

For observation i = 5:
- Residual: e₅ = 3.2
- Leverage: h₅₅ = 0.35
- s² = 4.0 (MSE from full model)

Calculate:
a) Standardized residual
b) Whether this point has high leverage (rule: h > 2p/n)
c) Approximate Cook's distance

**Your calculations:**
```
a) r₅ = e₅ / (s · √(1 - h₅₅))
      =


b) Threshold: 2p/n =
   h₅₅ = 0.35
   High leverage?


c) Cook's D₅ ≈ r₅² · h₅₅ / (p · (1 - h₅₅))
            =


   Is this concerning? (rule: D > 4/n or D > 1)

```

---

### Problem E.2
Calculate the VIF for X₁ given:
- R² from regressing X₁ on X₂ and X₃ is 0.85

Is there concerning multicollinearity?

**Your calculation:**
```
VIF₁ = 1 / (1 - R₁²)
     =


Concerning? (rule: VIF > 5 or 10)

```

---

### Problem E.3
The correlation matrix for three predictors is:

```
       X₁    X₂    X₃
X₁   1.00  0.95  0.10
X₂   0.95  1.00  0.15
X₃   0.10  0.15  1.00
```

a) Which variables are likely collinear?
b) What would you expect the VIFs to look like approximately?
c) What would you recommend?

**Your answers:**
```
a)


b)


c)

```

---

## Section F: Regularization ⭐⭐⭐

### Problem F.1
For Ridge regression: β̂_ridge = (X'X + λI)⁻¹X'y

Given (after centering):
```
X'X = [10  4]      X'y = [20]
      [4  10]            [10]
```

Calculate β̂_ridge for λ = 0, 2, and 10.

**Your calculations:**
```
λ = 0:
(X'X + 0·I)⁻¹ =


β̂ =



λ = 2:
(X'X + 2I) =

(X'X + 2I)⁻¹ =


β̂ =



λ = 10:
(X'X + 10I) =


β̂ =


```

What happens to the coefficients as λ increases?
```

```

---

### Problem F.2
You're selecting λ for Lasso using 5-fold CV. Your CV errors are:

| λ | CV Error |
|---|----------|
| 0.01 | 125 |
| 0.1 | 98 |
| 0.5 | 85 |
| 1.0 | 82 |
| 2.0 | 89 |
| 5.0 | 110 |

a) Which λ would you choose?
b) The "1-SE rule" suggests choosing the largest λ within 1 SE of the minimum. If SE at λ=1.0 is 8, what λ might you choose?

**Your answers:**
```
a)


b)

```

---

## Section G: Challenge Calculations ⭐⭐⭐⭐

### Problem G.1
Prove numerically that for your data in A.1, the projection matrix P = X(X'X)⁻¹X' satisfies:
a) P² = P
b) P' = P
c) rank(P) = 2

**Your verification:**
```
First, compute P:




a) P² =




b) P' =



c) rank(P) =

```

---

### Problem G.2
For simple linear regression, show that:

R² = [Σ(xᵢ - x̄)(yᵢ - ȳ)]² / [Σ(xᵢ - x̄)² · Σ(yᵢ - ȳ)²] = r²_{xy}

Using the data from B.1, verify this.

**Your verification:**
```
From B.1:
Sxy =
Sxx =
Syy = Σ(yᵢ - ȳ)² =


r²_{xy} = (Sxy)² / (Sxx · Syy)
        =



R² (calculated earlier) =


Are they equal?

```

---

### Problem G.3
The leverage of observation i is hᵢᵢ = xᵢ'(X'X)⁻¹xᵢ.

For simple linear regression, show that:
hᵢᵢ = 1/n + (xᵢ - x̄)²/Σⱼ(xⱼ - x̄)²

Verify using x = [1, 2, 3, 4, 5] for observation i = 1 and i = 5.

**Your calculations:**
```
First, find (X'X)⁻¹ for simple linear regression with intercept:




For i = 1 (x₁ = 1):
h₁₁ =



For i = 5 (x₅ = 5):
h₅₅ =



Which point has higher leverage? Why does this make sense?


```

---

## Computational Tools Check

Use Python/R to verify at least one answer from each section. Write your verification code here:

```python
# Your verification code







```

---

## Self-Check

Mark problems you found difficult:
- [ ] Matrix calculations
- [ ] Simple regression formulas
- [ ] Multiple regression
- [ ] Hypothesis testing
- [ ] Diagnostics calculations
- [ ] Regularization

Topics to review based on difficulties:
```



```
