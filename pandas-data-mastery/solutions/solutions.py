"""
SOLUTIONS
=========

⚠️  SPOILER ALERT: Only look after attempting exercises yourself!

Selected solutions for key exercises.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# 01 - CORE OPERATIONS
# =============================================================================

def solutions_01():
    """Core operations solutions."""
    customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
    orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
    products = pd.read_csv('../datasets/products.csv')

    # --- PART 1: Boolean Masks ---

    # 1.1: Boolean mask for premium customers
    mask_premium = customers['is_premium'] == True
    # or simply: mask_premium = customers['is_premium']

    # 1.2: Use mask to filter
    premium_customers = customers[mask_premium]

    # 1.3: Combine masks (premium AND West)
    premium_west = customers[(customers['is_premium']) & (customers['region'] == 'West')]

    # 1.4: Negate mask
    non_premium = customers[~customers['is_premium']]

    # 1.5: isin() for multiple values
    north_south = customers[customers['region'].isin(['North', 'South'])]

    # --- PART 2: loc vs iloc ---

    # 2.1: Select columns with loc
    name_region = customers.loc[:, ['name', 'region']]

    # 2.2: Select rows and columns
    first_10_name_email = customers.loc[:9, ['name', 'email']]

    # 2.3: iloc for position-based
    slice_iloc = customers.iloc[5:11, 0:2]

    # 2.4: Combine mask with loc
    premium_name_region = customers.loc[customers['is_premium'], ['name', 'region']]

    # --- PART 3: query() ---

    # 3.1: Simple query
    high_quantity = orders.query('quantity > 3')

    # 3.2: Multiple conditions
    completed_multi = orders.query('status == "completed" and quantity >= 2')

    # 3.3: Query with variable
    min_qty = 3
    above_min = orders.query('quantity > @min_qty')

    # 3.4: Query string
    electronics = products.query('category == "Electronics"')

    # --- PART 4: GroupBy ---

    # 4.1: Count per customer
    orders_per_customer = orders.groupby('customer_id').size()

    # 4.2: Sum quantity per customer
    qty_per_customer = orders.groupby('customer_id')['quantity'].sum()

    # 4.3: Multiple aggregations
    customer_stats = orders.groupby('customer_id')['quantity'].agg(['count', 'sum', 'mean'])

    # 4.4: GroupBy multiple columns
    orders_by_customer_status = orders.groupby(['customer_id', 'status']).size()

    # 4.5: Named aggregations
    named_stats = orders.groupby('customer_id').agg(
        total_orders=('order_id', 'count'),
        total_qty=('quantity', 'sum')
    )

    # --- CHALLENGES ---

    # C1: Customers in 2023, East or West
    customers_2023_ew = customers[
        (customers['signup_date'].dt.year == 2023) &
        (customers['region'].isin(['East', 'West']))
    ]

    # C2: Customers with > 5 orders
    order_counts = orders.groupby('customer_id').size()
    high_volume_customers = order_counts[order_counts > 5].index.tolist()

    # C3: Top 3 by quantity
    top_3_by_qty = (orders
        .groupby('customer_id')['quantity'].sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
        .rename(columns={'quantity': 'total_quantity'})
    )

    return {
        'premium_customers': premium_customers,
        'high_quantity': high_quantity,
        'customer_stats': customer_stats,
        'top_3_by_qty': top_3_by_qty
    }


# =============================================================================
# 02 - RESHAPING
# =============================================================================

def solutions_02():
    """Reshaping solutions."""
    sales = pd.read_csv('../datasets/sales_by_region.csv')

    # 1.1: Monthly by region pivot
    monthly_by_region = sales.pivot_table(
        index='month',
        columns='region',
        values='sales',
        aggfunc='sum'
    )

    # 1.2: Multiple values
    sales_and_units = sales.pivot_table(
        index='region',
        columns='product',
        values=['sales', 'units'],
        aggfunc='sum'
    )

    # 1.4: With margins
    with_totals = sales.pivot_table(
        index='month',
        columns='region',
        values='sales',
        aggfunc='sum',
        margins=True
    )

    # 3.1: Melt
    wide_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'math': [90, 85, 78],
        'science': [88, 92, 85],
        'english': [95, 78, 90]
    })
    long_data = pd.melt(wide_data, id_vars=['name'])

    # 3.2: Melt with custom names
    long_named = pd.melt(
        wide_data,
        id_vars=['name'],
        var_name='subject',
        value_name='score'
    )

    # 4.1: Stack
    pivot_example = sales.pivot_table(index='region', columns='product', values='sales', aggfunc='sum')
    stacked = pivot_example.stack()

    return {
        'monthly_by_region': monthly_by_region,
        'long_data': long_data,
        'stacked': stacked
    }


# =============================================================================
# 03 - JOINS AND MERGES
# =============================================================================

def solutions_03():
    """Joins solutions."""
    customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
    orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
    products = pd.read_csv('../datasets/products.csv')
    employees = pd.read_csv('../datasets/employees.csv')
    departments = pd.read_csv('../datasets/departments.csv')

    # 1.1: Inner join
    orders_with_customers = pd.merge(orders, customers, on='customer_id', how='inner')

    # 1.2: Left join
    orders_with_products = pd.merge(orders, products, on='product_id', how='left')

    # 1.3: Right join
    dept_with_employees = pd.merge(employees, departments, on='dept_id', how='right')

    # 1.4: Outer join
    full_join = pd.merge(employees, departments, on='dept_id', how='outer')

    # 5.1: Anti-join (customers without orders)
    customers_sample = pd.DataFrame({
        'customer_id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    })
    orders_sample = pd.DataFrame({
        'order_id': [101, 102, 103],
        'customer_id': [1, 2, 1]
    })

    merged = pd.merge(customers_sample, orders_sample, on='customer_id', how='left', indicator=True)
    no_orders = merged[merged['_merge'] == 'left_only'][['customer_id', 'name']]

    # 5.2: Semi-join (customers with orders)
    has_orders = customers_sample[
        customers_sample['customer_id'].isin(orders_sample['customer_id'])
    ]

    # 5.3: Anti-join with isin
    no_orders_alt = customers_sample[
        ~customers_sample['customer_id'].isin(orders_sample['customer_id'])
    ]

    # Challenge 1: Complete order report
    order_report = (orders
        .merge(customers[['customer_id', 'name', 'region']], on='customer_id')
        .merge(products[['product_id', 'product_name', 'category', 'price']], on='product_id')
        .assign(total_value=lambda df: df['price'] * df['quantity'])
    )

    # Challenge 3: Products never ordered
    never_ordered = products[~products['product_id'].isin(orders['product_id'])]

    return {
        'orders_with_customers': orders_with_customers,
        'no_orders': no_orders,
        'order_report': order_report,
        'never_ordered': never_ordered
    }


# =============================================================================
# 04 - ADVANCED PATTERNS
# =============================================================================

def solutions_04():
    """Advanced patterns solutions."""
    orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
    products = pd.read_csv('../datasets/products.csv')

    # 1.1: Method chaining
    chained_result = (orders
        .query('status == "completed"')
        .groupby('customer_id')['quantity'].sum()
        .reset_index()
        .rename(columns={'quantity': 'total_qty'})
    )

    # 1.2: assign()
    orders_enhanced = orders.assign(
        year=lambda df: df['order_date'].dt.year,
        month=lambda df: df['order_date'].dt.month,
        is_large=lambda df: df['quantity'] >= 3
    )

    # 2.1: Vectorized margin calculation
    products_copy = products.copy()
    products_copy['margin_pct'] = (products_copy['price'] - products_copy['cost']) / products_copy['price'] * 100

    # 2.3: np.select for categories
    conditions = [
        products_copy['price'] < 50,
        products_copy['price'] < 200,
        products_copy['price'] >= 200
    ]
    choices = ['budget', 'mid-range', 'premium']
    products_copy['price_tier'] = np.select(conditions, choices)

    # 3.1-3.4: Window functions
    daily_sales = orders.groupby('order_date')['quantity'].sum().reset_index()
    daily_sales = daily_sales.sort_values('order_date').reset_index(drop=True)
    daily_sales.columns = ['date', 'sales']

    daily_sales['rolling_7d'] = daily_sales['sales'].rolling(7).mean()
    daily_sales['rolling_7d_partial'] = daily_sales['sales'].rolling(7, min_periods=1).mean()
    daily_sales['cumsum'] = daily_sales['sales'].cumsum()
    daily_sales['cummean'] = daily_sales['sales'].expanding().mean()
    daily_sales['prev_day'] = daily_sales['sales'].shift(1)
    daily_sales['daily_change'] = daily_sales['sales'] - daily_sales['prev_day']

    # 4.1-4.4: String operations
    string_data = pd.DataFrame({
        'name': ['  John Smith  ', 'jane doe', 'BOB JONES', 'Alice Brown'],
        'email': ['john@example.com', 'jane@test.org', 'bob@example.com', 'alice@test.org'],
        'phone': ['123-456-7890', '(234) 567-8901', '345.678.9012', '456 789 0123']
    })

    string_data['name_clean'] = string_data['name'].str.strip().str.title()
    string_data['domain'] = string_data['email'].str.split('@').str[1]
    string_data['phone_clean'] = string_data['phone'].str.replace(r'\D', '', regex=True)

    return {
        'chained_result': chained_result,
        'products_copy': products_copy,
        'daily_sales': daily_sales,
        'string_data': string_data
    }


# =============================================================================
# 05 - REAL WORLD CHALLENGES
# =============================================================================

def solutions_05():
    """Real world challenge solutions."""
    customers = pd.read_csv('../datasets/customers.csv', parse_dates=['signup_date'])
    orders = pd.read_csv('../datasets/orders.csv', parse_dates=['order_date'])
    products = pd.read_csv('../datasets/products.csv')
    messy = pd.read_csv('../datasets/transactions_messy.csv')

    # Challenge 1: Clean messy data
    clean_df = messy.copy()

    # Remove duplicates
    clean_df = clean_df.drop_duplicates()

    # Clean amount
    clean_df['amount'] = (clean_df['amount']
        .str.replace('$', '', regex=False)
        .str.replace(' USD', '', regex=False)
        .astype(float)
    )
    clean_df['amount'] = clean_df['amount'].fillna(clean_df['amount'].median())

    # Clean category
    clean_df['category'] = clean_df['category'].str.lower().str.strip()
    category_map = {
        'electonics': 'electronics',
        'clothng': 'clothing',
        'hom': 'home'
    }
    clean_df['category'] = clean_df['category'].replace(category_map)
    clean_df['category'] = clean_df['category'].fillna('unknown')

    # Parse dates
    clean_df['date'] = pd.to_datetime(clean_df['date'], format='mixed')

    # Challenge 2: Customer segmentation
    orders_full = orders.merge(products, on='product_id')
    orders_full['revenue'] = orders_full['price'] * orders_full['quantity']

    # Order metrics
    order_metrics = orders_full.groupby('customer_id').agg(
        total_orders=('order_id', 'count'),
        total_items=('quantity', 'sum'),
        total_spent=('revenue', 'sum'),
        last_order_date=('order_date', 'max')
    ).reset_index()

    # Merge with customers
    customer_segments = customers.merge(order_metrics, on='customer_id', how='left')

    # Fill NaN for customers with no orders
    customer_segments['total_orders'] = customer_segments['total_orders'].fillna(0)
    customer_segments['total_items'] = customer_segments['total_items'].fillna(0)
    customer_segments['total_spent'] = customer_segments['total_spent'].fillna(0)

    # Calculate metrics
    today = datetime.now()
    customer_segments['days_as_customer'] = (today - customer_segments['signup_date']).dt.days
    customer_segments['days_since_last_order'] = (today - customer_segments['last_order_date']).dt.days
    customer_segments['avg_order_value'] = customer_segments['total_spent'] / customer_segments['total_orders'].replace(0, np.nan)

    # Segmentation
    conditions = [
        (customer_segments['total_spent'] > 1000) & (customer_segments['total_orders'] >= 10),
        (customer_segments['days_since_last_order'] > 180) & (customer_segments['total_orders'] > 0),
        (customer_segments['days_since_last_order'] > 365) | ((customer_segments['total_orders'] == 0) & (customer_segments['days_as_customer'] > 90)),
        customer_segments['days_as_customer'] <= 90,
    ]
    choices = ['VIP', 'At-Risk', 'Inactive', 'New']
    customer_segments['segment'] = np.select(conditions, choices, default='Regular')

    return {
        'clean_df': clean_df,
        'customer_segments': customer_segments
    }


# =============================================================================
# RUN SOLUTIONS
# =============================================================================

if __name__ == '__main__':
    print("Running solution checks...")

    try:
        sol_01 = solutions_01()
        print("✓ 01_core_operations solutions work")
    except Exception as e:
        print(f"✗ 01_core_operations error: {e}")

    try:
        sol_02 = solutions_02()
        print("✓ 02_reshaping solutions work")
    except Exception as e:
        print(f"✗ 02_reshaping error: {e}")

    try:
        sol_03 = solutions_03()
        print("✓ 03_joins_and_merges solutions work")
    except Exception as e:
        print(f"✗ 03_joins_and_merges error: {e}")

    try:
        sol_04 = solutions_04()
        print("✓ 04_advanced_patterns solutions work")
    except Exception as e:
        print(f"✗ 04_advanced_patterns error: {e}")

    try:
        sol_05 = solutions_05()
        print("✓ 05_real_world_challenges solutions work")
    except Exception as e:
        print(f"✗ 05_real_world_challenges error: {e}")

    print("\nDone!")
