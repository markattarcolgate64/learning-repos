# Properties of OLS Estimators

## The Big Questions

After deriving β̂ = (XᵀX)⁻¹Xᵀy, we need to understand:
1. Is it unbiased? (E[β̂] = β)
2. What's its variance?
3. Is it the "best" estimator?
4. What's its distribution?

---

## Part 1: Unbiasedness of OLS

### The Setup

Model: **y** = X**β** + **ε** where E[**ε** | X] = 0

Estimator: **β̂** = (XᵀX)⁻¹Xᵀ**y**

### Exercise 1.1: Express β̂ in Terms of True β ⭐⭐

**Task:** Substitute y = Xβ + ε into the formula for β̂ to express β̂ in terms of β and ε.

*Your derivation:*

```
β̂ = (XᵀX)⁻¹Xᵀy

   = (XᵀX)⁻¹Xᵀ(         )

   = (XᵀX)⁻¹Xᵀ(   ) + (XᵀX)⁻¹Xᵀ(   )

   =      +

```

### Exercise 1.2: Prove Unbiasedness ⭐⭐

**Task:** Take expectations of both sides (conditional on X) to show E[β̂ | X] = β.

*Your proof:*

```
From Exercise 1.1:

β̂ = β + (XᵀX)⁻¹Xᵀε

Taking conditional expectation:

E[β̂ | X] = E[β + (XᵀX)⁻¹Xᵀε | X]

         = β + (XᵀX)⁻¹XᵀE[ε | X]

         = β + (XᵀX)⁻¹Xᵀ(      )    [by assumption E[ε|X] = 0]

         =

```

### Exercise 1.3: What If E[ε | X] ≠ 0? ⭐⭐

**Task:** If E[ε | X] = Xγ for some γ ≠ 0 (endogeneity), what is E[β̂ | X]?

*Your derivation:*

```
E[β̂ | X] = β + (XᵀX)⁻¹XᵀE[ε | X]

         = β + (XᵀX)⁻¹Xᵀ(     )

         =

This shows β̂ is biased by:

```

### Exercise 1.4: Omitted Variable Bias ⭐⭐⭐

**Task:** True model: y = X₁β₁ + X₂β₂ + ε. You estimate y = X₁γ + u (omitting X₂).

Show that E[γ̂ | X₁, X₂] = β₁ + (X₁ᵀX₁)⁻¹X₁ᵀX₂β₂.

*Your derivation:*

```
The true DGP: y = X₁β₁ + X₂β₂ + ε

Your estimator: γ̂ = (X₁ᵀX₁)⁻¹X₁ᵀy

Substituting the true y:




Taking expectation:




```

**Follow-up:** When is there NO omitted variable bias?

*Your answer:*

```


```

---

## Part 2: Variance of OLS

### Setup

Under assumptions:
- E[ε | X] = 0
- Var(ε | X) = σ²I (homoskedasticity + no autocorrelation)

### Exercise 2.1: Derive Var(β̂ | X) ⭐⭐⭐

**Task:** Starting from β̂ = β + (XᵀX)⁻¹Xᵀε, derive Var(β̂ | X).

*Hint:* Use Var(Aε) = A Var(ε) Aᵀ

*Your derivation:*

```
β̂ - β = (XᵀX)⁻¹Xᵀε

Let A = (XᵀX)⁻¹Xᵀ

Var(β̂ | X) = Var(Aε | X)

            = A Var(ε | X) Aᵀ

            = A (σ²I) Aᵀ

            = σ² · A Aᵀ

            = σ² · (XᵀX)⁻¹Xᵀ · [(XᵀX)⁻¹Xᵀ]ᵀ

            = σ² · (XᵀX)⁻¹Xᵀ · (          )

            = σ² · (XᵀX)⁻¹ · (          ) · (XᵀX)⁻¹

            = σ² ·

```

### Exercise 2.2: Variance in Simple Regression ⭐⭐

**Task:** For simple linear regression with y = β₀ + β₁x + ε, show that:

Var(β̂₁) = σ² / Σᵢ(xᵢ - x̄)²

*Your derivation (hint: start from the scalar formula for β̂₁):*

```
Recall: β̂₁ = Σᵢ(xᵢ - x̄)(yᵢ - ȳ) / Σᵢ(xᵢ - x̄)²

Let SXX = Σᵢ(xᵢ - x̄)²

We can write: β̂₁ = Σᵢ wᵢyᵢ where wᵢ =

Since the yᵢ are independent with Var(yᵢ) = σ²:

Var(β̂₁) = Var(Σᵢ wᵢyᵢ)

         =

         =

         =

```

### Exercise 2.3: What Affects Precision? ⭐⭐

**Task:** Based on Var(β̂₁) = σ² / Σᵢ(xᵢ - x̄)², explain how each factor affects precision:

| Factor | Effect on Var(β̂₁) | Intuition |
|--------|-------------------|-----------|
| Larger σ² | | |
| Larger Σ(xᵢ - x̄)² | | |
| More spread out x values | | |
| More observations | | |

*Your answers:*

```
| Factor               | Effect on Var(β̂₁) | Intuition                    |
|---------------------|-------------------|------------------------------|
| Larger σ²           |                   |                              |
| Larger Σ(xᵢ - x̄)²  |                   |                              |
| More spread out x   |                   |                              |
| More observations   |                   |                              |
```

---

## Part 3: The Gauss-Markov Theorem

### The Statement

**Gauss-Markov Theorem:** Under assumptions:
1. Linearity: y = Xβ + ε
2. Strict exogeneity: E[ε | X] = 0
3. Homoskedasticity: Var(εᵢ | X) = σ²
4. No autocorrelation: Cov(εᵢ, εⱼ | X) = 0 for i ≠ j
5. No perfect multicollinearity: rank(X) = p

The OLS estimator β̂ is **BLUE**: Best Linear Unbiased Estimator.

- **Best** = minimum variance
- **Linear** = linear function of y
- **Unbiased** = E[β̂] = β

### Exercise 3.1: What Does "Linear" Mean? ⭐⭐

**Task:** Show that β̂ = (XᵀX)⁻¹Xᵀy is a linear function of y (can be written as Cy for some matrix C).

*Your work:*

```
β̂ = (XᵀX)⁻¹Xᵀy = Cy where C =


```

### Exercise 3.2: Set Up the Proof ⭐⭐⭐

**Task:** Consider any other linear unbiased estimator β̃ = Cy where C is a p×n matrix.

For unbiasedness, we need E[β̃ | X] = β. Show this requires CX = I.

*Your derivation:*

```
β̃ = Cy = C(Xβ + ε) =

E[β̃ | X] = E[CXβ + Cε | X]

         = CXβ + CE[ε | X]

         = CXβ + C(0)

         = CXβ

For this to equal β for all β:


```

### Exercise 3.3: The Variance Comparison ⭐⭐⭐⭐

**Task:** Let C = (XᵀX)⁻¹Xᵀ + D where D is any matrix with DX = 0.

Show that Var(β̃ | X) = Var(β̂ | X) + σ²DDᵀ, proving β̂ has minimum variance.

*Your proof:*

```
β̃ = Cy = [(XᵀX)⁻¹Xᵀ + D]y

Var(β̃ | X) = Var(Cy | X)

            = C Var(y | X) Cᵀ

            = σ² · CCᵀ

Now expand CCᵀ:

CCᵀ = [(XᵀX)⁻¹Xᵀ + D][(XᵀX)⁻¹Xᵀ + D]ᵀ

    = [(XᵀX)⁻¹Xᵀ + D][X(XᵀX)⁻¹ + Dᵀ]

    = (XᵀX)⁻¹XᵀX(XᵀX)⁻¹ + (XᵀX)⁻¹XᵀDᵀ + DX(XᵀX)⁻¹ + DDᵀ

Since DX = 0:




Therefore:

Var(β̃ | X) = σ² · [         +         ]

            = Var(β̂ | X) +

Since DDᵀ is positive semi-definite (why?):


```

### Exercise 3.4: Gauss-Markov Limitations ⭐⭐

**Task:** List situations where OLS is NOT the best estimator, and what you might do instead.

*Your answer:*

```
1. Heteroskedasticity:
   - Problem:
   - Alternative:

2. Autocorrelation:
   - Problem:
   - Alternative:

3. Non-normal errors:
   - Problem:
   - Alternative:

4. Outliers:
   - Problem:
   - Alternative:
```

---

## Part 4: Distribution of OLS Estimators

### With Normality

If we add the assumption ε | X ~ N(0, σ²I), then:

### Exercise 4.1: Distribution of β̂ ⭐⭐

**Task:** Given that β̂ = β + (XᵀX)⁻¹Xᵀε and ε | X ~ N(0, σ²I), derive the distribution of β̂ | X.

*Your derivation:*

```
β̂ | X = β + (XᵀX)⁻¹Xᵀε

Since ε | X ~ N(0, σ²I):

(XᵀX)⁻¹Xᵀε | X ~ N(      ,          )

Therefore:

β̂ | X ~ N(      ,          )

```

### Exercise 4.2: Distribution of a Single Coefficient ⭐⭐

**Task:** For a single coefficient β̂ⱼ:

- What is E[β̂ⱼ]?
- What is Var(β̂ⱼ)?
- What is the distribution of β̂ⱼ?

*Your answers:*

```
E[β̂ⱼ] =

Var(β̂ⱼ) =          (the j-th diagonal element of       )

β̂ⱼ ~

```

### Exercise 4.3: The t-Statistic ⭐⭐⭐

**Task:** In practice, σ² is unknown. We estimate it with:

s² = RSS / (n - p) = ||y - Xβ̂||² / (n - p)

Show that the t-statistic:

t = (β̂ⱼ - βⱼ) / SE(β̂ⱼ)

follows a t-distribution with n - p degrees of freedom.

*Your explanation (outline the key steps):*

```
Step 1: The numerator β̂ⱼ - βⱼ is normal with mean 0.


Step 2: The denominator involves s², which estimates σ².


Step 3: RSS/σ² follows a chi-squared distribution because:


Step 4: β̂ⱼ and s² are independent because:


Step 5: Therefore, the ratio follows a t-distribution:


```

---

## Part 5: Properties of Residuals and Fitted Values

### Exercise 5.1: Properties of Fitted Values ⭐⭐

**Task:** For ŷ = Xβ̂ = Py where P = X(XᵀX)⁻¹Xᵀ:

- a) Show E[ŷ | X] = Xβ
- b) Show Var(ŷ | X) = σ²P

*Your derivations:*

```
a) E[ŷ | X] = E[Py | X]

            = PE[y | X]

            = P(    )

            =


b) Var(ŷ | X) = Var(Py | X)

              = P Var(y | X) Pᵀ

              =

              =                (using P² = P and Pᵀ = P)

```

### Exercise 5.2: Properties of Residuals ⭐⭐

**Task:** For e = y - ŷ = (I - P)y:

- a) Show E[e | X] = 0
- b) Show Var(e | X) = σ²(I - P)
- c) Explain why individual residuals are NOT independent

*Your derivations:*

```
a)




b)




c)


```

### Exercise 5.3: Why n - p Degrees of Freedom? ⭐⭐⭐

**Task:** Explain intuitively why RSS has n - p degrees of freedom.

*Hint:* How many "free" residuals are there?

*Your explanation:*

```




```

---

## Summary Checklist

Before moving on, can you:

- [ ] Prove β̂ is unbiased?
- [ ] Derive Var(β̂ | X) = σ²(XᵀX)⁻¹?
- [ ] State the Gauss-Markov theorem and its assumptions?
- [ ] Explain what BLUE means?
- [ ] Outline the Gauss-Markov proof?
- [ ] Derive the distribution of β̂ under normality?
- [ ] Explain why we use the t-distribution for inference?
- [ ] Derive properties of residuals and fitted values?
