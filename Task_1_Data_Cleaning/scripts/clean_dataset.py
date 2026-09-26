from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw" / "online_retail_ii_raw.csv"
PROCESSED = BASE / "data" / "processed"
OUTPUTS = BASE / "outputs"
PROCESSED.mkdir(parents=True, exist_ok=True)
OUTPUTS.mkdir(parents=True, exist_ok=True)

if not RAW.exists():
    raise FileNotFoundError(
        f"Raw dataset not found: {RAW}\n"
        "Run download_dataset.py first."
    )

df = pd.read_csv(RAW)

# ---------- BEFORE-CLEANING QUALITY REPORT ----------
before = pd.DataFrame({
    "column": df.columns,
    "dtype": [str(x) for x in df.dtypes],
    "missing": df.isna().sum().values,
    "unique": df.nunique(dropna=True).values,
})
before["missing_pct"] = (before["missing"] / len(df) * 100).round(2)
before.to_csv(OUTPUTS / "data_quality_before.csv", index=False)

initial_rows = len(df)
initial_duplicates = int(df.duplicated().sum())

# ---------- STANDARDIZE STRUCTURE ----------
df.columns = (
    df.columns
      .str.strip()
      .str.replace(" ", "_")
      .str.replace(r"[^A-Za-z0-9_]", "", regex=True)
)

# Handle common Online Retail II naming variations.
rename_map = {
    "Invoice": "InvoiceNo",
    "StockCode": "StockCode",
    "Description": "Description",
    "Quantity": "Quantity",
    "InvoiceDate": "InvoiceDate",
    "Price": "Price",
    "Customer_ID": "CustomerID",
    "CustomerID": "CustomerID",
    "Country": "Country",
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# ---------- TEXT CLEANING ----------
for col in ["InvoiceNo", "StockCode", "Description", "CustomerID", "Country"]:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip()

# Blank descriptions become missing.
if "Description" in df.columns:
    df["Description"] = df["Description"].replace({"": pd.NA, "nan": pd.NA})

# ---------- DATA TYPES ----------
if "InvoiceDate" in df.columns:
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

for col in ["Quantity", "Price", "UnitPrice", "CustomerID"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------- DUPLICATES ----------
df = df.drop_duplicates().copy()

# ---------- BUSINESS VALIDATION ----------
# For this Task 1 sales-analysis dataset, retain positive sales transactions.
quantity_col = "Quantity"
price_col = "Price" if "Price" in df.columns else "UnitPrice"

if quantity_col in df.columns:
    df = df[df[quantity_col] > 0]

if price_col in df.columns:
    df = df[df[price_col] > 0]

# CustomerID is required for the downstream customer-analysis task.
if "CustomerID" in df.columns:
    df = df.dropna(subset=["CustomerID"])

# Remove records where essential transaction fields are missing.
required = [c for c in ["InvoiceNo", "StockCode", "InvoiceDate", "Quantity", price_col] if c in df.columns]
if required:
    df = df.dropna(subset=required)

# Convert CustomerID to nullable integer-like values after validation.
if "CustomerID" in df.columns:
    df["CustomerID"] = df["CustomerID"].astype("Int64")

# ---------- AFTER-CLEANING QUALITY REPORT ----------
after = pd.DataFrame({
    "column": df.columns,
    "dtype": [str(x) for x in df.dtypes],
    "missing": df.isna().sum().values,
    "unique": df.nunique(dropna=True).values,
})
after["missing_pct"] = (after["missing"] / len(df) * 100).round(2)
after.to_csv(OUTPUTS / "data_quality_after.csv", index=False)

# ---------- SAVE ----------
output = PROCESSED / "online_retail_ii_cleaned.csv"
df.to_csv(output, index=False)

print("TASK 1 CLEANING COMPLETE")
print(f"Initial rows:      {initial_rows:,}")
print(f"Initial duplicates:{initial_duplicates:,}")
print(f"Final rows:        {len(df):,}")
print(f"Rows removed:      {initial_rows - len(df):,}")
print(f"Remaining missing: {int(df.isna().sum().sum()):,}")
print(f"Final duplicates:  {int(df.duplicated().sum()):,}")
print(f"Cleaned file:      {output}")
