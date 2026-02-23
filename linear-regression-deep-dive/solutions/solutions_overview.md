# Solutions Overview

## ⚠️ WARNING: SOLUTIONS AHEAD!

**Please attempt all problems yourself before checking solutions!**

Struggling with problems is how you learn. Only use these solutions to:
1. Check your work after completing a problem
2. Get unstuck after spending significant time
3. Review material you've already learned

---

## How to Use Solutions

1. **Hide this folder** - Consider moving it somewhere less visible
2. **Time-box struggles** - If stuck for 20+ minutes, take a hint
3. **Understand, don't copy** - Reading a solution ≠ learning

---

## Solutions Index

### Mathematical Foundations
- [Linear Algebra Solutions](01_linear_algebra_solutions.md)
- [Calculus Solutions](02_calculus_solutions.md)
- [Probability Solutions](03_probability_solutions.md)

### Derivations and Proofs
- [Normal Equations Solutions](04_normal_equations_solutions.md)
- [OLS Properties Solutions](05_ols_properties_solutions.md)
- [Hypothesis Testing Solutions](06_hypothesis_testing_solutions.md)

### Coding Challenges
- [OLS Implementation](coding_solutions/01_ols_solution.py)
- [Gradient Descent](coding_solutions/02_gradient_descent_solution.py)
- [Regularization](coding_solutions/03_regularization_solution.py)
- [Diagnostics](coding_solutions/04_diagnostics_solution.py)

### Problem Sets
- [Conceptual Problems](07_conceptual_solutions.md)
- [Computational Problems](08_computational_solutions.md)
- [Case Studies](09_case_studies_solutions.md)

---

## Quick Reference: Key Results

### The Normal Equations
```
β̂ = (X'X)⁻¹X'y
```

### OLS Properties
```
E[β̂] = β                    (unbiased)
Var(β̂) = σ²(X'X)⁻¹          (variance)
```

### Simple Linear Regression
```
β̂₁ = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²  = Sxy/Sxx
β̂₀ = ȳ - β̂₁x̄
```

### Test Statistics
```
t = (β̂ⱼ - β⁰ⱼ) / SE(β̂ⱼ)     ~ t_{n-p}

F = [R²/(p-1)] / [(1-R²)/(n-p)]  ~ F_{p-1,n-p}
```

### R² and Adjusted R²
```
R² = 1 - RSS/TSS = 1 - Σ(yᵢ-ŷᵢ)²/Σ(yᵢ-ȳ)²

R̄² = 1 - (n-1)/(n-p) · (1-R²)
```

### Ridge Regression
```
β̂_ridge = (X'X + λI)⁻¹X'y
```

### Gauss-Markov
Under assumptions (linearity, E[ε|X]=0, Var(ε|X)=σ²I, no perfect multicollinearity):
OLS is BLUE (Best Linear Unbiased Estimator)

---

## Remember

> "The only way to learn mathematics is to do mathematics." - Paul Halmos

Good luck with your studies!
