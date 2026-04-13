# 🚗 Automotive Sales Analytics Pipeline

An end-to-end data analytics pipeline that processes raw automotive dealership sales data into KPI-oriented management dashboards & simulating the reporting infrastructure of a premium automotive financial services organisation.

**Tools & Skills:** Python · Pandas · SQL (SQLite) · Tableau Public · Data Cleaning · KPI Development · Management Reporting

---

## 📊 Live Tableau Dashboards

> 🔗 **[View Live Dashboards on Tableau Public](https://public.tableau.com/app/profile/kelvin.ngabo/viz/AutomotiveSalesAnalytics_17760438858520/RegionalSalesPerformance)**

| Dashboard | Description |
|-----------|-------------|
| Regional Sales Performance | Revenue, units sold & avg price across 5 Canadian regions |
| Revenue Trends & Growth | 24-month trend line with YoY growth analysis |
| Model & Inventory Performance | Model rankings by revenue with tier segmentation |

---

## 🎯 Project Overview

This project mirrors the data pipeline workflow used in automotive financial services environments, where raw dealer sales data must be gathered, cleaned, aggregated, and surfaced as actionable KPIs for management decision-making.

The pipeline processes **2,000 raw sales records** across **5 Canadian regions** and **14 dealerships**, producing **8 KPI output datasets** that power 3 interactive Tableau dashboards.

---

## 🗂️ Project Structure

```
automotive-sales-analytics/
├── data/
│   └── raw_sales_data.csv              # Raw generated dataset (2,000 rows)
├── src/
│   ├── generate_data.py                # Synthetic data generator with intentional noise
│   ├── 01_data_cleaning.py             # ETL: clean, standardise, engineer KPI features
│   ├── 02_sql_analysis.py              # SQL: 8 KPI queries via in-memory SQLite
│   └── 03_export_for_tableau.py        # Combines all KPIs into single Tableau-ready CSV
├── output/
│   ├── cleaned_sales_data.csv          # Analysis-ready dataset (1,202 rows)
│   ├── tableau_master.csv              # Combined KPI file for Tableau
│   ├── kpi_regional_performance.csv
│   ├── kpi_monthly_trend.csv
│   ├── kpi_quarterly_by_region.csv
│   ├── kpi_model_performance.csv
│   ├── kpi_dealer_rankings.csv
│   ├── kpi_finance_distribution.csv
│   ├── kpi_yoy_growth.csv
│   └── kpi_revenue_tiers.csv
├── tableau/
│   └── Automotive_Sales_Analytics.twb  # Tableau workbook
├── requirements.txt
└── README.md
```

---

## ⚙️ Pipeline Steps

### Step 1 — Data Generation (`generate_data.py`)
Generates a realistic raw dataset simulating a premium automotive dealership network:
- **2,000 sales records** across Ontario, BC, Alberta, Quebec, Manitoba
- **11 vehicle models** across Sedan, SUV, Coupe, and EV categories
- **Intentional data quality issues:** 87 null prices, inconsistent casing, whitespace noise, status encoding errors

### Step 2 — Data Cleaning (`01_data_cleaning.py`)
Transforms raw data into an analysis-ready format:
- Strips whitespace and standardises all string fields to Title Case
- Parses date strings to datetime objects
- Imputes **87 null `sale_price` values** using per-model median (preserves distribution)
- Filters out cancelled records (371 removed), retaining 1,629 active rows
- Isolates **1,202 completed sales** for KPI analysis
- Engineers KPI columns: `sale_year`, `sale_quarter`, `month_label`, `year_quarter`, `revenue_tier`
- Runs automated validation assertions before writing output

### Step 3 — SQL Analysis (`02_sql_analysis.py`)
Loads cleaned data into an in-memory SQLite database and executes 8 management-reporting SQL queries:

| Query | Description |
|-------|-------------|
| 1 | Regional Sales Performance (revenue, units, avg price) |
| 2 | Monthly Revenue Trend (24-month time series) |
| 3 | Quarterly Revenue by Region |
| 4 | Model & Category Performance |
| 5 | Top 10 Dealer Rankings |
| 6 | Finance Type Distribution (Cash / Finance / Lease) |
| 7 | Year-over-Year Revenue & Unit Growth (2023 vs 2024) |
| 8 | Revenue Tier Breakdown (Entry / Mid / Premium / Ultra) |

### Step 4 — Tableau Export (`03_export_for_tableau.py`)
Combines all 8 KPI outputs into a single `tableau_master.csv` with a `data_type` column for dashboard filtering — enabling one unified data source across all three Tableau dashboards.

### Step 5 — Tableau Dashboards
Three interactive dashboards published to Tableau Public:
1. **Regional Sales Performance** — Revenue by region, units sold, avg sale price with reference line
2. **Revenue Trends & Growth** — 24-month revenue trend line, monthly units trend, YoY comparison
3. **Model & Inventory Performance** — Horizontal bar chart by model coloured by category, revenue tier pie chart

---

## 📈 Key Findings

| Metric | Value |
|--------|-------|
| Total Completed Sales | 1,202 |
| Total Revenue (2023–2024) | ~$106.7M |
| YoY Revenue Growth | **+5.48%** |
| YoY Unit Growth | **+3.38%** |
| Top Region by Revenue | Ontario ($23.8M) |
| Top Model by Revenue | 8 Series ($18.1M) |
| Top Dealer | Prairie Motors — Manitoba ($11M) |
| Most Common Finance Type | Finance (33.8%) |
| Dominant Revenue Tier | Mid 60–90K (40.3% of units) |
| Peak Revenue Month | September 2024 ($5.9M) |

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/ngab0016/automotive-sales-analytics.git
cd automotive-sales-analytics

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the raw dataset
python3 src/generate_data.py

# 5. Run the data cleaning pipeline
python3 src/01_data_cleaning.py

# 6. Run the SQL KPI analysis
python3 src/02_sql_analysis.py

# 7. Export combined Tableau CSV
python3 src/03_export_for_tableau.py

# 8. Open output/tableau_master.csv in Tableau Public
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Data processing & pipeline orchestration |
| Pandas | Data cleaning, transformation, feature engineering |
| NumPy | Numerical operations & random data generation |
| SQLite (stdlib) | In-memory SQL analytical layer — no server required |
| SQL | KPI queries, aggregations, window functions, CTEs, YoY calculations |
| Tableau Public | Interactive dashboard visualisation & publishing |

---

## 👤 Author

**Kelvin Nsengiyumva Ngabo**

[GitHub](https://github.com/ngab0016) 
