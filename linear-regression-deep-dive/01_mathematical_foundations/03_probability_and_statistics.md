# Probability and Statistics for Linear Regression

## Why Probability?

Linear regression isn't just curve fitting—it's a statistical model with probabilistic assumptions. Understanding these allows you to:
- Quantify uncertainty in your estimates
- Perform hypothesis tests
- Construct confidence intervals
- Understand when the model breaks down

---

## 1. Random Variables and Expectation

### Key Concepts

For random variable X:
- **Expected value**: E[X] = Σx x·P(X=x) (discrete) or ∫x·f(x)dx (continuous)
- **Variance**: Var(X) = E[(X - E[X])²] = E[X²] - (E[X])²
- **Standard deviation**: SD(X) = √Var(X)

### Exercise 1.1 ⭐
**Question:** For a fair die roll X ∈ {1, 2, 3, 4, 5, 6}:
- a) Calculate E[X]
- b) Calculate E[X²]
- c) Calculate Var(X)

*Your work:*

```
a) E[X] =


b) E[X²] =


c) Var(X) =

```

### Exercise 1.2 ⭐
**Question:** Prove that Var(aX + b) = a²Var(X) for constants a and b.

*Your proof:*

```




```

---

## 2. Properties of Expectation

### Key Properties

For random variables X, Y and constants a, b:
- **Linearity**: E[aX + bY] = aE[X] + bE[Y] (always true!)
- **Product**: E[XY] = E[X]E[Y] only if X, Y are independent

### Exercise 2.1 ⭐⭐
**Question:** Prove that E[aX + bY] = aE[X] + bE[Y].

*Your proof:*

```




```

### Exercise 2.2 ⭐⭐
**Question:** For the OLS estimator β̂ = (XᵀX)⁻¹Xᵀ**y**, show that:

E[β̂] = (XᵀX)⁻¹XᵀE[**y**]

(Hint: Treat X as fixed/non-random, which is the standard assumption)

*Your derivation:*

```




```

---

## 3. Covariance and Correlation

### Key Concepts

- **Covariance**: Cov(X, Y) = E[(X - E[X])(Y - E[Y])] = E[XY] - E[X]E[Y]
- **Correlation**: ρ(X, Y) = Cov(X, Y) / (SD(X)·SD(Y)), where -1 ≤ ρ ≤ 1
- **Variance of sum**: Var(X + Y) = Var(X) + Var(Y) + 2Cov(X, Y)

### Exercise 3.1 ⭐
**Question:** If X and Y are independent, what is Cov(X, Y)? Prove it.

*Your proof:*

```



```

### Exercise 3.2 ⭐⭐
**Question:** Prove that Var(X + Y) = Var(X) + Var(Y) + 2Cov(X, Y).

*Your proof:*

```





```

### Exercise 3.3 ⭐⭐
**Question:** In simple linear regression y = β₀ + β₁x + ε:
- a) What does a high positive correlation between x and y suggest about β₁?
- b) What does zero correlation suggest?
- c) Can we have zero correlation but still a nonlinear relationship?

*Your answers:*

```
a)


b)


c)

```

---

## 4. The Normal Distribution

### Key Concepts

X ~ N(μ, σ²) means:
- PDF: f(x) = (1/√(2πσ²)) exp(-(x-μ)²/(2σ²))
- E[X] = μ
- Var(X) = σ²

Key properties:
- Linear combinations of normals are normal
- If X ~ N(μ, σ²), then aX + b ~ N(aμ + b, a²σ²)

### Exercise 4.1 ⭐
**Question:** If X ~ N(10, 4), find:
- a) E[X]
- b) SD(X)
- c) The distribution of Y = 3X - 5

*Your answers:*

```
a) E[X] =

b) SD(X) =

c) Y ~ N(?, ?)

```

### Exercise 4.2 ⭐⭐
**Question:** Why do we often assume errors are normally distributed in regression? Give at least two reasons.

*Your answer:*

```
1.


2.


```

---

## 5. Multivariate Normal Distribution

### Key Concepts

**X** ~ N(**μ**, Σ) where:
- **μ** is the mean vector
- Σ is the covariance matrix (symmetric, positive semi-definite)

PDF: f(**x**) = (2π)^(-p/2) |Σ|^(-1/2) exp(-½(**x**-**μ**)ᵀΣ⁻¹(**x**-**μ**))

### Exercise 5.1 ⭐⭐
**Question:** For bivariate normal (X, Y) with:
```
μ = [0]    Σ = [1    0.5]
    [0]        [0.5  1  ]
```

- a) What is Cov(X, Y)?
- b) What is Corr(X, Y)?
- c) What is the conditional distribution of Y given X = x?

*Your answers:*

```
a) Cov(X, Y) =


b) Corr(X, Y) =


c) Y | X = x ~ N(?, ?)
   (Hint: For bivariate normal, Y|X=x ~ N(μY + ρ(σY/σX)(x-μX), σY²(1-ρ²)))


```

### Exercise 5.2 ⭐⭐⭐
**Question:** In regression, why is the distribution of β̂ multivariate normal (under Gaussian errors)?

*Your explanation:*

```




```

---

## 6. Estimators and Their Properties

### Key Concepts

An **estimator** θ̂ is a function of the data that estimates a parameter θ.

Desirable properties:
- **Unbiased**: E[θ̂] = θ
- **Consistent**: θ̂ → θ as n → ∞ (in probability)
- **Efficient**: Minimum variance among unbiased estimators

### Exercise 6.1 ⭐
**Question:** Show that the sample mean X̄ = (1/n)Σᵢxᵢ is an unbiased estimator of the population mean μ.

*Your proof:*

```


```

### Exercise 6.2 ⭐⭐
**Question:** Calculate Var(X̄) when X₁, ..., Xₙ are i.i.d. with variance σ².

*Your derivation:*

```




```

### Exercise 6.3 ⭐⭐
**Question:** What happens to Var(X̄) as n increases? What is this property called?

*Your answer:*

```



```

---

## 7. The Regression Model Assumptions

### The Classical Linear Regression Model

For **y** = X**β** + **ε**, the standard assumptions are:

1. **Linearity**: The relationship is linear in parameters
2. **Strict exogeneity**: E[εᵢ | X] = 0
3. **No perfect multicollinearity**: rank(X) = p (full column rank)
4. **Homoskedasticity**: Var(εᵢ | X) = σ² (constant variance)
5. **No autocorrelation**: Cov(εᵢ, εⱼ | X) = 0 for i ≠ j
6. **Normality** (optional): ε | X ~ N(0, σ²I)

### Exercise 7.1 ⭐⭐
**Question:** In matrix form, assumptions 4 and 5 together can be written as:

Var(**ε** | X) = σ²I

What does this covariance matrix look like? What do the diagonal and off-diagonal elements represent?

*Your answer:*

```
The matrix:



Diagonal elements:


Off-diagonal elements:

```

### Exercise 7.2 ⭐⭐
**Question:** What goes wrong if we have heteroskedasticity (non-constant variance)?
- a) Is β̂ still unbiased?
- b) Are the standard errors still valid?
- c) What can we do about it?

*Your answers:*

```
a)


b)


c)

```

### Exercise 7.3 ⭐⭐⭐
**Question:** Derive Var(β̂ | X) under assumptions 1-5.

Hint: Start with β̂ = (XᵀX)⁻¹Xᵀ**y** and use Var(A**z**) = A·Var(**z**)·Aᵀ

*Your derivation:*

```
Step 1: Express β̂ in terms of ε




Step 2: Apply variance formula




Step 3: Simplify using Var(ε|X) = σ²I



```

---

## 8. Maximum Likelihood Estimation

### Key Concepts

Given data and a parametric model, the **likelihood function** L(θ) = P(data | θ).

The **maximum likelihood estimator** (MLE) maximizes L(θ), or equivalently, maximizes log L(θ).

### Exercise 8.1 ⭐⭐
**Question:** For y ~ N(μ, σ²) with n i.i.d. observations:
- a) Write the likelihood function L(μ, σ²)
- b) Write the log-likelihood ℓ(μ, σ²)

*Your work:*

```
a) L(μ, σ²) =




b) ℓ(μ, σ²) =



```

### Exercise 8.2 ⭐⭐⭐
**Question:** In Exercise 8.1, find the MLE for μ by setting ∂ℓ/∂μ = 0.

*Your derivation:*

```




```

### Exercise 8.3 ⭐⭐⭐
**Question:** For linear regression with normal errors, show that the MLE for **β** is the same as the OLS estimator.

*Your proof outline:*

```
Step 1: Write the likelihood assuming y|X ~ N(Xβ, σ²I)




Step 2: Write the log-likelihood




Step 3: Show maximizing log-likelihood ≡ minimizing sum of squared residuals




```

---

## Summary Checklist

Before moving on, make sure you can:

- [ ] Calculate expectations and variances
- [ ] Use linearity of expectation
- [ ] Explain covariance and correlation
- [ ] Work with normal and multivariate normal distributions
- [ ] State and explain the regression assumptions
- [ ] Derive Var(β̂) under standard assumptions
- [ ] Explain maximum likelihood estimation
- [ ] Connect MLE to least squares for Gaussian errors

---

## Further Reading

- Casella & Berger - "Statistical Inference" (Chapters 2-5)
- DeGroot & Schervish - "Probability and Statistics"
- Wasserman - "All of Statistics" (Chapters 1-5)
