import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({'figure.dpi': 120, 'font.family': 'DejaVu Sans', 'axes.spines.top': False, 'axes.spines.right': False})
sns.set_palette("muted")

# ── 1. LOAD & INSPECT ──────────────────────────────────────────────────────────
df = pd.read_csv('sales_data.csv', parse_dates=['date'])
print("=== DATASET OVERVIEW ===")
print(f"Shape: {df.shape}")
print(f"\nNull values:\n{df.isnull().sum()}")
print(f"\nDtypes:\n{df.dtypes}")

# ── 2. DATA CLEANING ───────────────────────────────────────────────────────────
print("\n=== DATA CLEANING ===")
before = len(df)
df = df.drop_duplicates()
print(f"Duplicates removed: {before - len(df)}")

df['discount'].fillna(df['discount'].median(), inplace=True)
df['region'].fillna(df['region'].mode()[0], inplace=True)
print(f"Nulls after cleaning: {df.isnull().sum().sum()}")

df['revenue'] = df['unit_price'] * df['quantity'] * (1 - df['discount'])
df['month'] = df['date'].dt.to_period('M')
df['month_num'] = df['date'].dt.month
df['month_name'] = df['date'].dt.strftime('%b')

# ── 3. EDA & KEY INSIGHTS ──────────────────────────────────────────────────────
print("\n=== KEY BUSINESS INSIGHTS ===")

total_revenue = df['revenue'].sum()
cat_revenue = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
top2_share = cat_revenue.head(2).sum() / total_revenue * 100
print(f"Total Revenue: ₹{total_revenue:,.0f}")
print(f"\nRevenue by Category:\n{cat_revenue.apply(lambda x: f'₹{x:,.0f}')}")
print(f"\nTop 2 categories account for {top2_share:.1f}% of total revenue")

monthly_rev = df.groupby('month_num')['revenue'].sum()
peak_month = monthly_rev.idxmax()
low_month = monthly_rev.idxmin()
print(f"\nPeak month: {peak_month} | Lowest month: {low_month}")

region_rev = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
print(f"\nRevenue by Region:\n{region_rev.apply(lambda x: f'₹{x:,.0f}')}")

underperforming = region_rev.tail(3)
print(f"\nUnderperforming regions: {list(underperforming.index)}")

avg_order = df.groupby('order_id')['revenue'].sum().mean()
print(f"\nAverage Order Value: ₹{avg_order:,.0f}")

# ── 4. VISUALIZATIONS ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Sales Data Analysis — Dashboard', fontsize=16, fontweight='bold', y=1.01)

# Plot 1: Revenue by Category
ax1 = axes[0, 0]
colors = ['#2ecc71' if i < 2 else '#95a5a6' for i in range(len(cat_revenue))]
bars = ax1.bar(cat_revenue.index, cat_revenue.values / 1e6, color=colors, edgecolor='white', linewidth=0.5)
ax1.set_title('Revenue by Category (₹ Million)', fontweight='bold')
ax1.set_xlabel('Category')
ax1.set_ylabel('Revenue (₹M)')
ax1.tick_params(axis='x', rotation=15)
for bar, val in zip(bars, cat_revenue.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'₹{val/1e6:.1f}M', ha='center', va='bottom', fontsize=8)

# Plot 2: Monthly Revenue Trend
ax2 = axes[0, 1]
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ax2.plot(range(1,13), [monthly_rev.get(i,0)/1e6 for i in range(1,13)],
         marker='o', color='#3498db', linewidth=2, markersize=6)
ax2.fill_between(range(1,13), [monthly_rev.get(i,0)/1e6 for i in range(1,13)], alpha=0.15, color='#3498db')
ax2.set_xticks(range(1,13))
ax2.set_xticklabels(month_names, rotation=30)
ax2.set_title('Monthly Revenue Trend (₹ Million)', fontweight='bold')
ax2.set_ylabel('Revenue (₹M)')

# Plot 3: Revenue by Region
ax3 = axes[1, 0]
wedges, texts, autotexts = ax3.pie(region_rev.values, labels=region_rev.index,
                                    autopct='%1.1f%%', startangle=90,
                                    colors=sns.color_palette("muted", len(region_rev)))
ax3.set_title('Revenue Share by Region', fontweight='bold')

# Plot 4: Discount vs Revenue scatter
ax4 = axes[1, 1]
sample = df.sample(2000, random_state=42)
scatter_colors = {'Electronics':'#e74c3c','Clothing':'#3498db','Food & Beverage':'#2ecc71',
                  'Home & Garden':'#f39c12','Sports':'#9b59b6'}
for cat in df['category'].unique():
    mask = sample['category'] == cat
    ax4.scatter(sample.loc[mask,'discount']*100, sample.loc[mask,'revenue'],
                alpha=0.4, s=15, label=cat, color=scatter_colors.get(cat,'gray'))
ax4.set_xlabel('Discount (%)')
ax4.set_ylabel('Revenue (₹)')
ax4.set_title('Discount vs Revenue by Category', fontweight='bold')
ax4.legend(fontsize=7, loc='upper right')

plt.tight_layout()
plt.savefig('sales_dashboard.png', bbox_inches='tight', dpi=150)
plt.close()
print("\nDashboard saved: sales_dashboard.png")

# ── 5. KPI SUMMARY TABLE ──────────────────────────────────────────────────────
print("\n=== KPI SUMMARY ===")
kpis = {
    'Total Revenue': f"₹{total_revenue/1e7:.2f} Cr",
    'Total Orders': f"{df['order_id'].nunique():,}",
    'Avg Order Value': f"₹{avg_order:,.0f}",
    'Top Category': cat_revenue.index[0],
    'Top Region': region_rev.index[0],
    'Peak Month': month_names[peak_month-1],
    'Top-2 Category Share': f"{top2_share:.1f}%"
}
for k, v in kpis.items():
    print(f"  {k:25s}: {v}")