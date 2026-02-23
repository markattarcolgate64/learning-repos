"""
01 - Core Pandas Operations
===========================

Topics covered:
- Boolean masks and filtering
- loc vs iloc
- query() method
- GroupBy aggregations
- Sorting and ranking
- Handling missing data

Run: python exercises.py
"""

import pandas as pd
import numpy as np

# Load data
customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
products = pd.read_csv('../datasets/products.csv')


# =============================================================================
# PART 1: Boolean Masks
# =============================================================================
# A boolean mask is a Series of True/False values used to filter a DataFrame.
# When you do df[mask], you get back only rows where mask is True.

print("=" * 60)
print("PART 1: Boolean Masks")
print("=" * 60)

# Example: Create a boolean mask
mask_example = customers['region'] == 'North'
print(f"\nBoolean mask (first 5): \n{mask_example.head()}")
print(f"Type: {type(mask_example)}")

# EXERCISE 1.1: Create a boolean mask for premium customers
# TODO: Create a mask that is True for premium customers
mask_premium = None  # Your code here

# EXERCISE 1.2: Use the mask to filter
# TODO: Use mask_premium to get only premium customers
premium_customers = None  # Your code here

# EXERCISE 1.3: Combine masks with & (and) and | (or)
# TODO: Get customers who are premium AND from the 'West' region
# Remember: Use parentheses! (mask1) & (mask2)
premium_west = None  # Your code here

# EXERCISE 1.4: Negate a mask with ~
# TODO: Get all NON-premium customers
non_premium = None  # Your code here

# EXERCISE 1.5: Use .isin() for multiple values
# TODO: Get customers from 'North' OR 'South' regions using isin()
north_south = None  # Your code here

print("\n--- Exercise Results ---")
print(f"1.1 Premium mask created: {mask_premium is not None}")
print(f"1.2 Premium customers count: {len(premium_customers) if premium_customers is not None else 'Not done'}")
print(f"1.3 Premium West count: {len(premium_west) if premium_west is not None else 'Not done'}")
print(f"1.4 Non-premium count: {len(non_premium) if non_premium is not None else 'Not done'}")
print(f"1.5 North/South count: {len(north_south) if north_south is not None else 'Not done'}")


# =============================================================================
# PART 2: loc vs iloc
# =============================================================================
# loc: Label-based indexing (use column names, row labels)
# iloc: Integer position-based indexing (use numbers like arrays)

print("\n" + "=" * 60)
print("PART 2: loc vs iloc")
print("=" * 60)

# EXERCISE 2.1: Select specific columns with loc
# TODO: Select 'name' and 'region' columns for all rows
name_region = None  # Your code here

# EXERCISE 2.2: Select rows and columns with loc
# TODO: Select first 10 rows, only 'name' and 'email' columns
first_10_name_email = None  # Your code here (use loc with slice)

# EXERCISE 2.3: Use iloc for position-based selection
# TODO: Select rows 5-10 (inclusive), columns 0-2 (exclusive)
slice_iloc = None  # Your code here

# EXERCISE 2.4: Combine boolean mask with loc
# TODO: Get 'name' and 'region' for premium customers only
premium_name_region = None  # Your code here (use loc with mask)

print("\n--- Exercise Results ---")
print(f"2.1 Shape: {name_region.shape if name_region is not None else 'Not done'}")
print(f"2.2 Shape: {first_10_name_email.shape if first_10_name_email is not None else 'Not done'}")
print(f"2.3 Shape: {slice_iloc.shape if slice_iloc is not None else 'Not done'}")
print(f"2.4 Shape: {premium_name_region.shape if premium_name_region is not None else 'Not done'}")


# =============================================================================
# PART 3: query() Method
# =============================================================================
# query() lets you filter using a string expression (like SQL WHERE)

print("\n" + "=" * 60)
print("PART 3: query() Method")
print("=" * 60)

# Example
example_query = customers.query('region == "North"')
print(f"\nquery('region == \"North\"') returns {len(example_query)} rows")

# EXERCISE 3.1: Simple query
# TODO: Get orders with quantity > 3
high_quantity = None  # Your code here

# EXERCISE 3.2: Query with multiple conditions
# TODO: Get completed orders with quantity >= 2
completed_multi = None  # Your code here

# EXERCISE 3.3: Query with variable
min_qty = 3
# TODO: Get orders where quantity > min_qty (use @ to reference variables)
above_min = None  # Your code here (hint: query('quantity > @min_qty'))

# EXERCISE 3.4: Query with string methods
# TODO: Get products where category is 'Electronics'
electronics = None  # Your code here

print("\n--- Exercise Results ---")
print(f"3.1 High quantity orders: {len(high_quantity) if high_quantity is not None else 'Not done'}")
print(f"3.2 Completed multi-item: {len(completed_multi) if completed_multi is not None else 'Not done'}")
print(f"3.3 Above min_qty: {len(above_min) if above_min is not None else 'Not done'}")
print(f"3.4 Electronics: {len(electronics) if electronics is not None else 'Not done'}")


# =============================================================================
# PART 4: GroupBy Aggregations
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: GroupBy Aggregations")
print("=" * 60)

# EXERCISE 4.1: Basic groupby with single aggregation
# TODO: Count orders per customer_id
orders_per_customer = None  # Your code here (groupby + size or count)

# EXERCISE 4.2: GroupBy with specific column aggregation
# TODO: Get total quantity ordered per customer
qty_per_customer = None  # Your code here

# EXERCISE 4.3: Multiple aggregations with agg()
# TODO: For each customer, get: count of orders, sum of quantity, mean quantity
customer_stats = None  # Your code here
# Hint: .agg({'quantity': ['count', 'sum', 'mean']})

# EXERCISE 4.4: GroupBy multiple columns
# TODO: Count orders by customer_id AND status
orders_by_customer_status = None  # Your code here

# EXERCISE 4.5: Named aggregations (modern pandas style)
# TODO: Get order stats with named columns
# Hint: .agg(total_orders=('order_id', 'count'), total_qty=('quantity', 'sum'))
named_stats = None  # Your code here

print("\n--- Exercise Results ---")
print(f"4.1 Orders per customer (first 3):\n{orders_per_customer.head(3) if orders_per_customer is not None else 'Not done'}")
print(f"4.2 Qty per customer (first 3):\n{qty_per_customer.head(3) if qty_per_customer is not None else 'Not done'}")
print(f"4.3 Customer stats shape: {customer_stats.shape if customer_stats is not None else 'Not done'}")
print(f"4.4 By customer+status:\n{orders_by_customer_status.head() if orders_by_customer_status is not None else 'Not done'}")


# =============================================================================
# PART 5: Sorting and Ranking
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: Sorting and Ranking")
print("=" * 60)

# EXERCISE 5.1: Sort by single column
# TODO: Sort products by price descending
products_by_price = None  # Your code here

# EXERCISE 5.2: Sort by multiple columns
# TODO: Sort orders by customer_id (asc), then order_date (desc)
orders_sorted = None  # Your code here

# EXERCISE 5.3: Get top N with nlargest
# TODO: Get top 5 most expensive products
top_5_expensive = None  # Your code here

# EXERCISE 5.4: Rank within groups
# TODO: Rank orders by quantity within each customer (dense rank)
# Hint: groupby + rank(method='dense')
orders_with_rank = orders.copy()
orders_with_rank['qty_rank'] = None  # Your code here

# EXERCISE 5.5: Value counts
# TODO: Count orders by status
status_counts = None  # Your code here

print("\n--- Exercise Results ---")
print(f"5.1 Most expensive product: {products_by_price['product_name'].iloc[0] if products_by_price is not None else 'Not done'}")
print(f"5.3 Top 5 expensive:\n{top_5_expensive[['product_name', 'price']].head() if top_5_expensive is not None else 'Not done'}")
print(f"5.5 Status counts:\n{status_counts if status_counts is not None else 'Not done'}")


# =============================================================================
# PART 6: Missing Data
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: Missing Data")
print("=" * 60)

# Create sample data with missing values
df_missing = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 2, 3, np.nan, 5],
    'C': ['x', 'y', np.nan, 'z', 'w']
})
print(f"\nSample data with nulls:\n{df_missing}")

# EXERCISE 6.1: Check for missing values
# TODO: Count missing values per column
missing_counts = None  # Your code here (hint: isna().sum())

# EXERCISE 6.2: Drop rows with any missing values
# TODO: Drop rows that have any NaN
df_dropna = None  # Your code here

# EXERCISE 6.3: Fill missing values
# TODO: Fill NaN in column 'A' with the mean of 'A'
df_filled = df_missing.copy()
df_filled['A'] = None  # Your code here

# EXERCISE 6.4: Fill with different values per column
# TODO: Fill A with 0, B with the median, C with 'unknown'
df_filled_multi = df_missing.copy()
# Your code here (hint: fillna({'A': 0, 'B': ..., 'C': ...}))

# EXERCISE 6.5: Forward fill / Back fill
# TODO: Forward fill column B (fill NaN with previous value)
df_ffill = df_missing.copy()
df_ffill['B'] = None  # Your code here

print("\n--- Exercise Results ---")
print(f"6.1 Missing counts:\n{missing_counts if missing_counts is not None else 'Not done'}")
print(f"6.2 After dropna: {len(df_dropna) if df_dropna is not None else 'Not done'} rows")
print(f"6.3 A filled:\n{df_filled['A'] if df_filled['A'] is not None else 'Not done'}")


# =============================================================================
# CHALLENGE EXERCISES
# =============================================================================

print("\n" + "=" * 60)
print("CHALLENGE EXERCISES")
print("=" * 60)

# CHALLENGE 1: Complex filter
# TODO: Get customers who signed up in 2023 AND are from 'East' or 'West' regions
# Hint: Use .dt.year to extract year from signup_date
customers_2023_ew = None  # Your code here

# CHALLENGE 2: Aggregation + filter
# TODO: Find customers who have placed more than 5 orders
# Return their customer_ids as a list
high_volume_customers = None  # Your code here

# CHALLENGE 3: Combine multiple operations
# TODO: Get the top 3 customers by total quantity ordered
# Return: customer_id, total_quantity (sorted descending)
top_3_by_qty = None  # Your code here

print("\n--- Challenge Results ---")
print(f"C1: 2023 East/West customers: {len(customers_2023_ew) if customers_2023_ew is not None else 'Not done'}")
print(f"C2: High volume customers: {high_volume_customers if high_volume_customers is not None else 'Not done'}")
print(f"C3: Top 3 by qty:\n{top_3_by_qty if top_3_by_qty is not None else 'Not done'}")


print("\n" + "=" * 60)
print("COMPLETE! Check your answers against the solutions.")
print("=" * 60)
