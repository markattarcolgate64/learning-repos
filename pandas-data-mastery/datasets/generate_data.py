"""
Generate practice datasets for pandas exercises.
Run this script first: python generate_data.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_customers(n=100):
    """Generate customer data."""
    regions = ['North', 'South', 'East', 'West']

    # Generate signup dates over past 2 years
    base_date = datetime(2023, 1, 1)
    signup_dates = [base_date + timedelta(days=np.random.randint(0, 730)) for _ in range(n)]

    customers = pd.DataFrame({
        'customer_id': range(1, n + 1),
        'name': [f'Customer_{i}' for i in range(1, n + 1)],
        'email': [f'customer{i}@example.com' for i in range(1, n + 1)],
        'region': np.random.choice(regions, n),
        'signup_date': signup_dates,
        'is_premium': np.random.choice([True, False], n, p=[0.3, 0.7])
    })

    return customers


def generate_products(n=20):
    """Generate product catalog."""
    categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books']

    products = pd.DataFrame({
        'product_id': range(1, n + 1),
        'product_name': [f'Product_{i}' for i in range(1, n + 1)],
        'category': np.random.choice(categories, n),
        'price': np.round(np.random.uniform(10, 500, n), 2),
        'cost': np.round(np.random.uniform(5, 300, n), 2),
        'in_stock': np.random.choice([True, False], n, p=[0.8, 0.2])
    })

    # Ensure cost < price
    products['cost'] = products.apply(lambda x: min(x['cost'], x['price'] * 0.7), axis=1)

    return products


def generate_orders(n_customers=100, n_products=20, n_orders=500):
    """Generate order data."""
    base_date = datetime(2023, 6, 1)
    order_dates = [base_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n_orders)]

    orders = pd.DataFrame({
        'order_id': range(1, n_orders + 1),
        'customer_id': np.random.randint(1, n_customers + 1, n_orders),
        'product_id': np.random.randint(1, n_products + 1, n_orders),
        'quantity': np.random.randint(1, 5, n_orders),
        'order_date': order_dates,
        'status': np.random.choice(['completed', 'pending', 'cancelled'], n_orders, p=[0.8, 0.15, 0.05])
    })

    return orders


def generate_messy_transactions(n=200):
    """Generate messy transaction data for cleaning practice."""

    # Inconsistent date formats
    date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d']
    base_date = datetime(2024, 1, 1)
    dates = []
    for _ in range(n):
        d = base_date + timedelta(days=np.random.randint(0, 180))
        fmt = np.random.choice(date_formats)
        dates.append(d.strftime(fmt))

    # Amount with inconsistent formatting
    amounts = []
    for _ in range(n):
        val = np.random.uniform(10, 1000)
        if np.random.random() < 0.2:
            amounts.append(f'${val:.2f}')
        elif np.random.random() < 0.1:
            amounts.append(f'{val:.2f} USD')
        else:
            amounts.append(f'{val:.2f}')

    # Categories with inconsistent casing/spelling
    categories_messy = ['electronics', 'Electronics', 'ELECTRONICS', 'Electonics',
                        'clothing', 'Clothing', 'CLOTHING', 'Clothng',
                        'home', 'Home', 'HOME', 'Hom']

    df = pd.DataFrame({
        'transaction_id': range(1, n + 1),
        'date': dates,
        'amount': amounts,
        'category': np.random.choice(categories_messy, n),
        'customer_id': np.random.randint(1, 101, n),
        'notes': [np.nan if np.random.random() < 0.3 else f'Note {i}' for i in range(n)]
    })

    # Add some duplicates
    n_dups = 10
    dup_indices = np.random.choice(range(n), n_dups, replace=False)
    duplicates = df.iloc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # Add some nulls
    for col in ['amount', 'category']:
        null_indices = np.random.choice(range(len(df)), 5, replace=False)
        df.loc[null_indices, col] = np.nan

    return df.sample(frac=1).reset_index(drop=True)  # Shuffle


def generate_employee_data():
    """Generate employee/department data for join exercises."""

    departments = pd.DataFrame({
        'dept_id': [1, 2, 3, 4, 5],
        'dept_name': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'],
        'budget': [500000, 300000, 200000, 150000, 250000]
    })

    employees = pd.DataFrame({
        'emp_id': range(1, 31),
        'name': [f'Employee_{i}' for i in range(1, 31)],
        'dept_id': np.random.choice([1, 2, 3, 4, 5, 6, None], 30),  # 6 doesn't exist, some nulls
        'salary': np.random.randint(50000, 150000, 30),
        'hire_date': [datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 1500)) for _ in range(30)]
    })

    # Some employees have no department (for outer join practice)
    employees.loc[employees['dept_id'] == 6, 'dept_id'] = np.nan

    return employees, departments


def generate_sales_by_region():
    """Generate sales data for reshaping exercises."""
    regions = ['North', 'South', 'East', 'West']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    products = ['A', 'B', 'C']

    data = []
    for region in regions:
        for month in months:
            for product in products:
                data.append({
                    'region': region,
                    'month': month,
                    'product': product,
                    'sales': np.random.randint(1000, 10000),
                    'units': np.random.randint(10, 100)
                })

    return pd.DataFrame(data)


if __name__ == '__main__':
    print("Generating datasets...")

    # Main relational tables
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders()

    # Additional datasets
    messy = generate_messy_transactions()
    employees, departments = generate_employee_data()
    sales = generate_sales_by_region()

    # Save all datasets
    customers.to_csv(os.path.join(SCRIPT_DIR, 'customers.csv'), index=False)
    products.to_csv(os.path.join(SCRIPT_DIR, 'products.csv'), index=False)
    orders.to_csv(os.path.join(SCRIPT_DIR, 'orders.csv'), index=False)
    messy.to_csv(os.path.join(SCRIPT_DIR, 'transactions_messy.csv'), index=False)
    employees.to_csv(os.path.join(SCRIPT_DIR, 'employees.csv'), index=False)
    departments.to_csv(os.path.join(SCRIPT_DIR, 'departments.csv'), index=False)
    sales.to_csv(os.path.join(SCRIPT_DIR, 'sales_by_region.csv'), index=False)

    print(f"Created: customers.csv ({len(customers)} rows)")
    print(f"Created: products.csv ({len(products)} rows)")
    print(f"Created: orders.csv ({len(orders)} rows)")
    print(f"Created: transactions_messy.csv ({len(messy)} rows)")
    print(f"Created: employees.csv ({len(employees)} rows)")
    print(f"Created: departments.csv ({len(departments)} rows)")
    print(f"Created: sales_by_region.csv ({len(sales)} rows)")
    print("\nDone! Datasets ready in datasets/ folder.")
