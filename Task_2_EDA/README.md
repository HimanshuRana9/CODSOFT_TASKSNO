# Task 2 — Exploratory Data Analysis (EDA)

## Objective
Examine features of the cleaned multi-year retail transactions dataset using descriptive statistics, analyze distributions, investigate temporal trends and seasonality, evaluate country and product revenue contributions, assess relationships between numerical features, detect and contextualize outliers using the Interquartile Range (IQR) method, and answer key business questions with empirical evidence.

---

## Dataset Information
- **Source:** Cleaned output from Task 1 (`Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`)
- **Total Records:** 779,425 verified rows
- **Total Columns:** 9 features
- **Missing Values:** 0
- **Duplicate Records:** 0
- **Date Range:** 2009-12-01 to 2011-12-09 (24 full months)
- **Gross Portfolio Revenue:** £17,374,804.25
- **Total Units Sold:** 10,513,952 units

### Schema
1. `InvoiceNo` — 6-digit transaction identifier
2. `StockCode` — 5-digit product item code
3. `Description` — Nominal product name
4. `Quantity` — Units ordered per line item (positive)
5. `InvoiceDate` — Timestamp of purchase
6. `Price` — Unit price in GBP (£)
7. `CustomerID` — Verified registered customer ID
8. `Country` — Customer residence country
9. `TotalPrice` — Derived line revenue (`Quantity * Price`)

---

## Technologies Used
- **Python 3.x**
- **Pandas** — Aggregation, descriptive statistics, grouping
- **NumPy** — Mathematical operations, array manipulations
- **Matplotlib & Seaborn** — Statistical plotting, distributions, and trend visualization
- **Jupyter Notebook** — Interactive analysis presentation

---

## Analysis Performed
1. **Dataset Overview:** Comprehensive profiling of unique orders (36,969), customers (5,878), products (4,631), and countries (41).
2. **Descriptive Statistics:** Full statistical breakdown (mean, std, quartiles, median, skewness, kurtosis) across numerical variables.
3. **Distribution Analysis:** Histograms and KDE curves for `Quantity`, `Price`, and `TotalPrice` (visualized up to the 99th percentile).
4. **Time Trend Analysis:** Monthly revenue, transaction counts, units sold, and average order value (AOV) tracking over 24 months.
5. **Country Analysis:** Geographic breakdown of revenue, orders, units, and customer counts across 41 countries.
6. **Product Performance:** Revenue and volume rankings for the top 100 product SKUs.
7. **Relationships & Correlation:** Pearson correlation matrix and log-scale scatter plots evaluating `Quantity` vs. `TotalPrice` and `Price` vs. `TotalPrice`.
8. **Outlier Detection:** IQR outlier boundary computation identifying high-value wholesale transactions.
9. **Business Questions:** Direct, evidence-based answers to 10 foundational business questions.

---

## Project Structure
```text
Task_2_EDA/
├── README.md                      # This comprehensive Task 2 guide
├── notebooks/
│   └── 02_eda.ipynb               # 14-section interactive Jupyter Notebook
├── scripts/
│   └── eda_analysis.py            # Automated, reproducible analysis script
└── outputs/
    ├── dataset_overview.csv       # High-level portfolio metrics
    ├── descriptive_statistics.csv # Parametric and non-parametric stats
    ├── monthly_revenue.csv        # 24-month revenue and volume metrics
    ├── country_analysis.csv       # Revenue and transactions across 41 nations
    ├── top_100_products.csv       # Top 100 revenue-generating SKUs
    ├── numeric_correlations.csv   # Correlation matrix
    ├── outlier_analysis.csv       # IQR boundaries and outlier percentages
    ├── monthly_revenue_trend.png  # Monthly revenue line & order bar chart
    ├── top_10_countries_revenue.png# Top 10 revenue-generating countries
    ├── quantity_distribution.png  # Quantity histogram (<=99th percentile)
    ├── price_distribution.png     # Unit price histogram (<=99th percentile)
    ├── totalprice_distribution.png# Line revenue histogram (<=99th percentile)
    ├── quantity_vs_totalprice.png # Scatter plot (log-scale, n=10,000)
    ├── price_vs_totalprice.png    # Scatter plot (log-scale, n=10,000)
    └── findings.md                # Formal analytical findings report
```

---

## How to Run

### 1. Execute Automated EDA Pipeline
From the repository root:
```bash
python Task_2_EDA/scripts/eda_analysis.py
```

### 2. Launch Interactive Notebook
```bash
jupyter notebook Task_2_EDA/notebooks/02_eda.ipynb
```

---

## Key Findings (Empirically Computed)

1. **Revenue Scale & Seasonality:** Total gross revenue reached **£17,374,804.25** across **36,969 transactions**. Sales exhibit strong Q4 seasonality, peaking in **November 2010** at **£1,166,460.02** (2,587 orders) compared to a trough in **February 2011** of **£446,084.92** (997 orders).
2. **Geographic Concentration:** The **United Kingdom** accounts for **£14,389,234.90** (**82.82%** of global revenue). Top international markets include **EIRE** (£616.5k), the **Netherlands** (£554.0k), **Germany** (£425.0k), and **France** (£348.8k).
3. **Top Product:** Stock Code `22423` (**REGENCY CAKESTAND 3 TIER**) is the single highest-grossing product, generating **£277,656.25** across **24,124 units** and **3,317 orders**.
4. **Strong Positive Skewness:** Line item revenue has a **mean of £22.29** vs. a **median of £12.48**, and units have a **mean of 13.49** vs. a **median of 6.00**.
5. **Drivers of Revenue:** `Quantity` is the primary driver of line revenue (**r = 0.8272**), whereas `Price` has a low correlation (**r = 0.1360**).
6. **Outlier Identification:** 8.15% of records exceed the IQR upper threshold (£42.08) for `TotalPrice`. These observations are statistical outliers under the IQR method. They should be investigated as potentially unusual but valid transactions rather than automatically removed, providing strong rationale for **Task 4 Customer Segmentation (RFM Analysis)**.
