# Calculus for Optimization

## Why Calculus?

Finding the "best" regression coefficients means minimizing a loss function. Calculus tells us how to find minima of functions, and matrix calculus extends this to multiple dimensions.

---

## 1. Review: Single Variable Optimization

### Key Concepts

For f(x):
- Critical points: where f'(x) = 0
- Local minimum: f'(x) = 0 and f''(x) > 0
- Local maximum: f'(x) = 0 and f''(x) < 0

### Exercise 1.1 ⭐
**Question:** Find the minimum of f(x) = x² - 4x + 7.

*Your work:*

```
Step 1: Find f'(x)


Step 2: Set f'(x) = 0 and solve


Step 3: Verify it's a minimum using f''(x)


```

### Exercise 1.2 ⭐
**Question:** For simple linear regression with one data point (x₁, y₁), we minimize:

L(β) = (y₁ - βx₁)²

Find the optimal β.

*Your work:*

```




```

---

## 2. Partial Derivatives

### Key Concepts

For f(x, y), the partial derivatives are:
- ∂f/∂x: derivative treating y as constant
- ∂f/∂y: derivative treating x as constant

### Exercise 2.1 ⭐
**Question:** For f(x, y) = x² + 3xy + y² - 6x - 3y + 9, find:
- a) ∂f/∂x
- b) ∂f/∂y

*Your work:*

```
a)


b)

```

### Exercise 2.2 ⭐⭐
**Question:** Find the critical point of the function in Exercise 2.1 (solve ∂f/∂x = 0 and ∂f/∂y = 0 simultaneously).

*Your work:*

```
System of equations:



Solution:


```

---

## 3. The Gradient

### Key Concepts

The gradient is the vector of all partial derivatives:

∇f = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]ᵀ

Key properties:
- ∇f points in the direction of steepest ascent
- -∇f points in the direction of steepest descent
- At a minimum, ∇f = **0**

### Exercise 3.1 ⭐
**Question:** For f(**x**) = x₁² + 2x₂² + 3x₃² - 2x₁ - 4x₂:

- a) Write out the gradient ∇f
- b) Find the critical point

*Your work:*

```
a) ∇f =



b) Setting ∇f = 0:



```

### Exercise 3.2 ⭐⭐
**Question:** For the least squares objective:

L(β₀, β₁) = Σᵢ (yᵢ - β₀ - β₁xᵢ)²

- a) Compute ∂L/∂β₀
- b) Compute ∂L/∂β₁
- c) Write the gradient ∇L

*Your work:*

```
a) ∂L/∂β₀ =



b) ∂L/∂β₁ =



c) ∇L =


```

---

## 4. The Hessian

### Key Concepts

The Hessian is the matrix of second partial derivatives:

```
H = [∂²f/∂x₁²      ∂²f/∂x₁∂x₂  ...  ∂²f/∂x₁∂xₙ]
    [∂²f/∂x₂∂x₁   ∂²f/∂x₂²    ...  ∂²f/∂x₂∂xₙ]
    [   ⋮            ⋮         ⋱       ⋮     ]
    [∂²f/∂xₙ∂x₁   ∂²f/∂xₙ∂x₂  ...  ∂²f/∂xₙ²  ]
```

For smooth functions, H is symmetric (mixed partials are equal).

### Second Derivative Test (Multivariable)

At a critical point:
- If H is positive definite → local minimum
- If H is negative definite → local maximum
- If H has both positive and negative eigenvalues → saddle point

### Exercise 4.1 ⭐⭐
**Question:** For f(x, y) = x² + xy + y²:

- a) Find the gradient
- b) Find the Hessian
- c) Classify the critical point

*Your work:*

```
a) ∇f =


b) H =


c) Classification:



```

### Exercise 4.2 ⭐⭐⭐
**Question:** For the least squares objective L(β₀, β₁) = Σᵢ (yᵢ - β₀ - β₁xᵢ)²:

- a) Compute the Hessian
- b) Under what conditions is it positive definite?
- c) What does this tell us about the least squares solution?

*Your work:*

```
a) H =




b) Positive definite when:



c) Interpretation:


```

---

## 5. Matrix Calculus

### Key Results You Need

These are the essential matrix calculus identities for regression:

| Function | Derivative |
|----------|------------|
| f(**x**) = **a**ᵀ**x** | ∇f = **a** |
| f(**x**) = **x**ᵀ**a** | ∇f = **a** |
| f(**x**) = **x**ᵀA**x** | ∇f = (A + Aᵀ)**x** = 2A**x** if A symmetric |
| f(**x**) = **x**ᵀ**x** | ∇f = 2**x** |
| f(**x**) = ||A**x** - **b**||² | ∇f = 2Aᵀ(A**x** - **b**) |

### Exercise 5.1 ⭐⭐
**Question:** Verify that ∂/∂**x** (**a**ᵀ**x**) = **a** by expanding **a**ᵀ**x** = Σᵢ aᵢxᵢ and taking partial derivatives.

*Your verification:*

```




```

### Exercise 5.2 ⭐⭐
**Question:** Verify that ∂/∂**x** (**x**ᵀA**x**) = 2A**x** for symmetric A by:
- a) Expanding **x**ᵀA**x** for a 2×2 case
- b) Taking partial derivatives with respect to x₁ and x₂
- c) Showing the result equals 2A**x**

*Your verification:*

```
a) Expansion (let A = [a b; b c], symmetric):
   xᵀAx =



b) Partial derivatives:
   ∂/∂x₁ =

   ∂/∂x₂ =


c) Show this equals 2Ax:



```

### Exercise 5.3 ⭐⭐⭐
**Question:** The least squares objective in matrix form is:

L(**β**) = (**y** - X**β**)ᵀ(**y** - X**β**)

Expand this and use matrix calculus to find ∇L.

*Your derivation:*

```
Step 1: Expand the product




Step 2: Take the gradient with respect to β




Step 3: Simplify



```

---

## 6. Convexity

### Key Concepts

A function f is **convex** if:
- f(λx + (1-λ)y) ≤ λf(x) + (1-λ)f(y) for all x, y and λ ∈ [0,1]
- Geometrically: the line segment between any two points lies above the graph
- Equivalently: the Hessian is positive semi-definite everywhere

For convex functions:
- Any local minimum is a global minimum
- If strictly convex, there is at most one minimum

### Exercise 6.1 ⭐⭐
**Question:** Prove that f(x) = x² is convex using the definition.

*Your proof:*

```
Need to show: f(λx + (1-λ)y) ≤ λf(x) + (1-λ)f(y)

LHS =


RHS =


Show LHS ≤ RHS:



```

### Exercise 6.2 ⭐⭐⭐
**Question:** Prove that the least squares objective L(**β**) = ||**y** - X**β**||² is convex in **β**.

*Your proof:*

```
Hint: Use the Hessian approach - show H is positive semi-definite.




```

### Exercise 6.3 ⭐⭐
**Question:** Why is convexity important for linear regression? What guarantee does it give us?

*Your answer:*

```




```

---

## 7. Gradient Descent

### Key Concepts

Gradient descent iteratively updates:

**β**ₜ₊₁ = **β**ₜ - α∇L(**β**ₜ)

Where α > 0 is the learning rate (step size).

### Exercise 7.1 ⭐⭐
**Question:** For f(x) = (x - 3)²:
- a) Compute f'(x)
- b) Starting from x₀ = 0 with α = 0.1, compute x₁, x₂, x₃

*Your work:*

```
a) f'(x) =


b) Iterations:
   x₁ = x₀ - αf'(x₀) =

   x₂ = x₁ - αf'(x₁) =

   x₃ = x₂ - αf'(x₂) =

```

### Exercise 7.2 ⭐⭐
**Question:** What happens if α is:
- a) Too small?
- b) Too large?
- c) For quadratic functions, what is the optimal α in terms of the Hessian?

*Your answers:*

```
a)


b)


c)

```

### Exercise 7.3 ⭐⭐⭐
**Question:** For linear regression, derive the gradient descent update rule:

Starting from L(**β**) = ||**y** - X**β**||², derive:

**β**ₜ₊₁ = **β**ₜ - α · (?)

*Your derivation:*

```




```

---

## Summary Checklist

Before moving on, make sure you can:

- [ ] Find critical points using gradients
- [ ] Classify critical points using the Hessian
- [ ] Apply key matrix calculus identities
- [ ] Derive ∇L for the least squares objective
- [ ] Prove the least squares objective is convex
- [ ] Explain why convexity guarantees a unique minimum
- [ ] Derive the gradient descent update rule

---

## Further Reading

- Boyd & Vandenberghe - "Convex Optimization" (Chapter 3)
- The Matrix Cookbook (free PDF online)
- 3Blue1Brown - "Gradient Descent" (YouTube)
