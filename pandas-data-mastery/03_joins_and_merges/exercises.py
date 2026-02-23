"""
03 - Joins and Merges (Focus Area)
==================================

Topics covered:
- merge() with different join types
- Joining on multiple keys
- Handling duplicate keys
- concat() vs merge()
- Anti-joins and semi-joins
- Common pitfalls

Run: python exercises.py
"""

import pandas as pd
import numpy as np

# Load data
customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
products = pd.read_csv('../datasets/products.csv')
employees = pd.read_csv('../datasets/employees.csv', parse_dates=['hire_date'])
departments = pd.read_csv('../datasets/departments.csv')

print("=== Data Preview ===")
print(f"Customers: {len(customers)} rows")
print(f"Orders: {len(orders)} rows")
print(f"Products: {len(products)} rows")
print(f"Employees: {len(employees)} rows")
print(f"Departments: {len(departments)} rows")


# =============================================================================
# PART 1: Basic Joins
# =============================================================================
# merge() is the primary function for combining DataFrames
# how='inner' (default), 'left', 'right', 'outer'

print("\n" + "=" * 60)
print("PART 1: Basic Joins")
print("=" * 60)

# EXERCISE 1.1: Inner Join (default)
# TODO: Join orders with customers on customer_id
# Only keeps rows where customer_id exists in BOTH tables
orders_with_customers = None  # Your code here

# EXERCISE 1.2: Left Join
# TODO: Left join orders with products on product_id
# Keeps ALL orders, adds product info where available
orders_with_products = None  # Your code here

# EXERCISE 1.3: Right Join
# TODO: Right join employees with departments on dept_id
# Keeps ALL departments, adds employee info where available
dept_with_employees = None  # Your code here

# EXERCISE 1.4: Outer Join (Full Join)
# TODO: Outer join employees with departments
# Keeps ALL rows from BOTH tables
full_join = None  # Your code here

print("\n--- Exercise Results ---")
print(f"1.1 Inner join shape: {orders_with_customers.shape if orders_with_customers is not None else 'Not done'}")
print(f"1.2 Left join shape: {orders_with_products.shape if orders_with_products is not None else 'Not done'}")
print(f"1.3 Right join shape: {dept_with_employees.shape if dept_with_employees is not None else 'Not done'}")
print(f"1.4 Outer join shape: {full_join.shape if full_join is not None else 'Not done'}")


# =============================================================================
# PART 2: Join Key Variations
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: Join Key Variations")
print("=" * 60)

# EXERCISE 2.1: Different column names
# Create sample data with different key names
df_left = pd.DataFrame({'id': [1, 2, 3], 'value_a': ['a', 'b', 'c']})
df_right = pd.DataFrame({'key': [1, 2, 4], 'value_b': ['x', 'y', 'z']})

# TODO: Join df_left and df_right where left 'id' matches right 'key'
# Hint: left_on='id', right_on='key'
different_names = None  # Your code here

# EXERCISE 2.2: Join on multiple keys
# Create data with composite key
sales_left = pd.DataFrame({
    'region': ['N', 'N', 'S', 'S'],
    'product': ['A', 'B', 'A', 'B'],
    'sales': [100, 200, 150, 250]
})
sales_right = pd.DataFrame({
    'region': ['N', 'S', 'N'],
    'product': ['A', 'A', 'C'],
    'target': [120, 140, 180]
})

# TODO: Join on BOTH region AND product
multi_key = None  # Your code here (hint: on=['region', 'product'])

# EXERCISE 2.3: Join on index
# TODO: Set customer_id as index on customers, then join with orders
# Hint: customers.set_index('customer_id') then use left_index=True or right_index=True
customers_indexed = customers.set_index('customer_id')
index_join = None  # Your code here

print("\n--- Exercise Results ---")
print(f"2.1 Different names:\n{different_names if different_names is not None else 'Not done'}")
print(f"2.2 Multi-key join:\n{multi_key if multi_key is not None else 'Not done'}")


# =============================================================================
# PART 3: Handling Duplicates
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: Handling Duplicates")
print("=" * 60)

# When joining, if there are duplicate keys, you get a Cartesian product
df_a = pd.DataFrame({'key': [1, 1, 2], 'val_a': ['a1', 'a2', 'a3']})
df_b = pd.DataFrame({'key': [1, 1, 2], 'val_b': ['b1', 'b2', 'b3']})

# EXERCISE 3.1: See the Cartesian product
# TODO: Join df_a and df_b on 'key' - observe how many rows result
cartesian = None  # Your code here
# Note: key=1 has 2 rows in each → 2*2 = 4 rows for key=1 in result

# EXERCISE 3.2: Validate no duplicates
# TODO: Use validate='one_to_many' to check for many-to-many joins
# This will raise an error if both sides have duplicates
# Uncomment to test:
# pd.merge(df_a, df_b, on='key', validate='one_to_one')  # Will error!

# EXERCISE 3.3: Check for many-to-many with indicator
# TODO: Join with indicator=True to see which rows matched
with_indicator = None  # Your code here (hint: indicator=True adds _merge column)

print("\n--- Exercise Results ---")
print(f"3.1 Cartesian result ({len(cartesian) if cartesian is not None else '?'} rows):\n{cartesian if cartesian is not None else 'Not done'}")
print(f"3.3 With indicator:\n{with_indicator if with_indicator is not None else 'Not done'}")


# =============================================================================
# PART 4: concat() vs merge()
# =============================================================================
# concat(): Stack DataFrames vertically (axis=0) or horizontally (axis=1)
# merge(): Join DataFrames based on keys

print("\n" + "=" * 60)
print("PART 4: concat() vs merge()")
print("=" * 60)

df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
df3 = pd.DataFrame({'C': [9, 10], 'D': [11, 12]})

# EXERCISE 4.1: Vertical concat (stack rows)
# TODO: Stack df1 and df2 vertically
vertical = None  # Your code here

# EXERCISE 4.2: Reset index after concat
# TODO: Same as above, but reset index to 0, 1, 2, 3
vertical_reset = None  # Your code here (hint: ignore_index=True)

# EXERCISE 4.3: Horizontal concat (add columns)
# TODO: Concatenate df1 and df3 side by side (axis=1)
horizontal = None  # Your code here

# EXERCISE 4.4: Concat with keys (MultiIndex)
# TODO: Concat df1 and df2 with keys ['first', 'second']
with_keys = None  # Your code here

print("\n--- Exercise Results ---")
print(f"4.1 Vertical:\n{vertical if vertical is not None else 'Not done'}")
print(f"4.3 Horizontal:\n{horizontal if horizontal is not None else 'Not done'}")


# =============================================================================
# PART 5: Anti-Joins and Semi-Joins
# =============================================================================
# These are filtering patterns, not true joins
# Anti-join: Rows in A that are NOT in B
# Semi-join: Rows in A that ARE in B (but don't add B's columns)

print("\n" + "=" * 60)
print("PART 5: Anti-Joins and Semi-Joins")
print("=" * 60)

# Sample data
customers_sample = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
})
orders_sample = pd.DataFrame({
    'order_id': [101, 102, 103],
    'customer_id': [1, 2, 1]  # Only customers 1 and 2 have orders
})

# EXERCISE 5.1: Anti-join - Customers WITHOUT orders
# TODO: Find customers who have NOT placed any orders
# Method: Left join with indicator, then filter for left_only
no_orders = None  # Your code here

# EXERCISE 5.2: Semi-join - Customers WITH orders
# TODO: Find customers who HAVE placed orders (but don't duplicate)
# Method: Filter customers where customer_id is in orders
has_orders = None  # Your code here

# EXERCISE 5.3: Anti-join alternative using isin()
# TODO: Same as 5.1, but use ~isin() method
no_orders_alt = None  # Your code here

# EXERCISE 5.4: Find orders for non-existent customers (data quality check)
# Using employees and departments:
# TODO: Find employees whose dept_id doesn't exist in departments
orphan_employees = None  # Your code here

print("\n--- Exercise Results ---")
print(f"5.1 Customers without orders:\n{no_orders if no_orders is not None else 'Not done'}")
print(f"5.2 Customers with orders:\n{has_orders if has_orders is not None else 'Not done'}")
print(f"5.4 Orphan employees:\n{orphan_employees if orphan_employees is not None else 'Not done'}")


# =============================================================================
# PART 6: Common Pitfalls
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: Common Pitfalls")
print("=" * 60)

# PITFALL 1: Column name collisions
# When both DataFrames have columns with the same name (besides the key)
df_x = pd.DataFrame({'key': [1, 2], 'value': [10, 20], 'other': ['a', 'b']})
df_y = pd.DataFrame({'key': [1, 2], 'value': [100, 200], 'other': ['x', 'y']})

# EXERCISE 6.1: Handle column collisions with suffixes
# TODO: Join df_x and df_y with custom suffixes '_left' and '_right'
with_suffixes = None  # Your code here

# PITFALL 2: Unexpected row multiplication
# EXERCISE 6.2: Check row counts before and after join
# TODO: Print row counts to verify join didn't multiply rows unexpectedly
print("\n6.2 Row count check:")
print(f"   Orders: {len(orders)}")
print(f"   Customers: {len(customers)}")
# TODO: Join and print result count
orders_customers_count = None  # Join orders with customers, then check len()

# PITFALL 3: NaN handling in joins
df_with_nan = pd.DataFrame({'key': [1, 2, np.nan], 'val': ['a', 'b', 'c']})
df_no_nan = pd.DataFrame({'key': [1, 2, 3], 'other': ['x', 'y', 'z']})

# EXERCISE 6.3: Join with NaN keys
# TODO: What happens when you join on a column with NaN?
nan_join = None  # Your code here
# Note: NaN does NOT match NaN in joins!

print("\n--- Exercise Results ---")
print(f"6.1 With suffixes:\n{with_suffixes if with_suffixes is not None else 'Not done'}")
print(f"6.3 NaN join result:\n{nan_join if nan_join is not None else 'Not done'}")


# =============================================================================
# CHALLENGE EXERCISES
# =============================================================================

print("\n" + "=" * 60)
print("CHALLENGE EXERCISES")
print("=" * 60)

# CHALLENGE 1: Build a complete order report
# TODO: Create a DataFrame with:
# - order_id, order_date, status
# - customer_name, customer_region
# - product_name, category, price
# - quantity, total_value (price * quantity)
order_report = None  # Your code here (multiple joins needed)

# CHALLENGE 2: Customer order summary
# TODO: For each customer, show:
# - customer_id, name, region
# - total_orders (count)
# - total_spent (sum of price * quantity)
# Include customers with 0 orders!
customer_summary = None  # Your code here

# CHALLENGE 3: Find products never ordered
# TODO: Get list of products that have never been ordered
never_ordered = None  # Your code here (anti-join pattern)

# CHALLENGE 4: Department budget utilization
# TODO: For each department, show:
# - dept_name, budget
# - total_salary (sum of employee salaries)
# - num_employees
# - budget_remaining (budget - total_salary)
# Include departments with no employees
budget_report = None  # Your code here

print("\n--- Challenge Results ---")
print(f"C1: Order report shape: {order_report.shape if order_report is not None else 'Not done'}")
print(f"C1 Sample:\n{order_report.head(3) if order_report is not None else 'Not done'}")
print(f"\nC3: Never ordered products:\n{never_ordered if never_ordered is not None else 'Not done'}")


print("\n" + "=" * 60)
print("COMPLETE! Check your answers against the solutions.")
print("=" * 60)
