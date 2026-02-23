# Connections to Machine Learning

## Linear Regression: The Foundation

Linear regression isn't just a standalone technique—it's the foundation for understanding many machine learning methods. This module explores these connections.

---

## Part 1: Linear Regression → Neural Networks

### The Simplest Neural Network

A single-layer neural network with no activation function IS linear regression:

```
Input: x ∈ ℝᵖ
Output: y = wᵀx + b
```

This is exactly y = β₀ + β₁x₁ + ... + βₚxₚ

### Exercise 1.1 ⭐⭐
**Question:** If neural networks are "just" stacked linear transformations with nonlinear activations, what happens if we remove all activations?

*Your answer:*
```




```

### Exercise 1.2 ⭐⭐
**Question:** The loss function in neural networks (MSE for regression) is the same as in OLS. But why don't we solve neural networks with the normal equations?

*Your answer:*
```




```

### Exercise 1.3 ⭐⭐⭐
**Question:** In neural networks, we use gradient descent. Derive the gradient descent update for linear regression and show it's identical to the neural network update.

*Your derivation:*
```
Loss: L(β) = (1/2n)||y - Xβ||²

Gradient: ∇L =



Update: β_{t+1} = β_t - α∇L =



For a neural network with one layer (no activation):

Forward pass: ŷ =

Backward pass: ∂L/∂w =

Update: w_{t+1} =


These are identical when:

```

---

## Part 2: Regularization Across ML

### The Regularization Framework

Many ML methods minimize: Loss + λ × Penalty

| Method | Loss | Penalty |
|--------|------|---------|
| Ridge Regression | ||y - Xβ||² | ||β||² |
| Lasso | ||y - Xβ||² | ||β||₁ |
| Elastic Net | ||y - Xβ||² | α||β||₁ + (1-α)||β||² |
| SVM (regression) | ε-insensitive | ||w||² |
| Neural Networks | Cross-entropy or MSE | ||w||² (weight decay) |

### Exercise 2.1 ⭐⭐
**Question:** "Weight decay" in neural networks is mathematically equivalent to which regression technique?

*Your answer:*
```


```

### Exercise 2.2 ⭐⭐⭐
**Question:** L1 regularization (Lasso) promotes sparsity. Why doesn't L2 (Ridge)?

*Hint:* Consider the geometry of the constraint regions.

*Your explanation with sketch:*
```




```

### Exercise 2.3 ⭐⭐⭐
**Question:** Dropout in neural networks has been shown to be approximately equivalent to L2 regularization. Explain the intuition.

*Your explanation:*
```




```

---

## Part 3: Kernel Methods and Linear Regression

### Kernelized Linear Regression

The "kernel trick" allows linear regression in high-dimensional feature spaces.

For features φ(x), we want: y = φ(x)ᵀβ

But instead of computing φ(x) explicitly, we use: K(x, x') = φ(x)ᵀφ(x')

### Exercise 3.1 ⭐⭐⭐
**Question:** The solution to kernelized ridge regression is:

f(x*) = k(x*)ᵀ(K + λI)⁻¹y

Where k(x*) = [K(x*, x₁), ..., K(x*, xₙ)]ᵀ and K is the n×n kernel matrix.

What is the computational complexity of:
a) Standard ridge regression with p features
b) Kernelized ridge regression with n observations

When is each preferable?

*Your analysis:*
```
a) Standard ridge: Complexity of (X'X + λI)⁻¹ is O(   )



b) Kernelized: Complexity of (K + λI)⁻¹ is O(   )



Preferable when:



```

### Exercise 3.2 ⭐⭐⭐
**Question:** Gaussian Process Regression is kernelized Bayesian linear regression. Explain the connection.

*Your explanation:*
```




```

---

## Part 4: GLMs and Beyond

### Generalized Linear Models

Linear regression assumes y is continuous. GLMs extend to:
- **Logistic regression**: y ∈ {0, 1}, link = logit
- **Poisson regression**: y ∈ {0, 1, 2, ...}, link = log
- **etc.**

All share: g(E[y]) = Xβ (linear in the link function)

### Exercise 4.1 ⭐⭐
**Question:** In logistic regression, we model:

log(p/(1-p)) = Xβ

How is this "linear" regression?

*Your answer:*
```




```

### Exercise 4.2 ⭐⭐⭐
**Question:** Why can't we use OLS for logistic regression?

*Your answer:*
```




```

### Exercise 4.3 ⭐⭐⭐
**Question:** The loss function for logistic regression is cross-entropy loss. Show that maximizing log-likelihood is equivalent to minimizing cross-entropy.

*Your derivation:*
```




```

---

## Part 5: PCA and Linear Regression

### Principal Component Regression (PCR)

1. Perform PCA on X to get principal components Z
2. Regress y on the first k principal components
3. Transform back to original variables

### Exercise 5.1 ⭐⭐
**Question:** When would PCR be useful compared to standard regression?

*Your answer:*
```




```

### Exercise 5.2 ⭐⭐⭐
**Question:** Ridge regression and PCR are related. Both can be written in terms of the SVD of X. Explain the connection.

*Hint:* If X = UDVᵀ, ridge regression shrinks each component by d²ⱼ/(d²ⱼ + λ), while PCR keeps some components entirely and discards others.

*Your explanation:*
```




```

### Exercise 5.3 ⭐⭐⭐
**Question:** Why might Ridge regression be preferred over PCR?

*Your answer:*
```




```

---

## Part 6: Ensemble Methods

### Bagging and Random Forests

Random Forests combine many decision trees. But what happens if we "bag" linear regressions?

### Exercise 6.1 ⭐⭐
**Question:** If we fit 100 different linear regressions on bootstrap samples and average the predictions, what do we get?

*Your analysis:*
```




```

### Exercise 6.2 ⭐⭐
**Question:** Boosting builds models sequentially, each correcting errors of the previous. "Boosted regression" starts with linear regression and iteratively fits residuals. How does this relate to forward stagewise regression?

*Your explanation:*
```




```

---

## Part 7: The Bias-Variance Tradeoff

### The Master Concept

Expected Test Error = Bias² + Variance + Irreducible Noise

This applies to ALL supervised learning.

### Exercise 7.1 ⭐⭐
**Question:** Fill in the bias-variance for each:

| Method | Bias | Variance | When Good |
|--------|------|----------|-----------|
| OLS | | | |
| Ridge | | | |
| Lasso | | | |
| Subset selection | | | |

*Your table:*
```
| Method          | Bias  | Variance | When Good                    |
|-----------------|-------|----------|------------------------------|
| OLS             |       |          |                              |
| Ridge           |       |          |                              |
| Lasso           |       |          |                              |
| Subset selection|       |          |                              |
```

### Exercise 7.2 ⭐⭐⭐
**Question:** Derive the bias-variance decomposition for linear regression.

For a new point x*, the expected squared error is:

E[(y* - ŷ*)²] = Bias²(ŷ*) + Var(ŷ*) + σ²

*Your derivation:*
```
E[(y* - ŷ*)²] = E[(y* - E[ŷ*] + E[ŷ*] - ŷ*)²]

             =




```

### Exercise 7.3 ⭐⭐⭐
**Question:** Ridge regression introduces bias to reduce variance. Show mathematically that Var(β̂_ridge) < Var(β̂_OLS).

*Your proof:*
```




```

---

## Part 8: Modern Perspectives

### Deep Learning and Linear Regression

Recent research has revealed surprising connections:
- Neural networks in "lazy training" regime behave like kernel regression
- Wide neural networks converge to Gaussian Processes
- The "neural tangent kernel" connects deep learning to linear models

### Exercise 8.1 ⭐⭐⭐⭐
**Question:** The Neural Tangent Kernel (NTK) for a neural network f(x; θ) is:

K_NTK(x, x') = ⟨∇_θ f(x; θ), ∇_θ f(x'; θ)⟩

For an infinitely wide network, this kernel is constant during training, making the network equivalent to kernel regression.

Why is this connection important?

*Your answer:*
```




```

### Exercise 8.2 ⭐⭐⭐
**Question:** "Double descent" is a phenomenon where test error first increases, then decreases, as model complexity increases past the interpolation threshold. How does this challenge the classical bias-variance picture?

*Your explanation:*
```




```

---

## Synthesis Questions

### Question S.1 ⭐⭐⭐⭐
Create a concept map showing how linear regression connects to at least 5 other ML methods.

*Your concept map:*
```







```

### Question S.2 ⭐⭐⭐
If you had to teach someone the most important concept from linear regression that transfers to all of ML, what would it be and why?

*Your answer:*
```




```

### Question S.3 ⭐⭐⭐⭐
Design an experiment to compare:
- Linear regression
- Ridge regression
- Lasso
- Neural network (1 hidden layer)
- Random forest

What datasets would you use? What metrics? What would you expect to find?

*Your experimental design:*
```
Datasets:



Metrics:



Expected findings:



```

---

## Summary

Linear regression connects to:
1. **Neural networks**: Single layer, no activation
2. **Regularization**: Ridge, Lasso, weight decay
3. **Kernels**: Basis expansion, Gaussian Processes
4. **GLMs**: Extends to non-Gaussian responses
5. **Dimensionality reduction**: PCR, partial least squares
6. **Ensembles**: Bagging, boosting foundations
7. **Bias-variance**: The master tradeoff

Understanding linear regression deeply means understanding the foundations of machine learning.

## Further Reading

- Hastie, Tibshirani, Friedman - "Elements of Statistical Learning"
- Murphy - "Machine Learning: A Probabilistic Perspective"
- Goodfellow, Bengio, Courville - "Deep Learning" (especially Chapter 5)
