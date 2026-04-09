"""
02_sql_analysis.py
───────────────────────────────────────────────────────────────
Step 2 of the Automotive Sales Analytics Pipeline.

Loads cleaned data into an in-memory SQLite database and runs
KPI-oriented SQL queries that mirror BMW Financial Services'
management reporting requirements:

  • Regional sales performance
  • Monthly & quarterly revenue trends
  • Model & category breakdown
  • Dealer-level rankings
  • Finance type distribution
  • Year-over-year growth

Output CSVs feed directly into Tableau dashboards.
"""

import pandas as pd
import sqlite3
import os

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_PATH = os.path.join(BASE_DIR, "output", "cleaned_sales_data.csv")
OUT_DIR    = os.path.join(BASE_DIR, "output")

# ── Load cleaned data into SQLite ─────────────────────────────
df = pd.read_csv(CLEAN_PATH)
conn = sqlite3.connect(":memory:")
df.to_sql("sales", conn, index=False, if_exists="replace")
print("SQLite in-memory DB loaded with cleaned sales data.\n")

def run_query(title, sql, out_file):
    """Execute a SQL query, print results, and save to CSV."""
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))
    path = os.path.join(OUT_DIR, out_file)
    result.to_csv(path, index=False)
    print(f"\n  [✓] Saved → output/{out_file}\n")
    return result

# ═════════════════════════════════════════════════════════════
# QUERY 1 — Regional Sales Performance KPIs
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 1: Regional Sales Performance",
    """
    SELECT
        region,
        COUNT(*)                          AS total_units_sold,
        ROUND(SUM(sale_price), 2)         AS total_revenue,
        ROUND(AVG(sale_price), 2)         AS avg_sale_price,
        ROUND(MIN(sale_price), 2)         AS min_sale_price,
        ROUND(MAX(sale_price), 2)         AS max_sale_price
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC
    """,
    "kpi_regional_performance.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 2 — Monthly Revenue Trend (for time-series chart)
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 2: Monthly Revenue Trend",
    """
    SELECT
        month_label,
        sale_year,
        sale_month,
        COUNT(*)                          AS units_sold,
        ROUND(SUM(sale_price), 2)         AS monthly_revenue,
        ROUND(AVG(sale_price), 2)         AS avg_price
    FROM sales
    GROUP BY month_label, sale_year, sale_month
    ORDER BY sale_year, sale_month
    """,
    "kpi_monthly_trend.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 3 — Quarterly Revenue by Region
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 3: Quarterly Revenue by Region",
    """
    SELECT
        year_quarter,
        region,
        COUNT(*)                          AS units_sold,
        ROUND(SUM(sale_price), 2)         AS quarterly_revenue
    FROM sales
    GROUP BY year_quarter, region
    ORDER BY year_quarter, quarterly_revenue DESC
    """,
    "kpi_quarterly_by_region.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 4 — Model & Category Performance
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 4: Model & Category Performance",
    """
    SELECT
        category,
        model,
        COUNT(*)                          AS units_sold,
        ROUND(SUM(sale_price), 2)         AS total_revenue,
        ROUND(AVG(sale_price), 2)         AS avg_price
    FROM sales
    GROUP BY category, model
    ORDER BY total_revenue DESC
    """,
    "kpi_model_performance.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 5 — Top 10 Dealer Rankings
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 5: Top 10 Dealer Rankings",
    """
    SELECT
        dealer,
        region,
        COUNT(*)                          AS units_sold,
        ROUND(SUM(sale_price), 2)         AS total_revenue,
        ROUND(AVG(sale_price), 2)         AS avg_sale_price
    FROM sales
    GROUP BY dealer, region
    ORDER BY total_revenue DESC
    LIMIT 10
    """,
    "kpi_dealer_rankings.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 6 — Finance Type Distribution
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 6: Finance Type Distribution",
    """
    SELECT
        finance_type,
        COUNT(*)                                        AS count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_of_total,
        ROUND(SUM(sale_price), 2)                       AS total_revenue
    FROM sales
    GROUP BY finance_type
    ORDER BY count DESC
    """,
    "kpi_finance_distribution.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 7 — Year-over-Year Growth (2023 vs 2024)
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 7: Year-over-Year Growth (2023 vs 2024)",
    """
    WITH yearly AS (
        SELECT
            sale_year,
            COUNT(*)                  AS units_sold,
            ROUND(SUM(sale_price), 2) AS total_revenue
        FROM sales
        GROUP BY sale_year
    )
    SELECT
        a.sale_year,
        a.units_sold,
        a.total_revenue,
        ROUND((a.total_revenue - b.total_revenue) / b.total_revenue * 100, 2) AS yoy_revenue_growth_pct,
        ROUND((a.units_sold    - b.units_sold)    / CAST(b.units_sold AS REAL) * 100, 2) AS yoy_units_growth_pct
    FROM yearly a
    LEFT JOIN yearly b ON a.sale_year = b.sale_year + 1
    ORDER BY a.sale_year
    """,
    "kpi_yoy_growth.csv"
)

# ═════════════════════════════════════════════════════════════
# QUERY 8 — Revenue Tier Breakdown (for Tableau pie/bar)
# ═════════════════════════════════════════════════════════════
run_query(
    "QUERY 8: Revenue Tier Breakdown",
    """
    SELECT
        revenue_tier,
        COUNT(*)                                           AS units_sold,
        ROUND(SUM(sale_price), 2)                          AS total_revenue,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_of_units
    FROM sales
    GROUP BY revenue_tier
    ORDER BY revenue_tier
    """,
    "kpi_revenue_tiers.csv"
)

conn.close()
print("\n" + "=" * 60)
print("ALL SQL QUERIES COMPLETE")
print(f"8 KPI output files saved to /output/")
print("=" * 60)
