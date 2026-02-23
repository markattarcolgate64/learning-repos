# Deriving the Normal Equations

## The Goal

Starting from "minimize the sum of squared errors," derive the famous formula:

**β̂ = (XᵀX)⁻¹Xᵀy**

We'll do this multiple ways—each approach gives different insight.

---

## Method 1: Calculus Approach

### Setup

We want to minimize:

L(**β**) = ||**y** - X**β**||² = (**y** - X**β**)ᵀ(**y** - X**β**)

### Exercise 1.1: Expand the Objective ⭐⭐

**Task:** Expand L(**β**) = (**y** - X**β**)ᵀ(**y** - X**β**) into separate terms.

*Your expansion:*

```
L(β) = (y - Xβ)ᵀ(y - Xβ)

     =


     =


     =

```

### Exercise 1.2: Take the Gradient ⭐⭐

**Task:** Using the matrix calculus identities:
- ∂/∂β (βᵀAβ) = 2Aβ (for symmetric A)
- ∂/∂β (aᵀβ) = a
- ∂/∂β (βᵀa) = a

Find ∇L(β).

*Your derivation:*

```
From the expansion above:

∂/∂β (yᵀy) =

∂/∂β (-2yᵀXβ) =

∂/∂β (βᵀXᵀXβ) =


Therefore:

∇L(β) =

```

### Exercise 1.3: Set Gradient to Zero ⭐⭐

**Task:** Set ∇L(β) = 0 and solve for β̂.

*Your solution:*

```
Setting ∇L(β) = 0:




Rearranging:




Solving for β:


```

### Exercise 1.4: Verify It's a Minimum ⭐⭐

**Task:** Compute the Hessian of L(β) and show it's positive semi-definite.

*Your verification:*

```
Hessian = ∂²L/∂β∂βᵀ =


This is positive semi-definite because:



```

---

## Method 2: Geometric Approach (Projection)

### The Key Insight

The fitted values **ŷ** = X**β̂** must be the orthogonal projection of **y** onto C(X).

### Exercise 2.1: Orthogonality Condition ⭐⭐

**Task:** If **ŷ** is the projection of **y** onto C(X), then the residual **e** = **y** - **ŷ** must be orthogonal to every vector in C(X).

Show that this means **e** ⊥ each column of X, which can be written as Xᵀ**e** = **0**.

*Your argument:*

```
Let x⁽ʲ⁾ denote the j-th column of X.

For e to be orthogonal to C(X):




In matrix form:



```

### Exercise 2.2: Derive Normal Equations Geometrically ⭐⭐

**Task:** Starting from Xᵀ**e** = **0** where **e** = **y** - X**β̂**, derive the normal equations.

*Your derivation:*

```
Xᵀe = 0

Substituting e = y - Xβ̂:




Rearranging:




Solving:


```

### Exercise 2.3: Why "Normal" Equations? ⭐

**Task:** The term "normal" in "normal equations" doesn't refer to the normal distribution. What does it refer to?

*Your explanation:*

```




```

---

## Method 3: Completing the Square

### A Clever Algebraic Approach

We can rewrite L(β) by "completing the square" to make the minimum obvious.

### Exercise 3.1: Complete the Square ⭐⭐⭐

**Task:** Show that:

L(β) = ||y - Xβ||² = ||y - Xβ̂||² + ||X(β - β̂)||²

where β̂ = (XᵀX)⁻¹Xᵀy.

*Hint:* Add and subtract Xβ̂.

*Your derivation:*

```
Let β̂ = (XᵀX)⁻¹Xᵀy and ŷ = Xβ̂

L(β) = ||y - Xβ||²

     = ||y - Xβ̂ + Xβ̂ - Xβ||²

     = ||(y - Xβ̂) + X(β̂ - β)||²

Now expand using ||a + b||² = ||a||² + 2aᵀb + ||b||²:




Show that the cross term vanishes:




Therefore:



```

### Exercise 3.2: Why Does This Show β̂ Is Optimal? ⭐⭐

**Task:** Looking at L(β) = ||y - Xβ̂||² + ||X(β - β̂)||², explain why β = β̂ minimizes L(β).

*Your explanation:*

```




```

---

## Method 4: Element-wise Derivation (Simple Linear Regression)

### For Intuition: The n=1 Predictor Case

Consider y = β₀ + β₁x + ε with data {(xᵢ, yᵢ)}ᵢ₌₁ⁿ.

### Exercise 4.1: Set Up the Loss ⭐

**Task:** Write the sum of squared residuals as a function of β₀ and β₁.

*Your expression:*

```
L(β₀, β₁) = Σᵢ₌₁ⁿ (           )²

          =
```

### Exercise 4.2: Derive Two Equations ⭐⭐

**Task:** Take partial derivatives and set them to zero.

*Your derivation:*

```
∂L/∂β₀ =



Setting to zero:



∂L/∂β₁ =



Setting to zero:


```

### Exercise 4.3: Solve the System ⭐⭐

**Task:** Solve the two equations simultaneously for β̂₀ and β̂₁.

*Hint:* From the first equation, express β₀ in terms of β₁ and means. Substitute into the second.

*Your solution:*

```
From ∂L/∂β₀ = 0:

β̂₀ =



Substituting into ∂L/∂β₁ = 0 equation:






Solving for β̂₁:



```

### Exercise 4.4: Connect to Covariance/Variance ⭐⭐

**Task:** Show that β̂₁ can be written as:

β̂₁ = Cov(x, y) / Var(x)

where these are sample covariance and variance.

*Your derivation:*

```
Recall:
- Sample variance: Var(x) = (1/n)Σ(xᵢ - x̄)²
- Sample covariance: Cov(x,y) = (1/n)Σ(xᵢ - x̄)(yᵢ - ȳ)

Starting from β̂₁ = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)²:




```

---

## Method 5: Maximum Likelihood Derivation

### Setup

Assume yᵢ | xᵢ ~ N(xᵢᵀβ, σ²) independently.

### Exercise 5.1: Write the Likelihood ⭐⭐

**Task:** Write L(β, σ² | y, X), the likelihood of observing y given the parameters.

*Your expression:*

```
L(β, σ²) = ∏ᵢ₌₁ⁿ P(yᵢ | xᵢ, β, σ²)

         = ∏ᵢ₌₁ⁿ (1/√(2πσ²)) exp(          )

         =

```

### Exercise 5.2: Write the Log-Likelihood ⭐⭐

**Task:** Take the log to get ℓ(β, σ²).

*Your expression:*

```
ℓ(β, σ²) = log L(β, σ²)

         =

         =

```

### Exercise 5.3: Maximize over β ⭐⭐

**Task:** Show that maximizing ℓ over β is equivalent to minimizing ||y - Xβ||².

*Your argument:*

```
The log-likelihood as a function of β (treating σ² as constant):




To maximize this over β, we need to:




This is equivalent to:


```

### Exercise 5.4: Find σ̂² ⭐⭐

**Task:** Taking β̂ as given, find the MLE for σ².

*Your derivation:*

```
∂ℓ/∂σ² =



Setting to zero:




Solving:

σ̂² =

```

---

## Synthesis Exercise ⭐⭐⭐

### Exercise 6.1: Compare All Methods

**Task:** Fill in this comparison table:

| Method | Key Insight | When Most Useful |
|--------|------------|------------------|
| Calculus | | |
| Geometric | | |
| Complete Square | | |
| Element-wise | | |
| MLE | | |

*Your answers:*

```
| Method          | Key Insight                    | When Most Useful           |
|-----------------|--------------------------------|----------------------------|
| Calculus        |                                |                            |
| Geometric       |                                |                            |
| Complete Square |                                |                            |
| Element-wise    |                                |                            |
| MLE             |                                |                            |
```

### Exercise 6.2: The Fundamental Trade-off

**Task:** Why do we need (XᵀX) to be invertible? What happens when it's not? Give a concrete example.

*Your explanation:*

```




Example:




```

---

## Final Check: Can You...

- [ ] Derive β̂ = (XᵀX)⁻¹Xᵀy from scratch using calculus?
- [ ] Explain the projection interpretation?
- [ ] Show that the residual is orthogonal to the column space?
- [ ] Derive the simple linear regression formulas by hand?
- [ ] Connect OLS to maximum likelihood under Gaussian errors?
- [ ] Explain what goes wrong when XᵀX is singular?
