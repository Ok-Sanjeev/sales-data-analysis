import pandas as pd
import numpy as np

np.random.seed(42)
n = 50000
regions = ['North', 'South', 'East', 'West', 'Central']
categories = ['Electronics', 'Clothing', 'Food & Beverage', 'Home & Garden', 'Sports']
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes'],
    'Food & Beverage': ['Coffee', 'Tea', 'Snacks', 'Beverages', 'Dairy'],
    'Home & Garden': ['Chair', 'Lamp', 'Curtains', 'Plant Pot', 'Rug'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Cycle', 'Cricket Bat']
}
months = pd.date_range('2023-01-01', '2023-12-31', freq='D')

cat_choices = np.random.choice(categories, n, p=[0.30, 0.23, 0.20, 0.15, 0.12])
prod_choices = [np.random.choice(products[c]) for c in cat_choices]
date_choices = np.random.choice(months, n)

base_price = {'Electronics': 25000, 'Clothing': 1200, 'Food & Beverage': 350, 'Home & Garden': 2200, 'Sports': 3500}
prices = [round(base_price[c] * np.random.uniform(0.7, 1.5), 2) for c in cat_choices]
quantities = np.random.randint(1, 6, n)
discounts = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], n, p=[0.5, 0.2, 0.15, 0.1, 0.05])
revenue = [round(p * q * (1 - d), 2) for p, q, d in zip(prices, quantities, discounts)]

# inject some missing values
order_ids = [f'ORD-{str(i).zfill(6)}' for i in range(1, n+1)]
customer_ids = np.random.randint(1000, 9999, n)
regions_col = np.random.choice(regions, n)

df = pd.DataFrame({
    'order_id': order_ids,
    'date': date_choices,
    'customer_id': customer_ids,
    'region': regions_col,
    'category': cat_choices,
    'product': prod_choices,
    'unit_price': prices,
    'quantity': quantities,
    'discount': discounts,
    'revenue': revenue
})

# inject nulls
null_idx = np.random.choice(df.index, 400, replace=False)
df.loc[null_idx[:200], 'discount'] = np.nan
df.loc[null_idx[200:], 'region'] = np.nan

df.to_csv('/home/claude/projects/sales-data-analysis/sales_data.csv', index=False)
print(f"Dataset created: {len(df)} rows, {df.isnull().sum().sum()} nulls injected")