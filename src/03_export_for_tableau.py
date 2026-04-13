"""
03_export_for_tableau.py
────────────────────────────────────────────────────────────
Combines all KPI outputs into a single Tableau-ready CSV.
One data source = one extract = no publishing errors.
"""

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR  = os.path.join(BASE_DIR, "output")

# ── Load all KPI files ────────────────────────────────────────
regional  = pd.read_csv(os.path.join(OUT_DIR, "kpi_regional_performance.csv"))
monthly   = pd.read_csv(os.path.join(OUT_DIR, "kpi_monthly_trend.csv"))
model     = pd.read_csv(os.path.join(OUT_DIR, "kpi_model_performance.csv"))
tiers     = pd.read_csv(os.path.join(OUT_DIR, "kpi_revenue_tiers.csv"))
yoy       = pd.read_csv(os.path.join(OUT_DIR, "kpi_yoy_growth.csv"))
dealer    = pd.read_csv(os.path.join(OUT_DIR, "kpi_dealer_rankings.csv"))

# ── Tag each with a source label ─────────────────────────────
regional["data_type"] = "Regional Performance"
monthly["data_type"]  = "Monthly Trend"
model["data_type"]    = "Model Performance"
tiers["data_type"]    = "Revenue Tiers"
yoy["data_type"]      = "YoY Growth"
dealer["data_type"]   = "Dealer Rankings"

# ── Combine into one master CSV ───────────────────────────────
combined = pd.concat([regional, monthly, model, tiers, yoy, dealer],
                     ignore_index=True)

out_path = os.path.join(OUT_DIR, "tableau_master.csv")
combined.to_csv(out_path, index=False)

print(f"[✓] Master Tableau CSV created → {out_path}")
print(f"[✓] Total rows: {len(combined)}")
print(f"[✓] Columns: {list(combined.columns)}")