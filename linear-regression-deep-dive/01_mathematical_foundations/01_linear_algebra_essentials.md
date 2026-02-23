# Linear Algebra Essentials for Linear Regression

## Why Linear Algebra?

Linear regression is fundamentally a linear algebra problem. The "linear" in linear regression refers to linearity in the parameters, and understanding the geometry of vector spaces gives you deep intuition about what regression is actually doing.

---

## 1. Vectors and Vector Spaces

### Key Concepts to Understand

A vector **x** ∈ ℝⁿ is an ordered collection of n real numbers:

```
x = [x₁, x₂, ..., xₙ]ᵀ
```

### Exercise 1.1 ⭐
**Question:** Given vectors **a** = [1, 2, 3]ᵀ and **b** = [4, 5, 6]ᵀ, compute:
- a) **a** + **b**
- b) 3**a**
- c) **a** · **b** (dot product)
- d) ||**a**|| (Euclidean norm)

*Space for your work:*

```
a)

b)

c)

d)
```

### Exercise 1.2 ⭐
**Question:** What is the geometric interpretation of the dot product **a** · **b**? When is it zero?

*Your answer:*

```




```

---

## 2. Matrices and Matrix Operations

### Key Concepts

A matrix **A** ∈ ℝᵐˣⁿ has m rows and n columns. Key operations:
- Matrix multiplication: (AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ
- Transpose: (Aᵀ)ᵢⱼ = Aⱼᵢ
- Inverse: AA⁻¹ = A⁻¹A = I (only for square, non-singular matrices)

### Exercise 2.1 ⭐
**Question:** Given:
```
A = [1  2]    B = [5  6]
    [3  4]        [7  8]
```

Compute:
- a) AB
- b) BA
- c) Aᵀ
- d) Is AB = BA? What does this tell you?

*Space for your work:*

```
a) AB =



b) BA =



c) Aᵀ =


d)
```

### Exercise 2.2 ⭐⭐
**Question:** Prove that (AB)ᵀ = BᵀAᵀ for conformable matrices A and B.

*Your proof:*

```






```

---

## 3. Column Space and Row Space

### Key Concepts

For matrix **X** ∈ ℝⁿˣᵖ:
- **Column space** C(X): All possible linear combinations of columns of X
- **Row space** R(X): All possible linear combinations of rows of X
- **Rank**: Dimension of the column space (= dimension of row space)

### Exercise 3.1 ⭐⭐
**Question:** Consider the design matrix in regression:
```
X = [1  x₁]
    [1  x₂]
    [1  x₃]
```

- a) What is the dimension of the column space of X?
- b) What does it mean geometrically that the column space is 2-dimensional in ℝ³?
- c) Why is the column space important for understanding linear regression?

*Your answers:*

```
a)


b)


c)


```

### Exercise 3.2 ⭐⭐
**Question:** When will the matrix XᵀX be invertible? What happens to linear regression when it's not?

*Your answer:*

```




```

---

## 4. Projections - THE Key Concept

### Why Projections Matter

**Linear regression IS projection.** You're projecting the response vector **y** onto the column space of **X**.

### The Projection Matrix

The projection of **y** onto C(X) is:
```
ŷ = X(XᵀX)⁻¹Xᵀy = Py
```

Where P = X(XᵀX)⁻¹Xᵀ is the **projection matrix** (also called the "hat matrix" because it puts the hat on y).

### Exercise 4.1 ⭐⭐
**Question:** Prove that the projection matrix P = X(XᵀX)⁻¹Xᵀ is:
- a) Symmetric (P = Pᵀ)
- b) Idempotent (P² = P)

*Your proofs:*

```
a) Prove P = Pᵀ:





b) Prove P² = P:





```

### Exercise 4.2 ⭐⭐
**Question:** What is the geometric interpretation of idempotency (P² = P)? Why does it make sense for a projection?

*Your answer:*

```




```

### Exercise 4.3 ⭐⭐⭐
**Question:** The residual vector is **e** = **y** - **ŷ** = (I - P)**y**.

Prove that **e** is orthogonal to every column of X. (Hint: Show Xᵀe = 0)

*Your proof:*

```






```

---

## 5. Eigenvalues and Eigenvectors

### Key Concepts

For square matrix A, if A**v** = λ**v** for non-zero **v**, then:
- λ is an eigenvalue
- **v** is the corresponding eigenvector

### Exercise 5.1 ⭐⭐
**Question:** Find the eigenvalues and eigenvectors of:
```
A = [4  1]
    [2  3]
```

*Your work:*

```
Step 1: Set up det(A - λI) = 0




Step 2: Solve the characteristic polynomial




Step 3: Find eigenvectors for each eigenvalue




```

### Exercise 5.2 ⭐⭐⭐
**Question:** For the matrix XᵀX in regression:
- a) Prove that all eigenvalues are non-negative
- b) What does it mean when an eigenvalue is zero?
- c) How do eigenvalues relate to multicollinearity?

*Your answers:*

```
a)



b)



c)


```

---

## 6. Positive Definite Matrices

### Key Concepts

A symmetric matrix A is **positive definite** if **x**ᵀA**x** > 0 for all non-zero **x**.

Equivalently:
- All eigenvalues are positive
- All leading principal minors are positive
- A = BᵀB for some invertible B

### Exercise 6.1 ⭐⭐
**Question:** Prove that XᵀX is always positive semi-definite (i.e., **x**ᵀ(XᵀX)**x** ≥ 0 for all **x**).

*Your proof:*

```




```

### Exercise 6.2 ⭐⭐
**Question:** Under what conditions is XᵀX positive definite (strictly positive)? Why does this matter for regression?

*Your answer:*

```




```

---

## 7. The Geometry of Least Squares

### The Big Picture

Imagine:
- **y** ∈ ℝⁿ is a vector in n-dimensional space
- C(X) is a p-dimensional subspace (where p < n)
- We want the point in C(X) closest to **y**

The closest point is the **orthogonal projection** of **y** onto C(X).

### Exercise 7.1 ⭐⭐⭐
**Question:** Draw (or describe) the geometry of simple linear regression (n=3 data points, fitting y = β₀ + β₁x):

- a) What are the dimensions involved?
- b) What does the column space look like?
- c) Where is **y** relative to this subspace?
- d) Where is **ŷ**?
- e) What direction does the residual vector point?

*Your description/drawing:*

```








```

### Exercise 7.2 ⭐⭐⭐
**Question:** Why does minimizing ||**y** - **ŷ**||² give the same answer as finding the orthogonal projection? Prove this is equivalent to requiring **e** ⊥ C(X).

*Your proof:*

```






```

---

## Summary Checklist

Before moving on, make sure you can:

- [ ] Compute dot products, matrix products, and transposes fluently
- [ ] Explain what the column space of X represents
- [ ] Derive and explain the projection matrix P
- [ ] Prove P is symmetric and idempotent
- [ ] Explain why e ⊥ C(X)
- [ ] Describe when XᵀX is invertible
- [ ] Explain the connection between eigenvalues and multicollinearity
- [ ] Visualize regression as orthogonal projection

---

## Further Reading

- Strang, G. - "Linear Algebra and Its Applications" (Chapter 4)
- Lay, D. - "Linear Algebra and Its Applications" (Chapter 6)
- 3Blue1Brown - "Essence of Linear Algebra" (YouTube series)
