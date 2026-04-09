"""
01_data_cleaning.py
───────────────────────────────────────────────────────────────
Step 1 of the Automotive Sales Analytics Pipeline.

Reads raw_sales_data.csv, performs data quality checks,
cleans and standardises all fields, engineers KPI columns,
and writes a clean analysis-ready CSV to /output/.

Skills demonstrated:
  - Raw data ingestion & profiling
  - Null handling & imputation
  - String normalisation
  - Date parsing & feature engineering
  - KPI column derivation
  - Filtering invalid records
"""

import pandas as pd
import numpy as np
import os

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH  = os.path.join(BASE_DIR, "data",   "raw_sales_data.csv")
OUT_PATH  = os.path.join(BASE_DIR, "output", "cleaned_sales_data.csv")

# ═════════════════════════════════════════════════════════════
# 1. EXTRACT — Load raw data
# ═════════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 1: EXTRACT — Loading raw data")
print("=" * 60)

df = pd.read_csv(RAW_PATH)

print(f"  Rows loaded       : {len(df):,}")
print(f"  Columns           : {list(df.columns)}")
print(f"\n  Null value counts :")
print(df.isnull().sum().to_string())
print(f"\n  Raw 'status' distribution:")
print(df["status"].value_counts().to_string())
print(f"\n  Raw 'finance_type' distribution:")
print(df["finance_type"].value_counts().to_string())

# ═════════════════════════════════════════════════════════════
# 2. TRANSFORM — Clean & standardise
# ═════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 2: TRANSFORM — Cleaning & standardising")
print("=" * 60)

# ── 2a. Strip whitespace and title-case string fields ─────────
str_cols = ["status", "finance_type", "sale_type", "customer_name",
            "region", "dealer", "model", "category"]
for col in str_cols:
    df[col] = df[col].str.strip().str.title()

print("  [✓] Stripped whitespace & standardised casing on all string columns")

# ── 2b. Parse sale_date to datetime ───────────────────────────
df["sale_date"] = pd.to_datetime(df["sale_date"], format="%Y-%m-%d")
print("  [✓] Parsed sale_date to datetime")

# ── 2c. Handle missing sale_price ─────────────────────────────
null_price_count = df["sale_price"].isnull().sum()
median_price_by_model = df.groupby("model")["sale_price"].transform("median")
df["sale_price"] = df["sale_price"].fillna(median_price_by_model)
df["sale_price"] = df["sale_price"].round(2)
print(f"  [✓] Imputed {null_price_count} null sale_price values using per-model median")

# ── 2d. Filter out cancelled records for KPI analysis ─────────
before = len(df)
df_active = df[df["status"].isin(["Completed", "Pending"])].copy()
removed = before - len(df_active)
print(f"  [✓] Removed {removed} cancelled records — retained {len(df_active):,} active rows")

# ── 2e. Filter out pending for revenue KPIs (completed only) ──
df_completed = df_active[df_active["status"] == "Completed"].copy()
print(f"  [✓] Completed sales for revenue analysis: {len(df_completed):,} rows")

# ═════════════════════════════════════════════════════════════
# 3. FEATURE ENGINEERING — KPI columns
# ═════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 3: FEATURE ENGINEERING — Deriving KPI columns")
print("=" * 60)

df_completed["sale_year"]    = df_completed["sale_date"].dt.year
df_completed["sale_month"]   = df_completed["sale_date"].dt.month
df_completed["sale_quarter"] = df_completed["sale_date"].dt.quarter
df_completed["month_label"]  = df_completed["sale_date"].dt.to_period("M").astype(str)
df_completed["year_quarter"] = (
    df_completed["sale_year"].astype(str) + "-Q" +
    df_completed["sale_quarter"].astype(str)
)

# Revenue tier segmentation
df_completed["revenue_tier"] = pd.cut(
    df_completed["sale_price"],
    bins=[0, 60000, 90000, 120000, float("inf")],
    labels=["Entry (<60K)", "Mid (60–90K)", "Premium (90–120K)", "Ultra (>120K)"]
)

print("  [✓] Derived: sale_year, sale_month, sale_quarter, month_label, year_quarter")
print("  [✓] Derived: revenue_tier (4-band segmentation)")

# ═════════════════════════════════════════════════════════════
# 4. VALIDATION — Sanity checks
# ═════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 4: VALIDATION — Data quality checks")
print("=" * 60)

assert df_completed["sale_price"].isnull().sum() == 0, "Nulls remain in sale_price"
assert df_completed["sale_date"].isnull().sum()  == 0, "Nulls remain in sale_date"
assert set(df_completed["status"].unique()) == {"Completed"}, "Non-completed rows in KPI set"
assert df_completed["sale_price"].min() > 0, "Negative or zero prices found"

print(f"  [✓] No null prices")
print(f"  [✓] No null dates")
print(f"  [✓] All rows are Completed status")
print(f"  [✓] All prices are positive")
print(f"  [✓] Date range: {df_completed['sale_date'].min().date()} → {df_completed['sale_date'].max().date()}")

# ═════════════════════════════════════════════════════════════
# 5. LOAD — Write clean file
# ═════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 5: LOAD — Writing clean data to output/")
print("=" * 60)

df_completed.to_csv(OUT_PATH, index=False)
print(f"  [✓] Cleaned data written → {OUT_PATH}")
print(f"  [✓] Final row count     : {len(df_completed):,}")
print(f"  [✓] Final column count  : {len(df_completed.columns)}")

print("\n  Preview (first 3 rows):")
print(df_completed[["sale_id","sale_date","region","model","category",
                     "sale_price","finance_type","year_quarter","revenue_tier"]].head(3).to_string())

print("\n  Revenue tier distribution:")
print(df_completed["revenue_tier"].value_counts().sort_index().to_string())

print("\n[DATA CLEANING COMPLETE]")
