# Sales Data Analysis 📊

An end-to-end data analysis project on a 50,000-row sales dataset covering data cleaning, exploratory data analysis (EDA), KPI tracking, and dashboard development.

## 🔍 Problem Statement
A retail business needed to understand its revenue distribution, identify underperforming regions, and detect seasonal demand patterns to optimise inventory and sales strategy.

## 📁 Dataset
- **Source:** Synthetically generated to mirror real-world retail sales data
- **Size:** 50,000 rows × 10 columns
- **Fields:** `order_id`, `date`, `customer_id`, `region`, `category`, `product`, `unit_price`, `quantity`, `discount`, `revenue`
- **Injected Issues:** 400 missing values (nulls in `discount` and `region`) for realistic cleaning

## 🛠️ Tools & Libraries
| Tool | Purpose |
|------|----------|
| Python | Core analysis |
| Pandas | Data cleaning & transformation |
| NumPy | Numerical operations |
| Matplotlib | Visualisations |
| Seaborn | Statistical plots |
| Excel | Interactive KPI dashboard |

## 🔧 Steps Followed
1. **Data Loading & Inspection** — shape, dtypes, null check
2. **Data Cleaning** — removed duplicates, imputed nulls (median for discount, mode for region), recalculated revenue
3. **Feature Engineering** — extracted `month`, `month_name`, `month_num`
4. **EDA** — revenue by category, monthly trend, regional breakdown
5. **Visualisation** — 4-panel dashboard (bar, line, pie, scatter)
6. **Business Recommendations** — based on findings

## 📈 Key Findings
| Metric | Value |
|--------|-------|
| Total Revenue | ₹134.55 Cr |
| Top Category (Electronics) | 87.3% of revenue |
| Peak Month | March |
| Avg Order Value | ₹26,911 |
| Underperforming Regions | West, Central, North |

- **Top-2 categories account for 92% of total revenue** — heavy concentration risk
- March–April shows a consistent seasonal peak → recommend pre-stocking
- 3 underperforming segments identified with targeted strategy recommendations

## 📊 Dashboard Preview
![Sales Dashboard](sales_dashboard.png)

## 🚀 How to Run
```bash
# Clone repo and navigate to folder
git clone https://github.com/Ok-Sanjeev/sales-data-analysis
cd sales-data-analysis

# Install dependencies
pip install -r requirements.txt

# Generate dataset
python generate_data.py

# Run analysis
python sales_analysis.py
```

## 📂 File Structure
```
sales-data-analysis/
├── generate_data.py        # Dataset generation script
├── sales_analysis.py       # Main analysis + visualisation
├── sales_data.csv          # Generated dataset
├── sales_dashboard.png     # Output dashboard
├── requirements.txt
└── README.md
```

## 💡 Business Recommendations
1. Diversify product mix — reduce over-reliance on Electronics (87% revenue share is high-risk)
2. Launch targeted promotions in West, Central, and North regions to close the gap
3. Pre-stock high-demand categories before March peak season