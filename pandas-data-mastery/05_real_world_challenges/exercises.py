"""
05 - Real World Challenges
==========================

Mini-projects combining all skills learned.
Each challenge simulates a real data task.

Run: python exercises.py
"""

import pandas as pd
import numpy as np

# Load all data
customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
products = pd.read_csv('../datasets/products.csv')
messy = pd.read_csv('../datasets/transactions_messy.csv')
employees = pd.read_csv('../datasets/employees.csv')
departments = pd.read_csv('../datasets/departments.csv')


# =============================================================================
# CHALLENGE 1: Clean Messy Transaction Data
# =============================================================================
# You've received a messy export that needs cleaning before analysis.

print("=" * 60)
print("CHALLENGE 1: Clean Messy Transaction Data")
print("=" * 60)
print(f"\nMessy data preview:\n{messy.head(10)}")
print(f"\nData types:\n{messy.dtypes}")
print(f"\nMissing values:\n{messy.isna().sum()}")

"""
TODO: Clean this data step by step

Step 1: Remove duplicate rows
- The data has exact duplicates that need to be removed
"""
clean_df = messy.copy()
clean_df = None  # Remove duplicates

"""
Step 2: Standardize the 'amount' column
- Remove '$' and 'USD' text
- Convert to float
- Handle any NaN values (fill with median or drop)
"""
# Your code here
# Hint: .str.replace('$', '').str.replace(' USD', '').astype(float)

"""
Step 3: Standardize the 'category' column
- Fix inconsistent casing (Electronics, ELECTRONICS, electronics → Electronics)
- Fix typos (Electonics → Electronics, Clothng → Clothing, Hom → Home)
- Handle NaN values
"""
# Your code here
# Hint: .str.lower() then .str.replace() or use a mapping dict

"""
Step 4: Parse dates consistently
- The 'date' column has multiple formats
- Convert all to datetime
"""
# Your code here
# Hint: pd.to_datetime(clean_df['date'], format='mixed') or infer_datetime_format=True

"""
Step 5: Validate customer_ids
- Check if all customer_ids exist in the customers table
- Flag or remove invalid ones
"""
# Your code here

"""
Step 6: Final validation
- Print summary of clean data
- Verify no nulls in critical columns
- Verify data types are correct
"""
print("\n--- After Cleaning ---")
if clean_df is not None:
    print(f"Rows: {len(messy)} → {len(clean_df)}")
    print(f"Missing values:\n{clean_df.isna().sum()}")
    print(f"\nClean data preview:\n{clean_df.head()}")
else:
    print("Not completed yet")


# =============================================================================
# CHALLENGE 2: Customer Segmentation Report
# =============================================================================
# Marketing wants to segment customers by behavior for targeted campaigns.

print("\n" + "=" * 60)
print("CHALLENGE 2: Customer Segmentation Report")
print("=" * 60)

"""
TODO: Create a customer segmentation DataFrame with:

Columns needed:
- customer_id
- name
- region
- signup_date
- days_as_customer (from signup to today)
- total_orders
- total_items (sum of quantity)
- total_spent (sum of price * quantity)
- avg_order_value
- days_since_last_order
- favorite_category (most ordered category)
- segment: 'VIP', 'Regular', 'At-Risk', 'New', 'Inactive'

Segmentation rules:
- VIP: total_spent > 1000 AND total_orders >= 10
- At-Risk: days_since_last_order > 180 AND total_orders > 0
- Inactive: days_since_last_order > 365 OR (no orders and days_as_customer > 90)
- New: days_as_customer <= 90
- Regular: everyone else
"""

customer_segments = None  # Your code here

# Build it step by step:

# Step 1: Calculate order metrics per customer
order_metrics = None  # groupby customer_id, aggregate order stats

# Step 2: Get last order date per customer
last_order = None  # groupby customer_id, get max order_date

# Step 3: Get favorite category per customer
# Hint: Join orders with products, groupby customer + category, count, then get idxmax
favorite_cat = None

# Step 4: Merge everything with customers table
# Use left join to keep customers with no orders

# Step 5: Calculate derived fields
# days_as_customer, days_since_last_order, etc.

# Step 6: Apply segmentation logic
# Hint: Use np.select() with conditions

print("\n--- Segmentation Results ---")
if customer_segments is not None:
    print(f"Segment distribution:\n{customer_segments['segment'].value_counts()}")
    print(f"\nSample:\n{customer_segments.head()}")
else:
    print("Not completed yet")


# =============================================================================
# CHALLENGE 3: Executive Dashboard Data
# =============================================================================
# Prepare data for a monthly executive dashboard.

print("\n" + "=" * 60)
print("CHALLENGE 3: Executive Dashboard Data")
print("=" * 60)

"""
TODO: Create multiple summary DataFrames for dashboard

1. monthly_summary: Monthly trends
   - year_month
   - total_orders
   - total_revenue
   - unique_customers
   - avg_order_value
   - mom_growth (month-over-month % change in revenue)

2. category_performance: Category breakdown
   - category
   - total_revenue
   - total_orders
   - avg_price
   - pct_of_total_revenue

3. regional_summary: By region
   - region
   - total_customers
   - total_orders
   - total_revenue
   - revenue_per_customer

4. top_products: Top 10 products by revenue
   - product_name
   - category
   - total_revenue
   - total_units_sold
   - unique_customers
"""

# Join orders with products and customers first for easier analysis
orders_full = orders.merge(products, on='product_id').merge(
    customers[['customer_id', 'region']], on='customer_id'
)
orders_full['revenue'] = orders_full['price'] * orders_full['quantity']

# 1. Monthly Summary
monthly_summary = None  # Your code here

# 2. Category Performance
category_performance = None  # Your code here

# 3. Regional Summary
regional_summary = None  # Your code here

# 4. Top Products
top_products = None  # Your code here

print("\n--- Dashboard Data ---")
print("\n1. Monthly Summary:")
print(monthly_summary.head() if monthly_summary is not None else "Not completed")

print("\n2. Category Performance:")
print(category_performance if category_performance is not None else "Not completed")

print("\n3. Regional Summary:")
print(regional_summary if regional_summary is not None else "Not completed")

print("\n4. Top 10 Products:")
print(top_products if top_products is not None else "Not completed")


# =============================================================================
# CHALLENGE 4: Data Quality Report
# =============================================================================
# QA team needs a data quality assessment.

print("\n" + "=" * 60)
print("CHALLENGE 4: Data Quality Report")
print("=" * 60)

"""
TODO: Create a data quality report that identifies:

1. Missing values summary for each table
2. Orphaned records (foreign keys pointing to non-existent records)
3. Duplicate detection
4. Outlier detection (e.g., orders with unusually high quantities)
5. Date validation (future dates, dates before business started)

Output should be a dictionary or set of DataFrames summarizing issues.
"""

quality_report = {
    'missing_values': {},
    'orphaned_orders': None,  # Orders with invalid customer_id or product_id
    'orphaned_employees': None,  # Employees with invalid dept_id
    'duplicate_orders': None,  # Potential duplicate orders (same customer, product, date, quantity)
    'quantity_outliers': None,  # Orders where quantity > mean + 3*std
    'date_issues': None,  # Orders with dates in the future
}

# TODO: Fill in each part of the quality report

# 1. Missing values for each table
for name, df in [('customers', customers), ('orders', orders), ('products', products)]:
    quality_report['missing_values'][name] = None  # df.isna().sum()

# 2. Orphaned records
quality_report['orphaned_orders'] = None  # Orders with customer_id not in customers

# 3. Duplicate detection
quality_report['duplicate_orders'] = None  # Find potential duplicates

# 4. Outlier detection
quality_report['quantity_outliers'] = None  # Orders with extreme quantities

# 5. Date issues
quality_report['date_issues'] = None  # Orders with future dates

print("\n--- Quality Report ---")
print("Missing values:", quality_report['missing_values'])
print(f"\nOrphaned orders: {len(quality_report['orphaned_orders']) if quality_report['orphaned_orders'] is not None else 'Not checked'}")
print(f"Quantity outliers: {len(quality_report['quantity_outliers']) if quality_report['quantity_outliers'] is not None else 'Not checked'}")


# =============================================================================
# BONUS: Export Results
# =============================================================================

print("\n" + "=" * 60)
print("BONUS: Export Your Results")
print("=" * 60)

"""
TODO (Optional): Export your cleaned/processed data

1. Save clean_df to 'transactions_clean.csv'
2. Save customer_segments to 'customer_segments.csv'
3. Save dashboard data to an Excel file with multiple sheets
"""

# Uncomment when ready:
# if clean_df is not None:
#     clean_df.to_csv('../datasets/transactions_clean.csv', index=False)
#     print("Saved transactions_clean.csv")

# if customer_segments is not None:
#     customer_segments.to_csv('../datasets/customer_segments.csv', index=False)
#     print("Saved customer_segments.csv")

# Export to Excel with multiple sheets:
# with pd.ExcelWriter('../datasets/dashboard_data.xlsx') as writer:
#     monthly_summary.to_excel(writer, sheet_name='Monthly', index=False)
#     category_performance.to_excel(writer, sheet_name='Categories', index=False)
#     regional_summary.to_excel(writer, sheet_name='Regions', index=False)
#     top_products.to_excel(writer, sheet_name='Top Products', index=False)


print("\n" + "=" * 60)
print("CHALLENGES COMPLETE!")
print("=" * 60)
print("""
Summary of what you practiced:
- Data cleaning (duplicates, types, inconsistent formats)
- Multi-table joins and aggregations
- Complex business logic with segmentation
- Creating analysis-ready datasets
- Data quality validation

Check your work against the solutions when ready.
""")
