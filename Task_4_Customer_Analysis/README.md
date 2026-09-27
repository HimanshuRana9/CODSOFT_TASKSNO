# Task 4 — Customer Data Analysis

## Objective

The objective of Task 4 is to perform comprehensive customer analytics on the multi-year retail transactions dataset. The analysis aims to:
- Understand customer purchasing behavior, order frequency, monetary value, and recency.
- Segment customers based on geographic location and buying patterns.
- Identify the most valuable customer groups driving company revenue and transaction volume.
- Create visual reports that clearly summarize customer insights.
- Provide strategic marketing recommendations (bonus requirement) tailored to distinct customer cohorts.

---

## Dataset

The customer analysis is built directly upon the cleaned and validated dataset from **Task 1**:
- **Dataset Path:** [`Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`](../Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv)
- **Verified Transactions:** 779,425 records
- **Unique Customers:** 5,878 registered accounts
- **Date Range:** December 1, 2009 to December 9, 2011 (24 months)
- **Data Quality:** Zero missing values, zero uncredited guest entries, positive quantities and prices.

> [!NOTE]
> The dataset is referenced directly from Task 1's processed storage to prevent duplicate storage overhead.

---

## Methodology

The customer analysis follows a reproducible 6-stage lifecycle:
1. **Data Ingestion & Integrity Auditing:** Loading the cleaned dataset and asserting 100% customer identification and valid pricing/quantity boundaries.
2. **Customer-Level Aggregation:** Collapsing transaction lines into individual customer profiles (1 row per `CustomerID`).
3. **Geographic Location Profiling:** Aggregating customer distribution, orders, and sales across 41 countries.
4. **Behavioral Distribution Modeling:** Analyzing the parametric and non-parametric distributions of order frequency, spend, basket size, and recency.
5. **Rule-Based Segmentation:** Applying transparent, empirically supported rules based on customer value (revenue), order frequency, and recency.
6. **Insight Derivation & Strategy Formulation:** Translating quantitative findings into actionable commercial marketing strategies.

---

## Customer Metrics

Each customer profile includes the following computed metrics:

| Metric | Type | Description |
| :--- | :--- | :--- |
| `CustomerID` | Integer | Unique identifier for registered customer account |
| `Country` | Categorical | Primary geographic residence of the customer |
| `TotalRevenue` | Float (£) | Aggregate monetary spending across all completed purchases |
| `TotalOrders` | Integer | Count of distinct completed purchase invoices |
| `TotalUnits` | Integer | Total physical inventory items ordered |
| `AverageOrderValue` | Float (£) | Mean spending per completed transaction order (`TotalRevenue / TotalOrders`) |
| `AverageUnitsPerOrder` | Float | Mean volume of items ordered per transaction |
| `FirstPurchaseDate` | Datetime | Timestamp of earliest recorded order |
| `LastPurchaseDate` | Datetime | Timestamp of most recent recorded order |
| `CustomerLifetimeDays` | Integer | Active timespan in days between first and last purchase |
| `RecencyDays` | Integer | Elapsed days between reference date and most recent order |
| `PurchaseFrequency` | Integer | Total distinct orders placed over the recording timeline |

---

## Segmentation Approach

Because the Online Retail dataset does not contain demographic age data, customer segmentation was conducted using **Location**, **Buying Patterns**, and **Customer Value**.

### Empirical Segmentation Rules:

```text
┌───────────────────────────┬─────────────────────────────────────────────────────────────────┐
│ Segment Name              │ Criteria / Definition                                           │
├───────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ High-Value Frequent       │ Revenue >= 75th percentile (£2,248) & Orders >= 6 & Recency <= 180 d │
│ High-Value Occasional     │ Revenue >= 75th percentile (£2,248) & Orders < 6 & Recency <= 180 d  │
│ High-Value Lapsed         │ Revenue >= 75th percentile (£2,248) & Recency > 180 d           │
│ Steady Repeat             │ Revenue < 75th percentile & Orders >= 3 & Recency <= 180 d      │
│ Occasional Active         │ Orders < 3 & Recency <= 180 d                                   │
│ Dormant / Inactive        │ Revenue < 75th percentile & Recency > 180 d                     │
└───────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

### Segment Breakdown Summary:

| Segment | Customer Count | Share (%) | Total Revenue (£) | Revenue Share (%) | Avg Revenue (£) | Avg Orders | Avg Order Value (£) | Avg Recency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **High-Value Frequent** | 1,177 | 20.02% | £12,409,720.48 | **71.42%** | £10,543.52 | 19.01 | £494.81 | 32.8 days |
| **Steady Repeat** | 1,272 | 21.64% | £1,523,518.83 | 8.77% | £1,197.73 | 5.13 | £250.60 | 53.2 days |
| **Dormant / Inactive** | 2,241 | **38.13%** | £1,242,995.69 | 7.15% | £554.66 | 2.12 | £279.15 | 426.6 days |
| **High-Value Lapsed** | 159 | 2.71% | £1,093,495.32 | 6.29% | £6,877.33 | 9.16 | £1,336.33 | 361.9 days |
| **High-Value Occasional** | 134 | 2.28% | £673,556.95 | 3.88% | £5,026.54 | 4.01 | **£1,710.38** | 61.7 days |
| **Occasional Active** | 895 | 15.23% | £431,516.98 | 2.48% | £482.14 | 1.48 | £330.38 | 61.8 days |

---

## Visualizations

All visual charts have been saved under [`outputs/charts/`](outputs/charts/):

1. **[`customers_by_country.png`](outputs/charts/customers_by_country.png):** Horizontal bar chart detailing customer concentration across the top 10 nations.
2. **[`revenue_by_customer_segment.png`](outputs/charts/revenue_by_customer_segment.png):** Comparative revenue bar chart displaying gross monetary contribution by customer segment.
3. **[`customer_frequency_distribution.png`](outputs/charts/customer_frequency_distribution.png):** Histogram showing customer order frequency distribution (≤ 98th percentile).
4. **[`customer_revenue_distribution.png`](outputs/charts/customer_revenue_distribution.png):** Histogram displaying customer lifetime revenue distribution (≤ 95th percentile).
5. **[`customer_segment_scatter.png`](outputs/charts/customer_segment_scatter.png):** Log-log scatter plot mapping Total Orders vs. Total Revenue color-coded by Customer Segment.

---

## Key Findings

1. **Extreme Revenue Concentration:** 20.02% of customers (**High-Value Frequent**) generate **71.42%** of gross portfolio revenue (£12.41M).
2. **Wholesale Sizing in International Markets:** European export markets (EIRE, Netherlands, Australia) demonstrate high average order values (£1,000–£2,400+) indicating bulk business-to-business purchasing.
3. **High Attrition Risk:** 38.13% of all registered accounts (2,241 customers) have not made a purchase in over 180 days.
4. **High-Value Win-Back Opportunity:** The **High-Value Lapsed** cohort represents £1.09M in prior sales across just 159 accounts, offering high return potential for reactivation campaigns.

---

## Marketing Strategy Suggestions (Bonus Requirement)

- **High-Value Frequent:** VIP loyalty tiers, early access to new seasonal collections, dedicated account managers.
- **High-Value Occasional:** Volume tiered discounts, automated reorder reminders timed with wholesale restock cycles.
- **High-Value Lapsed:** Targeted win-back campaigns offering bespoke incentives or direct outreach from sales.
- **Steady Repeat:** Cross-sell recommendations, product bundles, and milestone rewards to transition into high-value tiers.
- **Occasional Active:** Welcome back discounts, promotional shipping thresholds to encourage higher basket sizing.
- **Dormant / Inactive:** Automated sunset cadence, reactivation emails with aggressive introductory offers or feedback surveys.

---

## Limitations

> [!IMPORTANT]
> **Age Limitation:** Age-based segmentation was not performed because the selected Online Retail dataset does not contain customer age information. Customer segmentation was therefore based on available location and purchasing-behavior variables.

No synthetic, estimated, or fabricated age values were used.

---

## Project Structure

```text
Task_4_Customer_Analysis/
├── README.md                          # Comprehensive Task 4 guide
├── notebooks/
│   └── 04_customer_analysis.ipynb     # Interactive Jupyter Notebook
├── scripts/
│   └── customer_analysis.py           # Automated, reproducible analysis pipeline
├── outputs/
│   ├── customer_summary.csv           # Full customer profile metrics (5,878 rows)
│   ├── customer_segments.csv          # Customer segment assignments (5,878 rows)
│   ├── country_customer_analysis.csv  # Geographic country breakdown (41 countries)
│   ├── segment_summary.csv            # Segment performance summary matrix (6 segments)
│   └── charts/
│       ├── customers_by_country.png
│       ├── revenue_by_customer_segment.png
│       ├── customer_frequency_distribution.png
│       ├── customer_revenue_distribution.png
│       └── customer_segment_scatter.png
└── report/
    └── customer_analysis_report.md    # Formal customer data analysis report
```

---

## How to Run

### 1. Execute Automated Analysis Pipeline
From the repository root:
```bash
python Task_4_Customer_Analysis/scripts/customer_analysis.py
```

### 2. Launch Interactive Jupyter Notebook
```bash
jupyter notebook Task_4_Customer_Analysis/notebooks/04_customer_analysis.ipynb
```
