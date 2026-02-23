# Pandas Data Mastery

A practical, hands-on refresher for pandas and data manipulation.

## Setup

```bash
pip install pandas numpy
cd datasets && python generate_data.py
```

## Structure

```
pandas-data-mastery/
├── 01_core_operations/     # Selection, filtering, groupby
├── 02_reshaping/           # Pivot, melt, stack/unstack
├── 03_joins_and_merges/    # Multi-table operations
├── 04_advanced_patterns/   # Chaining, apply, windows
├── 05_real_world_challenges/  # End-to-end projects
├── datasets/               # Practice data
└── solutions/              # Check your work
```

## Learning Path

| Section | Topics | Time |
|---------|--------|------|
| 01 | loc/iloc, query, groupby, missing data | 30 min |
| 02 | pivot, melt, stack, crosstab | 30 min |
| 03 | merge, join, concat, anti-joins | 45 min |
| 04 | method chaining, apply, rolling | 30 min |
| 05 | Real projects combining all skills | 45 min |

## Datasets

- `customers.csv` - Customer info (id, name, region, signup_date)
- `orders.csv` - Order records (links to customers & products)
- `products.csv` - Product catalog
- `transactions_messy.csv` - Dirty data for cleaning practice

## How to Use

1. Run `generate_data.py` to create datasets
2. Open each `exercises.py` file
3. Complete the TODO sections
4. Run the file to check your work
5. Peek at solutions only when stuck

## Quick Reference

```python
# Selection
df.loc[rows, cols]          # Label-based
df.iloc[rows, cols]         # Position-based
df.query('col > 5')         # SQL-like filtering

# Aggregation
df.groupby('col').agg({'x': 'sum', 'y': 'mean'})
df.groupby(['a', 'b']).size()

# Reshaping
df.pivot(index, columns, values)
df.melt(id_vars, value_vars)
pd.crosstab(df.a, df.b)

# Joins
pd.merge(left, right, on='key', how='left')
pd.concat([df1, df2], axis=0)

# Chaining
df.assign(new_col=...).query(...).groupby(...).agg(...)
```
