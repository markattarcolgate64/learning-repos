# Problem Set 1: Conceptual Problems

## Instructions
These problems test your understanding of linear regression concepts.
Work through them on paper first, then check your reasoning.

---

## Section A: True/False with Justification ⭐

For each statement, indicate True or False and explain why.

### Problem A.1
**Statement:** If R² = 0.95, the linear model is appropriate for the data.

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.2
**Statement:** Adding more predictors to a regression can never decrease R².

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.3
**Statement:** If two predictors have correlation 0.99, we must remove one from the model.

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.4
**Statement:** The OLS estimator is unbiased even if the errors are not normally distributed.

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.5
**Statement:** If all the t-statistics for individual coefficients are insignificant, the F-test for overall significance must also be insignificant.

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.6
**Statement:** Heteroskedasticity causes the OLS estimates to be biased.

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.7
**Statement:** The residuals from OLS always sum to zero.

**Your answer:** T / F

**Justification:**
```




```

---

### Problem A.8
**Statement:** If y = β₀ + β₁x + ε and we fit y = γ₀ + γ₁(2x) + ε, then γ̂₁ = β̂₁/2.

**Your answer:** T / F

**Justification:**
```




```

---

## Section B: Short Answer ⭐⭐

### Problem B.1
You run a regression and find that the residuals are clearly non-normal (heavy tails). List three things you might consider doing and explain when each would be appropriate.

**Your answer:**
```
1.


2.


3.

```

---

### Problem B.2
Explain the difference between:
- A point with high leverage
- An outlier
- An influential point

Give an example of each that is NOT the other two.

**Your answer:**
```
High leverage:



Outlier:



Influential point:



Example of high leverage but not outlier or influential:



Example of outlier but not high leverage or influential:



Example of influential point:


```

---

### Problem B.3
Your R² is 0.89 on training data but 0.52 on test data. What does this suggest and what might you do?

**Your answer:**
```




```

---

### Problem B.4
You're modeling salary as a function of years of experience. You notice the residual plot shows a clear curved pattern. What does this suggest and how might you address it?

**Your answer:**
```




```

---

### Problem B.5
Explain why we use n-p degrees of freedom for the residual variance estimate s² = RSS/(n-p) rather than just n.

**Your answer:**
```




```

---

## Section C: Conceptual Scenarios ⭐⭐

### Problem C.1
You're modeling house prices with 10 predictors and 100 observations. Your colleague suggests adding 50 more predictors they collected. Discuss the pros and cons.

**Your answer:**
```
Pros:




Cons:




What would you recommend?


```

---

### Problem C.2
You fit a model predicting test scores from hours studied. β̂₁ = 5 (each hour of studying increases score by 5 points). Can you conclude that studying causes higher scores? Why or why not?

**Your answer:**
```




```

---

### Problem C.3
Two researchers fit the same model to the same data. Researcher A reports R² = 0.72 and Researcher B reports R² = 0.68. Assuming no errors, how is this possible?

**Your answer:**
```




```

---

### Problem C.4
You're comparing two models:
- Model 1: y ~ x₁ + x₂ (R² = 0.80, all coefficients significant)
- Model 2: y ~ x₁ + x₂ + x₃ (R² = 0.81, x₃ coefficient not significant)

Which model would you prefer and why?

**Your answer:**
```




```

---

### Problem C.5
Your model has VIF values: x₁: 1.2, x₂: 8.5, x₃: 9.1, x₄: 1.5

Interpret these values and suggest what might be happening.

**Your answer:**
```




```

---

## Section D: Interpretation Problems ⭐⭐

### Problem D.1
A regression of salary (in thousands) on years of education yields:

Salary = 15.2 + 4.3 × Education

SE(β̂₁) = 0.8, n = 500

a) Interpret the coefficient 4.3
b) Construct a 95% confidence interval for the education effect
c) Test whether education has a significant effect at α = 0.05

**Your answers:**
```
a)



b)



c)


```

---

### Problem D.2
A regression output shows:

| Variable | Coefficient | Std Error | t-stat | p-value |
|----------|------------|-----------|--------|---------|
| Intercept | 10.5 | 2.1 | 5.0 | <0.001 |
| X1 | 3.2 | 1.5 | 2.13 | 0.034 |
| X2 | -0.8 | 0.3 | -2.67 | 0.008 |
| X3 | 0.5 | 0.4 | 1.25 | 0.212 |

R² = 0.65, F = 45.2 (p < 0.001), n = 200

Interpret this output completely.

**Your interpretation:**
```













```

---

### Problem D.3
Consider the model: log(Income) = β₀ + β₁ × Education + β₂ × log(Age) + ε

If β̂₁ = 0.08 and β̂₂ = 0.5, interpret each coefficient.

**Your interpretation:**
```
β₁ = 0.08:



β₂ = 0.5:


```

---

## Section E: Deeper Understanding ⭐⭐⭐

### Problem E.1
Explain geometrically why the residual vector **e** is orthogonal to the column space of X. Draw or describe the picture.

**Your explanation:**
```




```

---

### Problem E.2
The Gauss-Markov theorem says OLS is BLUE. But under what circumstances might you prefer a biased estimator over OLS? Give a specific example.

**Your answer:**
```




```

---

### Problem E.3
Suppose the true model is y = β₀ + β₁x + β₂x² + ε, but you fit y = γ₀ + γ₁x + u.

a) Express E[γ̂₁] in terms of β₁ and β₂
b) Under what conditions is γ̂₁ unbiased for β₁?

**Your derivation:**
```
a)




b)


```

---

### Problem E.4
In Ridge regression, we minimize ||y - Xβ||² + λ||β||².

a) What happens to β̂_ridge as λ → 0?
b) What happens as λ → ∞?
c) Why might there exist a λ that gives lower prediction error than OLS?

**Your answers:**
```
a)


b)


c)



```

---

### Problem E.5
Consider standardizing variables before regression (subtract mean, divide by SD).

a) How does this affect the intercept?
b) How does this affect the interpretation of slope coefficients?
c) When is standardization particularly useful?

**Your answers:**
```
a)



b)



c)


```

---

## Section F: Challenge Problems ⭐⭐⭐⭐

### Problem F.1
Prove that the sample correlation between y and ŷ equals the square root of R².

**Your proof:**
```






```

---

### Problem F.2
In simple linear regression, prove that the regression line passes through the point (x̄, ȳ).

**Your proof:**
```




```

---

### Problem F.3
Show that for simple linear regression:

Var(ŷᵢ) = σ² · [1/n + (xᵢ - x̄)² / Σⱼ(xⱼ - x̄)²]

Interpret why variance of predictions is lowest at x̄.

**Your derivation and interpretation:**
```






```

---

### Problem F.4
The "hat matrix" H = X(X'X)⁻¹X' satisfies y_hat = Hy. Show that:
a) tr(H) = p (the number of parameters)
b) tr(I - H) = n - p

**Your proof:**
```
a)




b)


```

---

### Problem F.5
Consider two nested models:
- Reduced: y = X₁β₁ + ε
- Full: y = X₁β₁ + X₂β₂ + ε

The F-statistic for testing H₀: β₂ = 0 is:

F = [(RSS_R - RSS_F)/q] / [RSS_F/(n-p)]

where q = dim(β₂).

Show this is equivalent to testing whether the increase in R² is significant.

**Your derivation:**
```






```

---

## Self-Assessment

After completing these problems, rate your understanding:

| Topic | 1-5 Rating | Notes |
|-------|-----------|-------|
| OLS mechanics | | |
| Interpreting coefficients | | |
| R² and model fit | | |
| Hypothesis testing | | |
| Diagnostics | | |
| Multicollinearity | | |
| Gauss-Markov | | |
| Regularization concepts | | |

Areas to review:
```



```
