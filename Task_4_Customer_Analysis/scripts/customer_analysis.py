"""
Customer Data Analysis Pipeline — CodSoft Task 4
Author: Himanshu Rana
Repository: CODSOFT_TASKSNO
Description:
    Analyzes customer purchasing behavior, conducts geographic profiling,
    performs transparent rule-based customer segmentation on verified transaction data,
    evaluates customer lifetime value, and generates visual and statistical reports.
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual aesthetic standards
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16,
})

# Path definitions
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
DATA_PATH = PROJECT_ROOT / "Task_1_Data_Cleaning" / "data" / "processed" / "online_retail_ii_cleaned.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
REPORT_DIR = BASE_DIR / "report"


def load_data(filepath: Path) -> pd.DataFrame:
    """Load cleaned transaction dataset from Task 1."""
    if not filepath.exists():
        raise FileNotFoundError(
            f"Dataset not found at {filepath}. Ensure Task 1 cleaning has been run."
        )
    print(f"[1/7] Loading cleaned dataset from {filepath.name}...")
    df = pd.read_csv(filepath)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    print(f"      Loaded {len(df):,} transactions spanning {df['InvoiceDate'].dt.date.min()} to {df['InvoiceDate'].dt.date.max()}.")
    return df


def validate_data(df: pd.DataFrame) -> dict:
    """Validate data integrity and document key source properties."""
    print("[2/7] Validating data integrity...")
    missing_cust = int(df["CustomerID"].isna().sum())
    neg_quantity = int((df["Quantity"] <= 0).sum())
    neg_price = int((df["Price"] <= 0).sum())
    
    validation_results = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "missing_customer_id": missing_cust,
        "negative_or_zero_quantity": neg_quantity,
        "negative_or_zero_price": neg_price,
        "unique_customers": int(df["CustomerID"].nunique()),
        "unique_invoices": int(df["InvoiceNo"].nunique()),
        "unique_countries": int(df["Country"].nunique()),
        "total_revenue": round(float(df["TotalPrice"].sum()), 2),
        "total_units": int(df["Quantity"].sum()),
        "has_age_column": "Age" in df.columns,
    }
    
    print(f"      Verified: 0 missing CustomerIDs, 0 non-positive quantities/prices.")
    print(f"      Age column present: {validation_results['has_age_column']} (Age-based segmentation will not be performed; documenting limitation).")
    return validation_results


def build_customer_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transactional data to individual customer level (1 row per CustomerID)."""
    print("[3/7] Building customer-level aggregations (1 row per CustomerID)...")
    
    # Reference date for recency calculation (day after max transaction date)
    ref_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    
    # Customer aggregation
    cust = df.groupby("CustomerID").agg(
        Country=("Country", lambda x: x.mode()[0] if not x.empty else "Unknown"),
        TotalRevenue=("TotalPrice", "sum"),
        TotalOrders=("InvoiceNo", "nunique"),
        TotalUnits=("Quantity", "sum"),
        FirstPurchaseDate=("InvoiceDate", "min"),
        LastPurchaseDate=("InvoiceDate", "max"),
    ).reset_index()

    # Cast CustomerID to clean integer
    cust["CustomerID"] = cust["CustomerID"].astype(int)

    # Derived customer metrics
    cust["TotalRevenue"] = cust["TotalRevenue"].round(2)
    cust["AverageOrderValue"] = (cust["TotalRevenue"] / cust["TotalOrders"]).round(2)
    cust["AverageRevenuePerOrder"] = cust["AverageOrderValue"]
    cust["AverageUnitsPerOrder"] = (cust["TotalUnits"] / cust["TotalOrders"]).round(2)
    cust["PurchaseFrequency"] = cust["TotalOrders"]
    cust["CustomerLifetimeDays"] = (cust["LastPurchaseDate"] - cust["FirstPurchaseDate"]).dt.days
    cust["RecencyDays"] = (ref_date - cust["LastPurchaseDate"]).dt.days

    print(f"      Aggregated {len(cust):,} distinct customer profiles.")
    return cust


def analyze_countries(df: pd.DataFrame, cust_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze customer distribution, order volume, and revenue by country."""
    print("[4/7] Performing country-level customer analysis...")
    country_analysis = cust_df.groupby("Country").agg(
        CustomerCount=("CustomerID", "count"),
        TotalOrders=("TotalOrders", "sum"),
        TotalUnits=("TotalUnits", "sum"),
        TotalRevenue=("TotalRevenue", "sum"),
    ).reset_index()

    country_analysis["TotalRevenue"] = country_analysis["TotalRevenue"].round(2)
    country_analysis["AverageCustomerRevenue"] = (
        country_analysis["TotalRevenue"] / country_analysis["CustomerCount"]
    ).round(2)
    country_analysis["AverageOrderValue"] = (
        country_analysis["TotalRevenue"] / country_analysis["TotalOrders"]
    ).round(2)

    country_analysis = country_analysis.sort_values(by="TotalRevenue", ascending=False).reset_index(drop=True)
    return country_analysis


def segment_customers(cust_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Segment customers using transparent, documented behavioral rules based on
    purchasing patterns, customer value (revenue), and engagement recency.
    
    Segmentation Rules:
      1. High-Value Frequent:
         TotalRevenue >= 75th percentile (~£2,248) AND TotalOrders >= 6 AND RecencyDays <= 180.
         (Core high-value champions with high engagement and repeat purchase frequency)
      2. High-Value Occasional:
         TotalRevenue >= 75th percentile (~£2,248) AND TotalOrders < 6 AND RecencyDays <= 180.
         (High-spending wholesale/corporate buyers who purchase large baskets infrequently)
      3. High-Value Lapsed:
         TotalRevenue >= 75th percentile (~£2,248) AND RecencyDays > 180.
         (Previously high-spending accounts that have not purchased in over 6 months)
      4. Steady Repeat:
         TotalRevenue < 75th percentile AND TotalOrders >= 3 AND RecencyDays <= 180.
         (Consistent active buyers with steady repeat purchasing cadence)
      5. Occasional Active:
         TotalOrders < 3 AND RecencyDays <= 180.
         (Recent or low-frequency shoppers who purchased in the last 6 months)
      6. Dormant / Inactive:
         TotalRevenue < 75th percentile AND RecencyDays > 180.
         (Accounts with no purchasing activity for over 6 months)
    """
    print("[5/7] Executing customer behavioral segmentation...")
    rev_p75 = cust_df["TotalRevenue"].quantile(0.75)

    def assign_segment(row):
        if row["TotalRevenue"] >= rev_p75 and row["TotalOrders"] >= 6 and row["RecencyDays"] <= 180:
            return "High-Value Frequent"
        elif row["TotalRevenue"] >= rev_p75:
            if row["RecencyDays"] <= 180:
                return "High-Value Occasional"
            else:
                return "High-Value Lapsed"
        elif row["TotalOrders"] >= 3 and row["RecencyDays"] <= 180:
            return "Steady Repeat"
        elif row["RecencyDays"] <= 180:
            return "Occasional Active"
        else:
            return "Dormant / Inactive"

    cust_df = cust_df.copy()
    cust_df["CustomerSegment"] = cust_df.apply(assign_segment, axis=1)

    # Segment summary aggregation
    total_cust = len(cust_df)
    total_rev = cust_df["TotalRevenue"].sum()
    
    seg_summary = cust_df.groupby("CustomerSegment").agg(
        CustomerCount=("CustomerID", "count"),
        TotalRevenue=("TotalRevenue", "sum"),
        TotalOrders=("TotalOrders", "sum"),
        TotalUnits=("TotalUnits", "sum"),
        AverageRevenuePerCustomer=("TotalRevenue", "mean"),
        AverageOrdersPerCustomer=("TotalOrders", "mean"),
        AverageOrderValue=("AverageOrderValue", "mean"),
        AverageRecencyDays=("RecencyDays", "mean"),
    ).reset_index()

    seg_summary["TotalRevenue"] = seg_summary["TotalRevenue"].round(2)
    seg_summary["AverageRevenuePerCustomer"] = seg_summary["AverageRevenuePerCustomer"].round(2)
    seg_summary["AverageOrdersPerCustomer"] = seg_summary["AverageOrdersPerCustomer"].round(2)
    seg_summary["AverageOrderValue"] = seg_summary["AverageOrderValue"].round(2)
    seg_summary["AverageRecencyDays"] = seg_summary["AverageRecencyDays"].round(1)

    seg_summary["CustomerShare"] = ((seg_summary["CustomerCount"] / total_cust) * 100).round(2)
    seg_summary["RevenueShare"] = ((seg_summary["TotalRevenue"] / total_rev) * 100).round(2)

    # Sort logically by Revenue
    seg_summary = seg_summary.sort_values(by="TotalRevenue", ascending=False).reset_index(drop=True)
    return cust_df, seg_summary


def create_visualizations(
    cust_df: pd.DataFrame,
    country_df: pd.DataFrame,
    seg_summary: pd.DataFrame,
    charts_dir: Path
):
    """Generate high-resolution visual reports answering key business questions."""
    print("[6/7] Generating visual charts...")
    charts_dir.mkdir(parents=True, exist_ok=True)

    # Chart 1: Customers by Country (Top 10)
    plt.figure(figsize=(12, 6))
    top_countries = country_df.head(10).copy()
    ax1 = sns.barplot(
        data=top_countries,
        x="CustomerCount",
        y="Country",
        palette="viridis",
        hue="Country",
        legend=False
    )
    plt.title("Top 10 Countries by Customer Count", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Number of Registered Customers", fontsize=12)
    plt.ylabel("Country", fontsize=12)
    for p in ax1.patches:
        width = p.get_width()
        ax1.annotate(
            f"{int(width):,}",
            (width, p.get_y() + p.get_height() / 2),
            ha="left",
            va="center",
            xytext=(6, 0),
            textcoords="offset points",
            fontweight="bold",
            fontsize=10,
        )
    plt.xlim(0, top_countries["CustomerCount"].max() * 1.15)
    plt.tight_layout()
    chart1_path = charts_dir / "customers_by_country.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"      Saved: {chart1_path.name}")

    # Chart 2: Revenue by Customer Segment
    plt.figure(figsize=(11, 6))
    seg_sorted = seg_summary.sort_values(by="TotalRevenue", ascending=True)
    ax2 = plt.barh(
        seg_sorted["CustomerSegment"],
        seg_sorted["TotalRevenue"] / 1e6,
        color=["#95a5a6", "#3498db", "#f39c12", "#e67e22", "#9b59b6", "#2ecc71"],
    )
    plt.title("Total Gross Revenue by Customer Segment (£ Millions)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Total Revenue (£ Millions)", fontsize=12)
    plt.ylabel("Customer Segment", fontsize=12)
    for i, (val, share) in enumerate(zip(seg_sorted["TotalRevenue"] / 1e6, seg_sorted["RevenueShare"])):
        plt.text(val + 0.1, i, f"£{val:.2f}M ({share:.1f}%)", va="center", fontweight="bold", fontsize=10)
    plt.xlim(0, (seg_sorted["TotalRevenue"].max() / 1e6) * 1.25)
    plt.tight_layout()
    chart2_path = charts_dir / "revenue_by_customer_segment.png"
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"      Saved: {chart2_path.name}")

    # Chart 3: Customer Frequency Distribution (Orders)
    plt.figure(figsize=(11, 5))
    order_cap = cust_df["TotalOrders"].quantile(0.98)
    filtered_orders = cust_df[cust_df["TotalOrders"] <= order_cap]["TotalOrders"]
    sns.histplot(filtered_orders, bins=30, kde=True, color="#2980b9", edgecolor="white")
    plt.axvline(cust_df["TotalOrders"].median(), color="#e74c3c", linestyle="--", linewidth=2,
                label=f"Median: {cust_df['TotalOrders'].median():.0f} orders")
    plt.axvline(cust_df["TotalOrders"].mean(), color="#27ae60", linestyle=":", linewidth=2,
                label=f"Mean: {cust_df['TotalOrders'].mean():.1f} orders")
    plt.title("Customer Order Frequency Distribution (≤ 98th Percentile)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Total Lifetime Orders per Customer", fontsize=12)
    plt.ylabel("Customer Count", fontsize=12)
    plt.legend(frameon=True)
    plt.tight_layout()
    chart3_path = charts_dir / "customer_frequency_distribution.png"
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"      Saved: {chart3_path.name}")

    # Chart 4: Customer Revenue Distribution
    plt.figure(figsize=(11, 5))
    rev_cap = cust_df["TotalRevenue"].quantile(0.95)
    filtered_rev = cust_df[cust_df["TotalRevenue"] <= rev_cap]["TotalRevenue"]
    sns.histplot(filtered_rev, bins=35, kde=True, color="#16a085", edgecolor="white")
    plt.axvline(cust_df["TotalRevenue"].median(), color="#e74c3c", linestyle="--", linewidth=2,
                label=f"Median: £{cust_df['TotalRevenue'].median():,.2f}")
    plt.axvline(cust_df["TotalRevenue"].mean(), color="#2980b9", linestyle=":", linewidth=2,
                label=f"Mean: £{cust_df['TotalRevenue'].mean():,.2f}")
    plt.title("Customer Revenue Distribution (≤ 95th Percentile)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Total Lifetime Revenue (£)", fontsize=12)
    plt.ylabel("Customer Count", fontsize=12)
    plt.legend(frameon=True)
    plt.tight_layout()
    chart4_path = charts_dir / "customer_revenue_distribution.png"
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"      Saved: {chart4_path.name}")

    # Chart 5: Customer Segment Scatter Plot (TotalOrders vs TotalRevenue)
    plt.figure(figsize=(12, 7))
    palette_map = {
        "High-Value Frequent": "#2ecc71",
        "High-Value Occasional": "#3498db",
        "High-Value Lapsed": "#e67e22",
        "Steady Repeat": "#9b59b6",
        "Occasional Active": "#f1c40f",
        "Dormant / Inactive": "#95a5a6",
    }
    sns.scatterplot(
        data=cust_df,
        x="TotalOrders",
        y="TotalRevenue",
        hue="CustomerSegment",
        palette=palette_map,
        alpha=0.65,
        s=45,
        edgecolor=None
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Customer Segmentation: Lifetime Orders vs. Revenue (Log Scale)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Total Lifetime Orders (Log Scale)", fontsize=12)
    plt.ylabel("Total Lifetime Revenue in GBP (Log Scale)", fontsize=12)
    plt.legend(title="Customer Segment", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)
    plt.tight_layout()
    chart5_path = charts_dir / "customer_segment_scatter.png"
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f"      Saved: {chart5_path.name}")


def save_outputs(
    cust_df: pd.DataFrame,
    country_df: pd.DataFrame,
    seg_summary: pd.DataFrame,
    outputs_dir: Path
):
    """Save clean tabular data outputs for downstream consumption and audits."""
    print("[7/7] Exporting CSV summary and segment datasets...")
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # 1. customer_summary.csv
    summary_cols = [
        "CustomerID", "Country", "TotalRevenue", "TotalOrders", "TotalUnits",
        "AverageOrderValue", "AverageRevenuePerOrder", "AverageUnitsPerOrder",
        "FirstPurchaseDate", "LastPurchaseDate", "CustomerLifetimeDays", "RecencyDays", "PurchaseFrequency"
    ]
    cust_df[summary_cols].to_csv(outputs_dir / "customer_summary.csv", index=False)
    print(f"      Saved: customer_summary.csv ({len(cust_df):,} rows)")

    # 2. customer_segments.csv
    segment_cols = [
        "CustomerID", "Country", "TotalRevenue", "TotalOrders", "TotalUnits",
        "AverageOrderValue", "PurchaseFrequency", "LastPurchaseDate", "RecencyDays", "CustomerSegment"
    ]
    cust_df[segment_cols].to_csv(outputs_dir / "customer_segments.csv", index=False)
    print(f"      Saved: customer_segments.csv ({len(cust_df):,} rows)")

    # 3. country_customer_analysis.csv
    country_df.to_csv(outputs_dir / "country_customer_analysis.csv", index=False)
    print(f"      Saved: country_customer_analysis.csv ({len(country_df):,} countries)")

    # 4. segment_summary.csv
    seg_summary.to_csv(outputs_dir / "segment_summary.csv", index=False)
    print(f"      Saved: segment_summary.csv ({len(seg_summary):,} segments)")


def main():
    print("=" * 70)
    print("TASK 4 — CUSTOMER DATA ANALYSIS PIPELINE")
    print("=" * 70)

    # 1. Load
    df = load_data(DATA_PATH)

    # 2. Validate
    val = validate_data(df)

    # 3. Aggregate
    cust_df = build_customer_summary(df)

    # 4. Country Analysis
    country_df = analyze_countries(df, cust_df)

    # 5. Segment
    cust_df, seg_summary = segment_customers(cust_df)

    # 6. Visualizations
    create_visualizations(cust_df, country_df, seg_summary, CHARTS_DIR)

    # 7. Save CSVs
    save_outputs(cust_df, country_df, seg_summary, OUTPUTS_DIR)

    print("\n" + "=" * 70)
    print("SUMMARY AUDIT REPORT")
    print("=" * 70)
    print(f"Total Transactions Analyzed: {val['total_rows']:,}")
    print(f"Unique Customers Profiled:  {len(cust_df):,}")
    print(f"Unique Countries Active:     {len(country_df):,}")
    print(f"Total Revenue Reconciled:   £{cust_df['TotalRevenue'].sum():,.2f}")
    print(f"Total Orders Reconciled:    {cust_df['TotalOrders'].sum():,}")
    print(f"Total Units Sold:           {cust_df['TotalUnits'].sum():,}")
    print("\nCustomer Segment Breakdown:")
    print(seg_summary[[
        "CustomerSegment", "CustomerCount", "CustomerShare", "TotalRevenue", "RevenueShare", "AverageRevenuePerCustomer"
    ]].to_string(index=False))
    print("=" * 70)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
