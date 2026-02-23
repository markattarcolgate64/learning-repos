"""
02 - Reshaping Data
===================

Topics covered:
- pivot() vs pivot_table()
- melt() - wide to long
- stack() and unstack()
- crosstab()

Run: python exercises.py
"""

import pandas as pd
import numpy as np

# Load data
sales = pd.read_csv('../datasets/sales_by_region.csv')
orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('../datasets/customers.csv')

print("Sales data shape:", sales.shape)
print(sales.head(10))


# =============================================================================
# PART 1: Pivot Tables
# =============================================================================
# pivot_table() aggregates data and reshapes it
# Think: "I want rows to be X, columns to be Y, values to be Z"

print("\n" + "=" * 60)
print("PART 1: Pivot Tables")
print("=" * 60)

# Example: Region as rows, Product as columns, Sales as values
example_pivot = sales.pivot_table(
    index='region',
    columns='product',
    values='sales',
    aggfunc='sum'
)
print(f"\nExample pivot (region x product):\n{example_pivot}")

# EXERCISE 1.1: Basic pivot
# TODO: Create a pivot table with month as rows, region as columns, sales as values
# Use sum as aggregation
monthly_by_region = None  # Your code here

# EXERCISE 1.2: Pivot with multiple values
# TODO: Create pivot with region as rows, product as columns
# Show BOTH sales and units (hint: values=['sales', 'units'])
sales_and_units = None  # Your code here

# EXERCISE 1.3: Pivot with multiple aggregations
# TODO: Pivot with region as rows, product as columns, sales as values
# Show both sum AND mean (hint: aggfunc=['sum', 'mean'])
multi_agg = None  # Your code here

# EXERCISE 1.4: Pivot with margins (totals)
# TODO: Same as 1.1, but add row/column totals (margins=True)
with_totals = None  # Your code here

print("\n--- Exercise Results ---")
print(f"1.1 Monthly by region:\n{monthly_by_region if monthly_by_region is not None else 'Not done'}")
print(f"1.2 Shape: {sales_and_units.shape if sales_and_units is not None else 'Not done'}")


# =============================================================================
# PART 2: pivot() vs pivot_table()
# =============================================================================
# pivot() - simple reshape, no aggregation (fails if duplicates)
# pivot_table() - reshapes WITH aggregation (handles duplicates)

print("\n" + "=" * 60)
print("PART 2: pivot() vs pivot_table()")
print("=" * 60)

# Create simple data for pivot()
simple_data = pd.DataFrame({
    'date': ['Mon', 'Mon', 'Tue', 'Tue'],
    'city': ['NYC', 'LA', 'NYC', 'LA'],
    'temp': [70, 85, 72, 88]
})
print(f"\nSimple data:\n{simple_data}")

# EXERCISE 2.1: Use pivot() for simple reshape
# TODO: Reshape so dates are rows, cities are columns, temp is values
pivoted_simple = None  # Your code here (use .pivot())

# EXERCISE 2.2: When pivot() fails
# Try this (it will fail due to duplicates):
duplicate_data = pd.DataFrame({
    'date': ['Mon', 'Mon', 'Mon'],  # Two Mon+NYC entries!
    'city': ['NYC', 'NYC', 'LA'],
    'temp': [70, 72, 85]
})
# Uncomment to see the error:
# duplicate_data.pivot(index='date', columns='city', values='temp')

# TODO: Use pivot_table() instead to handle duplicates (takes mean by default)
pivoted_with_agg = None  # Your code here

print("\n--- Exercise Results ---")
print(f"2.1 Pivoted simple:\n{pivoted_simple if pivoted_simple is not None else 'Not done'}")
print(f"2.2 With aggregation:\n{pivoted_with_agg if pivoted_with_agg is not None else 'Not done'}")


# =============================================================================
# PART 3: melt() - Wide to Long
# =============================================================================
# melt() is the opposite of pivot - converts wide format to long format
# Use when you have data spread across columns that should be in rows

print("\n" + "=" * 60)
print("PART 3: melt() - Wide to Long")
print("=" * 60)

# Create wide data
wide_data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'math': [90, 85, 78],
    'science': [88, 92, 85],
    'english': [95, 78, 90]
})
print(f"\nWide data:\n{wide_data}")

# EXERCISE 3.1: Basic melt
# TODO: Convert wide_data to long format
# Keep 'name' as identifier, melt the subject columns
# Result should have columns: name, variable (subject), value (score)
long_data = None  # Your code here

# EXERCISE 3.2: Melt with custom column names
# TODO: Same as above, but name columns 'subject' and 'score'
# Hint: var_name='subject', value_name='score'
long_named = None  # Your code here

# EXERCISE 3.3: Melt specific columns only
# TODO: Melt only math and science (not english)
# Hint: value_vars=['math', 'science']
partial_melt = None  # Your code here

print("\n--- Exercise Results ---")
print(f"3.1 Long data:\n{long_data if long_data is not None else 'Not done'}")
print(f"3.2 Named columns:\n{long_named.head() if long_named is not None else 'Not done'}")


# =============================================================================
# PART 4: stack() and unstack()
# =============================================================================
# stack(): Columns -> Rows (creates MultiIndex)
# unstack(): Rows -> Columns (undoes stack)
# Useful for multi-index manipulation

print("\n" + "=" * 60)
print("PART 4: stack() and unstack()")
print("=" * 60)

# Create a pivot table to work with
pivot_example = sales.pivot_table(
    index='region',
    columns='product',
    values='sales',
    aggfunc='sum'
)
print(f"\nPivot table:\n{pivot_example}")

# EXERCISE 4.1: Stack - columns to rows
# TODO: Stack the pivot_example (columns become part of index)
stacked = None  # Your code here
# Result should be a Series with MultiIndex (region, product)

# EXERCISE 4.2: Unstack - rows to columns
# TODO: Unstack the stacked data back to original form
unstacked = None  # Your code here

# EXERCISE 4.3: Unstack specific level
# Create MultiIndex DataFrame
multi_idx = sales.groupby(['region', 'product', 'month'])['sales'].sum()
print(f"\nMulti-index series:\n{multi_idx.head(10)}")

# TODO: Unstack the 'month' level to columns
month_cols = None  # Your code here (hint: unstack('month') or unstack(level=-1))

print("\n--- Exercise Results ---")
print(f"4.1 Stacked (first 5):\n{stacked.head() if stacked is not None else 'Not done'}")
print(f"4.3 Month as columns:\n{month_cols.head() if month_cols is not None else 'Not done'}")


# =============================================================================
# PART 5: crosstab()
# =============================================================================
# crosstab() is a shortcut for frequency tables (like pivot_table for counts)

print("\n" + "=" * 60)
print("PART 5: crosstab()")
print("=" * 60)

# EXERCISE 5.1: Basic crosstab (frequency table)
# TODO: Create a crosstab of customer region vs is_premium
region_premium = None  # Your code here

# EXERCISE 5.2: Crosstab with normalize
# TODO: Same as above, but show percentages (normalize='all')
region_premium_pct = None  # Your code here

# EXERCISE 5.3: Crosstab with margins
# TODO: Add row/column totals
with_margins = None  # Your code here

# EXERCISE 5.4: Crosstab with custom aggregation
# TODO: Crosstab of order status vs customer region, but show COUNTS
# Use orders merged with customers first
orders_with_region = orders.merge(
    customers[['customer_id', 'region']],
    on='customer_id'
)
status_by_region = None  # Your code here

print("\n--- Exercise Results ---")
print(f"5.1 Region x Premium:\n{region_premium if region_premium is not None else 'Not done'}")
print(f"5.2 Percentages:\n{region_premium_pct if region_premium_pct is not None else 'Not done'}")


# =============================================================================
# CHALLENGE EXERCISES
# =============================================================================

print("\n" + "=" * 60)
print("CHALLENGE EXERCISES")
print("=" * 60)

# CHALLENGE 1: Create a report
# TODO: Create a pivot table showing:
# - Rows: region
# - Columns: month
# - Values: total sales
# - Add totals for rows and columns
# - Sort by total sales (descending)
sales_report = None  # Your code here

# CHALLENGE 2: Reshape and aggregate
# TODO: Starting from the sales dataframe:
# 1. Pivot to get region as rows, product as columns, sales as values
# 2. Add a 'total' column that sums across products
# 3. Sort by total descending
region_totals = None  # Your code here

# CHALLENGE 3: Long to wide and back
# TODO: Take long_data from exercise 3.1
# Convert it BACK to wide format using pivot
# Should get back the original wide_data structure
back_to_wide = None  # Your code here (if long_data exists)

print("\n--- Challenge Results ---")
print(f"C1: Sales report:\n{sales_report if sales_report is not None else 'Not done'}")
print(f"C2: Region totals:\n{region_totals if region_totals is not None else 'Not done'}")


print("\n" + "=" * 60)
print("COMPLETE! Check your answers against the solutions.")
print("=" * 60)
