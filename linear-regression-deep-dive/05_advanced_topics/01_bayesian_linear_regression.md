# Bayesian Linear Regression

## Why Go Bayesian?

Frequentist OLS gives point estimates. Bayesian regression gives:
- Full probability distributions over parameters
- Natural uncertainty quantification
- Principled way to incorporate prior knowledge
- Automatic regularization via priors

---

## Part 1: The Bayesian Framework

### Key Concepts

**Bayes' Theorem for Regression:**

P(β | y, X) = P(y | X, β) · P(β) / P(y | X)

- **Likelihood**: P(y | X, β) - how likely is the data given parameters
- **Prior**: P(β) - our beliefs about β before seeing data
- **Posterior**: P(β | y, X) - our updated beliefs after seeing data
- **Evidence**: P(y | X) - normalizing constant (often ignored)

### Exercise 1.1 ⭐⭐
**Question:** In frequentist regression, we find a single β̂. In Bayesian regression, we get a distribution. What are the advantages and disadvantages of each approach?

*Your answer:*
```
Frequentist advantages:



Frequentist disadvantages:



Bayesian advantages:



Bayesian disadvantages:


```

### Exercise 1.2 ⭐⭐
**Question:** The posterior is proportional to likelihood × prior:

P(β | y) ∝ P(y | β) · P(β)

Why can we ignore the denominator P(y) for most purposes?

*Your answer:*
```




```

---

## Part 2: Conjugate Priors

### The Normal-Normal Model

If:
- Likelihood: y | X, β, σ² ~ N(Xβ, σ²I)
- Prior: β ~ N(μ₀, Σ₀)

Then the posterior is also Normal (conjugate):
- Posterior: β | y, X, σ² ~ N(μₙ, Σₙ)

Where:
- Σₙ = (Σ₀⁻¹ + (1/σ²)XᵀX)⁻¹
- μₙ = Σₙ(Σ₀⁻¹μ₀ + (1/σ²)Xᵀy)

### Exercise 2.1 ⭐⭐⭐
**Question:** Derive the posterior mean μₙ and covariance Σₙ.

*Hint:* The posterior is proportional to exp(-½ · quadratic form in β). Complete the square.

*Your derivation:*
```
Posterior ∝ Likelihood × Prior

Log posterior ∝ -½(y - Xβ)ᵀ(1/σ²)I(y - Xβ) - ½(β - μ₀)ᵀΣ₀⁻¹(β - μ₀)

Expanding:




Collecting terms in β:




Completing the square:




Therefore:
Σₙ =

μₙ =

```

### Exercise 2.2 ⭐⭐⭐
**Question:** Show that as the prior variance goes to infinity (Σ₀ → ∞I, i.e., uninformative prior), the posterior mean approaches the OLS estimate.

*Your proof:*
```




```

### Exercise 2.3 ⭐⭐⭐
**Question:** Show that as n → ∞, the posterior variance Σₙ → 0 (the posterior concentrates on a point).

*Your proof:*
```




```

---

## Part 3: Ridge Regression as Bayesian MAP

### The Connection

Maximum A Posteriori (MAP) estimation finds the mode of the posterior:

β̂_MAP = argmax P(β | y, X)
       = argmax P(y | X, β) · P(β)

### Exercise 3.1 ⭐⭐⭐
**Question:** Show that Ridge regression is MAP estimation with a specific prior.

If we use:
- Likelihood: y | β ~ N(Xβ, σ²I)
- Prior: β ~ N(0, τ²I)

Show that β̂_MAP = (XᵀX + (σ²/τ²)I)⁻¹Xᵀy = β̂_ridge with λ = σ²/τ².

*Your derivation:*
```
Log posterior = log P(y|β) + log P(β) + const

             = -1/(2σ²)||y - Xβ||² - 1/(2τ²)||β||² + const

β̂_MAP maximizes this, or equivalently minimizes:




Setting gradient to zero:




Therefore:


```

### Exercise 3.2 ⭐⭐⭐
**Question:** What prior on β corresponds to Lasso regression? Note: This prior is not conjugate.

*Your answer:*
```




```

### Exercise 3.3 ⭐⭐
**Question:** In the Ridge-as-Bayesian interpretation, what does a larger prior variance τ² mean? What does a smaller τ² mean?

*Your interpretation:*
```
Larger τ²:



Smaller τ²:


```

---

## Part 4: Posterior Predictive Distribution

### Making Predictions the Bayesian Way

Instead of a point prediction, we get a distribution:

P(y* | x*, y, X) = ∫ P(y* | x*, β) P(β | y, X) dβ

This integrates over all possible β values, weighted by their posterior probability.

### Exercise 4.1 ⭐⭐⭐
**Question:** For the conjugate normal model with known σ², derive the posterior predictive distribution for a new observation y* at x*.

*Hint:* If β | y ~ N(μₙ, Σₙ) and y* | β ~ N(x*ᵀβ, σ²), then y* | y is also Normal.

*Your derivation:*
```
y* | β ~ N(x*ᵀβ, σ²)

β | y ~ N(μₙ, Σₙ)

Using the law of total variance:

E[y* | y] = E[E[y* | β] | y]
          =


Var(y* | y) = E[Var(y* | β) | y] + Var(E[y* | β] | y)
            =


Therefore:
y* | y, x* ~

```

### Exercise 4.2 ⭐⭐
**Question:** Compare the Bayesian predictive interval to the frequentist prediction interval. How do they differ?

*Your comparison:*
```
Frequentist prediction interval:



Bayesian predictive interval:



Key differences:


```

---

## Part 5: Unknown Variance

### The Full Bayesian Model

In practice, σ² is unknown. The full Bayesian model is:

- Likelihood: y | X, β, σ² ~ N(Xβ, σ²I)
- Prior on β: β | σ² ~ N(0, σ²Σ₀)  [often scaled by σ²]
- Prior on σ²: σ² ~ Inverse-Gamma(a, b)

### Exercise 5.1 ⭐⭐⭐
**Question:** Why do we often use β | σ² ~ N(0, σ²Σ₀) rather than β ~ N(0, Σ₀)?

*Hint:* This is called a g-prior or Zellner's prior.

*Your answer:*
```




```

### Exercise 5.2 ⭐⭐⭐
**Question:** With unknown σ², the marginal posterior of β (integrating out σ²) follows a t-distribution rather than Normal. Why does this make sense?

*Your explanation:*
```




```

---

## Part 6: Bayesian Model Comparison

### Bayes Factors

To compare models M₁ and M₂:

BF₁₂ = P(y | M₁) / P(y | M₂)

Where P(y | M) = ∫ P(y | θ, M) P(θ | M) dθ is the marginal likelihood.

### Exercise 6.1 ⭐⭐⭐
**Question:** What does a Bayes Factor of 10 mean? What about 0.1?

*Your interpretation:*
```
BF₁₂ = 10:



BF₁₂ = 0.1:


```

### Exercise 6.2 ⭐⭐⭐⭐
**Question:** The marginal likelihood naturally penalizes complex models (Bayesian Occam's Razor). Explain intuitively why this happens.

*Hint:* A complex model spreads its prior probability over more possibilities.

*Your explanation:*
```




```

---

## Part 7: Computational Methods

### When Conjugacy Fails

Real Bayesian problems often require computational methods:
- **MCMC (Markov Chain Monte Carlo)**: Sample from the posterior
- **Variational Inference**: Approximate the posterior with a simpler distribution

### Exercise 7.1 ⭐⭐⭐
**Question:** Describe the Gibbs sampling algorithm for Bayesian linear regression with unknown σ².

*Your description:*
```
Initialize β⁽⁰⁾ and (σ²)⁽⁰⁾

For t = 1, 2, ..., T:

  Step 1: Sample β⁽ᵗ⁾ from P(β | y, X, (σ²)⁽ᵗ⁻¹⁾)
          This distribution is:


  Step 2: Sample (σ²)⁽ᵗ⁾ from P(σ² | y, X, β⁽ᵗ⁾)
          This distribution is:


After burn-in, {β⁽ᵗ⁾, (σ²)⁽ᵗ⁾} are samples from the joint posterior.

```

---

## Exercises: Implement Bayesian Regression

### Coding Exercise 7.1 ⭐⭐⭐
Implement Bayesian linear regression with conjugate Normal prior (known σ²).

```python
import numpy as np

def bayesian_linear_regression(X, y, sigma_sq, prior_mean, prior_cov):
    """
    Compute posterior mean and covariance for Bayesian linear regression.

    Args:
        X: Design matrix (n, p)
        y: Response vector (n,)
        sigma_sq: Known error variance
        prior_mean: Prior mean for beta (p,)
        prior_cov: Prior covariance for beta (p, p)

    Returns:
        posterior_mean: Posterior mean (p,)
        posterior_cov: Posterior covariance (p, p)
    """
    # TODO: Implement the posterior calculations
    # Σₙ = (Σ₀⁻¹ + (1/σ²)XᵀX)⁻¹
    # μₙ = Σₙ(Σ₀⁻¹μ₀ + (1/σ²)Xᵀy)

    pass


def posterior_predictive(x_new, posterior_mean, posterior_cov, sigma_sq):
    """
    Compute posterior predictive distribution for a new point.

    Args:
        x_new: New feature vector (p,)
        posterior_mean: Posterior mean of beta
        posterior_cov: Posterior covariance of beta
        sigma_sq: Error variance

    Returns:
        pred_mean: Predictive mean
        pred_var: Predictive variance
    """
    # TODO: Implement predictive distribution
    # E[y*] = x*ᵀμₙ
    # Var(y*) = σ² + x*ᵀΣₙx*

    pass
```

### Coding Exercise 7.2 ⭐⭐⭐⭐
Implement a Gibbs sampler for Bayesian linear regression with unknown σ².

```python
def gibbs_sampler(X, y, n_samples=5000, burn_in=1000):
    """
    Gibbs sampler for Bayesian linear regression.

    Prior: β ~ N(0, 100*I), σ² ~ Inverse-Gamma(0.01, 0.01)

    Args:
        X: Design matrix (n, p)
        y: Response vector (n,)
        n_samples: Number of samples to draw
        burn_in: Number of initial samples to discard

    Returns:
        beta_samples: Array of shape (n_samples - burn_in, p)
        sigma_sq_samples: Array of shape (n_samples - burn_in,)
    """
    # TODO: Implement Gibbs sampler
    # Step 1: Sample β | y, σ² from Normal
    # Step 2: Sample σ² | y, β from Inverse-Gamma

    pass
```

---

## Summary

Key takeaways from Bayesian Linear Regression:

1. **Priors encode beliefs**: Choice of prior matters, especially with small data
2. **Posteriors quantify uncertainty**: Full distribution, not just point estimate
3. **Regularization is Bayesian**: Ridge/Lasso correspond to specific priors
4. **Predictions are distributions**: Predictive intervals account for parameter uncertainty
5. **Model comparison via marginal likelihood**: Automatic Occam's razor

## Further Reading

- Gelman et al. - "Bayesian Data Analysis" (Chapter 14)
- Bishop - "Pattern Recognition and Machine Learning" (Chapter 3)
- Murphy - "Machine Learning: A Probabilistic Perspective" (Chapter 7)
