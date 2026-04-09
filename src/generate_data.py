"""
generate_data.py
Generates a realistic automotive sales dataset simulating a
premium car dealership network across Canadian regions.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# ── Configuration ─────────────────────────────────────────────
REGIONS = ["Ontario", "British Columbia", "Alberta", "Quebec", "Manitoba"]

DEALERS = {
    "Ontario":          ["Downtown Auto Group", "Northside Motors", "Lakeview Cars", "Oakville Premium"],
    "British Columbia":  ["Pacific Auto Centre", "Vancouver Motors", "Westcoast Dealership"],
    "Alberta":          ["Calgary Auto Hub", "Edmonton Premier Cars", "Rocky Mountain Motors"],
    "Quebec":           ["Montreal Auto Group", "Quebec City Motors", "Laval Premium Cars"],
    "Manitoba":         ["Winnipeg Auto Centre", "Prairie Motors"],
}

MODELS = {
    "Sedan":  ["3 Series", "5 Series", "7 Series"],
    "SUV":    ["X3", "X5", "X7"],
    "Coupe":  ["4 Series", "8 Series"],
    "EV":     ["i4", "iX", "i7"],
}

# Base prices per model
BASE_PRICES = {
    "3 Series": 52000, "5 Series": 68000, "7 Series": 115000,
    "X3": 58000,       "X5": 78000,       "X7": 102000,
    "4 Series": 62000, "8 Series": 125000,
    "i4": 72000,       "iX": 92000,       "i7": 135000,
}

SALE_TYPES    = ["New", "Certified Pre-Owned", "Pre-Owned"]
FINANCE_TYPES = ["Cash", "Finance", "Lease"]
STATUSES      = ["Completed", "Completed", "Completed", "Pending", "Cancelled"]

# ── Date range: 2 full years ──────────────────────────────────
start_date = datetime(2023, 1, 1)
end_date   = datetime(2024, 12, 31)
date_range = (end_date - start_date).days

# ── Generate rows ─────────────────────────────────────────────
rows = []
for i in range(1, 2001):
    region  = random.choice(REGIONS)
    dealer  = random.choice(DEALERS[region])
    cat     = random.choice(list(MODELS.keys()))
    model   = random.choice(MODELS[cat])

    base    = BASE_PRICES[model]
    # Seasonal uplift: Q4 slightly higher
    sale_dt = start_date + timedelta(days=random.randint(0, date_range))
    seasonal_factor = 1.05 if sale_dt.month in [10, 11, 12] else 1.0
    price   = round(base * seasonal_factor * np.random.uniform(0.92, 1.08), 2)

    # Introduce realistic messiness for cleaning step
    customer_name = random.choice([
        "JOHN SMITH", "jane doe", "Robert Johnson", "MARY WILLIAMS",
        "james BROWN", "Patricia Davis", "michael Wilson", "LINDA MOORE",
        "David Taylor", "barbara Anderson", "Richard Thomas", "Susan Jackson",
        "Joseph White", "JESSICA HARRIS", "Thomas Martin", "SARAH THOMPSON",
        "charles garcia", "Karen Martinez", "Daniel Robinson", "LISA CLARK",
    ])

    sale_type    = random.choice(SALE_TYPES)
    finance_type = random.choice(FINANCE_TYPES)
    status       = random.choice(STATUSES)

    # Inject some nulls and dirty values
    if random.random() < 0.04:
        price = None          # ~4% missing prices
    if random.random() < 0.02:
        status = "  completed "  # whitespace noise
    if random.random() < 0.01:
        finance_type = "FINANCE"  # case inconsistency

    rows.append({
        "sale_id":       f"SAL-{i:04d}",
        "sale_date":     sale_dt.strftime("%Y-%m-%d"),
        "region":        region,
        "dealer":        dealer,
        "customer_name": customer_name,
        "model":         model,
        "category":      cat,
        "sale_type":     sale_type,
        "finance_type":  finance_type,
        "sale_price":    price,
        "status":        status,
    })

df = pd.DataFrame(rows)
df.to_csv("data/raw_sales_data.csv", index=False)

print(f"Dataset generated: {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print(f"\nSample (first 5 rows):")
print(df.head())
print(f"\nNull counts:\n{df.isnull().sum()}")
print(f"\nStatus value counts (raw):\n{df['status'].value_counts()}")
