# Problem Set 3: Applied Case Studies

## Instructions
These problems simulate real-world regression analysis scenarios.
For each case study, work through the analysis systematically.

---

## Case Study 1: Housing Prices ⭐⭐

### Background
You're analyzing house sale prices. The dataset contains:
- `price`: Sale price ($1000s)
- `sqft`: Square footage
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `age`: Age of house (years)
- `garage`: Number of garage spaces
- `pool`: 1 if has pool, 0 otherwise

n = 200 houses

### Preliminary Analysis Output

**Correlation Matrix:**
```
           price   sqft   beds   baths   age   garage
price      1.00   0.85   0.65   0.72   -0.35   0.45
sqft       0.85   1.00   0.75   0.80   -0.20   0.50
beds       0.65   0.75   1.00   0.60   -0.10   0.35
baths      0.72   0.80   0.60   1.00   -0.15   0.40
age       -0.35  -0.20  -0.10  -0.15    1.00  -0.25
garage     0.45   0.50   0.35   0.40   -0.25   1.00
```

### Regression Output

**Model 1: Price ~ Sqft + Bedrooms + Bathrooms + Age + Garage + Pool**

| Variable | Coef | SE | t-stat | p-value |
|----------|------|-----|--------|---------|
| Intercept | 15.2 | 12.5 | 1.22 | 0.225 |
| sqft | 0.085 | 0.012 | 7.08 | <0.001 |
| bedrooms | -8.5 | 4.2 | -2.02 | 0.044 |
| bathrooms | 22.3 | 7.8 | 2.86 | 0.005 |
| age | -0.95 | 0.25 | -3.80 | <0.001 |
| garage | 12.4 | 5.1 | 2.43 | 0.016 |
| pool | 18.7 | 8.9 | 2.10 | 0.037 |

R² = 0.78, Adjusted R² = 0.77
F(6, 193) = 112.5, p < 0.001
MSE = 625 (so s ≈ 25)

VIFs: sqft=3.2, beds=2.1, baths=2.8, age=1.3, garage=1.4, pool=1.1

### Questions

**Q1.1:** Interpret the coefficient on `sqft`. Be precise.
```
Your interpretation:




```

**Q1.2:** The coefficient on `bedrooms` is negative! Explain how this can happen and what it means.
```
Your explanation:




```

**Q1.3:** Are there multicollinearity concerns? What evidence supports your answer?
```
Your analysis:




```

**Q1.4:** Construct a 95% CI for the effect of having a pool.
```
Your calculation:




```

**Q1.5:** A client asks: "What's the expected price for a 2000 sqft, 3 bed, 2 bath, 10-year-old house with 2 garage spaces and a pool?" Calculate the point prediction.
```
Your calculation:




```

**Q1.6:** The residual plot shows a slight funnel shape (variance increasing with fitted values). What does this suggest and what might you do?
```
Your response:




```

**Q1.7:** Would you recommend any transformations? Why?
```
Your recommendation:




```

---

## Case Study 2: Marketing Effectiveness ⭐⭐⭐

### Background
A company wants to understand how advertising spending affects sales. Data from 50 regional markets:
- `sales`: Weekly sales (units)
- `tv`: TV advertising budget ($1000s)
- `radio`: Radio advertising budget ($1000s)
- `newspaper`: Newspaper advertising budget ($1000s)

### Regression Output

**Model A: Sales ~ TV + Radio + Newspaper**

| Variable | Coef | SE | t-stat | p-value |
|----------|------|-----|--------|---------|
| Intercept | 2.94 | 0.31 | 9.42 | <0.001 |
| tv | 0.046 | 0.001 | 32.8 | <0.001 |
| radio | 0.189 | 0.009 | 21.9 | <0.001 |
| newspaper | -0.001 | 0.006 | -0.18 | 0.860 |

R² = 0.897, Adjusted R² = 0.890

**Model B: Sales ~ TV + Radio**

| Variable | Coef | SE | t-stat | p-value |
|----------|------|-----|--------|---------|
| Intercept | 2.92 | 0.29 | 9.97 | <0.001 |
| tv | 0.046 | 0.001 | 32.9 | <0.001 |
| radio | 0.188 | 0.008 | 23.4 | <0.001 |

R² = 0.897, Adjusted R² = 0.892

**Model C: Sales ~ TV + Radio + TV×Radio**

| Variable | Coef | SE | t-stat | p-value |
|----------|------|-----|--------|---------|
| Intercept | 6.75 | 0.25 | 27.2 | <0.001 |
| tv | 0.019 | 0.002 | 12.7 | <0.001 |
| radio | 0.029 | 0.009 | 3.24 | 0.002 |
| tv×radio | 0.0011 | 0.00005 | 20.7 | <0.001 |

R² = 0.968, Adjusted R² = 0.966

### Questions

**Q2.1:** Compare Models A and B. Which is preferable? Justify your choice.
```
Your analysis:




```

**Q2.2:** Interpret the coefficient on TV in Model B. What does spending an extra $1000 on TV advertising do?
```
Your interpretation:



```

**Q2.3:** Model C includes an interaction term. Explain what an interaction means in this context.
```
Your explanation:




```

**Q2.4:** In Model C, interpret the effect of TV advertising. Note: With an interaction, the effect of TV depends on the level of Radio.
```
Your interpretation:




```

**Q2.5:** At radio = $30K, what is the marginal effect of an additional $1K of TV advertising? (Use Model C)
```
Your calculation:


Effect = β_tv + β_interaction × radio
       =

```

**Q2.6:** Based on R² improvement from Model B to C, is the interaction significant? How else could you test this?
```
Your analysis:




```

**Q2.7:** A manager wants to allocate a $100K budget between TV and Radio (no newspaper). Using Model C, how would you approach finding the optimal allocation?
```
Your approach:




```

---

## Case Study 3: Medical Study ⭐⭐⭐

### Background
A study examines factors affecting blood pressure. Data from 150 patients:
- `bp`: Systolic blood pressure (mmHg)
- `age`: Age (years)
- `weight`: Weight (kg)
- `exercise`: Hours of exercise per week
- `smoking`: 1 if smoker, 0 otherwise
- `stress`: Stress level (1-10 scale)

### Regression Output

| Variable | Coef | SE | t-stat | p-value |
|----------|------|-----|--------|---------|
| Intercept | 85.2 | 8.5 | 10.0 | <0.001 |
| age | 0.52 | 0.12 | 4.33 | <0.001 |
| weight | 0.38 | 0.08 | 4.75 | <0.001 |
| exercise | -1.85 | 0.65 | -2.85 | 0.005 |
| smoking | 8.2 | 2.1 | 3.90 | <0.001 |
| stress | 1.45 | 0.55 | 2.64 | 0.009 |

R² = 0.62, Adjusted R² = 0.59

### Diagnostic Information
- Residuals appear approximately normal
- No obvious patterns in residual plots
- Cook's D: One observation (#47) has D = 0.85
- VIFs all < 2

### Questions

**Q3.1:** Interpret the coefficient on `smoking`. Be precise about units and meaning.
```
Your interpretation:




```

**Q3.2:** A patient asks: "If I exercise 2 more hours per week, how much will my blood pressure drop?" What do you tell them, and what caveats do you mention?
```
Your response:




```

**Q3.3:** Can we conclude that smoking CAUSES higher blood pressure based on this analysis? Why or why not?
```
Your analysis:




```

**Q3.4:** Observation #47 has Cook's D = 0.85. Should we be concerned? What would you investigate?
```
Your response:




```

**Q3.5:** Calculate a 95% CI for the effect of a one-unit increase in stress on blood pressure.
```
Your calculation:



```

**Q3.6:** The R² is 0.62. Is this good or bad? Explain your reasoning.
```
Your analysis:




```

**Q3.7:** A colleague suggests adding `BMI` (Body Mass Index = weight/height²) to the model. You already have `weight`. Discuss the implications.
```
Your discussion:




```

---

## Case Study 4: High-Dimensional Data ⭐⭐⭐⭐

### Background
You're predicting customer churn using 50 features (demographics, behavior, etc.) but only have 80 observations.

### Preliminary Analysis
- OLS fails: "singular matrix" error
- When you remove 10 features, OLS gives very large coefficients with huge standard errors
- Correlation matrix shows many features are highly correlated

### Results from Regularized Models

**Ridge Regression (λ chosen by CV):**
- λ_best = 2.5
- Test R² = 0.45
- All 50 coefficients are non-zero

**Lasso Regression (λ chosen by CV):**
- λ_best = 0.8
- Test R² = 0.52
- 12 non-zero coefficients

**Elastic Net (α = 0.5, λ chosen by CV):**
- λ_best = 1.2
- Test R² = 0.51
- 18 non-zero coefficients

### Questions

**Q4.1:** Why did OLS fail with 50 features and 80 observations?
```
Your explanation:



```

**Q4.2:** Explain conceptually why regularization helps in this situation.
```
Your explanation:




```

**Q4.3:** Why does Lasso give a sparse solution (only 12 non-zero) while Ridge keeps all 50?
```
Your explanation:




```

**Q4.4:** Lasso has higher test R² than Ridge here. Is this always expected? When might Ridge outperform Lasso?
```
Your analysis:




```

**Q4.5:** The Elastic Net has 18 non-zero coefficients (between Lasso's 12 and Ridge's 50). What advantage might Elastic Net have over pure Lasso?
```
Your analysis:




```

**Q4.6:** If you had to choose one model for production, which would you choose and why?
```
Your decision:




```

**Q4.7:** What additional data would most help improve the model?
```
Your recommendation:



```

---

## Case Study 5: Model Selection ⭐⭐⭐

### Background
You're predicting employee performance ratings (1-10) using:
- `experience`: Years of experience
- `education`: Years of education
- `training`: Hours of training completed
- `tenure`: Years at company
- `age`: Age in years

n = 200 employees

### Model Comparison

| Model | Variables | R² | Adj R² | AIC | BIC |
|-------|-----------|-----|--------|-----|-----|
| M1 | exp | 0.35 | 0.35 | 450 | 457 |
| M2 | exp + edu | 0.42 | 0.41 | 430 | 440 |
| M3 | exp + edu + train | 0.48 | 0.47 | 410 | 423 |
| M4 | exp + edu + train + tenure | 0.49 | 0.48 | 408 | 425 |
| M5 | exp + edu + train + tenure + age | 0.49 | 0.47 | 410 | 430 |
| M6 | exp + train | 0.44 | 0.43 | 425 | 435 |

### Questions

**Q5.1:** Based on Adjusted R², which model is best? Why do we use Adjusted R² instead of R²?
```
Your analysis:




```

**Q5.2:** Based on AIC, which model is best? What does AIC balance?
```
Your analysis:




```

**Q5.3:** Based on BIC, which model is best? Why does BIC often select simpler models than AIC?
```
Your analysis:




```

**Q5.4:** Model M4 vs M5: Adding `age` increases R² but decreases Adjusted R². Explain.
```
Your explanation:




```

**Q5.5:** Suppose you must choose between M3 and M4. Design an F-test to make this decision. What are H₀ and H₁?
```
Your test design:




```

**Q5.6:** What's your final model recommendation and why?
```
Your recommendation:




```

---

## General Reflection Questions

After completing these case studies, answer:

**R1:** What are the most common mistakes you see in applied regression analysis?
```



```

**R2:** What diagnostics should you ALWAYS check after fitting a regression?
```



```

**R3:** When should you use regularization vs. standard OLS?
```



```

**R4:** How do you balance model interpretability vs. predictive accuracy?
```



```
