# Hypothesis Testing in Linear Regression

## Why Hypothesis Testing?

Having point estimates isn't enough. We need to:
- Test if coefficients are significantly different from zero
- Test if groups of coefficients are jointly significant
- Compare nested models
- Quantify uncertainty with confidence intervals

---

## Part 1: Testing Individual Coefficients

### The t-Test

For testing H₀: βⱼ = β⁰ⱼ vs H₁: βⱼ ≠ β⁰ⱼ

Test statistic: t = (β̂ⱼ - β⁰ⱼ) / SE(β̂ⱼ) ~ tₙ₋ₚ under H₀

### Exercise 1.1: Derive the Standard Error ⭐⭐

**Task:** The standard error of β̂ⱼ is SE(β̂ⱼ) = s√[(XᵀX)⁻¹]ⱼⱼ.

Explain where this formula comes from.

*Your explanation:*

```
From Var(β̂ | X) = σ²(XᵀX)⁻¹:

Var(β̂ⱼ | X) =

Taking square root for standard deviation:

SD(β̂ⱼ | X) =

Since σ² is unknown, we estimate it with s²:

SE(β̂ⱼ) =

```

### Exercise 1.2: Construct a t-Test ⭐⭐

**Task:** You have:
- β̂₁ = 2.5
- SE(β̂₁) = 0.8
- n = 50, p = 3

Test H₀: β₁ = 0 vs H₁: β₁ ≠ 0 at α = 0.05.

*Your work:*

```
Step 1: Calculate the t-statistic

t =


Step 2: Find the critical value or p-value

df =

Critical value (two-sided, α = 0.05) ≈

Step 3: Make a decision



```

### Exercise 1.3: Confidence Interval ⭐⭐

**Task:** Derive the formula for a (1-α)100% confidence interval for βⱼ.

*Your derivation:*

```
Under H₀, we have:

P(-tα/2 ≤ (β̂ⱼ - βⱼ)/SE(β̂ⱼ) ≤ tα/2) = 1 - α

Rearranging for βⱼ:




Therefore, the (1-α)100% CI is:


```

### Exercise 1.4: Interpretation ⭐

**Task:** For β̂₁ = 2.5 with 95% CI [0.9, 4.1], write the correct interpretation.

*Your interpretation:*

```
Correct interpretation:



Common INCORRECT interpretation:


```

---

## Part 2: Testing Multiple Coefficients - The F-Test

### The Setup

Consider testing whether a subset of coefficients equals zero:

- Full model: y = Xβ + ε with p parameters
- Restricted model: y = X₁β₁ + ε with p₁ parameters (p₁ < p)
- H₀: The extra p - p₁ coefficients are all zero

### Exercise 2.1: The F-Statistic Formula ⭐⭐

**Task:** The F-statistic is:

F = [(RSS_R - RSS_F) / (p - p₁)] / [RSS_F / (n - p)]

Explain each component:

*Your explanations:*

```
RSS_R = Residual Sum of Squares from restricted model =

RSS_F = Residual Sum of Squares from full model =

p - p₁ = Number of restrictions =

n - p = Degrees of freedom for full model =

The numerator measures:


The denominator measures:


```

### Exercise 2.2: Why Does It Work? ⭐⭐⭐

**Task:** Under H₀:
- (RSS_R - RSS_F) / σ² ~ χ²(p - p₁)
- RSS_F / σ² ~ χ²(n - p)
- These are independent

Show that F follows an F-distribution.

*Your derivation:*

```
Recall: If U ~ χ²(d₁) and V ~ χ²(d₂) are independent, then:

(U/d₁) / (V/d₂) ~ F(d₁, d₂)

Applying this:

F = [(RSS_R - RSS_F) / (p - p₁)] / [RSS_F / (n - p)]

  = [(RSS_R - RSS_F)/σ² / (p - p₁)] / [RSS_F/σ² / (n - p)]

  = [χ²(   )/(   )] / [χ²(   )/(   )]

  ~ F(   ,   )

```

### Exercise 2.3: Test for Overall Significance ⭐⭐

**Task:** To test if ALL slope coefficients are zero (H₀: β₁ = β₂ = ... = βₖ = 0):

- What is the restricted model?
- What is RSS_R in this case?
- Derive the F-statistic in terms of R².

*Your work:*

```
Restricted model (under H₀):



RSS_R = (This is called Total Sum of Squares, TSS)



F-statistic:

F = [(RSS_R - RSS_F)/(p-1)] / [RSS_F/(n-p)]

  = [(TSS - RSS_F)/(p-1)] / [RSS_F/(n-p)]


Since R² = 1 - RSS_F/TSS, show that:

F = [R²/(p-1)] / [(1-R²)/(n-p)]


Derivation:



```

### Exercise 2.4: Numerical Example ⭐⭐

**Task:** You have:
- n = 100 observations
- Full model with 5 predictors: RSS_F = 200
- Restricted model with 2 predictors: RSS_R = 280

Test whether the 3 excluded variables are jointly significant at α = 0.05.

*Your work:*

```
Step 1: Calculate the F-statistic

F =


Step 2: Find critical value

df₁ =
df₂ =
F_crit (α = 0.05) ≈

Step 3: Decision and interpretation



```

---

## Part 3: The Relationship Between t and F

### Exercise 3.1: t² = F for Single Coefficient ⭐⭐⭐

**Task:** For testing H₀: βⱼ = 0 (a single coefficient), show that t² = F.

*Hint:* The F-test with one restriction is equivalent to the two-sided t-test.

*Your proof:*

```
The t-statistic: t = β̂ⱼ / SE(β̂ⱼ)

For the F-test with one restriction, we need RSS_R - RSS_F.

Show that RSS_R - RSS_F = β̂ⱼ² / [(XᵀX)⁻¹]ⱼⱼ:
(This requires showing that removing one variable increases RSS by exactly this amount)




Then:

F = [(RSS_R - RSS_F)/1] / [RSS_F/(n-p)]

  =



  = t²

```

### Exercise 3.2: When Do They Differ? ⭐⭐

**Task:** Give an example where the individual t-tests and the joint F-test give different conclusions.

*Hint:* Think about correlated predictors.

*Your example:*

```
Scenario:




Why this happens:



```

---

## Part 4: R² and Adjusted R²

### Exercise 4.1: Define and Derive R² ⭐⭐

**Task:**

a) Define R² as a ratio of sums of squares.
b) Show R² = Corr(y, ŷ)².

*Your work:*

```
a) R² = 1 - RSS/TSS =



b) Proving R² = Corr(y, ŷ)²:

Corr(y, ŷ) = Cov(y, ŷ) / [SD(y) · SD(ŷ)]

Step 1: Find Cov(y, ŷ)



Step 2: Find the relationship between Var(ŷ) and Cov(y, ŷ)



Step 3: Complete the proof



```

### Exercise 4.2: Problems with R² ⭐⭐

**Task:** Prove that R² never decreases when you add a variable, even if it's useless.

*Your proof:*

```
Consider adding variable x_{k+1} to a model.

Old model: RSS₁ = min ||y - X₁β₁||²

New model: RSS₂ = min ||y - [X₁ x_{k+1}]β||²

Show RSS₂ ≤ RSS₁:




Therefore R² = 1 - RSS/TSS must:


```

### Exercise 4.3: Adjusted R² ⭐⭐

**Task:** The adjusted R² is:

R̄² = 1 - [RSS/(n-p)] / [TSS/(n-1)] = 1 - (n-1)/(n-p) · (1 - R²)

a) Show that R̄² can decrease when adding a variable.
b) When will adding a variable increase R̄²?

*Your work:*

```
a) R̄² = 1 - (n-1)/(n-p) · (1-R²)

When we add a variable, (n-p) becomes (n-p-1), so (n-1)/(n-p) becomes:



For R̄² to decrease:



b) R̄² increases when:

The new variable must explain enough variance to offset:


```

---

## Part 5: Confidence Regions for Multiple Parameters

### Exercise 5.1: Joint Confidence Region ⭐⭐⭐

**Task:** The (1-α)100% joint confidence region for all of β is:

{β : (β̂ - β)ᵀ XᵀX (β̂ - β) / (p · s²) ≤ F_{α,p,n-p}}

This is an ellipsoid. Explain why it's an ellipsoid and what determines its shape.

*Your explanation:*

```
Why an ellipsoid:



What determines the shape:

- XᵀX controls:

- s² controls:

- F_{α,p,n-p} controls:

```

### Exercise 5.2: Joint vs. Individual Intervals ⭐⭐⭐

**Task:** Explain why:
- Individual 95% CIs for each βⱼ separately do NOT give 95% joint coverage
- The joint confidence region is larger than the "box" formed by individual CIs

*Your explanation:*

```
Individual intervals:




Joint coverage problem:




Bonferroni correction:


```

---

## Part 6: The Likelihood Ratio Test

### Exercise 6.1: Define the LRT ⭐⭐⭐

**Task:** The likelihood ratio test statistic is:

λ = -2 log(L(θ̂_R) / L(θ̂_F))

For linear regression with normal errors, show this becomes:

λ = n · log(RSS_R / RSS_F)

*Your derivation:*

```
For the full model, the maximized log-likelihood is:

ℓ_F = -n/2 log(2π) - n/2 log(σ̂²_F) - n/2

where σ̂²_F = RSS_F / n

Similarly for restricted model:




The difference:

-2(ℓ_R - ℓ_F) =




```

### Exercise 6.2: Relationship to F-Test ⭐⭐⭐

**Task:** For large n, the LRT and F-test are approximately equivalent. Show this using the approximation log(1 + x) ≈ x for small x.

*Your derivation:*

```
λ = n · log(RSS_R / RSS_F)

  = n · log(1 + (RSS_R - RSS_F)/RSS_F)

For small (RSS_R - RSS_F)/RSS_F:

  ≈ n · (RSS_R - RSS_F)/RSS_F



Compare to F-statistic:




```

---

## Summary Checklist

Before moving on, can you:

- [ ] Construct and interpret a t-test for a single coefficient?
- [ ] Derive and compute confidence intervals?
- [ ] Explain the F-test for multiple restrictions?
- [ ] Show that t² = F for a single coefficient?
- [ ] Explain why R² always increases with more variables?
- [ ] Derive and interpret adjusted R²?
- [ ] Explain joint confidence regions?
- [ ] Connect the likelihood ratio test to the F-test?
