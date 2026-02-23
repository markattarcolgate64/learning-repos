"""
04 - Advanced Patterns
======================

Topics covered:
- Method chaining with assign() and pipe()
- apply() vs vectorized operations
- Window functions (rolling, expanding, shift)
- String and datetime accessors

Run: python exercises.py
"""

import pandas as pd
import numpy as np

# Load data
orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
products = pd.read_csv('../datasets/products.csv')


# =============================================================================
# PART 1: Method Chaining
# =============================================================================
# Chain operations together for readable, maintainable code
# Key methods: .assign(), .pipe(), .query()

print("=" * 60)
print("PART 1: Method Chaining")
print("=" * 60)

# Without chaining (harder to read)
temp = orders.copy()
temp = temp[temp['status'] == 'completed']
temp = temp.groupby('customer_id')['quantity'].sum()
temp = temp.reset_index()
temp = temp.rename(columns={'quantity': 'total_qty'})
print(f"\nWithout chaining:\n{temp.head()}")

# EXERCISE 1.1: Rewrite with chaining
# TODO: Rewrite the above using method chaining
chained_result = None  # Your code here
# Hint: orders.query(...).groupby(...)[...].sum().reset_index().rename(...)

# EXERCISE 1.2: Use assign() to add columns
# TODO: Add columns in a chain:
# - 'year' from order_date
# - 'month' from order_date
# - 'is_large' True if quantity >= 3
orders_enhanced = None  # Your code here
# Hint: .assign(year=lambda df: df['order_date'].dt.year, ...)

# EXERCISE 1.3: Use pipe() for custom functions
def add_running_total(df, col, new_col):
    """Add cumulative sum column."""
    df = df.copy()
    df[new_col] = df[col].cumsum()
    return df

# TODO: Sort orders by date, then pipe through add_running_total
# to add 'running_qty' column
with_running = None  # Your code here
# Hint: orders.sort_values(...).pipe(add_running_total, 'quantity', 'running_qty')

print("\n--- Exercise Results ---")
print(f"1.1 Chained:\n{chained_result.head() if chained_result is not None else 'Not done'}")
print(f"1.2 Enhanced columns: {orders_enhanced.columns.tolist() if orders_enhanced is not None else 'Not done'}")


# =============================================================================
# PART 2: apply() vs Vectorized Operations
# =============================================================================
# Vectorized operations are MUCH faster than apply()
# Use apply() only when you can't vectorize

print("\n" + "=" * 60)
print("PART 2: apply() vs Vectorized Operations")
print("=" * 60)

# EXERCISE 2.1: Vectorized is better
# BAD (slow):
# products['margin'] = products.apply(lambda row: row['price'] - row['cost'], axis=1)
# GOOD (fast):
# products['margin'] = products['price'] - products['cost']

# TODO: Calculate profit margin percentage: (price - cost) / price * 100
# Use vectorized operations
products_copy = products.copy()
products_copy['margin_pct'] = None  # Your code here (vectorized)

# EXERCISE 2.2: When apply() IS needed
# TODO: Create a function that categorizes prices and apply it
def categorize_price(price):
    if price < 50:
        return 'budget'
    elif price < 200:
        return 'mid-range'
    else:
        return 'premium'

products_copy['price_tier'] = None  # Your code here (use apply)

# EXERCISE 2.3: Better alternative with np.select or pd.cut
# TODO: Rewrite 2.2 using pd.cut() or np.select()
# This is vectorized and much faster
conditions = [
    products_copy['price'] < 50,
    products_copy['price'] < 200,
    products_copy['price'] >= 200
]
choices = ['budget', 'mid-range', 'premium']
products_copy['price_tier_fast'] = None  # Your code here (hint: np.select(conditions, choices))

# EXERCISE 2.4: apply() on groups
# TODO: For each category, calculate price as percentage of category max
# Hint: groupby + apply with a lambda that divides by max
products_copy['pct_of_cat_max'] = None  # Your code here

print("\n--- Exercise Results ---")
print(f"2.1 Margin pct sample:\n{products_copy[['product_name', 'price', 'cost', 'margin_pct']].head() if products_copy['margin_pct'] is not None else 'Not done'}")
print(f"2.2 Price tiers:\n{products_copy['price_tier'].value_counts() if products_copy['price_tier'] is not None else 'Not done'}")


# =============================================================================
# PART 3: Window Functions
# =============================================================================
# rolling(): Fixed window size
# expanding(): Growing window from start
# shift(): Offset data by periods

print("\n" + "=" * 60)
print("PART 3: Window Functions")
print("=" * 60)

# Create time series data for exercises
daily_sales = orders.groupby('order_date')['quantity'].sum().reset_index()
daily_sales = daily_sales.sort_values('order_date').reset_index(drop=True)
daily_sales.columns = ['date', 'sales']
print(f"\nDaily sales (first 10):\n{daily_sales.head(10)}")

# EXERCISE 3.1: Rolling average
# TODO: Calculate 7-day rolling average of sales
daily_sales['rolling_7d'] = None  # Your code here

# EXERCISE 3.2: Rolling with min_periods
# TODO: Calculate 7-day rolling average, but allow partial windows
# (show result even if fewer than 7 days available)
daily_sales['rolling_7d_partial'] = None  # Your code here (hint: min_periods=1)

# EXERCISE 3.3: Expanding (cumulative) functions
# TODO: Calculate cumulative sum and cumulative mean
daily_sales['cumsum'] = None  # Your code here
daily_sales['cummean'] = None  # Your code here (expanding().mean())

# EXERCISE 3.4: shift() for lagged values
# TODO: Create column with previous day's sales
daily_sales['prev_day'] = None  # Your code here

# TODO: Create column with sales change from previous day
daily_sales['daily_change'] = None  # Your code here (sales - prev_day)

# EXERCISE 3.5: Rolling within groups
# TODO: For each customer, calculate rolling 3-order average quantity
orders_sorted = orders.sort_values(['customer_id', 'order_date'])
orders_sorted['rolling_3_qty'] = None  # Your code here
# Hint: groupby('customer_id')['quantity'].rolling(3).mean().reset_index(...)

print("\n--- Exercise Results ---")
print(f"3.1-3.4 Daily sales with windows:\n{daily_sales.head(10) if daily_sales['rolling_7d'] is not None else 'Not done'}")


# =============================================================================
# PART 4: String Accessors (.str)
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: String Accessors")
print("=" * 60)

# Create sample data with strings
string_data = pd.DataFrame({
    'name': ['  John Smith  ', 'jane doe', 'BOB JONES', 'Alice Brown'],
    'email': ['john@example.com', 'jane@test.org', 'bob@example.com', 'alice@test.org'],
    'phone': ['123-456-7890', '(234) 567-8901', '345.678.9012', '456 789 0123']
})
print(f"\nString data:\n{string_data}")

# EXERCISE 4.1: Basic string operations
# TODO: Clean the name column: strip whitespace, title case
string_data['name_clean'] = None  # Your code here (.str.strip().str.title())

# EXERCISE 4.2: Extract with regex
# TODO: Extract the domain from email (part after @)
string_data['domain'] = None  # Your code here (.str.extract() or .str.split('@').str[1])

# EXERCISE 4.3: Contains and filtering
# TODO: Create boolean mask for emails from 'example.com'
is_example = None  # Your code here (.str.contains())

# EXERCISE 4.4: Replace with regex
# TODO: Standardize phone numbers to format: XXXXXXXXXX (just digits)
string_data['phone_clean'] = None  # Your code here (.str.replace() with regex)

# EXERCISE 4.5: Split and expand
# TODO: Split name into first_name and last_name columns
name_split = None  # Your code here (.str.split(expand=True))

print("\n--- Exercise Results ---")
print(f"4.1 Clean names: {string_data['name_clean'].tolist() if string_data['name_clean'] is not None else 'Not done'}")
print(f"4.2 Domains: {string_data['domain'].tolist() if string_data['domain'] is not None else 'Not done'}")
print(f"4.4 Clean phones: {string_data['phone_clean'].tolist() if string_data['phone_clean'] is not None else 'Not done'}")


# =============================================================================
# PART 5: Datetime Accessors (.dt)
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: Datetime Accessors")
print("=" * 60)

# EXERCISE 5.1: Extract date components
# TODO: Add columns: year, month, day, day_of_week, quarter
orders_dt = orders.copy()
orders_dt['year'] = None  # Your code here
orders_dt['month'] = None  # Your code here
orders_dt['day_of_week'] = None  # Your code here (.dt.dayofweek, 0=Monday)
orders_dt['quarter'] = None  # Your code here

# EXERCISE 5.2: Date formatting
# TODO: Create formatted date string 'YYYY-MM'
orders_dt['year_month'] = None  # Your code here (.dt.strftime('%Y-%m'))

# EXERCISE 5.3: Date arithmetic
# TODO: Calculate days since order (from today)
from datetime import datetime
today = datetime.now()
orders_dt['days_ago'] = None  # Your code here ((today - orders_dt['order_date']).dt.days)

# EXERCISE 5.4: Filter by date components
# TODO: Get orders from Q4 (October-December) of any year
q4_orders = None  # Your code here (filter where month >= 10)

# EXERCISE 5.5: Resample time series
# TODO: Resample daily_sales to monthly totals
# Hint: Need to set date as index first, then .resample('M').sum()
daily_sales_indexed = daily_sales.set_index('date')
monthly_sales = None  # Your code here

print("\n--- Exercise Results ---")
print(f"5.1 Date components:\n{orders_dt[['order_date', 'year', 'month', 'day_of_week', 'quarter']].head() if orders_dt['year'] is not None else 'Not done'}")
print(f"5.4 Q4 orders count: {len(q4_orders) if q4_orders is not None else 'Not done'}")


# =============================================================================
# CHALLENGE EXERCISES
# =============================================================================

print("\n" + "=" * 60)
print("CHALLENGE EXERCISES")
print("=" * 60)

# CHALLENGE 1: Complete analysis chain
# TODO: In one chain, do:
# 1. Join orders with products
# 2. Add 'total_value' = price * quantity
# 3. Filter to completed orders
# 4. Group by category
# 5. Calculate sum of total_value
# 6. Sort descending
# 7. Reset index
category_sales = None  # Your code here (one chain!)

# CHALLENGE 2: Customer cohort analysis
# TODO: For each customer:
# - Calculate days between signup and first order
# - Handle customers with no orders (NaN)
# Hint: Get first order date per customer, merge with customers, calculate diff
days_to_first_order = None  # Your code here

# CHALLENGE 3: Rolling rank within group
# TODO: For each product category, rank products by price
# Then calculate a 3-product rolling average of the rank
products_ranked = products.copy()
# Step 1: Rank by price within category
products_ranked['price_rank'] = None  # groupby + rank
# Step 2: Rolling average of rank (within category)
products_ranked['rolling_rank'] = None  # groupby + rolling

print("\n--- Challenge Results ---")
print(f"C1: Category sales:\n{category_sales if category_sales is not None else 'Not done'}")
print(f"\nC2: Days to first order:\n{days_to_first_order.head() if days_to_first_order is not None else 'Not done'}")


print("\n" + "=" * 60)
print("COMPLETE! Check your answers against the solutions.")
print("=" * 60)
