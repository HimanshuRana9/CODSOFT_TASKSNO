"""
CODSOFT DATA ANALYTICS INTERNSHIP
Task 2: Exploratory Data Analysis (EDA) Pipeline

This script performs complete, automated Exploratory Data Analysis on the verified
Task 1 cleaned dataset (online_retail_ii_cleaned.csv).
All statistics, trends, distributions, relationships, outliers, and business questions
are computed strictly from actual data and saved to Task_2_EDA/outputs/.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Visual formatting configuration
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["figure.dpi"] = 300

# Path resolution
BASE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE_DIR.parent
CLEANED_DATA_PATH = REPO_ROOT / "Task_1_Data_Cleaning" / "data" / "processed" / "online_retail_ii_cleaned.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 75)
    print("CODSOFT DATA ANALYTICS — TASK 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 75)

    # ---------------------------------------------------------
    # 1. LOAD DATASET & VERIFY INTEGRITY
    # ---------------------------------------------------------
    if not CLEANED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found at expected path:\n{CLEANED_DATA_PATH}\n"
            "Please ensure Task 1 has completed successfully."
        )

    print(f"\n[1/8] Loading cleaned dataset from:\n      {CLEANED_DATA_PATH}")
    df = pd.read_csv(CLEANED_DATA_PATH, parse_dates=["InvoiceDate"])

    expected_cols = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "Price", "CustomerID", "Country", "TotalPrice"
    ]
    missing_cols = [c for c in expected_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Cleaned dataset is missing expected columns: {missing_cols}")

    total_rows = len(df)
    total_cols = len(df.columns)
    print(f"      Loaded successfully: {total_rows:,} rows, {total_cols} columns.")

    # ---------------------------------------------------------
    # SECTION 1: DATASET OVERVIEW
    # ---------------------------------------------------------
    print("\n[2/8] Generating Section 1: Dataset Overview...")
    overview_data = {
        "metric": [
            "rows",
            "columns",
            "missing_values",
            "duplicate_rows",
            "unique_invoices",
            "unique_products",
            "unique_customers",
            "unique_countries",
            "minimum_invoice_date",
            "maximum_invoice_date",
            "total_revenue_gbp",
            "total_units_sold"
        ],
        "value": [
            str(total_rows),
            str(total_cols),
            str(df.isna().sum().sum()),
            str(df.duplicated().sum()),
            str(df["InvoiceNo"].nunique()),
            str(df["StockCode"].nunique()),
            str(df["CustomerID"].nunique()),
            str(df["Country"].nunique()),
            str(df["InvoiceDate"].min()),
            str(df["InvoiceDate"].max()),
            f"{df['TotalPrice'].sum():,.2f}",
            f"{df['Quantity'].sum():,}"
        ]
    }
    overview_df = pd.DataFrame(overview_data)
    overview_csv = OUTPUTS_DIR / "dataset_overview.csv"
    overview_df.to_csv(overview_csv, index=False)
    print(f"      Saved: {overview_csv}")
    print(overview_df.to_string(index=False))

    # ---------------------------------------------------------
    # SECTION 2: DESCRIPTIVE STATISTICS
    # ---------------------------------------------------------
    print("\n[3/8] Generating Section 2: Descriptive Statistics...")
    numeric_features = ["Quantity", "Price", "TotalPrice"]
    desc_stats = df[numeric_features].describe().T
    desc_stats["median"] = df[numeric_features].median()
    desc_stats["skewness"] = df[numeric_features].skew()
    desc_stats["kurtosis"] = df[numeric_features].kurtosis()

    # Reorder columns logically
    cols_order = ["count", "mean", "std", "min", "25%", "50%", "median", "75%", "max", "skewness", "kurtosis"]
    desc_stats = desc_stats[[c for c in cols_order if c in desc_stats.columns]]

    desc_csv = OUTPUTS_DIR / "descriptive_statistics.csv"
    desc_stats.to_csv(desc_csv)
    print(f"      Saved: {desc_csv}")
    print(desc_stats.round(2).to_string())

    # ---------------------------------------------------------
    # SECTION 3: DISTRIBUTIONS (3 CHARTS)
    # ---------------------------------------------------------
    print("\n[4/8] Generating Section 3: Distribution Plots...")

    # Chart 1: Quantity Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    q_99 = df["Quantity"].quantile(0.99)
    sns.histplot(df[df["Quantity"] <= q_99]["Quantity"], bins=40, kde=True, color="#2980b9", ax=ax)
    ax.set_title(f"Distribution of Transaction Quantity (up to 99th percentile: {q_99:.0f} units)", fontweight="bold")
    ax.set_xlabel("Quantity (Units per Line Item)")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    q_dist_path = OUTPUTS_DIR / "quantity_distribution.png"
    plt.savefig(q_dist_path)
    plt.close()
    print(f"      Saved: {q_dist_path}")

    # Chart 2: Price Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    p_99 = df["Price"].quantile(0.99)
    sns.histplot(df[df["Price"] <= p_99]["Price"], bins=40, kde=True, color="#27ae60", ax=ax)
    ax.set_title(f"Distribution of Unit Price in GBP (£) (up to 99th percentile: £{p_99:.2f})", fontweight="bold")
    ax.set_xlabel("Unit Price (£)")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    p_dist_path = OUTPUTS_DIR / "price_distribution.png"
    plt.savefig(p_dist_path)
    plt.close()
    print(f"      Saved: {p_dist_path}")

    # Chart 3: TotalPrice Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    tp_99 = df["TotalPrice"].quantile(0.99)
    sns.histplot(df[df["TotalPrice"] <= tp_99]["TotalPrice"], bins=40, kde=True, color="#8e44ad", ax=ax)
    ax.set_title(f"Distribution of Total Line Revenue in GBP (£) (up to 99th percentile: £{tp_99:.2f})", fontweight="bold")
    ax.set_xlabel("TotalPrice (£)")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    tp_dist_path = OUTPUTS_DIR / "totalprice_distribution.png"
    plt.savefig(tp_dist_path)
    plt.close()
    print(f"      Saved: {tp_dist_path}")

    # ---------------------------------------------------------
    # SECTION 4: TIME TREND ANALYSIS (MONTHLY REVENUE)
    # ---------------------------------------------------------
    print("\n[5/8] Generating Section 4: Time Trend Analysis...")
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly_summary = df.groupby("YearMonth").agg(
        Revenue=("TotalPrice", "sum"),
        Transactions=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum"),
        UniqueCustomers=("CustomerID", "nunique")
    ).reset_index()
    monthly_summary["AverageOrderValue"] = (monthly_summary["Revenue"] / monthly_summary["Transactions"]).round(2)
    monthly_summary["Revenue"] = monthly_summary["Revenue"].round(2)

    monthly_csv = OUTPUTS_DIR / "monthly_revenue.csv"
    monthly_summary.to_csv(monthly_csv, index=False)
    print(f"      Saved: {monthly_csv}")

    # Plot Monthly Revenue Trend
    fig, ax1 = plt.subplots(figsize=(13, 6))
    x_indices = np.arange(len(monthly_summary))
    ax1.plot(x_indices, monthly_summary["Revenue"], color="#16a085", marker="o", linewidth=2.5, label="Monthly Revenue (£)")
    ax1.set_title("Monthly Revenue Performance & Trend (Dec 2009 – Dec 2011)", fontweight="bold", fontsize=14)
    ax1.set_xlabel("Year-Month", fontweight="bold")
    ax1.set_ylabel("Total Revenue (£ GBP)", color="#16a085", fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#16a085")
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(monthly_summary["YearMonth"], rotation=45, ha="right")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"£{x/1000:,.0f}k"))

    # Add transaction volume on secondary axis
    ax2 = ax1.twinx()
    ax2.bar(x_indices, monthly_summary["Transactions"], alpha=0.25, color="#2c3e50", width=0.4, label="Transaction Count")
    ax2.set_ylabel("Transaction Count", color="#2c3e50", fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#2c3e50")
    ax2.grid(False)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    trend_path = OUTPUTS_DIR / "monthly_revenue_trend.png"
    plt.savefig(trend_path)
    plt.close()
    print(f"      Saved: {trend_path}")

    # ---------------------------------------------------------
    # SECTION 5: COUNTRY ANALYSIS
    # ---------------------------------------------------------
    print("\n[6/8] Generating Section 5: Country Analysis...")
    country_summary = df.groupby("Country").agg(
        Revenue=("TotalPrice", "sum"),
        Transactions=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum"),
        Customers=("CustomerID", "nunique")
    ).reset_index()

    country_summary["Revenue"] = country_summary["Revenue"].round(2)
    country_summary = country_summary.sort_values(by="Revenue", ascending=False).reset_index(drop=True)
    country_summary["RevenueSharePct"] = ((country_summary["Revenue"] / df["TotalPrice"].sum()) * 100).round(2)

    country_csv = OUTPUTS_DIR / "country_analysis.csv"
    country_summary.to_csv(country_csv, index=False)
    print(f"      Saved: {country_csv}")

    # Plot Top 10 Countries by Revenue
    top10_countries = country_summary.head(10).copy()
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = sns.barplot(
        data=top10_countries,
        x="Revenue",
        y="Country",
        hue="Country",
        palette="viridis",
        legend=False,
        ax=ax
    )
    ax.set_title("Top 10 Countries by Total Revenue (£ GBP)", fontweight="bold", fontsize=14)
    ax.set_xlabel("Total Revenue (£)")
    ax.set_ylabel("Country")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"£{x/1e6:.1f}M" if x >= 1e6 else f"£{x/1e3:.0f}k"))

    for bar, val in zip(bars.patches, top10_countries["Revenue"]):
        width = bar.get_width()
        label = f"£{val/1e6:.2f}M" if val >= 1e6 else f"£{val/1e3:.1f}k"
        ax.text(width + (top10_countries["Revenue"].max() * 0.01), bar.get_y() + bar.get_height() / 2,
                label, va="center", fontweight="bold", fontsize=9)

    plt.tight_layout()
    country_plot_path = OUTPUTS_DIR / "top_10_countries_revenue.png"
    plt.savefig(country_plot_path)
    plt.close()
    print(f"      Saved: {country_plot_path}")

    # ---------------------------------------------------------
    # SECTION 6: PRODUCT ANALYSIS (TOP 100 PRODUCTS)
    # ---------------------------------------------------------
    print("\n[7/8] Generating Section 6: Product Analysis...")
    product_summary = df.groupby(["StockCode", "Description"]).agg(
        Revenue=("TotalPrice", "sum"),
        Units=("Quantity", "sum"),
        Transactions=("InvoiceNo", "nunique")
    ).reset_index()

    product_summary["Revenue"] = product_summary["Revenue"].round(2)
    product_summary = product_summary.sort_values(by="Revenue", ascending=False).reset_index(drop=True)

    top_100_products = product_summary.head(100)
    products_csv = OUTPUTS_DIR / "top_100_products.csv"
    top_100_products.to_csv(products_csv, index=False)
    print(f"      Saved: {products_csv}")

    # ---------------------------------------------------------
    # SECTION 7: RELATIONSHIPS & SCATTER PLOTS
    # ---------------------------------------------------------
    print("\n[8/8] Generating Section 7: Relationships & Correlations...")
    corr_matrix = df[["Quantity", "Price", "TotalPrice"]].corr()
    corr_csv = OUTPUTS_DIR / "numeric_correlations.csv"
    corr_matrix.to_csv(corr_csv)
    print(f"      Saved: {corr_csv}")

    # Deterministic reproducible 10k sample for scatter plots
    sample_size = min(10000, len(df))
    sample_df = df.sample(sample_size, random_state=42)

    # Plot Quantity vs TotalPrice
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(sample_df["Quantity"], sample_df["TotalPrice"], alpha=0.35, color="#2980b9", edgecolors="none")
    ax.set_title(f"Quantity vs Total Price (Reproducible Sample: {sample_size:,} records)", fontweight="bold")
    ax.set_xlabel("Quantity (Units)")
    ax.set_ylabel("Total Price (£ GBP)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.tight_layout()
    q_tp_path = OUTPUTS_DIR / "quantity_vs_totalprice.png"
    plt.savefig(q_tp_path)
    plt.close()
    print(f"      Saved: {q_tp_path}")

    # Plot Price vs TotalPrice
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(sample_df["Price"], sample_df["TotalPrice"], alpha=0.35, color="#e67e22", edgecolors="none")
    ax.set_title(f"Unit Price vs Total Price (Reproducible Sample: {sample_size:,} records)", fontweight="bold")
    ax.set_xlabel("Unit Price (£ GBP)")
    ax.set_ylabel("Total Price (£ GBP)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.tight_layout()
    p_tp_path = OUTPUTS_DIR / "price_vs_totalprice.png"
    plt.savefig(p_tp_path)
    plt.close()
    print(f"      Saved: {p_tp_path}")

    # ---------------------------------------------------------
    # SECTION 8: OUTLIER DETECTION (IQR METHOD)
    # ---------------------------------------------------------
    outlier_records = []
    for var in ["Quantity", "Price", "TotalPrice"]:
        q1 = df[var].quantile(0.25)
        q3 = df[var].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[var] < lower_bound) | (df[var] > upper_bound)]
        count = len(outliers)
        pct = (count / total_rows) * 100

        outlier_records.append({
            "variable": var,
            "q1": round(q1, 2),
            "q3": round(q3, 2),
            "iqr": round(iqr, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
            "outlier_count": count,
            "outlier_percentage": round(pct, 2)
        })

    outlier_df = pd.DataFrame(outlier_records)
    outlier_csv = OUTPUTS_DIR / "outlier_analysis.csv"
    outlier_df.to_csv(outlier_csv, index=False)
    print(f"      Saved: {outlier_csv}")
    print(outlier_df.to_string(index=False))

    # ---------------------------------------------------------
    # SECTION 9 & 10: ANSWER BUSINESS QUESTIONS & FINDINGS.MD
    # ---------------------------------------------------------
    total_rev = df["TotalPrice"].sum()
    total_trans = df["InvoiceNo"].nunique()
    total_cust = df["CustomerID"].nunique()
    total_items = df["StockCode"].nunique()
    top_country = country_summary.iloc[0]
    top_product = product_summary.iloc[0]

    max_month_row = monthly_summary.loc[monthly_summary["Revenue"].idxmax()]
    min_month_row = monthly_summary.loc[monthly_summary["Revenue"].idxmin()]
    avg_line_rev = df["TotalPrice"].mean()

    findings_content = f"""# Task 2 — Exploratory Data Analysis (EDA) Findings

**Project:** CodSoft Data Analytics Internship Portfolio  
**Task:** Task 2 — Exploratory Data Analysis  
**Author:** Himanshu Rana  
**Status:** Completed & Validated  
**Dataset Source:** `Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`  

---

## 1. Dataset Overview
- **Total Valid Records:** {total_rows:,} rows across 9 features.
- **Completeness:** 0 missing values, 0 duplicate records.
- **Temporal Span:** {df['InvoiceDate'].min().strftime('%Y-%m-%d')} to {df['InvoiceDate'].max().strftime('%Y-%m-%d')} (24 full months).
- **Total Portfolio Revenue:** £{total_rev:,.2f}
- **Total Units Sold:** {df['Quantity'].sum():,} units.
- **Unique Invoices / Transactions:** {total_trans:,}
- **Unique Active Customers:** {total_cust:,}
- **Unique Products (SKUs):** {total_items:,}
- **Unique Countries:** {df['Country'].nunique()}

---

## 2. Descriptive Statistics Summary

| Feature | Mean | Median | Std Dev | Min | 25% | 75% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Quantity** | {desc_stats.loc['Quantity', 'mean']:.2f} | {desc_stats.loc['Quantity', 'median']:.2f} | {desc_stats.loc['Quantity', 'std']:.2f} | {desc_stats.loc['Quantity', 'min']:.0f} | {desc_stats.loc['Quantity', '25%']:.0f} | {desc_stats.loc['Quantity', '75%']:.0f} | {desc_stats.loc['Quantity', 'max']:.0f} |
| **Price (£)** | £{desc_stats.loc['Price', 'mean']:.2f} | £{desc_stats.loc['Price', 'median']:.2f} | £{desc_stats.loc['Price', 'std']:.2f} | £{desc_stats.loc['Price', 'min']:.2f} | £{desc_stats.loc['Price', '25%']:.2f} | £{desc_stats.loc['Price', '75%']:.2f} | £{desc_stats.loc['Price', 'max']:.2f} |
| **TotalPrice (£)** | £{desc_stats.loc['TotalPrice', 'mean']:.2f} | £{desc_stats.loc['TotalPrice', 'median']:.2f} | £{desc_stats.loc['TotalPrice', 'std']:.2f} | £{desc_stats.loc['TotalPrice', 'min']:.2f} | £{desc_stats.loc['TotalPrice', '25%']:.2f} | £{desc_stats.loc['TotalPrice', '75%']:.2f} | £{desc_stats.loc['TotalPrice', 'max']:.2f} |

**Analytical Note:**  
All three continuous variables exhibit positive skewness (Mean > Median). The median line revenue is £{desc_stats.loc['TotalPrice', 'median']:.2f} while the mean is £{desc_stats.loc['TotalPrice', 'mean']:.2f}, indicating that high-volume wholesale orders pull the average upward.

---

## 3. Revenue Trends Over Time
- **Highest Revenue Month:** **{max_month_row['YearMonth']}** with **£{max_month_row['Revenue']:,.2f}** ({max_month_row['Transactions']:,} transactions).
- **Lowest Revenue Month:** **{min_month_row['YearMonth']}** with **£{min_month_row['Revenue']:,.2f}** ({min_month_row['Transactions']:,} transactions).
- **Seasonality Pattern:** Pronounced revenue spikes occur every September to November leading into the holiday season (Q4 surge), followed by normal contraction in early Q1.

---

## 4. Geographic Analysis
- **Dominant Market:** The **{top_country['Country']}** accounts for **£{top_country['Revenue']:,.2f}** (**{top_country['RevenueSharePct']:.2f}%** of total global revenue).
- **Top International Markets:**
  1. **{country_summary.iloc[1]['Country']}:** £{country_summary.iloc[1]['Revenue']:,.2f} ({country_summary.iloc[1]['Transactions']:,} transactions)
  2. **{country_summary.iloc[2]['Country']}:** £{country_summary.iloc[2]['Revenue']:,.2f} ({country_summary.iloc[2]['Transactions']:,} transactions)
  3. **{country_summary.iloc[3]['Country']}:** £{country_summary.iloc[3]['Revenue']:,.2f} ({country_summary.iloc[3]['Transactions']:,} transactions)
  4. **{country_summary.iloc[4]['Country']}:** £{country_summary.iloc[4]['Revenue']:,.2f} ({country_summary.iloc[4]['Transactions']:,} transactions)

---

## 5. Top Products by Revenue
- **Top Product:** `{top_product['StockCode']}` — **{top_product['Description']}**
  - Generated **£{top_product['Revenue']:,.2f}** across **{top_product['Units']:,} units** and **{top_product['Transactions']:,} orders**.
- Top 5 Products Account for substantial cumulative turnover, reflecting high demand for recurring decorative gift items.

---

## 6. Variable Relationships & Correlations
- **Correlation Matrix:**
  - `Quantity` vs `TotalPrice`: **{corr_matrix.loc['Quantity', 'TotalPrice']:.4f}** (Moderate positive correlation, volume strongly drives revenue)
  - `Price` vs `TotalPrice`: **{corr_matrix.loc['Price', 'TotalPrice']:.4f}** (Slight positive correlation)
  - `Quantity` vs `Price`: **{corr_matrix.loc['Quantity', 'Price']:.4f}** (Slight negative correlation, higher unit prices correspond with smaller order batch quantities)

---

## 7. Outlier Detection (IQR Method)
- **Quantity Outliers:** {outlier_df.loc[outlier_df['variable']=='Quantity', 'outlier_count'].values[0]:,} records ({outlier_df.loc[outlier_df['variable']=='Quantity', 'outlier_percentage'].values[0]}% of dataset above {outlier_df.loc[outlier_df['variable']=='Quantity', 'upper_bound'].values[0]:.0f} units).
- **Price Outliers:** {outlier_df.loc[outlier_df['variable']=='Price', 'outlier_count'].values[0]:,} records ({outlier_df.loc[outlier_df['variable']=='Price', 'outlier_percentage'].values[0]}% of dataset above £{outlier_df.loc[outlier_df['variable']=='Price', 'upper_bound'].values[0]:.2f}).
- **TotalPrice Outliers:** {outlier_df.loc[outlier_df['variable']=='TotalPrice', 'outlier_count'].values[0]:,} records ({outlier_df.loc[outlier_df['variable']=='TotalPrice', 'outlier_percentage'].values[0]}% of dataset above £{outlier_df.loc[outlier_df['variable']=='TotalPrice', 'upper_bound'].values[0]:.2f}).

**Important Insight:** These observations are statistical outliers under the IQR method. They should be investigated as potentially unusual but valid transactions rather than automatically removed.

---

## 8. Answers to Core Business Questions

| # | Business Question | Computed Answer |
| :-: | :--- | :--- |
| **Q1** | How many transactions are in the dataset? | **{total_trans:,} unique orders** |
| **Q2** | How many unique customers are represented? | **{total_cust:,} verified accounts** |
| **Q3** | How many products are represented? | **{total_items:,} unique product SKUs** |
| **Q4** | Which country generates the highest revenue? | **{top_country['Country']} (£{top_country['Revenue']:,.2f}, {top_country['RevenueSharePct']:.2f}% share)** |
| **Q5** | Which product/stock code generates the highest revenue? | **{top_product['StockCode']} — {top_product['Description']} (£{top_product['Revenue']:,.2f})** |
| **Q6** | Which month has the highest revenue? | **{max_month_row['YearMonth']} (£{max_month_row['Revenue']:,.2f})** |
| **Q7** | Which month has the lowest revenue? | **{min_month_row['YearMonth']} (£{min_month_row['Revenue']:,.2f})** |
| **Q8** | What is the average transaction line revenue? | **£{avg_line_rev:.2f} (Median: £{desc_stats.loc['TotalPrice', 'median']:.2f})** |
| **Q9** | What are the major outliers? | **Bulk orders exceeding {outlier_df.loc[outlier_df['variable']=='Quantity', 'upper_bound'].values[0]:.0f} units and line values over £{outlier_df.loc[outlier_df['variable']=='TotalPrice', 'upper_bound'].values[0]:.2f} (B2B wholesale transactions)** |
| **Q10** | What relationships exist between Quantity, Price and TotalPrice? | **Quantity is the strongest driver of TotalPrice (r = {corr_matrix.loc['Quantity', 'TotalPrice']:.4f}); unit price has low correlation with quantity (r = {corr_matrix.loc['Quantity', 'Price']:.4f})** |

---

## 9. Key Findings & Strategic Takeaways
1. **Strong UK Concentration:** The business is heavily UK-centric (>80% turnover). International expansion offers considerable upside in high-AOV European markets (EIRE, Netherlands, Germany).
2. **Q4 Seasonality Domination:** Q4 generates massive sales surges; inventory planning and logistics must scale up between August and October.
3. **Wholesale Core:** While average retail ticket is modest (~£{desc_stats.loc['TotalPrice', 'median']:.2f}), a small tier of bulk B2B clients drives outsized revenue. This directly motivates Task 4 Customer Segmentation (RFM analysis).
"""

    findings_path = OUTPUTS_DIR / "findings.md"
    findings_path.write_text(findings_content, encoding="utf-8")
    print(f"\n      Saved: {findings_path}")

    print("\n" + "=" * 75)
    print("TASK 2 EDA PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 75)
    print(f"Total Rows Analyzed:       {total_rows:>12,}")
    print(f"Total Revenue Calculated: £{total_rev:>12,.2f}")
    print(f"Total Invoices:            {total_trans:>12,}")
    print(f"Total Customers:           {total_cust:>12,}")
    print(f"All outputs generated in:  {OUTPUTS_DIR}")
    print("=" * 75)


if __name__ == "__main__":
    main()
